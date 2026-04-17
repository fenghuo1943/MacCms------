"""
MacCMS 豆瓣评分自动获取工具 - Selenium方案主入口

功能：
- 使用Selenium浏览器自动化从豆瓣网页获取信息
- 智能重试机制
- 断点续传
- 完整的反爬虫规避
- 支持优雅停止（Ctrl+C、Ctrl+Z、停止文件）
"""
import signal
import sys
from selenium_fetcher import SeleniumDoubanFetcher
from selenium_fetcher.config import DB_CONFIG_EXAMPLE, DEFAULT_RUN_CONFIG


def main():
    """主函数"""
    
    # 数据库配置（从 config.py 导入）
    # 如需修改，请编辑 selenium_fetcher/config.py 中的 DB_CONFIG_EXAMPLE
    db_config = DB_CONFIG_EXAMPLE.copy()
    
    # 可选：Selenium配置
    selenium_config = {
        'browser': 'edge',        # 浏览器类型: chrome, firefox, edge
        'headless': True,         # 是否无头模式（后台运行）- True=隐藏窗口, False=显示窗口
        'timeout': 30,            # 页面加载超时时间(秒)
        'implicit_wait': 10,      # 隐式等待时间(秒)
    }
    
    # 创建获取器实例
    fetcher = SeleniumDoubanFetcher(
        db_config=db_config,
        selenium_config=selenium_config
    )
    
    # 设置信号处理（支持 Ctrl+C 优雅停止）
    def signal_handler(sig, frame):
        if sig == signal.SIGINT:
            print("\n\n⚠️  检测到停止信号 (Ctrl+C)")
        else:
            print(f"\n\n⚠️  检测到停止信号")
        print("正在优雅停止任务...（请勿强制关闭，等待程序自然退出）")
        fetcher.stop_requested = True
    
    # 注册信号处理器
    try:
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # 终止信号
        # 注意：Windows 不支持 SIGTSTP (Ctrl+Z)，该快捷键在Windows下无效
        # 建议使用 Ctrl+C 或创建 stop.flag 文件
    except (ValueError, OSError) as e:
        print(f"警告: 无法注册所有信号处理器: {e}")
    
    print("=" * 70)
    print("提示：以下方法可以优雅停止任务：")
    print("  1. 按 Ctrl+C (推荐，Windows唯一支持的快捷键)")
    print("  2. 创建 'stop.flag' 文件（适合后台运行）")
    print("\n注意：Windows系统不支持 Ctrl+Z 停止")
    print("=" * 70)
    
    # 运行任务
    fetcher.run(
        batch_size=DEFAULT_RUN_CONFIG['batch_size']
    )


if __name__ == '__main__':
    main()
