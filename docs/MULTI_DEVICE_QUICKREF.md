# 多设备并发 - 快速参考

## 🚀 3步开始

### 1️⃣ 执行数据库迁移
```bash
mysql -h 192.168.114.4 -P 3307 -u user -p maccms < sql/migration.sql
```

### 2️⃣ 在两台设备上运行
```bash
python main.py
```

### 3️⃣ 监控进度
```sql
SELECT vod_fetch_worker, COUNT(*) FROM mac_vod 
WHERE vod_fetch_worker != '' GROUP BY vod_fetch_worker;
```

---

## 📋 关键SQL查询

### 查看各设备状态
```sql
SELECT 
    vod_fetch_worker AS 设备,
    CASE vod_fetch_status
        WHEN 0 THEN '成功'
        WHEN 1 THEN '待处理'
        WHEN 2 THEN '多个结果'
        WHEN 3 THEN '无搜索'
        WHEN 4 THEN '错误'
        WHEN 6 THEN '无匹配'
    END AS 状态,
    COUNT(*) AS 数量
FROM mac_vod
GROUP BY vod_fetch_worker, vod_fetch_status
ORDER BY vod_fetch_worker, vod_fetch_status;
```

### 查看总体进度
```sql
SELECT 
    CASE vod_fetch_status
        WHEN 0 THEN '✅ 成功'
        WHEN 1 THEN '⏳ 待处理'
        WHEN 2 THEN '⚠️ 多个结果'
        WHEN 3 THEN '❌ 无搜索'
        WHEN 4 THEN '❌ 错误'
        WHEN 5 THEN '🚫 被限流'
        WHEN 6 THEN '⚠️ 无匹配'
    END AS 状态,
    COUNT(*) AS 数量,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM mac_vod), 2) AS 百分比
FROM mac_vod
GROUP BY vod_fetch_status;
```

### 清理过期锁定（紧急情况）
```sql
UPDATE mac_vod 
SET vod_fetch_worker = '',
    vod_fetch_time = 0,
    vod_fetch_lock_time = 0
WHERE vod_fetch_status = 1 
  AND vod_fetch_worker != ''
  AND vod_fetch_lock_time < UNIX_TIMESTAMP() - 300;
```

---

## 🔧 配置调整

### 修改锁定超时时间
文件：`douban_fetcher/database.py` 第80行
```python
def lock_videos_atomically(self, worker_id, limit=50, lock_timeout=300):
    # 改为 600 = 10分钟
```

### 修改批次大小
启动时指定：
```python
fetcher.run(batch_size=100)  # API方案
fetcher.run(batch_size=30)   # Selenium方案
```

---

## 🐛 常见问题速查

| 问题 | 原因 | 解决 |
|------|------|------|
| 锁定失败 | 未执行迁移 | 运行 `migration.sql` |
| 视频重复 | MyISAM引擎 | 改为 InnoDB |
| 全部锁定但无人处理 | 设备崩溃 | 等待5分钟或手动清理 |
| 速度慢 | API限流 | 降低速率或增加设备 |

---

## 📊 性能参考

| 设备数 | 理论加速 | 实际加速 |
|--------|----------|----------|
| 1台 | 1.0x | 1.0x |
| 2台 | 2.0x | 1.8-2.0x |
| 3台 | 3.0x | 2.5-3.0x |
| 4台 | 4.0x | 3.2-3.8x |

---

## 📝 日志关键词

```
✓ 当前设备标识: DESKTOP-A_a1b2c3d4
✓ 设备 xxx 成功锁定 50 个视频
✓ 本批次锁定: 50 个视频
✗ 锁定视频失败: ...
ℹ 暂无可处理的视频，等待中...
```

---

## 🔍 测试命令

```bash
# 测试多设备功能
python tests/test_multi_device.py

# 查看统计文件
type fetch_stats_*.json
type selenium_fetch_stats_*.json
```

---

## 💡 提示

- ✅ 设备标识自动生成，无需配置
- ✅ 每台设备独立统计文件
- ✅ 支持随时增减设备
- ✅ 自动处理异常情况
- ⚠️ 确保使用 InnoDB 引擎
- ⚠️ 注意数据库连接数限制

---

**详细文档：** `docs/MULTI_DEVICE_GUIDE.md`  
**完成总结：** `docs/MULTI_DEVICE_SUMMARY.md`
