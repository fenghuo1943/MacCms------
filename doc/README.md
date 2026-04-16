# MacCMS 豆瓣评分自动获取工具 - 生产级版本

## 🎯 功能特性

### ✨ 核心功能
- ✅ **智能限速**：Token Bucket算法，自动控制请求速率
- ✅ **断点续传**：支持中断后继续，不重复处理已完成的视频
- ✅ **可选代理**：支持配置代理池，突破IP限制
- ✅ **自动调优**：根据API响应自动调整请求速率
- ✅ **实时监控**：显示进度、成功率、预计完成时间
- ✅ **详细报告**：自动生成JSON报告和数据库统计

### 📊 数据更新
除了评分信息，还会自动更新以下字段（如果API返回）：
- 演员、导演、编剧
- 海报图片
- 类型、地区、语言
- 剧情简介
- 集数、时长
- 上映日期
- 别名/副标题

## 📦 安装依赖

```bash
pip install pymysql requests
```

## 🔧 使用前准备

### 1. 执行数据库迁移

在数据库中执行以下SQL，为 `mac_vod` 表添加必要字段：

```sql
ALTER TABLE `mac_vod` 
ADD COLUMN `vod_fetch_status` TINYINT(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '评分获取状态：1=未获取，0=获取成功，2=获取失败（多个结果），3=获取失败（无结果），4=获取失败（其他错误）',
ADD COLUMN `vod_imdb_id` VARCHAR(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT 'IMDB ID',
ADD COLUMN `vod_imdb_votes` MEDIUMINT(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'IMDB 投票人数',
ADD COLUMN `vod_imdb_rating` DECIMAL(3, 1) UNSIGNED NOT NULL DEFAULT 0.0 COMMENT 'IMDB 评分';

ALTER TABLE `mac_vod` ADD INDEX `vod_fetch_status` (`vod_fetch_status`);
```

### 2. 配置数据库连接

编辑 `main.py` 文件，修改数据库配置：

```python
db_config = {
    'host': '192.168.114.4',
    'port': 3307,
    'user': 'your_username',      # 修改为你的数据库用户名
    'password': 'your_password',   # 修改为你的数据库密码
    'database': 'maccms'
}
```

## 🚀 使用方法

### 基础使用（推荐）

```bash
python main.py
```

### 配置说明

在 `main()` 函数中可以调整以下参数：

```python
fetcher = DoubanScoreFetcher(
    db_config=db_config,
    max_requests_per_second=2.0,  # 每秒请求数
    use_proxy=False,               # 是否使用代理
    proxy_list=[]                  # 代理列表
)

fetcher.run(
    batch_size=500,                # 每批处理数量
    max_requests_per_second=2.0,   # 最大请求速率
    adjust_rate=True               # 自动调整速率
)
```

### 性能建议

| 数据量 | 推荐速率 | 预计时间 | 说明 |
|--------|---------|---------|------|
| 1万条 | 2 req/s | ~1.4小时 | 保守模式，稳定 |
| 1万条 | 3 req/s | ~56分钟 | 平衡模式 |
| 2万条 | 2 req/s | ~2.8小时 | 保守模式 |
| 2万条 | 3 req/s | ~1.9小时 | 平衡模式 |

**首次运行建议使用 1-2 req/s 测试API限制**

### 启用代理（如需）

如果有代理服务器，可以配置：

```python
proxy_list = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://proxy3.example.com:8080',
]

fetcher = DoubanScoreFetcher(
    db_config=db_config,
    max_requests_per_second=1.0,
    use_proxy=True,
    proxy_list=proxy_list
)
```

## 📈 运行监控

### 实时日志输出

```
2024-01-15 10:30:00 - INFO - ======================================================================
2024-01-15 10:30:00 - INFO - 开始豆瓣评分获取任务（生产级版本）
2024-01-15 10:30:00 - INFO - 配置: 速率=2.0req/s, 批次大小=500
2024-01-15 10:30:00 - INFO - ======================================================================
2024-01-15 10:30:01 - INFO - 剩余待处理: 15234 个视频
2024-01-15 10:30:01 - INFO - 当前速率: 1.85 req/s
2024-01-15 10:30:01 - INFO - 统计: {"total_requests": 0, "failed_requests": 0, "success_rate": "0.00%", "rate_limited_count": 0, "current_rate": "0.00 req/s"}
2024-01-15 10:30:01 - INFO - 获取到 500 个待处理视频
2024-01-15 10:30:15 - INFO -   [10/500] ✓ ID:1234
2024-01-15 10:30:30 - INFO -   [20/500] ✓ ID:1235
...
2024-01-15 10:35:00 - INFO -   进度: 50 | 成功: 45 | 速度: 1.67/s | 预计剩余: 2小时30分钟
```

### 生成的文件

1. **douban_score_fetch.log** - 详细日志文件
2. **fetch_stats.json** - 断点续传统计（自动保存）
3. **report_YYYYMMDD_HHMMSS.json** - 任务完成报告

### 报告示例

```json
{
  "task_summary": {
    "total_videos": 10000,
    "successful": 8500,
    "failed": 1500,
    "success_rate": "85.00%",
    "total_time": "2小时45分钟",
    "avg_speed": "1.68 videos/sec"
  },
  "api_stats": {
    "total_requests": 10000,
    "failed_requests": 1500,
    "success_rate": "85.00%",
    "rate_limited_count": 23,
    "current_rate": "1.65 req/s"
  },
  "timestamp": "2024-01-15T13:15:00"
}
```

## 🔍 获取状态说明

| 状态码 | 说明 | 处理方式 |
|--------|------|---------|
| 1 | 未获取（初始状态） | 等待处理 |
| 0 | 获取成功 | 已完成 |
| 2 | 匹配到多个结果 | 需手动检查或优化匹配逻辑 |
| 3 | 无搜索结果 | API无此视频数据 |
| 4 | 其他错误 | 网络或API异常 |
| 5 | 被限流 | 触发API频率限制 |

### 重新处理失败的视频

```sql
-- 将所有失败的视频重置为未处理状态
UPDATE mac_vod SET vod_fetch_status = 1 WHERE vod_fetch_status IN (2, 3, 4, 5);

-- 或者只重置特定状态
UPDATE mac_vod SET vod_fetch_status = 1 WHERE vod_fetch_status = 4;
```

## ⚙️ 高级配置

### 调整请求速率

如果遇到API限流（429错误），降低速率：

```python
fetcher = DoubanScoreFetcher(
    db_config=db_config,
    max_requests_per_second=1.0,  # 降低到1次/秒
    use_proxy=False
)
```

### 禁用自动调优

如果希望保持固定速率：

```python
fetcher.run(
    batch_size=500,
    max_requests_per_second=2.0,
    adjust_rate=False  # 禁用自动调整
)
```

### 批量大小调整

- **小批量（100-200）**：适合测试或不稳定网络
- **中批量（500）**：推荐，平衡性能和稳定性
- **大批量（1000+）**：适合稳定环境和高速网络

## 🛠️ 故障排除

### 问题1：API请求频繁超时

**解决方案：**
```python
# 降低请求速率
max_requests_per_second=0.5

# 增加超时时间（需修改代码中的timeout参数）
```

### 问题2：大量视频匹配失败

**可能原因：**
- 视频名称不准确
- 年份信息缺失或错误

**解决方案：**
```sql
-- 查看匹配失败的分布
SELECT vod_fetch_status, COUNT(*) as count 
FROM mac_vod 
GROUP BY vod_fetch_status;

-- 手动检查状态2（多个结果）的视频
SELECT vod_id, vod_name, vod_year 
FROM mac_vod 
WHERE vod_fetch_status = 2 
LIMIT 10;
```

### 问题3：程序中断后如何继续

**无需任何操作！** 程序会自动从上次中断的地方继续：
- 统计信息保存在 `fetch_stats.json`
- 数据库状态保持不变
- 下次运行会自动跳过已处理的视频

### 问题4：想查看实时进度

日志会每50个视频显示一次进度：
```
进度: 500 | 成功: 450 | 速度: 1.67/s | 预计剩余: 2小时30分钟
```

## 📝 注意事项

1. **首次运行前务必备份数据库**
2. **建议先在测试环境验证**
3. **根据API实际限制调整请求速率**
4. **定期检查日志文件，避免磁盘空间不足**
5. **长时间运行建议使用 screen 或 nohup**

### Linux后台运行

```bash
# 使用 nohup
nohup python main.py > output.log 2>&1 &

# 使用 screen
screen -S douban_fetch
python main.py
# Ctrl+A, D 分离会话
# screen -r douban_fetch 恢复会话
```

### Windows后台运行

```powershell
# 使用 Start-Process
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden

# 或使用任务计划程序
```

## 🎓 技术原理

### Token Bucket 限流算法

```
令牌桶容量: 5
生成速率: 2个/秒

每次请求消耗1个令牌
令牌不足时等待
自动补充令牌
```

### 指数退避重试

```
第1次失败: 等待 1秒
第2次失败: 等待 2秒
第3次失败: 等待 4秒
第4次失败: 等待 8秒
第5次失败: 放弃
```

### 自动速率调整

```
检测到频繁限流 → 降低速率 × 0.8
成功率 > 95% 且无限流 → 提高速率 × 1.2
速率不超过设定的最大值
```

## 📞 支持与反馈

如遇到问题，请检查：
1. 日志文件 `douban_score_fetch.log`
2. 数据库连接配置
3. API是否可访问
4. 防火墙/代理设置

---

**祝使用愉快！** 🎉
