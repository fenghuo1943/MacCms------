# 🚀 快速开始 - 3步上手

## 1️⃣ 安装依赖

```bash
install.bat
```

或

```bash
pip install -r requirements.txt
```

## 2️⃣ 配置数据库

编辑 `main.py`，修改：

```python
db_config = {
    'host': '192.168.114.4',
    'port': 3307,
    'user': '你的用户名',      # ← 修改这里
    'password': '你的密码',    # ← 修改这里
    'database': 'maccms'
}
```

## 3️⃣ 运行程序

```bash
start.bat
```

或

```bash
python main.py
```

---

**就这么简单！** 🎉

## 📚 需要更多帮助？

- 📖 详细说明 → README.md
- ⚡ 快速指南 → QUICKSTART.md
- 📦 包说明 → PACKAGE_INFO.md
- 🏗️ 模块说明 → MODULES.md
- 📁 项目结构 → STRUCTURE.md
