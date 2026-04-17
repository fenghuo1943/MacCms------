"""
数据库配置示例 - 请复制此文件为 config.py 并填入真实配置

⚠️ 安全警告：
1. 不要将包含真实密码的 config.py 提交到 Git
2. config.py 已在 .gitignore 中排除
3. 请使用强密码并定期更换
"""
import logging

# 配置日志
logger = logging.getLogger('douban_fetcher')
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# 统计文件路径
STATS_FILE = 'fetch_stats.json'

# API配置
API_CONFIG = {
    'base_url': 'https://api.wmdb.tv/api/v1',
    'timeout': 30,
    'max_retries': 3,
}

# 速率限制配置
RATE_LIMIT_CONFIG = {
    'max_requests_per_second': 2.0,
    'burst_size': 5,
}

# 数据库配置
DB_CONFIG = {
    'host': 'your_database_host',      # 数据库主机地址
    'port': 3306,                       # 数据库端口
    'user': 'your_username',            # 数据库用户名
    'password': 'your_password',        # ⚠️ 数据库密码（请勿提交到Git）
    'database': 'maccms',               # 数据库名称
    'charset': 'utf8mb4'
}
