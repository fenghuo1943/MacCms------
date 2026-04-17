# Selenium Fetcher 日志隐藏说明

## 问题描述

运行时出现重复的日志输出：
```
2026-04-17 12:56:12,839 - selenium_fetcher - INFO - 成功提取电影信息: 黑猩猩帝国 Chimp Empire
2026-04-17 12:56:12,839 - INFO - 成功提取电影信息: 黑猩猩帝国 Chimp Empire
```

## 日志来源分析

### 第一条日志（带 `selenium_fetcher` 前缀）
```
2026-04-17 12:56:12,839 - selenium_fetcher - INFO - 成功提取电影信息: ...
         ↑                    ↑                ↑
       时间戳              模块名            日志级别
```

**来源文件**：`selenium_fetcher/extractor.py` 第293行
```python
logger.info(f"成功提取电影信息: {info.get('title', 'Unknown')}")
```

**Logger定义**：`selenium_fetcher/config.py` 第8行
```python
logger = logging.getLogger('selenium_fetcher')
```

**Formatter格式**：
```python
'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
               ↑
          这里会显示模块名 'selenium_fetcher'
```

### 第二条日志（不带模块名）
```
2026-04-17 12:56:12,839 - INFO - 成功提取电影信息: ...
         ↑                    ↑
       时间戳              日志级别（无模块名）
```

**来源**：这是主程序 `douban_fetcher` 的 logger 输出的，使用了不同的 formatter 格式。

## 解决方案

### 已实施的修复

在 `selenium_fetcher/config.py` 中禁用 logger：

```python
# 配置日志
logger = logging.getLogger('selenium_fetcher')
logger.setLevel(logging.CRITICAL)  # 设置为CRITICAL，几乎不输出任何日志
logger.disabled = True  # 完全禁用此logger的输出
```

### 效果

修复后，只会看到第二条日志（来自主程序），第一条带有 `selenium_fetcher` 前缀的日志将被隐藏。

**修复前**：
```
2026-04-17 12:56:12,839 - selenium_fetcher - INFO - 成功提取电影信息: 黑猩猩帝国 Chimp Empire
2026-04-17 12:56:12,839 - INFO - 成功提取电影信息: 黑猩猩帝国 Chimp Empire
```

**修复后**：
```
2026-04-17 12:56:12,839 - INFO - 成功提取电影信息: 黑猩猩帝国 Chimp Empire
```

## 其他可选方案

### 方案1：提高日志级别（保留错误日志）
```python
logger.setLevel(logging.WARNING)  # 只显示WARNING和ERROR
# 不使用 logger.disabled = True
```

### 方案2：只删除特定的INFO日志
编辑 `selenium_fetcher/extractor.py` 第293行，注释掉或删除：
```python
# logger.info(f"成功提取电影信息: {info.get('title', 'Unknown')}")
```

### 方案3：修改日志格式（不显示模块名）
编辑 `selenium_fetcher/config.py` 第13-14行：
```python
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'  # 移除 %(name)s
)
```

## 为什么会有两条日志？

这是因为代码中存在两个不同的 logger：

1. **selenium_fetcher 的 logger**：
   - 定义在 `selenium_fetcher/config.py`
   - 名称：`'selenium_fetcher'`
   - 格式：包含模块名 `%(name)s`

2. **douban_fetcher 的 logger**（主程序）：
   - 定义在 `douban_fetcher/config.py`
   - 名称：`'douban_fetcher'` 或 root logger
   - 格式：可能不包含模块名

当 selenium_fetcher 完成数据提取后，可能会将结果传递给主程序，主程序再次记录日志，导致重复输出。

## 验证修复

运行程序观察日志输出：
```bash
python main_selenium.py
```

应该只看到不带 `selenium_fetcher` 前缀的日志。

## 相关文件

- 日志配置：`selenium_fetcher/config.py` (第7-17行)
- 日志输出：`selenium_fetcher/extractor.py` (第293行)
- 主程序日志：`douban_fetcher/config.py`
