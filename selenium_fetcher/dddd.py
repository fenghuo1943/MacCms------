"""
查找ChromeDriver位置的脚本
"""
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def find_chromedriver():
    """查找ChromeDriver位置"""
    print("="*70)
    print("查找ChromeDriver位置")
    print("="*70)
    
    # 方法1: 使用Selenium Manager（Selenium 4.x）
    print("\n【方法1】Selenium自动管理（推荐）")
    print("-" * 70)
    try:
        driver = webdriver.Chrome()
        service = driver.service
        print(f"✓ ChromeDriver路径: {service.path}")
        print(f"✓ Chrome版本: {driver.capabilities['browserVersion']}")
        print(f"✓ ChromeDriver版本: {driver.capabilities['chromedriverVersion']}")
        driver.quit()
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    # 方法2: 检查系统PATH
    print("\n【方法2】系统PATH中的ChromeDriver")
    print("-" * 70)
    path_dirs = os.environ.get('PATH', '').split(';')
    for path_dir in path_dirs:
        chromedriver_path = os.path.join(path_dir, 'chromedriver.exe')
        if os.path.exists(chromedriver_path):
            print(f"✓ 找到: {chromedriver_path}")
    
    # 方法3: 常见安装位置
    print("\n【方法3】常见安装位置")
    print("-" * 70)
    common_locations = [
        r"C:\Users\%USERNAME%\.cache\selenium\chromedriver",
        r"C:\WebDriver\chromedriver.exe",
        r".\chromedriver.exe",  # 当前目录
    ]
    
    for loc in common_locations:
        loc = os.path.expandvars(loc)  # 展开环境变量
        if os.path.exists(loc):
            if os.path.isdir(loc):
                # 如果是目录，列出其中的exe文件
                for file in os.listdir(loc):
                    if file.endswith('.exe'):
                        print(f"✓ 找到: {os.path.join(loc, file)}")
            else:
                print(f"✓ 找到: {loc}")
    
    # 方法4: Selenium缓存目录
    print("\n【方法4】Selenium缓存目录")
    print("-" * 70)
    home = os.path.expanduser('~')
    selenium_cache = os.path.join(home, '.cache', 'selenium')
    if os.path.exists(selenium_cache):
        print(f"✓ Selenium缓存目录: {selenium_cache}")
        for root, dirs, files in os.walk(selenium_cache):
            for file in files:
                if 'chromedriver' in file.lower():
                    full_path = os.path.join(root, file)
                    print(f"  - {full_path}")
    else:
        print(f"✗ Selenium缓存目录不存在: {selenium_cache}")
        print("  （首次运行时会自动创建）")
    
    print("\n" + "="*70)
    print("提示:")
    print("1. Selenium 4.x会自动管理ChromeDriver，无需手动下载")
    print("2. 如果需要指定路径，可以这样写:")
    print("   service = Service('你的/chromedriver/路径')")
    print("   driver = webdriver.Chrome(service=service, options=options)")
    print("="*70)

if __name__ == '__main__':
    find_chromedriver()