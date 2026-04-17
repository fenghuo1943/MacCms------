"""
Selenium浏览器驱动管理模块
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from typing import Optional

from .config import logger, SELENIUM_CONFIG


class BrowserManager:
    """浏览器驱动管理器"""
    
    def __init__(self, config: dict = None):
        """
        初始化浏览器管理器
        
        Args:
            config: Selenium配置字典（会与默认配置合并）
        """
        # 合并配置：默认配置 + 用户配置
        from .config import SELENIUM_CONFIG
        self.config = SELENIUM_CONFIG.copy()
        if config:
            self.config.update(config)
        self.driver = None
        self.wait = None
    
    def init_driver(self):
        """初始化WebDriver"""
        try:
            if self.config['browser'].lower() == 'chrome':
                self._init_chrome()
            elif self.config['browser'].lower() == 'firefox':
                self._init_firefox()
            elif self.config['browser'].lower() == 'edge':
                self._init_edge()
            else:
                raise ValueError(f"不支持的浏览器类型: {self.config['browser']}")
            
            # 设置隐式等待
            self.driver.implicitly_wait(self.config['implicit_wait'])
            self.wait = WebDriverWait(self.driver, self.config['timeout'])
            
            logger.info(f"Selenium驱动初始化成功 ({self.config['browser']})")
            
        except Exception as e:
            logger.error(f"Selenium驱动初始化失败: {str(e)}")
            raise
    
    def _init_chrome(self):
        """初始化Chrome浏览器"""
        options = ChromeOptions()
        
        if self.config['headless']:
            options.add_argument('--headless')
        
        options.add_argument(f'user-agent={self.config["user_agent"]}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 禁用日志输出
        options.add_argument('--log-level=3')  # 只显示致命错误
        options.add_argument('--silent')       # 静默模式
        
        # 设置窗口大小
        options.add_argument(
            f'--window-size={self.config["window_size"][0]},{self.config["window_size"][1]}'
        )
        
        self.driver = webdriver.Chrome(options=options)
        
        # 执行CDP命令来隐藏webdriver属性
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
    
    def _init_firefox(self):
        """初始化Firefox浏览器"""
        options = FirefoxOptions()
        
        if self.config['headless']:
            options.add_argument('--headless')
        
        options.set_preference('general.useragent.override', self.config['user_agent'])
        options.set_preference('dom.webdriver.enabled', False)
        options.set_preference('useAutomationExtension', False)
        
        self.driver = webdriver.Firefox(options=options)
    
    def _init_edge(self):
        """初始化Edge浏览器"""
        options = EdgeOptions()
        
        if self.config['headless']:
            options.add_argument('--headless')
        
        options.add_argument(f'user-agent={self.config["user_agent"]}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 禁用日志输出
        options.add_argument('--log-level=3')  # 只显示致命错误
        options.add_argument('--silent')       # 静默模式
        
        # 设置窗口大小
        options.add_argument(
            f'--window-size={self.config["window_size"][0]},{self.config["window_size"][1]}'
        )
        
        self.driver = webdriver.Edge(options=options)
        
        # 执行CDP命令来隐藏webdriver属性（Edge也支持）
        try:
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
        except Exception as e:
            logger.warning(f"Edge CDP命令执行失败（非致命）: {str(e)}")
    
    def quit_driver(self):
        """关闭WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Selenium驱动已关闭")
            except Exception as e:
                logger.warning(f"关闭Selenium驱动时出错: {str(e)}")
            finally:
                self.driver = None
                self.wait = None
    
    def get_driver(self):
        """获取WebDriver实例，如果未初始化则自动初始化"""
        if self.driver is None:
            self.init_driver()
        return self.driver
    
    def get_wait(self):
        """获取WebDriverWait实例"""
        if self.wait is None:
            self.init_driver()
        return self.wait
