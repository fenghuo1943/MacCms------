# 优雅停止 - 快速参考

## 🚀 三种停止方法

### 1️⃣ Ctrl+C（推荐）
```
直接按 Ctrl+C
```
✅ 最简单 | ✅ 最可靠 | ✅ 立即生效

---

### 2️⃣ Ctrl+Z
```
直接按 Ctrl+Z
```
⚠️ Windows下可能不生效 | 建议用Ctrl+C

---

### 3️⃣ 停止文件
```powershell
# PowerShell
New-Item -Path "stop.flag" -ItemType File

# CMD
type nul > stop.flag
```
✅ 适合后台运行 | ✅ 远程服务器

---

## 📊 停止后会怎样？

✅ 完成当前视频处理  
✅ 保存所有进度  
✅ 释放数据库锁  
✅ 生成任务报告  
✅ 数据不丢失  

---

## 🔄 如何恢复？

```bash
python main.py
```
程序会自动从上次停止的位置继续！

---

## ⚠️ 不要这样做

❌ 直接关闭窗口  
❌ 任务管理器强制结束  
❌ kill -9 命令  

---

## 💡 提示

- 日志会显示："任务已优雅停止！"
- 统计信息保存在 `fetch_stats_*.json`
- 可以随时安全地重新启动
