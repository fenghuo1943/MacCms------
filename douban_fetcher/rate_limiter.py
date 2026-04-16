"""
限流器模块 - Token Bucket 算法和速率监控
"""
import time
import threading
from collections import deque
from typing import Dict


class TokenBucket:
    """令牌桶限流器"""
    
    def __init__(self, rate: float, capacity: int):
        """
        Args:
            rate: 每秒产生的令牌数（请求速率）
            capacity: 桶容量（最大突发请求数）
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_time = time.time()
        self.lock = threading.RLock()  # 使用可重入锁，避免嵌套调用时死锁
    
    def acquire(self, blocking=True, timeout=None) -> bool:
        """获取令牌"""
        start_time = time.time()
        
        while True:
            with self.lock:
                now = time.time()
                elapsed = now - self.last_time
                self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
                self.last_time = now
                
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
            
            if not blocking:
                return False
            
            if timeout and (time.time() - start_time) > timeout:
                return False
            
            time.sleep(0.01)


class RateLimitMonitor:
    """速率限制监控器"""
    
    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self.requests = deque()
        self.lock = threading.RLock()  # 使用可重入锁，避免 get_stats 调用 get_current_rate 时死锁
        self.total_requests = 0
        self.failed_requests = 0
        self.rate_limited_count = 0
    
    def record_request(self, success: bool, rate_limited: bool = False):
        """记录请求结果"""
        with self.lock:
            now = time.time()
            self.requests.append(now)
            self.total_requests += 1
            
            if not success:
                self.failed_requests += 1
            if rate_limited:
                self.rate_limited_count += 1
            
            # 清理过期记录
            cutoff = now - self.window_size
            while self.requests and self.requests[0] < cutoff:
                self.requests.popleft()
    
    def get_current_rate(self) -> float:
        """获取当前请求速率（请求/秒）"""
        with self.lock:
            now = time.time()
            cutoff = now - self.window_size
            recent = [r for r in self.requests if r >= cutoff]
            
            if len(recent) < 2:
                return 0.0
            
            time_span = recent[-1] - recent[0]
            if time_span == 0:
                return 0.0
            
            return len(recent) / time_span
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self.lock:
            success_rate = ((self.total_requests - self.failed_requests) / 
                          self.total_requests * 100) if self.total_requests > 0 else 0
            
            return {
                'total_requests': self.total_requests,
                'failed_requests': self.failed_requests,
                'success_rate': f"{success_rate:.2f}%",
                'rate_limited_count': self.rate_limited_count,
                'current_rate': f"{self.get_current_rate():.2f} req/s"
            }
