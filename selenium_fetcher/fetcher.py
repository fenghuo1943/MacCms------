"""
Selenium方案主获取器模块
"""
import time
import json
import os
from typing import Dict, Tuple, Optional
from datetime import datetime

# 复用douban_fetcher的数据库、模型和API客户端
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from douban_fetcher.database import DatabaseManager
from douban_fetcher.models import FetchStatus
from douban_fetcher.config import logger as main_logger
from douban_fetcher.api_client import ApiClient
from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.worker_config import get_worker_id

from .config import logger, SELENIUM_CONFIG, DOUBAN_MOVIE_URL, RETRY_CONFIG, STATS_FILE
from .browser import BrowserManager
from .extractor import DoubanPageExtractor


class SeleniumDoubanFetcher:
    """基于Selenium的豆瓣评分获取器"""
    
    def __init__(self, db_config: Dict[str, any], selenium_config: Dict = None):
        """
        初始化获取器
        
        Args:
            db_config: 数据库配置
            selenium_config: Selenium配置
        """
        # 初始化组件
        self.db = DatabaseManager(db_config)
        self.api_client = ApiClient()  # 使用API进行搜索
        self.browser_manager = BrowserManager(selenium_config)  # BrowserManager会自动合并配置
        self.extractor = DoubanPageExtractor()
        
        # 设备标识
        self.worker_id = get_worker_id()
        main_logger.info(f"当前设备标识: {self.worker_id}")
        
        # 统计文件（每个设备独立的统计文件）
        self.stats_file = f"selenium_fetch_stats_{self.worker_id}.json"
        self.load_stats()
        
        # 连续无结果计数器
        self.consecutive_no_results = 0
        self.max_consecutive_no_results = 20
    
    def load_stats(self):
        """加载统计信息（断点续传）"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
                main_logger.info(f"加载历史统计: {self.stats}")
            except:
                self.stats = {'start_time': None, 'total_processed': 0, 'total_success': 0}
        else:
            self.stats = {'start_time': None, 'total_processed': 0, 'total_success': 0}
    
    def save_stats(self):
        """保存统计信息"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def search_douban(self, video_name: str) -> Optional[list]:
        """
        使用豆瓣API搜索（快速）
        
        Args:
            video_name: 视频名称
            
        Returns:
            搜索结果列表，失败返回None
        """
        try:
            main_logger.info(f"使用API搜索: {video_name}")
            
            # 使用豆瓣API搜索
            search_results = self.api_client.search_douban(video_name)
            
            if search_results is None:
                main_logger.warning("API搜索失败")
                return None
            
            # 转换API结果为统一格式
            results = []
            for item in search_results:
                subject = item.get('subject', {})
                douban_id = item.get('id', '')
                title = item.get('title', '')
                year = item.get('year', '')
                #director = item.get('directors', [{}])[0].get('name', '')
                # 安全地获取导演信息
                directors = item.get('directors', [])
                director = directors[0].get('name', '') if directors and len(directors) > 0 else ''
                
                # 确定类型
                subtype = item.get('subtype', '')
                content_type = 'movie' if subtype == 'movie' else 'tv'
                
                if douban_id and title:
                    results.append({
                        'id': str(douban_id),
                        'title': title,
                        'year': str(year) if year else '',
                        'type': content_type,
                        'director': director,                        
                        'url': f'https://movie.douban.com/subject/{douban_id}/'
                    })
            
            #main_logger.info(f"API搜索到 {len(results)} 个结果")
            return results
            
        except Exception as e:
            main_logger.error(f"API搜索时出错: {str(e)}")
            return None
    
    def get_movie_detail(self, douban_id: str) -> Optional[Dict]:
        """
        获取豆瓣电影详情
        
        Args:
            douban_id: 豆瓣ID
            
        Returns:
            电影详细信息，失败返回None
        """
        driver = self.browser_manager.get_driver()
        
        for attempt in range(RETRY_CONFIG['max_retries']):
            try:
                url = DOUBAN_MOVIE_URL.format(douban_id=douban_id)
                #main_logger.info(f"正在获取详情: {douban_id} (尝试 {attempt + 1}/{RETRY_CONFIG['max_retries']})")
                
                # 访问详情页
                driver.get(url)
                
                # 等待页面加载
                time.sleep(3)
                
                # 获取页面HTML
                html_content = driver.page_source
                
                # 检查是否被拦截
                """ if 'sec' in html_content and 'tok' in html_content:
                    main_logger.warning("检测到豆瓣反爬虫验证，等待后重试...")
                    wait_time = RETRY_CONFIG['base_delay'] * (2 ** attempt)
                    time.sleep(min(wait_time, RETRY_CONFIG['max_delay']))
                    continue """
                
                # 提取详细信息
                movie_info = self.extractor.extract_movie_info(html_content)
                return movie_info
                
            except Exception as e:
                main_logger.error(f"获取详情时出错: {str(e)}")
                if attempt < RETRY_CONFIG['max_retries'] - 1:
                    wait_time = RETRY_CONFIG['base_delay'] * (2 ** attempt)
                    time.sleep(min(wait_time, RETRY_CONFIG['max_delay']))
                    continue
                return None
        
        return None
    
    def process_single_video(self, video: Dict) -> Tuple[int, bool, str]:
        """
        处理单个视频（API搜索 + Selenium详情）
        
        Args:
            video: 视频信息字典
            
        Returns:
            (vod_id, success, message)
        """
        vod_id = video['vod_id']
        vod_name = video['vod_name']
        vod_area = video.get('vod_area', '')
        vod_year = video.get('vod_year', '')
        vod_director = video.get('vod_director', '')
        
        try:
            # 1. 使用API搜索豆瓣（快速）
            search_results = self.search_douban(vod_name)
            
            if search_results is None:
                self.db.update_video_score_with_unlock(vod_id, {}, FetchStatus.ERROR, self.worker_id)
                return (vod_id, False, "豆瓣搜索失败")
            
            if len(search_results) == 0:
                self.consecutive_no_results += 1
                main_logger.warning(f"连续无结果次数: {self.consecutive_no_results}/{self.max_consecutive_no_results}")
                self.db.update_video_score_with_unlock(vod_id, {}, FetchStatus.NO_SEARCH_RESULT, self.worker_id)
                main_logger.warning(f"无搜索结果: {vod_name}")
                return (vod_id, False, "无搜索结果")
            
            # 有结果，重置连续无结果计数
            self.consecutive_no_results = 0
            
            # 2. 匹配视频（使用DataProcessor）
            matched = DataProcessor.match_douban_search_results(search_results, vod_name, vod_year, vod_area, vod_director)
            
            if matched == 'multiple':
                self.db.update_video_score_with_unlock(vod_id, {}, FetchStatus.MULTIPLE_RESULTS, self.worker_id)
                main_logger.warning(f"匹配到多个结果: {vod_name}")
                return (vod_id, False, "匹配到多个结果")
            
            if matched is None:
                self.db.update_video_score_with_unlock(vod_id, {}, FetchStatus.NO_MATCH_RESULT, self.worker_id)
                main_logger.warning(f"未找到匹配结果: {vod_name}")
                return (vod_id, False, "未找到匹配")
            
            # 3. 获取豆瓣ID
            douban_id = matched.get('id', '')
            if not douban_id:
                self.db.update_video_score_with_unlock(vod_id, {}, FetchStatus.ERROR, self.worker_id)
                return (vod_id, False, "无法获取豆瓣ID")
            
            # 4. 使用Selenium获取详细信息（网页更完整）
            movie_info = self.get_movie_detail(douban_id)
            
            if not movie_info:
                self.db.update_video_score_with_unlock(vod_id, {}, FetchStatus.ERROR, self.worker_id)
                return (vod_id, False, "获取豆瓣详情失败")
            
            # 5. 准备数据库更新信息（使用database.py期望的字段名）
            info = {
                'doubanId': douban_id,  # 豆瓣ID
                'doubanRating': movie_info.get('rating', 0.0),
                'doubanVotes': movie_info.get('votes', 0),
                'imdbId': movie_info.get('imdb_id', ''),  # IMDB ID
                'imdbRating': '',  # Selenium方案不获取IMDB评分
                'imdbVotes': 0,
                'writers': movie_info.get('writers', ''),
                'description': movie_info.get('summary', ''),
                'episodes': movie_info.get('episodes', 0),
                'duration': movie_info.get('duration', 0),
                'dateReleased': movie_info.get('release_date', ''),
                'alias': '',  # 别名，Selenium方案暂不提取
                'tags': movie_info.get('genres', ''),  # 类型作为标签
            }
            
            # 6. 更新数据库并释放锁定（SQL层面已做条件判断，空值不会覆盖原有数据）
            self.db.update_video_score_with_unlock(vod_id, info, FetchStatus.SUCCESS, self.worker_id)
            
            msg = f"豆瓣:{info['doubanRating']}({info['doubanVotes']}人)"
            if info.get('tags'):
                msg += f" 类型:{info['tags'][:30]}"
            if info.get('episodes'):
                msg += f" 集数:{info['episodes']}"
            if info.get('duration'):
                msg += f" 片长:{info['duration']}分钟"
            
            # 使用主程序的logger输出成功信息（可选）
            main_logger.info(f"✓ ID:{vod_id} {vod_name} - {msg}")
            
            return (vod_id, True, msg)
            
        except Exception as e:
            main_logger.error(f"处理视频 {vod_id} 时发生错误: {str(e)}")
            try:
                self.db.update_video_score_with_unlock(vod_id, {}, FetchStatus.ERROR, self.worker_id)
            except:
                pass
            return (vod_id, False, f"异常: {str(e)[:50]}")
    
    @staticmethod
    def format_eta(seconds: float) -> str:
        """格式化剩余时间"""
        if seconds < 60:
            return f"{int(seconds)}秒"
        elif seconds < 3600:
            return f"{int(seconds/60)}分钟"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}小时{minutes}分钟"
    
    def run(self, batch_size: int = 50):
        """
        运行主任务
        
        Args:
            batch_size: 每批处理数量
        """
        main_logger.info("=" * 70)
        main_logger.info("开始Selenium豆瓣评分获取任务")
        main_logger.info(f"设备标识: {self.worker_id}")
        main_logger.info(f"配置: 批次大小={batch_size}")
        main_logger.info("=" * 70)
        
        if self.stats['start_time'] is None:
            self.stats['start_time'] = datetime.now().isoformat()
        
        total_processed = self.stats['total_processed']
        total_success = self.stats['total_success']
        start_time = time.time()
        
        try:
            while True:
                # 使用原子锁定机制获取视频
                videos = self.db.lock_videos_atomically(self.worker_id, limit=batch_size)
                
                pending_count = self.db.get_total_pending()
                if pending_count == 0 and not videos:
                    main_logger.info("✓ 所有视频已处理完成！")
                    break
                
                if not videos:
                    main_logger.info("暂无可处理的视频，等待中...")
                    time.sleep(10)
                    continue
                
                main_logger.info(f"\n{'='*70}")
                main_logger.info(f"剩余待处理: {pending_count} 个视频")
                main_logger.info(f"本批次锁定: {len(videos)} 个视频")
                
                batch_start = time.time()
                batch_success = 0
                
                for i, video in enumerate(videos, 1):
                    vod_id, success, msg = self.process_single_video(video)
                    
                    if success:
                        total_success += 1
                        batch_success += 1
                        if i % 5 == 0 or i == len(videos):
                            main_logger.info(f"  [{i}/{len(videos)}] ✓ ID:{vod_id}")
                    else:
                        if i % 5 == 0 or i == len(videos):
                            main_logger.warning(f"  [{i}/{len(videos)}] ✗ ID:{vod_id} - {msg}")
                    
                    total_processed += 1
                    
                    elapsed = time.time() - start_time
                    avg_speed = total_processed / elapsed if elapsed > 0 else 0
                    remaining = pending_count - (total_processed - self.stats['total_processed'])
                    eta = remaining / avg_speed if avg_speed > 0 else 0
                    
                    if i % 10 == 0:
                        main_logger.info(f"  进度: {total_processed} | 成功: {total_success} | "
                                      f"速度: {avg_speed:.2f}/s | 预计剩余: {self.format_eta(eta)}")
                    
                    self.stats['total_processed'] = total_processed
                    self.stats['total_success'] = total_success
                    self.save_stats()
                
                batch_elapsed = time.time() - batch_start
                main_logger.info(f"批次完成: {len(videos)}个, 成功{batch_success}个, "
                               f"耗时{batch_elapsed:.1f}秒")
                
                # 检查连续无结果次数
                if self.consecutive_no_results >= self.max_consecutive_no_results:
                    main_logger.warning(f"检测到连续无结果次数达到阈值 ({self.consecutive_no_results}), "
                                     f"自动停止任务")
                    break
        
        finally:
            # 确保浏览器关闭
            self.browser_manager.quit_driver()
        
        total_elapsed = time.time() - start_time
        main_logger.info("\n" + "=" * 70)
        main_logger.info("任务完成！")
        main_logger.info(f"总处理: {total_processed} 个")
        main_logger.info(f"成功: {total_success} 个 ({total_success/total_processed*100:.1f}%)")
        main_logger.info(f"总耗时: {self.format_eta(total_elapsed)}")
        main_logger.info(f"平均速度: {total_processed/total_elapsed:.2f} 个/秒")
        main_logger.info("=" * 70)
