# ⚙️ 配置说明

## 📍 配置文件位置

所有配置都在 **`douban_fetcher/config.py`** 中统一管理。

> ✅ **优势**: 集中管理，一处修改，全局生效

---

## 🔧 数据库配置

### DB_CONFIG_EXAMPLE

```python
DB_CONFIG_EXAMPLE = {
    'host': '192.168.114.4',      # 数据库主机地址
    'port': 3307,                  # 数据库端口
    'user': 'maccms',              # 数据库用户名
    'password': 'q5DdyjsI5%GJOr',  # 数据库密码
    'database': 'maccms'           # 数据库名称
}
```

**如何修改：**
1. 打开 `douban_fetcher/config.py`
2. 找到 `DB_CONFIG_EXAMPLE`
3. 修改对应的值
4. 保存文件

**示例：**
```python
DB_CONFIG_EXAMPLE = {
    'host': 'localhost',           # 本地数据库
    'port': 3306,                  # MySQL默认端口
    'user': 'root',                # root用户
    'password': 'your_password',   # 你的密码
    'database': 'maccms_db'        # 数据库名
}
```

---

## 🚀 运行配置

### DEFAULT_RUN_CONFIG

```python
DEFAULT_RUN_CONFIG = {
    'batch_size': 50,                    # 每批处理的视频数量
    'max_requests_per_second': 2.0,      # 每秒最大请求数
    'adjust_rate': True,                 # 是否自动调整速率
    'use_proxy': False,                  # 是否使用代理
    'proxy_list': []                     # 代理列表
}
```

### 参数说明

#### batch_size（批处理大小）
- **默认值**: 50
- **建议范围**: 10-100
- **说明**: 每次从数据库读取的视频数量
- **调优建议**:
  - 数据量大 → 增大（如 100）
  - 内存有限 → 减小（如 20）

#### max_requests_per_second（请求速率）
- **默认值**: 2.0 req/s
- **建议范围**: 0.5-5.0
- **说明**: 每秒向API发送的请求数
- **调优建议**:
  - API限制严格 → 降低（如 1.0）
  - API限制宽松 → 提高（如 3.0）
  - 被限流时会自动降速

#### adjust_rate（自动调速）
- **默认值**: True
- **选项**: True / False
- **说明**: 根据API响应自动调整请求速率
- **建议**: 保持 True，让程序智能调速

#### use_proxy（使用代理）
- **默认值**: False
- **选项**: True / False
- **说明**: 是否启用代理服务器
- **何时启用**:
  - IP被API封禁
  - 需要突破地域限制
  - 提高并发能力

#### proxy_list（代理列表）
- **默认值**: []
- **格式**: `['http://proxy1:port', 'http://proxy2:port']`
- **说明**: 代理服务器列表，会轮换使用
- **示例**:
  ```python
  proxy_list = [
      'http://127.0.0.1:7890',
      'http://127.0.0.1:7891',
      'socks5://user:pass@proxy.example.com:1080'
  ]
  ```

---

## 🌐 API配置

### API_CONFIG

```python
API_CONFIG = {
    'base_url': 'https://api.wmdb.tv/api/v1/movie/search',
    'timeout': 15,                      # 请求超时时间（秒）
    'max_retries': 5,                   # 最大重试次数
    'headers': {
        'User-Agent': 'Mozilla/5.0 ...',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
}
```

**一般不需要修改**，除非：
- API地址变更
- 需要调整超时时间
- API要求特殊的请求头

---

## 📝 日志配置

```python
logging.basicConfig(
    level=logging.INFO,                 # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('douban_score_fetch.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
```

**日志级别选项**:
- `logging.DEBUG` - 调试信息（最详细）
- `logging.INFO` - 一般信息（推荐）
- `logging.WARNING` - 警告信息
- `logging.ERROR` - 错误信息
- `logging.CRITICAL` - 严重错误

---

## 💡 常见配置场景

### 场景1：首次测试（保守配置）

```python
DEFAULT_RUN_CONFIG = {
    'batch_size': 10,                   # 小批量测试
    'max_requests_per_second': 1.0,     # 低速请求
    'adjust_rate': True,
    'use_proxy': False,
    'proxy_list': []
}
```

### 场景2：生产环境（高效配置）

```python
DEFAULT_RUN_CONFIG = {
    'batch_size': 100,                  # 大批量处理
    'max_requests_per_second': 3.0,     # 较高速率
    'adjust_rate': True,                # 自动调速
    'use_proxy': False,
    'proxy_list': []
}
```

### 场景3：使用代理

```python
DEFAULT_RUN_CONFIG = {
    'batch_size': 50,
    'max_requests_per_second': 2.0,
    'adjust_rate': True,
    'use_proxy': True,                  # 启用代理
    'proxy_list': [
        'http://127.0.0.1:7890',
        'http://127.0.0.1:7891',
    ]
}
```

### 场景4：调试模式

```python
# config.py 顶部
logging.basicConfig(
    level=logging.DEBUG,                # 调试级别
    # ...
)

DEFAULT_RUN_CONFIG = {
    'batch_size': 5,                    # 最小批量
    'max_requests_per_second': 0.5,     # 极低速
    'adjust_rate': False,               # 禁用自动调速
    'use_proxy': False,
    'proxy_list': []
}
```

---

## 🔍 验证配置

运行配置验证脚本：

```bash
python test_config.py
```

输出示例：
```
============================================================
配置验证
============================================================

✓ 配置模块导入成功

【数据库配置】
  主机: 192.168.114.4
  端口: 3307
  用户: maccms
  密码: **************
  数据库: maccms

【运行配置】
  批处理大小: 50
  请求速率: 2.0 req/s
  自动调速: True
  使用代理: False
  代理列表: []

✓ 数据库配置完整
✓ 运行配置完整

【main.py 配置引用检查】
✓ main.py 使用了 DB_CONFIG_EXAMPLE
✓ main.py 使用了 DEFAULT_RUN_CONFIG
✓ main.py 中没有硬编码配置

============================================================
配置验证完成！
============================================================
```

---

## ⚠️ 注意事项

### 1. 不要直接修改 main.py 中的配置

❌ **错误做法**:
```python
# main.py
db_config = {
    'host': '192.168.114.4',  # 不要在这里硬编码
    # ...
}
```

✅ **正确做法**:
```python
# douban_fetcher/config.py
DB_CONFIG_EXAMPLE = {
    'host': '192.168.114.4',  # 在这里统一配置
    # ...
}
```

### 2. 使用 .copy() 避免修改原始配置

main.py 中使用 `.copy()` 创建副本：
```python
db_config = DB_CONFIG_EXAMPLE.copy()
```

这样可以防止意外修改全局配置。

### 3. 敏感信息安全

- ⚠️ 不要将包含真实密码的配置文件提交到Git
- ✅ 使用 `.gitignore` 忽略敏感配置
- ✅ 生产环境使用环境变量或配置管理服务

### 4. 配置备份

修改配置前建议备份：
```bash
copy douban_fetcher\config.py douban_fetcher\config.py.bak
```

---

## 📚 相关文档

- 🚀 快速开始 → START_HERE.md
- 📖 完整文档 → README.md
- 🏗️ 模块说明 → MODULES.md
- 📦 包说明 → PACKAGE_INFO.md

---

**配置完成！现在可以运行程序了！** 🎉

```bash
start.bat
```
