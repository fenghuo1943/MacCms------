"""
数据库操作模块
"""
import pymysql
from typing import List, Dict, Optional
from .config import logger


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_config: Dict):
        self.db_config = db_config
    
    def get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(
            host=self.db_config['host'],
            port=self.db_config.get('port', 3306),
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    
    def get_pending_videos(self, limit: int = 500, status: int = 1) -> List[Dict]:
        """
        获取待处理的视频列表
        
        Args:
            limit: 每次获取的数量
            status: 获取状态
            
        Returns:
            视频列表
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT vod_id, vod_name, vod_year 
                    FROM mac_vod 
                    WHERE vod_fetch_status = %s 
                    ORDER BY vod_id ASC
                    LIMIT %s
                """
                cursor.execute(sql, (status, limit))
                videos = cursor.fetchall()
                logger.info(f"获取到 {len(videos)} 个待处理视频")
                return videos
        finally:
            conn.close()
    
    def get_total_pending(self, status: int = 1) -> int:
        """
        获取待处理总数
        
        Args:
            status: 获取状态
            
        Returns:
            待处理数量
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT COUNT(*) as count FROM mac_vod WHERE vod_fetch_status = %s"
                cursor.execute(sql, (status,))
                result = cursor.fetchone()
                return result['count'] if result else 0
        finally:
            conn.close()
    
    def update_video_score(self, vod_id: int, info: Dict, status: int):
        """
        更新视频评分信息
        
        Args:
            vod_id: 视频ID
            info: 评分信息
            status: 获取状态
        """
        from .models import FetchStatus
        from .data_processor import DataProcessor
        
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                if status == FetchStatus.SUCCESS:
                    # 计算综合评分（如果只有豆瓣评分，就使用豆瓣评分）
                    imdb_rating = info.get('imdbRating', '') or 0.0
                    douban_rating = info.get('doubanRating', 0.0)
                    imdb_votes = info.get('imdbVotes', 0) or 0
                    douban_votes = info.get('doubanVotes', 0) or 0
                    
                    combined_score, combined_votes = DataProcessor.calculate_combined_score(
                        imdb_rating, 
                        douban_rating,
                        imdb_votes,
                        douban_votes
                    )
                    
                    sql = """
                        UPDATE mac_vod 
                        SET vod_douban_id = CASE WHEN LENGTH(%s) > 0 THEN %s ELSE vod_douban_id END,
                            vod_douban_score = CASE WHEN %s > 0 THEN %s ELSE vod_douban_score END,
                            vod_imdb_id = CASE WHEN %s IS NOT NULL AND LENGTH(%s) > 0 THEN %s ELSE vod_imdb_id END,
                            vod_imdb_votes = CASE WHEN %s > 0 THEN %s ELSE vod_imdb_votes END,
                            vod_imdb_rating = CASE WHEN %s IS NOT NULL AND LENGTH(%s) > 0 AND %s > 0 THEN %s ELSE vod_imdb_rating END,
                            vod_score = CASE WHEN %s > 0 THEN %s ELSE vod_score END,
                            vod_score_num = CASE WHEN %s > 0 THEN %s ELSE vod_score_num END,
                            vod_writer = CASE WHEN LENGTH(%s) > 0 THEN LEFT(%s, 255) ELSE vod_writer END,
                            vod_blurb = CASE WHEN LENGTH(%s) > 0 THEN LEFT(%s, 255) ELSE vod_blurb END,
                            vod_content = CASE WHEN LENGTH(%s) > 0 THEN %s ELSE vod_content END,
                            vod_total = CASE WHEN %s > 0 THEN %s ELSE vod_total END,
                            vod_duration = CASE WHEN %s > 0 THEN %s ELSE vod_duration END,
                            vod_pubdate = CASE WHEN LENGTH(%s) > 0 THEN LEFT(%s, 100) ELSE vod_pubdate END,
                            vod_sub = CASE WHEN LENGTH(%s) > 0 THEN LEFT(%s, 255) ELSE vod_sub END,
                            vod_tag = CASE WHEN LENGTH(%s) > 0 THEN LEFT(%s, 100) ELSE vod_tag END,
                            vod_fetch_status = %s
                        WHERE vod_id = %s
                    """
                    cursor.execute(sql, (
                        # vod_douban_id
                        info.get('doubanId', ''), info.get('doubanId', ''),
                        # vod_douban_score
                        info.get('doubanRating', 0), info.get('doubanRating', 0),
                        # vod_imdb_id
                        info.get('imdbId'), info.get('imdbId'), info.get('imdbId'),
                        # vod_imdb_votes
                        info.get('imdbVotes', 0), info.get('imdbVotes', 0),
                        # vod_imdb_rating
                        info.get('imdbRating'), info.get('imdbRating'), info.get('imdbRating', 0), info.get('imdbRating', 0),
                        # vod_score (豆瓣评分)
                        info.get('doubanRating', 0), info.get('doubanRating', 0),
                        # vod_score_num (豆瓣投票数)
                        info.get('doubanVotes', 0), info.get('doubanVotes', 0),
                        # vod_writer
                        info.get('writers', ''), info.get('writers', ''),
                        # vod_blurb (简介)
                        info.get('description', ''), info.get('description', ''),
                        # vod_content (详细内容)
                        info.get('description', ''), info.get('description', ''),
                        # vod_total (集数)
                        info.get('episodes', 0), info.get('episodes', 0),
                        # vod_duration (片长)
                        info.get('duration', 0), str(info.get('duration', 0)),
                        # vod_pubdate (上映日期)
                        info.get('dateReleased', ''), info.get('dateReleased', ''),
                        # vod_sub (别名)
                        info.get('alias', ''), info.get('alias', ''),
                        # vod_tag (类型标签)
                        info.get('tags', ''), info.get('tags', ''),
                        # vod_fetch_status
                        status,
                        # vod_id
                        vod_id
                    ))
                else:
                    # 更新获取状态
                    sql = """
                        UPDATE mac_vod 
                        SET vod_fetch_status = %s
                        WHERE vod_id = %s
                    """
                    cursor.execute(sql, (status, vod_id))
                
                #logger.info(f"更新视频 {vod_id} 的状态为 {status}")
                
        except Exception as e:
            logger.error(f"更新视频 {vod_id} 失败: {str(e)}")
            raise
        finally:
            conn.close()
    
    def get_status_distribution(self) -> List[Dict]:
        """获取状态分布统计"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT 
                        vod_fetch_status,
                        COUNT(*) as count
                    FROM mac_vod
                    GROUP BY vod_fetch_status
                """
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conn.close()
