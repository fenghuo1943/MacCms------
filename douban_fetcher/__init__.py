"""
MacCMS 豆瓣评分自动获取工具

功能：
- 智能限速（Token Bucket算法）
- 断点续传
- 可选代理支持
- 自动速率调整
- 完整数据提取和更新
"""

__version__ = '1.0.0'
__author__ = 'MacCMS Tools'

# 延迟导入，避免在导入包时就加载所有依赖
def __getattr__(name):
    if name == 'DoubanScoreFetcher':
        from .fetcher import DoubanScoreFetcher
        return DoubanScoreFetcher
    elif name == 'DatabaseManager':
        from .database import DatabaseManager
        return DatabaseManager
    elif name == 'ApiClient':
        from .api_client import ApiClient
        return ApiClient
    elif name == 'DataProcessor':
        from .data_processor import DataProcessor
        return DataProcessor
    elif name == 'TokenBucket':
        from .rate_limiter import TokenBucket
        return TokenBucket
    elif name == 'RateLimitMonitor':
        from .rate_limiter import RateLimitMonitor
        return RateLimitMonitor
    elif name == 'FetchStatus':
        from .models import FetchStatus
        return FetchStatus
    elif name == 'VideoInfo':
        from .models import VideoInfo
        return VideoInfo
    elif name == 'logger':
        from .config import logger
        return logger
    elif name == 'API_CONFIG':
        from .config import API_CONFIG
        return API_CONFIG
    elif name == 'DB_CONFIG_EXAMPLE':
        from .config import DB_CONFIG_EXAMPLE
        return DB_CONFIG_EXAMPLE
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    'DoubanScoreFetcher',
    'DatabaseManager',
    'ApiClient',
    'DataProcessor',
    'TokenBucket',
    'RateLimitMonitor',
    'FetchStatus',
    'VideoInfo',
    'logger',
    'API_CONFIG',
    'DB_CONFIG_EXAMPLE',
]
