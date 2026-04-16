# 📁 项目文件结构

```
MacCms自动获取评分/
│
├── 📄 核心代码模块
│   ├── main.py                 # 主入口文件 (47行)
│   ├── config.py               # 配置管理 (50行)
│   ├── models.py               # 数据模型和常量 (54行)
│   ├── rate_limiter.py         # 限流器模块 (106行)
│   ├── database.py             # 数据库操作 (184行)
│   ├── api_client.py           # API客户端 (113行)
│   ├── data_processor.py       # 数据处理 (167行)
│   └── fetcher.py              # 主获取器 (257行)
│
├── 📊 数据库相关
│   ├── maccms.sql              # MacCMS原始数据库结构
│   └── migration.sql           # 数据库迁移脚本
│
├── 📚 文档
│   ├── README.md               # 完整使用文档
│   ├── QUICKSTART.md           # 5分钟快速开始
│   ├── MODULES.md              # 模块详细说明
│   ├── PROJECT_SUMMARY.md      # 项目完成总结
│   ├── REFACTORING_SUMMARY.md  # 重构总结
│   └── STRUCTURE.md            # 本文件
│
├── 🚀 启动脚本
│   └── start.bat               # Windows快速启动
│
└── ⚙️ 运行时生成
    ├── douban_score_fetch.log  # 日志文件
    ├── fetch_stats.json        # 断点续传统计
    └── report_*.json           # 任务报告
```

## 🔍 模块功能速查

| 模块 | 主要功能 | 关键类/函数 |
|------|---------|------------|
| **main.py** | 程序入口 | `main()` |
| **config.py** | 配置管理 | `API_CONFIG`, `DB_CONFIG_EXAMPLE` |
| **models.py** | 数据模型 | `FetchStatus`, `VideoInfo` |
| **rate_limiter.py** | 速率控制 | `TokenBucket`, `RateLimitMonitor` |
| **database.py** | 数据库操作 | `DatabaseManager` |
| **api_client.py** | API调用 | `ApiClient` |
| **data_processor.py** | 数据处理 | `DataProcessor` |
| **fetcher.py** | 任务协调 | `DoubanScoreFetcher` |

## 🔄 数据流向

```
用户启动
   ↓
main.py (读取配置)
   ↓
fetcher.py (创建实例)
   ↓
   ├──→ rate_limiter.py (初始化限流器)
   ├──→ database.py (连接数据库)
   └──→ api_client.py (初始化API客户端)
   
开始处理循环
   ↓
database.py (获取待处理视频)
   ↓
fetcher.py (逐个处理)
   ↓
   ├──→ rate_limiter.py (获取令牌，控制速率)
   ├──→ api_client.py (调用API搜索)
   ├──→ data_processor.py (匹配视频)
   ├──→ data_processor.py (提取信息)
   └──→ database.py (更新数据库)
   
继续下一个...
   ↓
完成所有视频
   ↓
fetcher.py (生成报告)
   ↓
结束
```

## 📦 模块依赖图

```
                    ┌─────────────┐
                    │   main.py   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  fetcher.py │
                    └──┬──┬──┬───┘
                       │  │  │
          ┌────────────┘  │  └────────────┐
          │               │               │
   ┌──────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
   │ database.py │ │api_client. │ │data_proces-│
   │             │ │   py       │ │  sor.py    │
   └──────┬──────┘ └─────┬──────┘ └─────┬──────┘
          │               │               │
          └───────────────┼───────────────┘
                          │
                   ┌──────▼──────┐
                   │ config.py   │◄──────────┐
                   │ models.py   │           │
                   └─────────────┘           │
                          ▲                  │
                   ┌──────┴──────┐           │
                   │rate_limiter.│           │
                   │    py       │           │
                   └─────────────┘           │
                                             │
                   所有模块都依赖 ────────────┘
```

## 🎯 快速定位

### 需要修改配置？
→ `config.py`

### 需要修改数据库查询？
→ `database.py`

### 需要修改API调用？
→ `api_client.py`

### 需要修改数据处理逻辑？
→ `data_processor.py`

### 需要调整限流策略？
→ `rate_limiter.py`

### 需要修改主流程？
→ `fetcher.py`

### 需要修改启动参数？
→ `main.py`

## 💡 开发提示

### 添加新功能

1. **确定功能类型**
   - API相关 → `api_client.py`
   - 数据库相关 → `database.py`
   - 数据处理 → `data_processor.py`
   - 配置相关 → `config.py`
   - 新组件 → 创建新文件

2. **实现功能**
   ```python
   # 在对应模块中添加
   class NewFeature:
       def __init__(self):
           pass
       
       def do_something(self):
           pass
   ```

3. **集成到主流程**
   ```python
   # 在 fetcher.py 中导入和使用
   from new_module import NewFeature
   
   self.new_feature = NewFeature()
   ```

### 调试技巧

```python
# 在任何模块中添加调试
from config import logger

logger.debug("变量值: %s", variable)
logger.info("执行到这里")
logger.warning("需要注意")
logger.error("出错了: %s", error)
```

### 性能优化

```python
# 查看当前速率
from config import logger
logger.info(f"当前速率: {monitor.get_current_rate()}")

# 查看统计信息
stats = monitor.get_stats()
logger.info(f"统计: {stats}")
```

## 📊 文件大小分布

```
核心代码 (约978行)
├── fetcher.py       ████████████████████ 257行 (26%)
├── database.py      ██████████████ 184行 (19%)
├── data_processor.py █████████████ 167行 (17%)
├── api_client.py    █████████ 113行 (12%)
├── rate_limiter.py  ████████ 106行 (11%)
├── models.py        ████ 54行 (5%)
├── config.py        ████ 50行 (5%)
└── main.py          ███ 47行 (5%)
```

## 🎨 命名规范

- **模块名**: 小写+下划线 (snake_case)
  - ✅ `api_client.py`
  - ❌ `ApiClient.py`

- **类名**: 大驼峰 (PascalCase)
  - ✅ `DatabaseManager`
  - ❌ `database_manager`

- **函数/变量**: 小写+下划线 (snake_case)
  - ✅ `get_pending_videos()`
  - ❌ `getPendingVideos()`

- **常量**: 大写+下划线 (UPPER_CASE)
  - ✅ `API_CONFIG`
  - ❌ `api_config`

---

**清晰的結構，高效的開發！** 🚀
