"""
测试优雅停止功能

这个脚本演示如何使用不同的方法停止任务
"""
import os
import time
import threading
from douban_fetcher import DoubanScoreFetcher
from douban_fetcher.config import DB_CONFIG_EXAMPLE, DEFAULT_RUN_CONFIG


def test_signal_handler():
    """测试信号处理器（需要手动按 Ctrl+C 或 Ctrl+Z）"""
    print("=" * 70)
    print("测试1: 信号处理器")
    print("=" * 70)
    print("程序将在3秒后启动...")
    print("启动后请按 Ctrl+C 或 Ctrl+Z 来测试停止功能")
    print("=" * 70)
    time.sleep(3)
    
    db_config = DB_CONFIG_EXAMPLE.copy()
    fetcher = DoubanScoreFetcher(
        db_config=db_config,
        max_requests_per_second=DEFAULT_RUN_CONFIG['max_requests_per_second'],
        use_proxy=DEFAULT_RUN_CONFIG['use_proxy'],
        proxy_list=DEFAULT_RUN_CONFIG['proxy_list']
    )
    
    # 注意：这个测试会实际运行任务，请准备好按 Ctrl+C
    fetcher.run(
        batch_size=5,  # 小批量用于测试
        max_requests_per_second=DEFAULT_RUN_CONFIG['max_requests_per_second'],
        adjust_rate=False
    )


def test_stop_flag_file():
    """测试停止文件方法"""
    print("=" * 70)
    print("测试2: 停止文件方法")
    print("=" * 70)
    
    db_config = DB_CONFIG_EXAMPLE.copy()
    fetcher = DoubanScoreFetcher(
        db_config=db_config,
        max_requests_per_second=DEFAULT_RUN_CONFIG['max_requests_per_second'],
        use_proxy=DEFAULT_RUN_CONFIG['use_proxy'],
        proxy_list=DEFAULT_RUN_CONFIG['proxy_list']
    )
    
    def run_task():
        """在后台运行任务"""
        fetcher.run(
            batch_size=10,
            max_requests_per_second=0.5,  # 慢速以便观察
            adjust_rate=False
        )
    
    # 启动任务线程
    task_thread = threading.Thread(target=run_task, daemon=True)
    task_thread.start()
    
    print("任务已启动，等待5秒...")
    time.sleep(5)
    
    # 创建停止文件
    print("创建停止文件: stop.flag")
    with open("stop.flag", "w") as f:
        f.write("")
    
    print("等待任务停止...")
    task_thread.join(timeout=30)  # 最多等待30秒
    
    if not task_thread.is_alive():
        print("✓ 任务已成功停止")
    else:
        print("✗ 任务未在预期时间内停止")
    
    # 清理
    if os.path.exists("stop.flag"):
        os.remove("stop.flag")


def test_programmatic_stop():
    """测试程序化停止"""
    print("=" * 70)
    print("测试3: 程序化停止")
    print("=" * 70)
    
    db_config = DB_CONFIG_EXAMPLE.copy()
    fetcher = DoubanScoreFetcher(
        db_config=db_config,
        max_requests_per_second=DEFAULT_RUN_CONFIG['max_requests_per_second'],
        use_proxy=DEFAULT_RUN_CONFIG['use_proxy'],
        proxy_list=DEFAULT_RUN_CONFIG['proxy_list']
    )
    
    def run_task():
        """在后台运行任务"""
        fetcher.run(
            batch_size=10,
            max_requests_per_second=0.5,
            adjust_rate=False
        )
    
    # 启动任务线程
    task_thread = threading.Thread(target=run_task, daemon=True)
    task_thread.start()
    
    print("任务已启动，等待5秒...")
    time.sleep(5)
    
    # 设置停止标志
    print("设置停止标志: fetcher.stop_requested = True")
    fetcher.stop_requested = True
    
    print("等待任务停止...")
    task_thread.join(timeout=30)
    
    if not task_thread.is_alive():
        print("✓ 任务已成功停止")
    else:
        print("✗ 任务未在预期时间内停止")


def main():
    """主函数"""
    print("\n")
    print("=" * 70)
    print("优雅停止功能测试")
    print("=" * 70)
    print("\n请选择测试方法：")
    print("1. 测试信号处理器 (Ctrl+C / Ctrl+Z)")
    print("2. 测试停止文件方法")
    print("3. 测试程序化停止")
    print("=" * 70)
    
    choice = input("\n请输入选项 (1/2/3): ").strip()
    
    if choice == "1":
        test_signal_handler()
    elif choice == "2":
        test_stop_flag_file()
    elif choice == "3":
        test_programmatic_stop()
    else:
        print("无效选项")


if __name__ == '__main__':
    main()
