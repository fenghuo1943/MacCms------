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
                    # 计算综合评分
                    combined_score, combined_votes = DataProcessor.calculate_combined_score(
                        info['imdbRating'], 
                        info['doubanRating'],
                        info['imdbVotes'],
                        info['doubanVotes']
                    )
                    
                    sql = """
                        UPDATE mac_vod 
                        SET vod_douban_id = %s,
                            vod_douban_score = %s,
                            vod_imdb_id = %s,
                            vod_imdb_votes = %s,
                            vod_imdb_rating = %s,
                            vod_score = %s,
                            vod_score_num = %s,
                            vod_writer = CASE WHEN %s != '' THEN LEFT(%s, 255) ELSE vod_writer END,
                            vod_blurb = CASE WHEN %s != '' THEN LEFT(%s, 255) ELSE vod_blurb END,
                            vod_content = CASE WHEN %s != '' THEN %s ELSE vod_content END,
                            vod_total = CASE WHEN %s > 0 THEN %s ELSE vod_total END,
                            vod_duration = CASE WHEN %s > 0 THEN %s ELSE vod_duration END,
                            vod_pubdate = CASE WHEN %s != '' THEN LEFT(%s, 100) ELSE vod_pubdate END,
                            vod_sub = CASE WHEN %s != '' THEN LEFT(%s, 255) ELSE vod_sub END,
                            vod_tag = CASE WHEN %s != '' THEN LEFT(%s, 100) ELSE vod_tag END,
                            vod_fetch_status = %s
                        WHERE vod_id = %s
                    """
                    cursor.execute(sql, (
                        info['doubanId'],
                        info['doubanRating'],
                        info['imdbId'],
                        info['imdbVotes'],
                        info['imdbRating'],
                        #combined_score,
                        info['doubanRating'],
                        #combined_votes,
                        info['doubanVotes'],
                        info['writers'], info['writers'],
                        info['description'], info['description'],
                        info['description'], info['description'],
                        info['episodes'], info['episodes'],
                        info['duration'], str(info['duration']),
                        info['dateReleased'], info['dateReleased'],
                        info['alias'], info['alias'],
                        info['tags'], info['tags'],
                        status,
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
                
                logger.info(f"更新视频 {vod_id} 的状态为 {status}")
                
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
