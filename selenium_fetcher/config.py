"""
Selenium方案配置模块
"""
import logging
import os

# 配置日志
logger = logging.getLogger('selenium_fetcher')
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# 统计文件路径
STATS_FILE = 'selenium_fetch_stats.json'

# Selenium配置
SELENIUM_CONFIG = {
    'browser': 'edge',  # 浏览器类型: chrome, firefox, edge
    'headless': True,     # 是否无头模式
    'timeout': 30,        # 页面加载超时时间(秒)
    'implicit_wait': 10,  # 隐式等待时间(秒)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'window_size': (1920, 1080),  # 窗口大小
}

# 豆瓣搜索URL模板
DOUBAN_SEARCH_URL = 'https://www.douban.com/search?q={query}'

# 豆瓣电影详情页URL模板
DOUBAN_MOVIE_URL = 'https://movie.douban.com/subject/{douban_id}/'

# 重试配置
RETRY_CONFIG = {
    'max_retries': 3,
    'base_delay': 2,
    'max_delay': 30,
}

# 数据库配置示例（与主项目保持一致）
DB_CONFIG_EXAMPLE = {
    'host': 'mylove.fenghuo1943.cn',
    'port': 13307,
    'user': 'maccms',
    'password': 'q5DdyjsI5%GJOr',
    'database': 'maccms',
    'charset': 'utf8mb4'
}

# 默认运行配置
DEFAULT_RUN_CONFIG = {
    'batch_size': 50,  # Selenium较慢，减小批次
    'max_requests_per_second': 0.2,  # Selenium很慢，降低速率
    'adjust_rate': False,
    'use_proxy': False,
    'proxy_list': [],
}
