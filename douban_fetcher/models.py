"""
数据模型和常量定义
"""
from typing import Dict


class FetchStatus:
    """获取状态常量"""
    NOT_FETCHED = 1           # 未获取
    SUCCESS = 0               # 获取成功
    MULTIPLE_RESULTS = 2      # 多个结果
    NO_SEARCH_RESULT = 3      # 搜索结果为空
    NO_MATCH_RESULT = 6       # 匹配结果为空（有搜索结果但无匹配）
    ERROR = 4                 # 其他错误
    RATE_LIMITED = 5          # 被限流
    
    STATUS_MAP = {
        0: '成功',
        1: '未处理',
        2: '多个结果',
        3: '搜索结果为空',
        4: '错误',
        5: '被限流',
        6: '匹配结果为空'
    }


class VideoInfo:
    """视频信息数据类"""
    
    @staticmethod
    def create_empty() -> Dict:
        """创建空的视频信息字典"""
        return {
            'imdbId': '',
            'imdbVotes': 0,
            'imdbRating': 0.0,
            'doubanId': 0,
            'doubanRating': 0.0,
            'doubanVotes': 0,
            'year': '',
            'type': '',
            'alias': '',
            'episodes': 0,
            'duration': 0,
            'dateReleased': '',
            'actors': '',
            'directors': '',
            'writers': '',
            'genre': '',
            'country': '',
            'language': '',
            'poster': '',
            'description': '',
            'tags': '',
        }
