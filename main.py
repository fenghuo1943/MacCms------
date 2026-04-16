"""
MacCMS 豆瓣评分自动获取工具 - 主入口

功能：
- 智能限速（Token Bucket算法）
- 断点续传
- 可选代理支持
- 自动速率调整
- 完整数据提取和更新
"""
from douban_fetcher import DoubanScoreFetcher
from douban_fetcher.config import DB_CONFIG_EXAMPLE, DEFAULT_RUN_CONFIG


def main():
    """主函数"""
    
    # 数据库配置（从 config.py 导入）
    # 如需修改，请编辑 douban_fetcher/config.py 中的 DB_CONFIG_EXAMPLE
    db_config = DB_CONFIG_EXAMPLE.copy()  # 使用副本，避免修改原始配置
    
    # 可选：代理列表（如果需要）
    proxy_list = DEFAULT_RUN_CONFIG['proxy_list']
    use_proxy = DEFAULT_RUN_CONFIG['use_proxy']
    
    # 创建获取器实例
    fetcher = DoubanScoreFetcher(
        db_config=db_config,
        max_requests_per_second=DEFAULT_RUN_CONFIG['max_requests_per_second'],
        use_proxy=use_proxy,
        proxy_list=proxy_list
    )
    
    # 运行任务
    fetcher.run(
        batch_size=DEFAULT_RUN_CONFIG['batch_size'],
        max_requests_per_second=DEFAULT_RUN_CONFIG['max_requests_per_second'],
        adjust_rate=DEFAULT_RUN_CONFIG['adjust_rate']
    )


if __name__ == '__main__':
    main()