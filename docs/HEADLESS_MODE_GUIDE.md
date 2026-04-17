# Selenium 无头模式配置说明

## 问题原因

之前浏览器窗口仍然显示的原因是：**main_selenium.py 中的配置覆盖了默认配置**。

## 配置优先级

配置按照以下优先级合并（后面的会覆盖前面的）：

```
默认配置 (selenium_fetcher/config.py)
    ↓ 被覆盖
运行时配置 (main_selenium.py 中的 selenium_config)
```

### 之前的错误配置
```python
# main_selenium.py 第24行
selenium_config = {
    'headless': False,  # ❌ 这里设置为False，覆盖了默认的True
}
```

### 修复后的配置
```python
# main_selenium.py 第24行
selenium_config = {
    'headless': True,   # ✅ 现在设置为True，浏览器窗口会隐藏
}
```

## 如何控制浏览器窗口显示

### 方法1：修改 main_selenium.py（推荐）

编辑 `main_selenium.py` 第24行：

```python
# 隐藏浏览器窗口（生产环境）
'headless': True,

# 显示浏览器窗口（调试用）
'headless': False,
```

### 方法2：修改默认配置

编辑 `selenium_fetcher/config.py` 第25行：

```python
SELENIUM_CONFIG = {
    'headless': True,  # 修改这里的默认值
    ...
}
```

> ⚠️ 注意：如果 main_selenium.py 中显式设置了 headless，这个默认值会被覆盖。

## 验证配置是否生效

运行测试脚本：
```bash
python tests/test_headless_mode.py
```

或者运行主程序观察：
```bash
python main_selenium.py
```

- ✅ **无头模式生效**：不会看到浏览器窗口，任务在后台运行
- ❌ **无头模式未生效**：会弹出Edge浏览器窗口

## 常见问题

### Q: 为什么配置了 headless=True 还是显示窗口？

A: 检查是否有地方显式设置了 `headless: False`：
1. 检查 `main_selenium.py` 中的 `selenium_config`
2. 检查创建 `SeleniumDoubanFetcher` 时传入的配置
3. 检查是否有其他代码调用了 `BrowserManager` 并传入了配置

### Q: 调试时想看到浏览器窗口怎么办？

A: 临时修改 `main_selenium.py`：
```python
selenium_config = {
    'headless': False,  # 改为False，显示窗口
    ...
}
```

### Q: 无头模式和普通模式有什么区别？

| 特性 | 无头模式 (True) | 有头模式 (False) |
|------|----------------|-----------------|
| 显示窗口 | ❌ 不显示 | ✅ 显示 |
| 性能 | ⚡ 更快 | 🐢 较慢 |
| 资源占用 | 💾 较少 | 💾 较多 |
| 适用场景 | 生产环境 | 调试测试 |
| 可见性 | 后台运行 | 可以看到操作过程 |

## 最佳实践

- ✅ **生产环境**：使用 `headless: True`（隐藏窗口，性能更好）
- 🔧 **开发调试**：使用 `headless: False`（显示窗口，方便观察）
- 📝 **注释说明**：在配置旁边添加注释，说明当前设置的作用

## 相关文件

- 默认配置：`selenium_fetcher/config.py` (第23-30行)
- 主程序配置：`main_selenium.py` (第22-27行)
- 浏览器初始化：`selenium_fetcher/browser.py` (第101-136行)
- 测试脚本：`tests/test_headless_mode.py`
