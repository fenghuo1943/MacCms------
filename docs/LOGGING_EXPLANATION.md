# Selenium 日志配置详解

## 问题：为什么禁用 selenium_fetcher 日志后，主程序也不输出了？

### 原因分析

**误解澄清**：实际上只有一条 "成功提取电影信息" 的日志，不是两条。

#### 日志来源

```python
# selenium_fetcher/extractor.py 第293行
logger.info(f"成功提取电影信息: {info.get('title', 'Unknown')}")
```

这个 `logger` 是 `selenium_fetcher` 模块的 logger：
```python
# selenium_fetcher/config.py 第8行
logger = logging.getLogger('selenium_fetcher')
```

#### 为什么看起来像两条？

可能的原因：
1. **日志格式相似**，误以为是两条
2. **之前的缓存**，看到的是历史输出
3. **其他模块的类似日志**

### Python Logging 层级关系

```
root logger (douban_fetcher 配置)
    └── selenium_fetcher logger (子logger)
```

当你设置 `logger.disabled = True` 时：
- ✅ `selenium_fetcher` logger 被完全禁用
- ❌ 所有使用该 logger 的日志都不会输出
- ⚠️ 不影响 root logger 或其他 logger

## 已实施的解决方案

### 方案1：提高日志级别（已采用）

**文件**: `selenium_fetcher/config.py`

```python
logger.setLevel(logging.WARNING)  # 只显示WARNING和ERROR
```

**效果**：
- ✅ INFO 级别的日志不输出（包括"成功提取电影信息"）
- ✅ WARNING 和 ERROR 仍然输出（用于调试问题）
- ✅ 保持日志系统的完整性

### 方案2：注释掉特定日志（已采用）

**文件**: `selenium_fetcher/extractor.py` 第293行

```python
# logger.info(f"成功提取电影信息: {info.get('title', 'Unknown')}")
```

**效果**：
- ✅ 精确控制哪些日志输出
- ✅ 减少不必要的日志噪音
- ✅ 保留重要的错误和警告日志

### 方案3：使用主程序 Logger（可选）

**文件**: `selenium_fetcher/fetcher.py`

```python
# 导入主程序的logger
from douban_fetcher.config import logger as main_logger

# 在成功处理后输出
main_logger.info(f"✓ ID:{vod_id} {vod_name} - {msg}")
```

**优点**：
- 使用统一的日志格式
- 更容易追踪整个流程
- 不受 selenium_fetcher logger 禁用影响

## 日志级别说明

| 级别 | 值 | 用途 | 是否输出 |
|------|-----|------|---------|
| DEBUG | 10 | 调试信息 | ❌ |
| INFO | 20 | 一般信息 | ❌ (已禁用) |
| WARNING | 30 | 警告信息 | ✅ |
| ERROR | 40 | 错误信息 | ✅ |
| CRITICAL | 50 | 严重错误 | ✅ |

## 如何自定义日志输出

### 想看到更多日志

编辑 `selenium_fetcher/config.py`：

```python
# 显示INFO级别
logger.setLevel(logging.INFO)

# 或者完全启用
logger.setLevel(logging.DEBUG)
logger.disabled = False
```

### 想隐藏所有日志

```python
logger.setLevel(logging.CRITICAL)
logger.disabled = True
```

### 只想隐藏特定的INFO日志

注释掉对应的 `logger.info()` 调用，如 extractor.py 第293行。

## 最佳实践

### 1. 分层日志策略

```python
# 开发环境：详细日志
logger.setLevel(logging.DEBUG)

# 测试环境：一般日志
logger.setLevel(logging.INFO)

# 生产环境：只记录问题和错误
logger.setLevel(logging.WARNING)
```

### 2. 关键操作记录

```python
# ✅ 应该记录的
logger.error("数据库连接失败")
logger.warning("API请求超时，重试中...")
logger.critical("系统资源不足")

# ❌ 不需要记录的
logger.info("成功提取电影信息")  # 太频繁，产生噪音
logger.debug("变量x的值为5")     # 只在调试时需要
```

### 3. 使用不同的Logger

```python
# 为不同模块创建独立的logger
api_logger = logging.getLogger('selenium_fetcher.api')
browser_logger = logging.getLogger('selenium_fetcher.browser')
extractor_logger = logging.getLogger('selenium_fetcher.extractor')

# 可以分别控制
api_logger.setLevel(logging.WARNING)
browser_logger.setLevel(logging.ERROR)
extractor_logger.setLevel(logging.INFO)
```

## 常见问题

### Q: 为什么设置了 disabled=True 后，ERROR 也不输出了？

A: `disabled=True` 会完全禁用该 logger，所有级别的日志都不会输出。如果只想隐藏 INFO，应该使用 `setLevel(logging.WARNING)`。

### Q: 如何让不同的模块使用不同的日志级别？

A: 为每个模块创建独立的 logger：
```python
logger1 = logging.getLogger('module1')
logger2 = logging.getLogger('module2')
logger1.setLevel(logging.INFO)
logger2.setLevel(logging.ERROR)
```

### Q: 日志输出到文件和控制台，如何只隐藏控制台的？

A: 配置不同的 Handler：
```python
# 文件Handler：记录所有日志
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# 控制台Handler：只显示WARNING以上
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
```

## 相关文件

- 日志配置：`selenium_fetcher/config.py`
- 日志输出：`selenium_fetcher/extractor.py` (第293行，已注释)
- 主程序日志：`douban_fetcher/config.py`
- 详细说明：`docs/SELENIUM_LOGGING_GUIDE.md`

---

**最后更新**: 2026-04-17
**状态**: 已优化，减少日志噪音，保留重要信息
