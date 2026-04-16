# 🚀 快速开始指南

## 5分钟快速上手

### 步骤1：执行数据库迁移（2分钟）

1. 打开数据库管理工具（如 Navicat、phpMyAdmin）
2. 连接到你的 MacCMS 数据库
3. 执行 `migration.sql` 文件中的SQL语句

或者在命令行执行：
```bash
mysql -u 用户名 -p 数据库名 < migration.sql
```

### 步骤2：配置数据库连接（1分钟）

编辑 `main.py` 文件，找到 `main()` 函数，修改数据库配置：

```python
db_config = {
    'host': '192.168.114.4',      # 你的数据库地址
    'port': 3307,                  # 你的数据库端口
    'user': 'your_username',       # 改为你的数据库用户名
    'password': 'your_password',   # 改为你的数据库密码
    'database': 'maccms'           # 你的数据库名
}
```

### 步骤3：安装依赖（1分钟）

**方法1：使用安装脚本（推荐）**
```bash
install.bat
```

**方法2：手动安装**
```bash
pip install -r requirements.txt
```

### 步骤4：运行程序（1分钟）

**Windows用户：**
双击 `start.bat` 文件

**或命令行运行：**
```bash
python main.py
```

## ⚙️ 常用配置

### 调整处理速度

如果API有限制，降低速率：

```python
# 在 main() 函数中修改
fetcher = DoubanScoreFetcher(
    db_config=db_config,
    max_requests_per_second=1.0,  # 改为1次/秒（更保守）
    use_proxy=False,
    proxy_list=[]
)
```

### 启用代理（如有需要）

```python
proxy_list = [
    'http://代理IP:端口',
]

fetcher = DoubanScoreFetcher(
    db_config=db_config,
    max_requests_per_second=1.0,
    use_proxy=True,          # 改为True
    proxy_list=proxy_list    # 填入代理列表
)
```

## 📊 查看进度

程序运行时会实时显示：
- ✅ 已处理数量
- ✅ 成功数量  
- ✅ 处理速度
- ✅ 预计剩余时间

日志保存在 `douban_score_fetch.log`

## 🔄 中断后继续

**无需任何操作！** 

程序会自动保存进度，下次运行会从断点继续。

## ❓ 常见问题

### Q: 如何知道处理完成了？
A: 看到以下日志表示完成：
```
✓ 所有视频已处理完成！
任务完成！
总处理: XXXX 个
成功: XXXX 个 (XX.X%)
```

### Q: 想重新处理失败的视频怎么办？
A: 在数据库中执行：
```sql
UPDATE mac_vod SET vod_fetch_status = 1 
WHERE vod_fetch_status IN (2, 3, 4, 5);
```

### Q: 可以中途停止吗？
A: 可以！按 `Ctrl+C` 停止，下次运行会继续。

### Q: 如何处理大量数据（1万+）？
A: 建议使用以下配置：
```python
fetcher.run(
    batch_size=500,                # 每批500个
    max_requests_per_second=2.0,   # 每秒2次请求
    adjust_rate=True               # 自动调整
)
```

预计时间：
- 1万条 @ 2req/s ≈ 1.4小时
- 2万条 @ 2req/s ≈ 2.8小时

## 📞 需要帮助？

1. 查看 `README.md` 获取详细说明
2. 检查 `douban_score_fetch.log` 日志文件
3. 查看生成的报告文件 `report_*.json`

---

**开始使用吧！** 🎉
