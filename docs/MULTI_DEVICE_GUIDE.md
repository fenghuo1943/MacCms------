# 多设备并发获取指南

## 概述

本系统已支持多台设备同时获取视频数据，通过数据库锁机制确保不会发生冲突或重复处理。

## 核心特性

✅ **原子锁定**：使用数据库事务和 `FOR UPDATE` 确保同一视频只被一台设备处理  
✅ **自动故障恢复**：超时锁定（默认5分钟）会自动释放，处理设备异常退出情况  
✅ **动态负载均衡**：处理速度快的设备可以获取更多任务  
✅ **独立统计**：每台设备有独立的统计文件，便于监控  
✅ **可扩展性**：轻松支持2台、3台甚至更多设备同时工作  

## 快速开始

### 1. 执行数据库迁移

首先需要在数据库中添加强制字段和索引：

```bash
# 连接到你的数据库
mysql -h 192.168.114.4 -P 3307 -u your_user -p maccms < sql/migration.sql
```

或者手动执行 `sql/migration.sql` 中的SQL语句。

新增字段说明：
- `vod_fetch_worker`: 处理设备标识
- `vod_fetch_time`: 开始获取时间戳
- `vod_fetch_lock_time`: 锁定时间戳

### 2. 在两台设备上运行

#### 设备1
```bash
# Windows
start.bat

# 或直接运行
python main.py
```

#### 设备2
```bash
# Windows
start.bat

# 或直接运行
python main.py
```

**无需任何额外配置！** 系统会自动生成唯一的设备标识（主机名 + UUID）。

### 3. 监控运行状态

查看各设备处理情况：
```sql
SELECT 
    vod_fetch_worker,
    vod_fetch_status,
    COUNT(*) as count
FROM mac_vod
WHERE vod_fetch_worker != ''
GROUP BY vod_fetch_worker, vod_fetch_status;
```

查看待处理总数：
```sql
SELECT 
    vod_fetch_status,
    COUNT(*) as count
FROM mac_vod
GROUP BY vod_fetch_status;
```

## 工作原理

### 锁定流程

```
设备A                          数据库                        设备B
  |                              |                             |
  |--- 请求锁定50个视频 -------->|                             |
  |                              |--- 清理过期锁定 ------------|
  |                              |--- SELECT ... FOR UPDATE ---|
  |                              |--- UPDATE 设置 worker=A ----|
  |<-- 返回50个已锁定视频 -------|                             |
  |                              |                             |
  |--- 处理视频1 ----------------|                             |
  |--- 处理视频2 ----------------|                             |
  |                              |--- 请求锁定50个视频 --------|
  |                              |--- SELECT (跳过A的) --------|
  |                              |--- UPDATE 设置 worker=B ----|
  |                              |<-- 返回其他50个视频 ---------|
  |--- 更新并释放锁定 -----------|                             |
  |                              |                             |
```

### 关键代码

**原子锁定方法** (`douban_fetcher/database.py`):
```python
def lock_videos_atomically(self, worker_id: str, limit: int = 50, lock_timeout: int = 300):
    # 1. 清理过期锁定（超过5分钟未完成的）
    # 2. 使用 FOR UPDATE 锁定行
    # 3. 批量更新 worker_id 和时间戳
    # 4. 提交事务
```

**带解锁的更新** (`douban_fetcher/database.py`):
```python
def update_video_score_with_unlock(self, vod_id, info, status, worker_id):
    # 更新评分信息
    # 同时清空 vod_fetch_worker, vod_fetch_time, vod_fetch_lock_time
```

## 配置说明

### 锁定超时时间

默认锁定超时为 **300秒（5分钟）**。如果某设备处理一个批次超过5分钟，其他设备可以接管这些视频。

修改位置：`douban_fetcher/database.py` 第80行
```python
def lock_videos_atomically(self, worker_id: str, limit: int = 50, lock_timeout: int = 300):
```

### 批次大小

建议根据网络速度和API限流情况调整：
- API方案：500-1000
- Selenium方案：20-50

修改位置：启动脚本或配置文件

### 设备标识

设备标识自动生成，格式为：`{主机名}_{UUID前8位}`

例如：`DESKTOP-ABC123_a1b2c3d4`

如需自定义，可修改 `douban_fetcher/worker_config.py`。

## 常见问题

### Q1: 如何确认两台设备都在工作？

查看日志输出，应该看到不同的设备标识：
```
当前设备标识: DESKTOP-A_1a2b3c4d
设备 DESKTOP-A_1a2b3c4d 成功锁定 50 个视频
```

```
当前设备标识: DESKTOP-B_5e6f7g8h
设备 DESKTOP-B_5e6f7g8h 成功锁定 50 个视频
```

### Q2: 如果一台设备突然断电怎么办？

系统会自动处理：
1. 下次其他设备锁定时，会先清理超过5分钟的过期锁定
2. 这些视频会被重新分配给其他设备处理

### Q3: 可以扩展到3台或更多设备吗？

完全可以！只需在更多设备上运行程序即可，无需修改任何代码。

### Q4: 如何暂停某个设备的任务？

直接停止该设备的程序即可。它已锁定的视频会在5分钟后自动释放。

### Q5: 统计文件在哪里？

每台设备有独立的统计文件：
- API方案：`fetch_stats_{worker_id}.json`
- Selenium方案：`selenium_fetch_stats_{worker_id}.json`

### Q6: 如何查看实时进度？

查询数据库：
```sql
-- 查看各设备处理数量
SELECT 
    vod_fetch_worker,
    vod_fetch_status,
    COUNT(*) as count
FROM mac_vod
GROUP BY vod_fetch_worker, vod_fetch_status;

-- 查看总体进度
SELECT 
    CASE vod_fetch_status
        WHEN 0 THEN '成功'
        WHEN 1 THEN '待处理'
        WHEN 2 THEN '多个结果'
        WHEN 3 THEN '无搜索结果'
        WHEN 4 THEN '错误'
        WHEN 5 THEN '被限流'
        WHEN 6 THEN '匹配结果为空'
    END as 状态,
    COUNT(*) as 数量
FROM mac_vod
GROUP BY vod_fetch_status;
```

## 性能优化建议

1. **合理设置批次大小**：
   - 太快可能导致API限流
   - 太慢会降低并发效率

2. **监控数据库连接**：
   - 确保数据库能处理并发连接
   - 考虑增加连接池大小

3. **网络带宽**：
   - Selenium方案需要加载网页，确保带宽充足
   - API方案对带宽要求较低

4. **CPU和内存**：
   - Selenium方案较耗资源，建议4GB+内存
   - API方案资源占用较低

## 技术细节

### 事务隔离级别

使用 MySQL/MariaDB 默认的 `REPEATABLE READ` 隔离级别，配合 `FOR UPDATE` 实现行级锁。

### 死锁预防

- 按 `vod_id ASC` 顺序锁定，避免循环等待
- 使用短事务，快速提交
- 超时自动回滚

### 索引优化

已为以下字段添加索引：
- `vod_fetch_status`
- `vod_fetch_worker`
- `vod_fetch_lock_time`

## 故障排查

### 问题1: 所有视频都被锁定但无人处理

检查是否有设备异常退出：
```sql
SELECT * FROM mac_vod 
WHERE vod_fetch_worker != '' 
  AND vod_fetch_status = 1
LIMIT 10;
```

解决方案：等待5分钟让锁定自动过期，或手动清理：
```sql
UPDATE mac_vod 
SET vod_fetch_worker = '', 
    vod_fetch_time = 0,
    vod_fetch_lock_time = 0
WHERE vod_fetch_worker != '' 
  AND vod_fetch_status = 1;
```

### 问题2: 两台设备处理相同的视频

这不应该发生。如果发生了，检查：
1. 数据库是否使用了 InnoDB 引擎（支持事务）
2. 是否正确执行了迁移脚本
3. 查看日志确认设备标识是否唯一

### 问题3: 锁定失败报错

查看错误日志，常见原因：
- 数据库连接失败
- 表结构不正确（缺少新字段）
- 权限不足

## 总结

多设备并发功能让你能够：
- 🚀 **加倍处理速度**：2台设备理论上可达2倍速度
- 🔒 **安全可靠**：数据库级别的原子操作保证不重复
- 🔄 **容错性强**：自动处理异常情况
- 📊 **易于监控**：清晰的统计和日志

开始享受高效的并发处理吧！
