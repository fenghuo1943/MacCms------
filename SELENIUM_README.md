# Selenium方案使用说明

## 概述

本方案采用**混合模式**：使用豆瓣API进行搜索（快速），使用Selenium获取详情页信息（完整）。

### 工作流程

1. **搜索阶段**: 使用豆瓣API快速搜索视频
2. **匹配阶段**: 使用智能匹配算法找到最相关的结果
3. **详情获取**: 使用Selenium访问网页获取完整信息
4. **数据更新**: 将提取的信息更新到数据库

## 优势

1. **搜索快速**: API搜索比网页搜索快5-10倍
2. **数据完整**: Selenium获取的详情页信息更全面
3. **绕过限制**: 详情获取使用浏览器，不受API调用次数限制
4. **智能匹配**: 复用成熟的DataProcessor匹配算法
5. **更好的反爬虫规避**: 仅在详情获取时模拟浏览器

## 劣势

1. **速度中等**: 比纯API慢，但比纯Selenium快（详情获取仍需加载页面）
2. **资源占用中等**: 仅在获取详情时启动浏览器
3. **稳定性依赖**: 依赖API可用性和页面结构

## 安装依赖

```bash
pip install -r requirements.txt
```

还需要安装浏览器驱动：

### Chrome浏览器
1. 下载ChromeDriver: https://chromedriver.chromium.org/
2. 确保ChromeDriver版本与Chrome浏览器版本匹配
3. 将ChromeDriver添加到系统PATH

### Firefox浏览器
1. 下载GeckoDriver: https://github.com/mozilla/geckodriver/releases
2. 将GeckoDriver添加到系统PATH

## 使用方法

### 方式1: 直接运行
```bash
python main_selenium.py
```

### 方式2: 自定义配置
编辑 `main_selenium.py` 中的配置：

```python
# 数据库配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'maccms',
    'charset': 'utf8mb4'
}

# Selenium配置
selenium_config = {
    'browser': 'chrome',      # chrome 或 firefox
    'headless': True,         # True=后台运行, False=显示浏览器窗口
    'timeout': 30,            # 页面加载超时时间(秒)
    'implicit_wait': 10,      # 隐式等待时间(秒)
}
```

## 配置说明

### selenium_fetcher/config.py

```python
SELENIUM_CONFIG = {
    'browser': 'chrome',          # 浏览器类型
    'headless': True,             # 无头模式
    'timeout': 30,                # 超时时间
    'implicit_wait': 10,          # 隐式等待
    'user_agent': '...',          # User-Agent
    'window_size': (1920, 1080),  # 窗口大小
}

DEFAULT_RUN_CONFIG = {
    'batch_size': 50,             # 每批处理数量（建议较小）
    'max_requests_per_second': 0.2, # 请求速率（很慢）
}
```

## 测试

运行测试脚本验证功能：

```bash
python test_selenium_basic.py
```

## 与API方案对比

| 特性 | API方案 | Selenium方案 |
|------|---------|--------------|
| 速度 | 快 | 慢 |
| 稳定性 | 受API限制 | 受页面结构影响 |
| 数据完整性 | 取决于API | 完整 |
| 资源占用 | 低 | 高 |
| 反爬虫 | 容易被限 | 较难检测 |
| 适用场景 | 批量快速处理 | API受限时的备选 |

## 注意事项

1. **首次运行**: 可能需要下载浏览器驱动
2. **内存占用**: Selenium会占用较多内存，建议减小batch_size
3. **反爬虫**: 虽然使用了反检测技术，但仍可能被豆瓣识别
4. **页面变化**: 如果豆瓣页面结构变化，需要更新提取器代码
5. **建议使用**: 仅在API方案不可用时使用此方案

## 故障排除

### 问题1: WebDriver初始化失败
```
解决方案: 
- 检查是否安装了Chrome/Firefox浏览器
- 检查ChromeDriver/GeckoDriver是否正确安装
- 确保驱动版本与浏览器版本匹配
```

### 问题2: 页面加载超时
```
解决方案:
- 增加timeout配置值
- 检查网络连接
- 考虑使用代理
```

### 问题3: 被豆瓣拦截
```
解决方案:
- 启用headless模式
- 降低请求频率
- 增加随机等待时间
- 使用代理IP
```

## 开发计划

- [ ] 支持多浏览器实例并行
- [ ] 优化页面加载速度
- [ ] 增加更多反检测手段
- [ ] 支持Cookie管理
- [ ] 自动处理验证码
