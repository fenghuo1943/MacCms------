# Selenium配置说明

## 配置合并机制

`BrowserManager` 采用**智能配置合并**机制：
- 默认配置来自 `SELENIUM_CONFIG`
- 用户传入的配置会覆盖默认配置
- 未指定的字段使用默认值

## 使用示例

### 方式1: 使用默认配置（推荐）
```python
from selenium_fetcher import SeleniumDoubanFetcher
from selenium_fetcher.config import DB_CONFIG_EXAMPLE

# 不传selenium_config，使用全部默认值
fetcher = SeleniumDoubanFetcher(DB_CONFIG_EXAMPLE)
```

### 方式2: 部分配置覆盖
```python
# 只指定需要修改的配置
selenium_config = {
    'headless': False,  # 显示浏览器窗口
}

fetcher = SeleniumDoubanFetcher(
    DB_CONFIG_EXAMPLE,
    selenium_config=selenium_config
)
# 其他配置自动使用默认值
```

### 方式3: 完整自定义配置
```python
selenium_config = {
    'browser': 'chrome',
    'headless': True,
    'timeout': 60,
    'implicit_wait': 15,
    'user_agent': 'Custom UA',
    'window_size': (1920, 1080),
}

fetcher = SeleniumDoubanFetcher(
    DB_CONFIG_EXAMPLE,
    selenium_config=selenium_config
)
```

## 配置项说明

### SELENIUM_CONFIG 默认值

```python
SELENIUM_CONFIG = {
    'browser': 'chrome',           # 浏览器类型: chrome, firefox
    'headless': True,              # 无头模式（后台运行）
    'timeout': 30,                 # 页面加载超时时间(秒)
    'implicit_wait': 10,           # 隐式等待时间(秒)
    'user_agent': 'Mozilla/5.0...', # User-Agent字符串
    'window_size': (1920, 1080),   # 浏览器窗口大小
}
```

### 常用配置场景

#### 1. 调试模式（显示浏览器）
```python
selenium_config = {
    'headless': False,  # 显示浏览器窗口，方便调试
}
```

#### 2.  Firefox浏览器
```python
selenium_config = {
    'browser': 'firefox',
}
```

#### 3. 增加超时时间（网络慢时）
```python
selenium_config = {
    'timeout': 60,         # 增加到60秒
    'implicit_wait': 20,   # 增加到20秒
}
```

#### 4. 移动端模拟
```python
selenium_config = {
    'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)...',
    'window_size': (375, 667),  # iPhone尺寸
}
```

## 在 main_selenium.py 中配置

```python
def main():
    # 数据库配置
    db_config = DB_CONFIG_EXAMPLE.copy()
    
    # Selenium配置（只需指定需要修改的项）
    selenium_config = {
        'headless': True,      # 后台运行
        # 'timeout': 60,       # 如需修改可取消注释
        # 'browser': 'firefox' # 如需切换浏览器可取消注释
    }
    
    # 创建获取器
    fetcher = SeleniumDoubanFetcher(
        db_config=db_config,
        selenium_config=selenium_config  # 可以传None使用默认配置
    )
    
    # 运行任务
    fetcher.run(batch_size=50)
```

## 配置验证

可以通过以下方式验证配置是否正确合并：

```python
from selenium_fetcher.browser import BrowserManager

# 测试配置合并
bm = BrowserManager({'headless': False})
print(bm.config)
# 输出: {
#     'browser': 'chrome',      # 默认值
#     'headless': False,         # 被覆盖
#     'timeout': 30,             # 默认值
#     'implicit_wait': 10,       # 默认值
#     'user_agent': '...',       # 默认值
#     'window_size': (1920, 1080) # 默认值
# }
```

## 注意事项

⚠️ **重要提醒**:

1. **不要传入None以外的不完整配置**
   ```python
   # ✗ 错误：缺少必要字段
   config = {'browser': 'chrome'}  # 缺少user_agent等
   
   # ✓ 正确：让BrowserManager自动合并
   config = {'browser': 'chrome'}  # BrowserManager会补充缺失字段
   ```

2. **headless模式建议**
   - 生产环境: `True`（后台运行，节省资源）
   - 调试环境: `False`（可以看到浏览器操作）

3. **超时设置**
   - 网络好: `timeout=30`
   - 网络差: `timeout=60`
   - 不建议超过120秒

4. **窗口大小**
   - 桌面端: `(1920, 1080)` 或 `(1366, 768)`
   - 移动端: `(375, 667)` (iPhone) 或 `(360, 640)` (Android)

## 故障排除

### 问题1: 'user_agent' KeyError
**原因**: 旧版本代码直接使用用户配置，未合并默认值  
**解决**: 已修复，现在会自动合并配置

### 问题2: WebDriver初始化失败
**检查**:
```python
# 打印配置查看是否正确
fetcher = SeleniumDoubanFetcher(db_config, selenium_config)
print(fetcher.browser_manager.config)
```

### 问题3: 配置不生效
**检查**:
- 确认传入的是字典而不是None
- 确认键名拼写正确
- 查看日志输出的实际配置

---

**更新时间**: 2026-04-17  
**版本**: v1.1.1 (配置合并优化)
