"""
数据库配置示例 - 请复制此文件为 config.py 并填入真实配置

⚠️ 安全警告：
1. 不要将包含真实密码的 config.py 提交到 Git
2. config.py 已在 .gitignore 中排除
3. 请使用强密码并定期更换
"""

# 数据库配置
DB_CONFIG = {
    'host': 'your_database_host',      # 数据库主机地址
    'port': 3306,                       # 数据库端口
    'user': 'your_username',            # 数据库用户名
    'password': 'your_password',        # ⚠️ 数据库密码（请勿提交到Git）
    'database': 'maccms',               # 数据库名称
    'charset': 'utf8mb4'
}

# Selenium配置
SELENIUM_CONFIG = {
    'browser': 'edge',                  # 浏览器类型: chrome, firefox, edge
    'headless': True,                   # 是否无头模式（后台运行）
    'timeout': 30,                      # 页面加载超时时间(秒)
    'implicit_wait': 10,                # 隐式等待时间(秒)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'window_size': (1920, 1080),        # 窗口大小
}

# 默认运行配置
DEFAULT_RUN_CONFIG = {
    'batch_size': 50,                   # Selenium较慢，减小批次
    'max_requests_per_second': 0.2,     # Selenium很慢，降低速率
    'adjust_rate': False,
    'use_proxy': False,
    'proxy_list': [],
}
