"""
MacCMS 豆瓣评分自动获取工具 - Selenium方案主入口

功能：
- 使用Selenium浏览器自动化从豆瓣网页获取信息
- 智能重试机制
- 断点续传
- 完整的反爬虫规避
"""
from selenium_fetcher import SeleniumDoubanFetcher
from selenium_fetcher.config import DB_CONFIG_EXAMPLE, DEFAULT_RUN_CONFIG


def main():
    """主函数"""
    
    # 数据库配置（从 config.py 导入）
    # 如需修改，请编辑 selenium_fetcher/config.py 中的 DB_CONFIG_EXAMPLE
    db_config = DB_CONFIG_EXAMPLE.copy()
    
    # 可选：Selenium配置
    selenium_config = {
        'browser': 'chrome',      # 浏览器类型: chrome, firefox
        'headless': False,         # 是否无头模式（后台运行）
        'timeout': 30,            # 页面加载超时时间(秒)
        'implicit_wait': 10,      # 隐式等待时间(秒)
    }
    
    # 创建获取器实例
    fetcher = SeleniumDoubanFetcher(
        db_config=db_config,
        selenium_config=selenium_config
    )
    
    # 运行任务
    fetcher.run(
        batch_size=DEFAULT_RUN_CONFIG['batch_size']
    )


if __name__ == '__main__':
    main()
