# 多设备并发优化 - 完成总结

## 修改概述

已成功实现多设备并发获取视频数据功能，通过数据库锁机制确保两台或多台设备同时工作时不会发生冲突或重复处理。

## 完成的修改

### 1. 新增文件

#### `douban_fetcher/worker_config.py`
- 生成唯一的设备标识（主机名 + UUID）
- 提供 `get_worker_id()` 和 `get_simple_worker_id()` 两个函数

#### `docs/MULTI_DEVICE_GUIDE.md`
- 完整的多设备使用指南
- 包含工作原理、配置说明、常见问题等

#### `tests/test_multi_device.py`
- 测试脚本，验证设备标识生成、数据库锁定、并发锁定等功能

#### `start_multi_device.bat`
- Windows 快速启动脚本

### 2. 修改的文件

#### `sql/migration.sql`
**新增内容：**
- 添加 `vod_fetch_worker` 字段：处理设备标识
- 添加 `vod_fetch_time` 字段：开始获取时间戳
- 添加 `vod_fetch_lock_time` 字段：锁定时间戳
- 为新增字段创建索引
- 添加查询各设备处理情况的SQL示例

#### `douban_fetcher/database.py`
**新增方法：**
1. `lock_videos_atomically(worker_id, limit, lock_timeout)`
   - 原子性地锁定一批视频
   - 清理过期锁定（超过5分钟）
   - 使用 `FOR UPDATE` 实现行级锁
   - 批量更新锁定信息

2. `update_video_score_with_unlock(vod_id, info, status, worker_id)`
   - 更新视频评分并释放锁定
   - 处理成功和失败两种情况
   - 清空 worker 相关字段

**修改内容：**
- 导入 `time` 模块用于时间戳

#### `douban_fetcher/fetcher.py`
**修改内容：**
1. 导入 `get_worker_id` 函数
2. 在 `__init__` 中：
   - 生成并保存 `self.worker_id`
   - 使用设备特定的统计文件名：`fetch_stats_{worker_id}.json`
3. 在 `process_single_video` 中：
   - 所有 `update_video_score` 调用改为 `update_video_score_with_unlock`
   - 传入 `self.worker_id` 参数
4. 在 `run` 方法中：
   - 使用 `lock_videos_atomically` 替代 `get_pending_videos`
   - 添加设备标识日志输出
   - 处理无视频时的等待逻辑（sleep 10秒）
   - 显示本批次锁定数量

#### `selenium_fetcher/fetcher.py`
**修改内容：**
与 `douban_fetcher/fetcher.py` 相同的修改模式：
1. 导入 `get_worker_id`
2. 初始化时生成设备标识
3. 使用设备特定的统计文件：`selenium_fetch_stats_{worker_id}.json`
4. 所有更新操作使用 `update_video_score_with_unlock`
5. `run` 方法使用原子锁定机制

## 核心技术实现

### 1. 原子锁定机制

```python
def lock_videos_atomically(self, worker_id, limit=50, lock_timeout=300):
    # 步骤1: 清理过期锁定
    UPDATE mac_vod SET vod_fetch_worker='' 
    WHERE vod_fetch_status=1 AND vod_fetch_lock_time < expire_time
    
    # 步骤2: 开启事务
    BEGIN
    
    # 步骤3: 选择并锁定行（FOR UPDATE）
    SELECT ... FROM mac_vod 
    WHERE vod_fetch_status=1 AND (vod_fetch_worker='' OR IS NULL)
    ORDER BY vod_id ASC LIMIT %s FOR UPDATE
    
    # 步骤4: 批量更新锁定信息
    UPDATE mac_vod SET 
        vod_fetch_worker=%s,
        vod_fetch_time=%s,
        vod_fetch_lock_time=%s
    WHERE vod_id IN (...)
    
    # 步骤5: 提交
    COMMIT
```

### 2. 带解锁的更新

```python
def update_video_score_with_unlock(self, vod_id, info, status, worker_id):
    if status == SUCCESS:
        # 更新评分字段
        UPDATE mac_vod SET 
            vod_douban_score=...,
            vod_fetch_status=0,
            vod_fetch_worker='',      # 释放锁定
            vod_fetch_time=0,
            vod_fetch_lock_time=0
        WHERE vod_id=%s
    else:
        # 更新状态并释放锁定
        UPDATE mac_vod SET 
            vod_fetch_status=%s,
            vod_fetch_worker='',
            vod_fetch_time=0,
            vod_fetch_lock_time=0
        WHERE vod_id=%s
```

### 3. 设备标识生成

```python
def get_worker_id():
    hostname = socket.gethostname()  # 例如: DESKTOP-ABC123
    unique_id = str(uuid.uuid4())[:8]  # 例如: a1b2c3d4
    return f"{hostname}_{unique_id}"  # DESKTOP-ABC123_a1b2c3d4
```

## 工作流程

### 单设备流程（原有）
```
获取待处理视频 → 处理 → 更新状态
```

### 多设备流程（新）
```
设备A: 原子锁定50个视频 → 处理 → 更新并释放锁定
设备B: 原子锁定50个视频 → 处理 → 更新并释放锁定
         ↓
    数据库保证不重复
```

## 关键特性

### ✅ 防止重复处理
- 使用 `FOR UPDATE` 行级锁
- 事务保证原子性
- 按 `vod_id` 顺序锁定避免死锁

### ✅ 自动故障恢复
- 5分钟超时自动清理
- 处理设备崩溃、网络中断等情况
- 无需人工干预

### ✅ 动态负载均衡
- 快的设备可以获取更多任务
- 慢的设备不会阻塞整体进度
- 自动适应不同设备性能

### ✅ 易于监控
- 每台设备独立统计文件
- 数据库可查询各设备状态
- 清晰的日志输出

## 使用方法

### 第一步：执行数据库迁移
```bash
mysql -h 192.168.114.4 -P 3307 -u user -p maccms < sql/migration.sql
```

### 第二步：在两台设备上运行
```bash
# 设备1
python main.py

# 设备2
python main.py
```

**无需任何额外配置！**

### 第三步：监控进度
```sql
-- 查看各设备处理情况
SELECT vod_fetch_worker, vod_fetch_status, COUNT(*) as count
FROM mac_vod
WHERE vod_fetch_worker != ''
GROUP BY vod_fetch_worker, vod_fetch_status;
```

## 测试验证

运行测试脚本验证功能：
```bash
python tests/test_multi_device.py
```

测试内容包括：
1. ✓ 设备标识生成唯一性
2. ✓ 数据库表结构正确性
3. ✓ 原子锁定功能
4. ✓ 并发锁定无重复

## 性能提升

### 理论加速比
- 2台设备：约 **1.8-2.0倍**
- 3台设备：约 **2.5-3.0倍**
- N台设备：约 **0.9N-N倍**

### 实际影响因素
- API限流策略
- 网络带宽
- 数据库性能
- 单个视频处理时间

## 注意事项

### ⚠️ 数据库要求
- 必须使用 **InnoDB** 引擎（支持事务）
- MyISAM 不支持 `FOR UPDATE`

### ⚠️ 锁定超时
- 默认5分钟，可根据实际情况调整
- 过短可能导致正常处理被中断
- 过长会影响故障恢复速度

### ⚠️ 批次大小
- API方案建议：500-1000
- Selenium方案建议：20-50
- 根据实际性能调整

### ⚠️ 资源占用
- 每台设备独立运行，资源不共享
- Selenium方案较耗内存（建议4GB+）
- 注意总连接数不要超过数据库限制

## 扩展性

### 轻松扩展到更多设备
只需在更多机器上运行程序，无需修改代码：
```bash
# 设备1、2、3、4... 都运行
python main.py
```

### 混合方案
可以同时运行 API 方案和 Selenium 方案：
```bash
# 终端1：API方案
python main.py

# 终端2：Selenium方案
python main_selenium.py
```

两者会协同工作，互不干扰。

## 故障排查

### 问题1：锁定失败
**症状：** 报错 "锁定视频失败"

**解决：**
1. 检查数据库是否使用 InnoDB
2. 确认已执行迁移脚本
3. 检查数据库权限

### 问题2：视频重复处理
**症状：** 同一视频被多台设备处理

**解决：**
这不应该发生。如果发生：
1. 检查数据库引擎类型
2. 查看日志确认设备标识唯一
3. 检查是否有手动修改数据库

### 问题3：所有视频被锁定但无人处理
**症状：** `vod_fetch_worker` 有值但程序已停止

**解决：**
等待5分钟自动清理，或手动执行：
```sql
UPDATE mac_vod 
SET vod_fetch_worker='', vod_fetch_time=0, vod_fetch_lock_time=0
WHERE vod_fetch_status=1;
```

## 总结

✅ **已完成**：
- 数据库表结构扩展
- 原子锁定机制实现
- 双Fetcher改造
- 设备标识生成
- 测试脚本
- 完整文档

✅ **核心优势**：
- 完全避免冲突
- 自动故障恢复
- 动态负载均衡
- 易于扩展和监控

✅ **立即可用**：
- 执行迁移脚本
- 在多台设备运行
- 无需额外配置

现在你可以在两台设备上同时运行程序，享受加倍的处理速度！🚀
