"""
测试无头模式配置
"""
import sys
sys.path.insert(0, 'e:/python/MacCms自动获取评分')

from selenium_fetcher.browser import BrowserManager
from selenium_fetcher.config import SELENIUM_CONFIG
import time

def test_headless_mode():
    """测试无头模式"""
    print("=" * 70)
    print("测试无头模式配置")
    print("=" * 70)
    
    # 测试1: 无头模式（默认）
    print("\n测试1: 无头模式 (headless=True)")
    print("  浏览器将在后台运行，不会显示窗口")
    config_headless = SELENIUM_CONFIG.copy()
    config_headless['headless'] = True
    
    try:
        browser = BrowserManager(config_headless)
        browser.init_driver()
        driver = browser.get_driver()
        
        # 访问一个简单页面测试
        driver.get('https://www.baidu.com')
        print(f"  ✓ 浏览器启动成功")
        print(f"  ✓ 页面标题: {driver.title}")
        print(f"  ✓ 当前URL: {driver.current_url}")
        
        browser.quit_driver()
        print("  ✓ 浏览器已关闭")
    except Exception as e:
        print(f"  ✗ 错误: {str(e)}")
    
    # 测试2: 有头模式（显示窗口）
    print("\n测试2: 有头模式 (headless=False)")
    print("  浏览器窗口将会显示（如果想测试，请取消下面的注释）")
    print("  ⚠️  注意：这会打开一个可见的浏览器窗口")
    
    # 取消下面的注释来测试有头模式
    """
    config_visible = SELENIUM_CONFIG.copy()
    config_visible['headless'] = False
    
    try:
        browser = BrowserManager(config_visible)
        browser.init_driver()
        driver = browser.get_driver()
        
        driver.get('https://www.baidu.com')
        print(f"  ✓ 浏览器窗口已显示")
        print(f"  ✓ 页面标题: {driver.title}")
        
        # 等待5秒让你看到窗口
        print("  等待5秒后关闭...")
        time.sleep(5)
        
        browser.quit_driver()
        print("  ✓ 浏览器已关闭")
    except Exception as e:
        print(f"  ✗ 错误: {str(e)}")
    """
    
    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
    print("\n提示:")
    print("  - headless=True  : 浏览器在后台运行（推荐用于生产环境）")
    print("  - headless=False : 显示浏览器窗口（用于调试和测试）")
    print("  - 修改位置: selenium_fetcher/config.py 第25行")

if __name__ == '__main__':
    test_headless_mode()
