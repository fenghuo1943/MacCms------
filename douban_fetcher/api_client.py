"""
API客户端模块
"""
import requests
import time
import random
from typing import Optional, List, Dict
from .config import logger, API_CONFIG, DOUBAN_API_CONFIG


class ApiClient:
    """WMDB API客户端"""
    
    def __init__(self, use_proxy: bool = False, proxy_list: List[str] = None, rate_limiter=None):
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        self.current_proxy_index = 0
        self.rate_limiter = rate_limiter  # 速率限制器
        
        self.session = requests.Session()
        self.session.headers.update(API_CONFIG['headers'])
    
    def get_next_proxy(self) -> Optional[str]:
        """获取下一个代理"""
        if not self.proxy_list:
            return None
        
        proxy = self.proxy_list[self.current_proxy_index % len(self.proxy_list)]
        self.current_proxy_index += 1
        return proxy
    
    def search_video(self, video_name: str, monitor=None, max_retries: int = 5) -> Optional[List[Dict]]:
        """
        搜索视频
        
        Args:
            video_name: 视频名称
            monitor: 速率监控器（可选）
            max_retries: 最大重试次数
            
        Returns:
            搜索结果列表，失败返回None
        """
        # 在API调用前进行速率限制
        if self.rate_limiter:
            self.rate_limiter.acquire(timeout=60)
        
        url = API_CONFIG['base_url']
        params = {'q': video_name}
        
        base_delay = 1
        for attempt in range(max_retries):
            try:
                proxies = None
                if self.use_proxy and self.proxy_list:
                    proxy = self.get_next_proxy()
                    proxies = {'http': proxy, 'https': proxy}
                
                response = self.session.get(
                    url,
                    params=params,
                    timeout=API_CONFIG['timeout'],
                    proxies=proxies
                )
                
                if response.status_code == 429:
                    wait_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"触发频率限制，等待 {wait_time:.1f} 秒")
                    if monitor:
                        monitor.record_request(False, rate_limited=True)
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                if not isinstance(data, dict) or 'data' not in data:
                    logger.warning(f"API返回格式异常")
                    if monitor:
                        monitor.record_request(False)
                    return None
                
                result_data = data.get('data', [])
                if not isinstance(result_data, list):
                    if monitor:
                        monitor.record_request(False)
                    return None
                
                if monitor:
                    monitor.record_request(True)
                return result_data
                
            except requests.exceptions.Timeout:
                logger.warning(f"请求超时 (尝试 {attempt + 1}/{max_retries})")
                if monitor:
                    monitor.record_request(False)
                if attempt < max_retries - 1:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                return None
                
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"连接错误 (尝试 {attempt + 1}/{max_retries}): {str(e)[:100]}")
                if monitor:
                    monitor.record_request(False)
                if attempt < max_retries - 1:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                return None
                
            except Exception as e:
                logger.error(f"请求异常: {video_name}, 错误: {str(e)[:100]}")
                if monitor:
                    monitor.record_request(False)
                return None
        
        return None
    
    def get_douban_by_imdb(self, imdb_id: str, monitor=None, max_retries: int = 5) -> Optional[Dict]:
        """
        通过IMDB ID从豆瓣API获取信息
        
        Args:
            imdb_id: IMDB ID
            monitor: 速率监控器（可选）
            max_retries: 最大重试次数
            
        Returns:
            豆瓣信息字典，失败返回None
        """
        if not imdb_id:
            logger.warning("IMDB ID为空")
            if monitor:
                monitor.record_request(False)
            return None
        
        # 在API调用前进行速率限制
        if self.rate_limiter:
            self.rate_limiter.acquire(timeout=60)
        
        url = f"{DOUBAN_API_CONFIG['base_url']}{imdb_id}"
        
        base_delay = 1
        for attempt in range(max_retries):
            try:
                proxies = None
                if self.use_proxy and self.proxy_list:
                    proxy = self.get_next_proxy()
                    proxies = {'http': proxy, 'https': proxy}
                
                # 使用POST方法，apikey在请求体中
                data = {'apikey': DOUBAN_API_CONFIG['apikey']}
                
                response = self.session.post(
                    url,
                    data=data,
                    timeout=DOUBAN_API_CONFIG['timeout'],
                    proxies=proxies
                )
                
                if response.status_code == 429:
                    wait_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"豆瓣API触发频率限制，等待 {wait_time:.1f} 秒")
                    if monitor:
                        monitor.record_request(False, rate_limited=True)
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                if not isinstance(data, dict):
                    logger.warning(f"豆瓣API返回格式异常")
                    if monitor:
                        monitor.record_request(False)
                    return None
                
                if monitor:
                    monitor.record_request(True)
                return data
                
            except requests.exceptions.Timeout:
                logger.warning(f"豆瓣API请求超时 (尝试 {attempt + 1}/{max_retries})")
                if monitor:
                    monitor.record_request(False)
                if attempt < max_retries - 1:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                return None
                
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"豆瓣API连接错误 (尝试 {attempt + 1}/{max_retries}): {str(e)[:100]}")
                if monitor:
                    monitor.record_request(False)
                if attempt < max_retries - 1:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                return None
                
            except Exception as e:
                logger.error(f"豆瓣API请求异常: {imdb_id}, 错误: {str(e)[:100]}")
                if monitor:
                    monitor.record_request(False)
                return None
        
        return None
    
    def get_douban_by_id(self, douban_id: str, monitor=None, max_retries: int = 5) -> Optional[Dict]:
        """
        通过豆瓣ID从豆瓣API获取信息
        
        Args:
            douban_id: 豆瓣ID
            monitor: 速率监控器（可选）
            max_retries: 最大重试次数
            
        Returns:
            豆瓣信息字典，失败返回None
        """
        if not douban_id:
            logger.warning("豆瓣ID为空")
            if monitor:
                monitor.record_request(False)
            return None
        
        # 在API调用前进行速率限制
        if self.rate_limiter:
            self.rate_limiter.acquire(timeout=60)
        
        # 使用subject路径而不是imdb路径
        url = f"https://api.douban.com/v2/movie/subject/{douban_id}"
        
        base_delay = 1
        for attempt in range(max_retries):
            try:
                proxies = None
                if self.use_proxy and self.proxy_list:
                    proxy = self.get_next_proxy()
                    proxies = {'http': proxy, 'https': proxy}
                
                # 使用POST方法，apikey在请求体中
                data = {'apikey': DOUBAN_API_CONFIG['apikey']}
                
                response = self.session.post(
                    url,
                    data=data,
                    timeout=DOUBAN_API_CONFIG['timeout'],
                    proxies=proxies
                )
                
                if response.status_code == 429:
                    wait_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"豆瓣API触发频率限制，等待 {wait_time:.1f} 秒")
                    if monitor:
                        monitor.record_request(False, rate_limited=True)
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                if not isinstance(data, dict):
                    logger.warning(f"豆瓣API返回格式异常")
                    if monitor:
                        monitor.record_request(False)
                    return None
                
                if monitor:
                    monitor.record_request(True)
                return data
                
            except requests.exceptions.Timeout:
                logger.warning(f"豆瓣API请求超时 (尝试 {attempt + 1}/{max_retries})")
                if monitor:
                    monitor.record_request(False)
                if attempt < max_retries - 1:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                return None
                
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"豆瓣API连接错误 (尝试 {attempt + 1}/{max_retries}): {str(e)[:100]}")
                if monitor:
                    monitor.record_request(False)
                if attempt < max_retries - 1:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                return None
                
            except Exception as e:
                logger.error(f"豆瓣API请求异常: {douban_id}, 错误: {str(e)[:100]}")
                if monitor:
                    monitor.record_request(False)
                return None
        
        return None
