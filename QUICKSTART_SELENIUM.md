# Selenium方案 - 快速开始

## 📦 安装

```bash
# 1. 安装Python依赖
pip install selenium beautifulsoup4 lxml

# 2. 安装ChromeDriver（与Chrome版本匹配）
# 下载地址: https://chromedriver.chromium.org/
```

## 🚀 运行

### 方式1: 使用启动脚本（推荐）
```bash
start_selenium.bat
```

### 方式2: 直接运行
```bash
python main_selenium.py
```

### 方式3: 测试功能
```bash
python test_selenium_basic.py
```

## ⚙️ 配置

编辑 `main_selenium.py`:

```python
# 数据库配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的密码',
    'database': 'maccms',
}

# Selenium配置
selenium_config = {
    'browser': 'chrome',   # chrome 或 firefox
    'headless': True,      # True=后台运行
    'timeout': 30,
}
```

## 📊 性能提示

- **速度**: 约 0.2-0.5 个视频/秒（比API慢10-50倍）
- **批次大小**: 建议 20-50
- **内存占用**: 每个浏览器实例 200-500MB
- **适用场景**: API受限时的备选方案

## 🔧 常见问题

**Q: WebDriver初始化失败？**  
A: 检查ChromeDriver是否正确安装且版本匹配

**Q: 页面加载超时？**  
A: 增加timeout值或检查网络

**Q: 被豆瓣拦截？**  
A: 启用headless模式，降低请求频率

## 📁 文件说明

```
selenium_fetcher/
├── browser.py      # 浏览器驱动管理
├── config.py       # 配置管理
├── extractor.py    # 数据提取器
├── fetcher.py      # 主获取器
└── __init__.py     # 模块入口

main_selenium.py          # 主程序入口
test_selenium_basic.py    # 测试脚本
start_selenium.bat        # Windows启动脚本
SELENIUM_README.md        # 详细文档
```

## 🌿 Git分支

当前在分支: `selenium-webpage-fetcher`

切换到其他分支:
```bash
git checkout main                        # 主分支
git checkout feature/douban-api-search   # API方案分支
```

---

更多信息请查看 `SELENIUM_README.md`
