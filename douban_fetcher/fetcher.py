"""
主获取器模块 - 协调各组件完成数据获取任务
"""
import json
import os
import time
from typing import Dict, Tuple
from datetime import datetime

from .config import logger, STATS_FILE
from .models import FetchStatus
from .rate_limiter import TokenBucket, RateLimitMonitor
from .database import DatabaseManager
from .api_client import ApiClient
from .data_processor import DataProcessor


class DoubanScoreFetcher:
    """豆瓣评分获取器 - 生产级版本"""
    
    def __init__(self, db_config: Dict[str, any], 
                 max_requests_per_second: float = 2.0,
                 use_proxy: bool = False,
                 proxy_list: list = None):
        """
        初始化获取器
        
        Args:
            db_config: 数据库配置
            max_requests_per_second: 最大请求速率
            use_proxy: 是否使用代理
            proxy_list: 代理列表
        """
        # 初始化组件
        self.db = DatabaseManager(db_config)
        self.api_client = ApiClient(use_proxy=use_proxy, proxy_list=proxy_list or [])
        self.rate_limiter = TokenBucket(rate=max_requests_per_second, capacity=5)
        self.monitor = RateLimitMonitor()
        
        # 统计文件
        self.stats_file = STATS_FILE
        self.load_stats()
    
    def load_stats(self):
        """加载统计信息（断点续传）"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
                logger.info(f"加载历史统计: {self.stats}")
            except:
                self.stats = {'start_time': None, 'total_processed': 0, 'total_success': 0}
        else:
            self.stats = {'start_time': None, 'total_processed': 0, 'total_success': 0}
    
    def save_stats(self):
        """保存统计信息"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def process_single_video(self, video: Dict) -> Tuple[int, bool, str]:
        """
        处理单个视频（使用豆瓣API）
        
        Args:
            video: 视频信息字典
            
        Returns:
            (vod_id, success, message)
        """
        vod_id = video['vod_id']
        vod_name = video['vod_name']
        vod_year = video.get('vod_year', '')
        
        try:
            # 速率限制
            self.rate_limiter.acquire(timeout=60)
            
            # 1. 使用豆瓣搜索API
            search_results = self.api_client.search_douban(vod_name, monitor=self.monitor)
            
            if search_results is None:
                # API请求失败
                self.db.update_video_score(vod_id, {}, FetchStatus.ERROR)
                return (vod_id, False, "豆瓣API请求失败")
            
            if len(search_results) == 0:
                # 无结果
                self.db.update_video_score(vod_id, {}, FetchStatus.NO_RESULT)
                return (vod_id, False, "无搜索结果")
            
            # 2. 匹配视频
            matched = DataProcessor.match_douban_search_results(search_results, vod_name, vod_year)
            
            if matched == 'multiple':
                # 多个结果
                self.db.update_video_score(vod_id, {}, FetchStatus.MULTIPLE_RESULTS)
                return (vod_id, False, "匹配到多个结果")
            
            if matched is None:
                # 无匹配
                self.db.update_video_score(vod_id, {}, FetchStatus.NO_RESULT)
                return (vod_id, False, "未找到匹配")
            
            # 3. 获取豆瓣ID
            douban_id = matched.get('id', '')
            if not douban_id:
                self.db.update_video_score(vod_id, {}, FetchStatus.ERROR)
                return (vod_id, False, "无法获取豆瓣ID")
            
            # 4. 使用Subject API获取详细信息
            subject_data = self.api_client.get_douban_subject(douban_id, monitor=self.monitor)
            
            if not subject_data:
                self.db.update_video_score(vod_id, {}, FetchStatus.ERROR)
                return (vod_id, False, "获取豆瓣详情失败")
            
            # 5. 提取豆瓣信息
            douban_info = DataProcessor.extract_douban_subject_info(subject_data)
            
            # 6. 准备数据库更新信息
            info = DataProcessor.prepare_db_info_from_douban(douban_info)
            
            # 7. 更新数据库
            self.db.update_video_score(vod_id, info, FetchStatus.SUCCESS)
            
            msg = f"豆瓣:{info['doubanRating']}({info['doubanVotes']}人)"
            if info.get('tags'):
                msg += f" 类型:{info['tags'][:30]}"
            if info.get('episodes'):
                msg += f" 集数:{info['episodes']}"
            return (vod_id, True, msg)
            
        except Exception as e:
            logger.error(f"处理视频 {vod_id} 时发生错误: {str(e)}")
            try:
                self.db.update_video_score(vod_id, {}, FetchStatus.ERROR)
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
    
    def run(self, batch_size: int = 500, 
            max_requests_per_second: float = 2.0,
            adjust_rate: bool = True):
        """
        运行主任务
        
        Args:
            batch_size: 每批处理数量
            max_requests_per_second: 最大请求速率
            adjust_rate: 是否根据限流情况自动调整速率
        """
        logger.info("=" * 70)
        logger.info("开始豆瓣评分获取任务（生产级版本）")
        logger.info(f"配置: 速率={max_requests_per_second}req/s, 批次大小={batch_size}")
        logger.info("=" * 70)
        
        if self.stats['start_time'] is None:
            self.stats['start_time'] = datetime.now().isoformat()
        
        total_processed = self.stats['total_processed']
        total_success = self.stats['total_success']
        start_time = time.time()
        
        while True:
            pending_count = self.db.get_total_pending()
            if pending_count == 0:
                logger.info("✓ 所有视频已处理完成！")
                break
            
            logger.info(f"\n{'='*70}")
            logger.info(f"剩余待处理: {pending_count} 个视频")
            logger.info(f"当前速率: {self.monitor.get_current_rate():.2f} req/s")
            logger.info(f"统计: {json.dumps(self.monitor.get_stats(), ensure_ascii=False)}")
            
            videos = self.db.get_pending_videos(limit=batch_size)
            if not videos:
                break
            
            batch_start = time.time()
            batch_success = 0
            
            for i, video in enumerate(videos, 1):
                vod_id, success, msg = self.process_single_video(video)
                
                if success:
                    total_success += 1
                    batch_success += 1
                    if i % 10 == 0 or i == len(videos):
                        logger.info(f"  [{i}/{len(videos)}] ✓ ID:{vod_id}")
                else:
                    if i % 10 == 0 or i == len(videos):
                        logger.warning(f"  [{i}/{len(videos)}] ✗ ID:{vod_id} - {msg}")
                
                total_processed += 1
                
                elapsed = time.time() - start_time
                avg_speed = total_processed / elapsed if elapsed > 0 else 0
                remaining = pending_count - (total_processed - self.stats['total_processed'])
                eta = remaining / avg_speed if avg_speed > 0 else 0
                
                if i % 50 == 0:
                    logger.info(f"  进度: {total_processed} | 成功: {total_success} | "
                              f"速度: {avg_speed:.2f}/s | 预计剩余: {self.format_eta(eta)}")
                
                self.stats['total_processed'] = total_processed
                self.stats['total_success'] = total_success
                self.save_stats()
            
            batch_elapsed = time.time() - batch_start
            logger.info(f"批次完成: {len(videos)}个, 成功{batch_success}个, "
                       f"耗时{batch_elapsed:.1f}秒")
            
            if adjust_rate:
                stats = self.monitor.get_stats()
                if stats['rate_limited_count'] > 5:
                    logger.warning("检测到频繁限流，降低请求速率")
                    self.rate_limiter.rate *= 0.8
                elif stats['success_rate'].rstrip('%') > '95' and stats['rate_limited_count'] == 0:
                    current_rate = float(stats['current_rate'].split()[0])
                    if current_rate < max_requests_per_second * 0.9:
                        logger.info("成功率良好，尝试提高请求速率")
                        self.rate_limiter.rate = min(max_requests_per_second, 
                                                    self.rate_limiter.rate * 1.2)
        
        total_elapsed = time.time() - start_time
        logger.info("\n" + "=" * 70)
        logger.info("任务完成！")
        logger.info(f"总处理: {total_processed} 个")
        logger.info(f"成功: {total_success} 个 ({total_success/total_processed*100:.1f}%)")
        logger.info(f"总耗时: {self.format_eta(total_elapsed)}")
        logger.info(f"平均速度: {total_processed/total_elapsed:.2f} 个/秒")
        logger.info("=" * 70)
        
        self.generate_report(total_processed, total_success, total_elapsed)
    
    def generate_report(self, total: int, success: int, elapsed: float):
        """生成详细报告"""
        report = {
            'task_summary': {
                'total_videos': total,
                'successful': success,
                'failed': total - success,
                'success_rate': f"{success/total*100:.2f}%" if total > 0 else "0%",
                'total_time': self.format_eta(elapsed),
                'avg_speed': f"{total/elapsed:.2f} videos/sec" if elapsed > 0 else "0",
            },
            'api_stats': self.monitor.get_stats(),
            'timestamp': datetime.now().isoformat()
        }
        
        report_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n详细报告已保存到: {report_file}")
        
        # 显示状态分布
        status_dist = self.db.get_status_distribution()
        
        logger.info("\n状态分布:")
        for row in status_dist:
            status_name = FetchStatus.STATUS_MAP.get(row['vod_fetch_status'], '未知')
            logger.info(f"  {status_name} ({row['vod_fetch_status']}): {row['count']} 个")
