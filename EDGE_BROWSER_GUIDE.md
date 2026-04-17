# Edge浏览器配置说明

## ✅ 已完成配置

项目已支持 **Microsoft Edge** 浏览器，并设置为默认浏览器。

### 当前配置

```python
SELENIUM_CONFIG = {
    'browser': 'edge',  # 默认使用Edge
    'headless': True,   # 无头模式
    'timeout': 30,
    'implicit_wait': 10,
    'user_agent': 'Mozilla/5.0 ... Edg/120.0.0.0',  # Edge UA
}
```

## 🌐 支持的浏览器

现在支持三种浏览器：

| 浏览器 | 配置值 | 说明 |
|--------|--------|------|
| Chrome | `'chrome'` | Google Chrome |
| Firefox | `'firefox'` | Mozilla Firefox |
| Edge | `'edge'` | Microsoft Edge（默认）✅ |

## 🔧 切换浏览器

### 方式1: 修改配置文件

编辑 `selenium_fetcher/config.py`:

```python
SELENIUM_CONFIG = {
    'browser': 'chrome',  # 改为chrome
    # 或 'browser': 'firefox'  # 改为firefox
    # 或 'browser': 'edge'     # 使用edge
    ...
}
```

### 方式2: 在main_selenium.py中指定

```python
selenium_config = {
    'browser': 'edge',  # 这里指定
    'headless': False,
}

fetcher = SeleniumDoubanFetcher(
    db_config=db_config,
    selenium_config=selenium_config
)
```

### 方式3: 运行时动态切换

```python
from selenium_fetcher.browser import BrowserManager

# 使用Edge
bm = BrowserManager({'browser': 'edge'})

# 使用Chrome
bm = BrowserManager({'browser': 'chrome'})

# 使用Firefox
bm = BrowserManager({'browser': 'firefox'})
```

## 📋 Edge浏览器要求

### 1. 安装Microsoft Edge

确保系统中已安装Microsoft Edge浏览器：
- Windows 10/11: 通常预装
- 下载地址: https://www.microsoft.com/edge

### 2. EdgeDriver自动管理

Selenium 4.x会自动管理EdgeDriver，无需手动下载。

首次运行时会自动：
1. 检测Edge版本
2. 下载匹配的EdgeDriver
3. 缓存到系统目录

### 3. 验证Edge是否可用

```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)
print("✓ Edge浏览器可用")
print(f"Edge版本: {driver.capabilities['browserVersion']}")
driver.quit()
```

## 🎯 Edge浏览器优势

### 相比Chrome的优势

1. **更好的兼容性**
   - Windows系统原生支持
   - 与Windows更新同步

2. **更低的资源占用**
   - 内存管理更优
   - CPU使用率更低

3. **内置功能丰富**
   - 垂直标签页
   - 睡眠标签页
   - PDF阅读器等

4. **企业级支持**
   - Microsoft官方支持
   - 更适合企业环境

### Selenium中的表现

- ✅ 完全兼容Chrome的API
- ✅ 支持相同的反检测技术
- ✅ CDP命令支持良好
- ✅ 驱动管理自动化

## 🔍 查看Edge版本

### 方法1: 通过注册表
```powershell
reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version
```

### 方法2: 通过Python
```python
import subprocess
result = subprocess.run(
    ['reg', 'query', r'HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon'],
    capture_output=True, text=True
)
print(result.stdout)
```

### 方法3: 在浏览器中
打开Edge → 设置 → 关于Microsoft Edge

## ⚙️ Edge特有配置

### 启用睡眠标签页
```python
options = EdgeOptions()
options.add_experimental_option('prefs', {
    'profile.default_content_setting_values.notifications': 2
})
```

### 禁用扩展
```python
options.add_argument('--disable-extensions')
```

### 自定义用户数据目录
```python
options.add_argument(f'--user-data-dir=C:\\EdgeProfile')
```

## 🐛 常见问题

### Q1: EdgeDriver找不到？
**A**: Selenium 4.x会自动下载，确保网络畅通即可。

### Q2: Edge版本不匹配？
**A**: 更新Edge浏览器到最新版本，Selenium会自动匹配。

### Q3: 如何切换到有头模式调试？
```python
selenium_config = {
    'browser': 'edge',
    'headless': False,  # 显示浏览器窗口
}
```

### Q4: Edge启动很慢？
**A**: 尝试禁用不必要的扩展：
```python
options.add_argument('--disable-extensions')
options.add_argument('--no-first-run')
```

## 📊 性能对比

| 指标 | Chrome | Edge | Firefox |
|------|--------|------|---------|
| 启动速度 | 快 | **更快** | 中等 |
| 内存占用 | 高 | **较低** | 中等 |
| CPU占用 | 中 | **较低** | 高 |
| 兼容性 | 好 | **更好** | 好 |
| 驱动管理 | 自动 | **自动** | 自动 |

## 💡 最佳实践

### 推荐配置（生产环境）
```python
selenium_config = {
    'browser': 'edge',      # 使用Edge
    'headless': True,       # 无头模式
    'timeout': 30,          # 30秒超时
    'implicit_wait': 10,    # 10秒隐式等待
}
```

### 推荐配置（调试环境）
```python
selenium_config = {
    'browser': 'edge',
    'headless': False,      # 显示窗口
    'timeout': 60,          # 更长超时
}
```

## 🔄 从Chrome迁移到Edge

如果你之前使用Chrome，迁移非常简单：

```python
# 只需修改一行
selenium_config = {
    'browser': 'edge',  # 原来是 'chrome'
}
```

其他代码完全不需要改动！

## 📝 总结

✅ Edge浏览器已配置为默认浏览器  
✅ 支持Chrome/Firefox/Edge三种浏览器  
✅ 自动管理EdgeDriver，无需手动下载  
✅ 性能优于Chrome，更适合Windows环境  
✅ 完全兼容现有代码，无缝切换  

---

**更新时间**: 2026-04-17  
**Edge版本**: 147.0.3912.60  
**分支**: selenium-webpage-fetcher
