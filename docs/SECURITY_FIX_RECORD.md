# 🔧 数据库凭据泄露修复记录

## 📅 修复日期
2026-04-17

## ⚠️ 问题描述

GitGuardian 检测到 GitHub 仓库中暴露了数据库配置信息：
- **Secret type**: Generic Database Assignment
- **Repository**: fenghuo1943/MacCms------
- **Pushed date**: April 17th 2026, 04:51:49 UTC

### 泄露的文件
1. `douban_fetcher/config.py` - 包含数据库密码
2. `selenium_fetcher/config.py` - 包含数据库密码

### 泄露的敏感信息
```python
'password': 'q5DdyjsI5%GJOr'  # ⚠️ 已泄露，需要立即更改
```

## ✅ 已执行的修复步骤

### 1. 更新 .gitignore
**文件**: `.gitignore`

添加了配置文件排除规则：
```gitignore
# 配置文件（包含敏感信息，如数据库密码）
*config.py
!.gitignore
# 保留示例配置文件
!*example*.py
```

### 2. 创建配置模板文件

#### douban_fetcher/config_example.py
- 包含所有必要的配置项
- 使用占位符代替真实值
- 添加安全警告注释

#### selenium_fetcher/config_example.py
- 包含 Selenium 和数据库配置
- 使用占位符代替真实值
- 添加安全警告注释

### 3. 创建安全文档

#### docs/SECURITY_GUIDE.md
- 紧急处理流程
- 正确的配置管理方法
- 密码安全最佳实践
- 安全检查清单
- 检测工具使用方法

#### docs/SELENIUM_LOGGING_GUIDE.md
- Selenium 日志配置说明

### 4. 禁用 Selenium 日志输出
**文件**: `selenium_fetcher/config.py`

```python
logger.setLevel(logging.CRITICAL)
logger.disabled = True
```

## 🔄 需要手动执行的步骤

### ⚠️ 紧急：立即更改数据库密码

```sql
-- 登录数据库执行
ALTER USER 'maccms'@'%' IDENTIFIED BY '新的强密码';
FLUSH PRIVILEGES;
```

### 从 Git 历史中删除敏感文件

```bash
# 方法1：使用 git filter-branch
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch douban_fetcher/config.py selenium_fetcher/config.py' \
  --prune-empty --tag-name-filter cat -- --all

# 清理并强制推送
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force --all
git push --force --tags

# 方法2：使用 BFG Repo-Cleaner（推荐，更快）
java -jar bfg.jar --delete-files config.py
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

### 通知团队成员

如果有其他开发者使用此仓库：
1. 通知他们密码已更改
2. 让他们重新克隆仓库
3. 指导他们使用新的配置模板

## 📋 后续预防措施

### 1. 配置管理流程

```bash
# 新用户设置步骤
cp douban_fetcher/config_example.py douban_fetcher/config.py
cp selenium_fetcher/config_example.py selenium_fetcher/config.py

# 编辑 config.py 填入真实配置
# 永远不要提交 config.py！
```

### 2. 代码审查检查点

在 Pull Request 中检查：
- [ ] 没有硬编码的密码
- [ ] 没有真实的 API 密钥
- [ ] config.py 没有被包含
- [ ] 使用的是配置模板

### 3. 自动化扫描

集成以下工具到 CI/CD：
- GitGuardian
- truffleHog
- detect-secrets

```bash
# 添加到 pre-commit hook
pip install pre-commit
pre-commit install
```

### 4. 使用环境变量（推荐方案）

创建 `.env` 文件：
```bash
DB_HOST=your_host
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=maccms
```

代码中读取：
```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'password': os.getenv('DB_PASSWORD'),
    # ...
}
```

## 📊 修复状态

- [x] 更新 .gitignore
- [x] 创建配置模板
- [x] 创建安全文档
- [x] 禁用敏感日志
- [ ] ⚠️ 更改数据库密码（需手动执行）
- [ ] ⚠️ 清理 Git 历史（需手动执行）
- [ ] ⚠️ 通知团队成员（如有）

## 🔗 相关文件

- `.gitignore` - Git 忽略规则
- `douban_fetcher/config_example.py` - 配置模板
- `selenium_fetcher/config_example.py` - 配置模板
- `docs/SECURITY_GUIDE.md` - 安全指南
- `docs/SELENIUM_LOGGING_GUIDE.md` - 日志配置指南

## 💡 经验教训

1. **永远不要提交敏感信息**
   - 使用配置模板
   - 使用 .gitignore
   - 使用环境变量

2. **定期审计代码**
   - 使用自动化工具扫描
   - 代码审查时特别注意

3. **最小权限原则**
   - 数据库用户只授予必要权限
   - 定期轮换凭据

4. **教育和培训**
   - 团队成员了解安全风险
   - 建立清晰的配置管理流程

---

**最后更新**: 2026-04-17
**负责人**: [你的名字]
**状态**: 部分完成（需要手动执行密码更改和 Git 历史清理）
