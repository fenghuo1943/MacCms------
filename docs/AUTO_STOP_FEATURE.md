# 自动停止功能说明

## 问题描述

在使用豆瓣API进行多次获取后，可能会出现无法搜索得到视频信息的情况，并且也没有报429错误（静默限制）。这会导致程序继续无效请求，浪费时间。

## 解决方案

实现了三层自动停止检测机制：

### 1. 连续API请求失败检测

**实现位置**: `douban_fetcher/api_client.py`

- 在 `ApiClient` 类中添加了 `consecutive_failures` 计数器
- 当API请求失败时（超时、连接错误、异常等），计数器+1
- 当API请求成功时，计数器重置为0
- 默认阈值：10次连续失败

**检测的失败类型**:
- 请求超时
- 连接错误
- 返回格式异常
- 其他网络异常

### 2. 连续无结果检测

**实现位置**: `douban_fetcher/fetcher.py`

- 在 `DoubanScoreFetcher` 类中添加了 `consecutive_no_results` 计数器
- 当搜索返回空结果列表时，计数器+1
- 当搜索返回有结果时，计数器重置为0
- 默认阈值：20次连续无结果

**为什么需要这个检测**:
- 豆瓣API可能在不返回429状态码的情况下静默限制
- 表现为持续返回空结果列表
- 这种情况下需要主动停止，避免无效请求

### 3. 整批失败检测

**实现位置**: `douban_fetcher/fetcher.py` 的 `run()` 方法

- 每批处理完成后检查
- 如果一批数据全部处理失败
- 且连续失败次数 >= 5次
- 则自动停止任务

## 代码修改详情

### 1. api_client.py 修改

```python
class ApiClient:
    def __init__(self, ...):
        # 添加连续失败计数器
        self.consecutive_failures = 0
        self.max_consecutive_failures = 10
    
    def search_douban(self, ...):
        # 在失败时增加计数
        self.consecutive_failures += 1
        # 在成功时重置计数
        self.consecutive_failures = 0
    
    def get_douban_subject(self, ...):
        # 同样的逻辑
```

### 2. fetcher.py 修改

```python
class DoubanScoreFetcher:
    def __init__(self, ...):
        # 添加连续无结果计数器
        self.consecutive_no_results = 0
        self.max_consecutive_no_results = 20
    
    def process_single_video(self, video):
        # 无结果时增加计数
        if len(search_results) == 0:
            self.consecutive_no_results += 1
            logger.warning(f"连续无结果次数: {self.consecutive_no_results}/{self.max_consecutive_no_results}")
        
        # 有结果时重置计数
        if search_results:
            self.consecutive_no_results = 0
    
    def run(self, ...):
        # 批次完成后检查
        if self.api_client.consecutive_failures >= self.api_client.max_consecutive_failures:
            logger.warning("检测到连续失败次数达到阈值，自动停止任务")
            break
        
        if self.consecutive_no_results >= self.max_consecutive_no_results:
            logger.warning("检测到连续无结果次数达到阈值，可能API已被静默限制，自动停止任务")
            break
```

## 使用建议

### 调整阈值

如果默认的阈值不适合你的使用场景，可以在代码中调整：

```python
# 在 api_client.py 中
self.max_consecutive_failures = 10  # 调整为合适的值

# 在 fetcher.py 中
self.max_consecutive_no_results = 20  # 调整为合适的值
```

### 监控日志

运行时注意观察日志输出：
- `连续无结果次数: X/20` - 显示当前连续无结果情况
- `检测到连续失败次数达到阈值` - API被限制的警告
- `检测到连续无结果次数达到阈值` - 静默限制的警告

### 重启策略

当任务自动停止后：
1. 等待一段时间（建议30分钟以上）让API限制解除
2. 重新运行程序，会自动从上次中断的地方继续（断点续传）
3. 如果频繁触发自动停止，考虑降低请求速率

## 测试

运行测试脚本验证功能：

```bash
python test_auto_stop.py
python test_consecutive_failures.py
```

## 注意事项

1. **不是所有无结果都是API限制**: 有些视频确实在豆瓣上找不到，这是正常情况
2. **阈值设置要合理**: 太低会误判，太高会浪费请求
3. **结合速率限制使用**: 自动停止是最后一道防线，主要还是靠合理的速率控制
4. **监控日志很重要**: 通过日志可以判断是真正的API限制还是正常的无结果

## 效果

实施此功能后：
- ✓ 避免在API被限制后继续无效请求
- ✓ 节省时间和API配额
- ✓ 提供清晰的停止原因日志
- ✓ 支持断点续传，限制解除后可继续
