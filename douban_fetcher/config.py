"""
配置管理模块
"""
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('douban_score_fetch.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# API配置
API_CONFIG = {
    'base_url': 'https://api.wmdb.tv/api/v1/movie/search',
    'timeout': 15,
    'max_retries': 5,
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
}

# 豆瓣API配置
DOUBAN_API_CONFIG = {
    'search_url': 'https://api.douban.com/v2/movie/search',
    'subject_base_url': 'https://api.douban.com/v2/movie/subject/',
    'apikey': '0ab215a8b1977939201640fa14c66bab',
    'timeout': 15,
    'max_retries': 5,
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
}

# 数据库配置示例
DB_CONFIG_EXAMPLE = {
    'host': '192.168.114.4',
    'port': 3307,
    'user': 'maccms',
    'password': 'q5DdyjsI5%GJOr',
    'database': 'maccms'
}

# 默认运行配置
DEFAULT_RUN_CONFIG = {
    'batch_size': 50,
    'max_requests_per_second': 0.5,
    'adjust_rate': True,
    'use_proxy': False,
    'proxy_list': [
        'http://127.0.0.1:10809',  # 本地代理
    ]
}

# 统计文件
STATS_FILE = 'fetch_stats.json'
