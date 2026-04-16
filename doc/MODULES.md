# 项目模块说明

## 📁 模块结构

代码已按功能拆分为以下模块，使代码更清晰、易维护：

```
MacCms自动获取评分/
├── main.py              # 主入口文件（简洁）
├── config.py            # 配置管理
├── models.py            # 数据模型和常量
├── rate_limiter.py      # 限流器（Token Bucket + 监控）
├── database.py          # 数据库操作
├── api_client.py        # API客户端
├── data_processor.py    # 数据处理（匹配、提取、计算）
├── fetcher.py           # 主获取器（协调各组件）
├── migration.sql        # 数据库迁移脚本
├── start.bat            # Windows启动脚本
└── README.md            # 使用文档
```

## 🔧 模块详解

### 1. config.py - 配置管理

**职责：** 集中管理所有配置项

**包含内容：**
- 日志配置
- API配置（URL、超时、重试次数、请求头）
- 数据库配置示例
- 默认运行配置
- 统计文件名

**使用示例：**
```python
from config import API_CONFIG, logger

# 使用API配置
url = API_CONFIG['base_url']
timeout = API_CONFIG['timeout']

# 记录日志
logger.info("这是一条日志")
```

---

### 2. models.py - 数据模型和常量

**职责：** 定义数据结构和常量

**包含内容：**
- `FetchStatus` - 获取状态常量类
- `VideoInfo` - 视频信息数据类

**使用示例：**
```python
from models import FetchStatus, VideoInfo

# 使用状态常量
if status == FetchStatus.SUCCESS:
    print("成功")

# 创建空视频信息
info = VideoInfo.create_empty()
```

---

### 3. rate_limiter.py - 限流器

**职责：** 实现速率控制和监控

**包含类：**
- `TokenBucket` - 令牌桶限流算法
- `RateLimitMonitor` - 速率监控器

**使用示例：**
```python
from rate_limiter import TokenBucket, RateLimitMonitor

# 创建限流器（每秒2个请求，最大突发5个）
limiter = TokenBucket(rate=2.0, capacity=5)

# 创建监控器
monitor = RateLimitMonitor()

# 获取令牌（会阻塞直到有可用令牌）
limiter.acquire(timeout=60)

# 记录请求
monitor.record_request(success=True)

# 获取统计
stats = monitor.get_stats()
```

---

### 4. database.py - 数据库操作

**职责：** 封装所有数据库操作

**包含类：**
- `DatabaseManager` - 数据库管理器

**主要方法：**
- `get_pending_videos()` - 获取待处理视频
- `get_total_pending()` - 获取待处理总数
- `update_video_score()` - 更新视频评分
- `get_status_distribution()` - 获取状态分布

**使用示例：**
```python
from database import DatabaseManager

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'password',
    'database': 'maccms'
}

db = DatabaseManager(db_config)

# 获取待处理视频
videos = db.get_pending_videos(limit=100)

# 更新视频
db.update_video_score(vod_id=123, info=video_info, status=0)
```

---

### 5. api_client.py - API客户端

**职责：** 封装API调用逻辑

**包含类：**
- `ApiClient` - WMDB API客户端

**主要方法：**
- `search_video()` - 搜索视频（支持重试、代理、限流检测）

**使用示例：**
```python
from api_client import ApiClient

# 创建客户端
client = ApiClient(
    use_proxy=False,
    proxy_list=[]
)

# 搜索视频
results = client.search_video(
    video_name="爱情公寓",
    monitor=monitor,  # 可选的监控器
    max_retries=5
)
```

---

### 6. data_processor.py - 数据处理

**职责：** 数据匹配、提取、计算

**包含类：**
- `DataProcessor` - 数据处理器（静态方法）

**主要方法：**
- `match_video()` - 匹配视频（名称+年份）
- `extract_video_info()` - 提取视频信息
- `extract_list_names()` - 提取列表名称
- `calculate_combined_score()` - 计算综合评分

**使用示例：**
```python
from data_processor import DataProcessor

# 匹配视频
matched = DataProcessor.match_video(
    search_results=results,
    target_name="爱情公寓",
    target_year="2020"
)

# 提取信息
info = DataProcessor.extract_video_info(matched)

# 计算综合评分
score, votes = DataProcessor.calculate_combined_score(
    imdb_rating=8.0,
    douban_rating=7.5,
    imdb_votes=1000,
    douban_votes=5000
)
```

---

### 7. fetcher.py - 主获取器

**职责：** 协调各组件完成数据获取任务

**包含类：**
- `DoubanScoreFetcher` - 豆瓣评分获取器

**主要方法：**
- `process_single_video()` - 处理单个视频
- `run()` - 运行主任务
- `generate_report()` - 生成报告
- `format_eta()` - 格式化剩余时间

**使用示例：**
```python
from fetcher import DoubanScoreFetcher

fetcher = DoubanScoreFetcher(
    db_config=db_config,
    max_requests_per_second=2.0,
    use_proxy=False,
    proxy_list=[]
)

# 运行任务
fetcher.run(
    batch_size=500,
    max_requests_per_second=2.0,
    adjust_rate=True
)
```

---

### 8. main.py - 主入口

**职责：** 程序入口，配置和启动

**包含内容：**
- 数据库配置
- 代理配置（可选）
- 启动获取器

**使用示例：**
```python
# 直接运行
python main.py

# 或双击 start.bat
```

---

## 🔄 模块依赖关系

```
main.py
  └── fetcher.py
       ├── config.py
       ├── models.py
       ├── rate_limiter.py
       ├── database.py
       │    └── config.py
       ├── api_client.py
       │    └── config.py
       └── data_processor.py
            └── models.py
```

## ✨ 模块化优势

### 1. **清晰的职责划分**
每个模块只负责一个功能领域，易于理解和维护。

### 2. **便于测试**
可以单独测试每个模块，无需运行整个程序。

```python
# 单独测试数据处理器
from data_processor import DataProcessor

info = DataProcessor.extract_video_info(test_data)
assert info['doubanRating'] == 7.5
```

### 3. **易于扩展**
- 需要更换API？只需修改 `api_client.py`
- 需要更换数据库？只需修改 `database.py`
- 需要新的限流算法？只需修改 `rate_limiter.py`

### 4. **代码复用**
其他项目可以直接使用这些模块：
```python
# 在其他项目中使用限流器
from rate_limiter import TokenBucket

limiter = TokenBucket(rate=10.0, capacity=20)
```

### 5. **团队协作**
多人可以同时开发不同模块，减少冲突。

## 🛠️ 开发指南

### 添加新功能

1. **确定功能归属**
   - API相关 → `api_client.py`
   - 数据库相关 → `database.py`
   - 数据处理 → `data_processor.py`
   - 配置相关 → `config.py`

2. **实现功能**
   在对应模块中添加方法或类

3. **更新依赖**
   如果需要新模块，在 `fetcher.py` 中导入和使用

4. **测试**
   编写单元测试验证功能

### 修改配置

所有配置都在 `config.py` 中，修改一处即可全局生效。

### 调试技巧

```python
# 在任意模块中添加调试日志
from config import logger

logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
```

## 📊 性能考虑

### 模块加载顺序

Python会按需加载模块，首次导入时会执行模块级代码。

### 循环导入避免

当前设计已避免循环导入：
- `config.py` 和 `models.py` 不依赖其他模块
- 其他模块只依赖这两个基础模块
- `fetcher.py` 作为协调者，依赖所有模块但不会被其他模块依赖

### 内存使用

- 每个模块独立，便于垃圾回收
- 数据库连接使用后及时关闭
- 统计数据定期保存到文件

---

**模块化完成！代码更清晰、更易维护！** 🎉
