# 🔒 安全配置指南

## ⚠️ 紧急：数据库凭据泄露处理

如果你看到 GitGuardian 或其他工具警告数据库凭据泄露，请立即执行以下步骤：

### 1. 立即撤销泄露的凭据

```bash
# 登录数据库并修改密码
mysql -u root -p
```

```sql
-- 修改用户密码
ALTER USER 'maccms'@'%' IDENTIFIED BY '新的强密码';
FLUSH PRIVILEGES;
```

### 2. 从 Git 历史中删除敏感文件

```bash
# 方法1：使用 git filter-branch（推荐）
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch douban_fetcher/config.py selenium_fetcher/config.py' \
  --prune-empty --tag-name-filter cat -- --all

# 方法2：使用 BFG Repo-Cleaner（更快）
# 下载 BFG: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files config.py

# 清理并强制推送
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force --all
git push --force --tags
```

### 3. 通知团队成员

如果其他开发者也使用了这个仓库，通知他们：
- 重新克隆仓库
- 不要使用旧的配置文件
- 创建自己的 config.py

## 📋 正确的配置管理流程

### 步骤1：复制示例配置文件

```bash
# 对于 douban_fetcher
cp douban_fetcher/config_example.py douban_fetcher/config.py

# 对于 selenium_fetcher
cp selenium_fetcher/config_example.py selenium_fetcher/config.py
```

### 步骤2：编辑配置文件

打开 `config.py` 文件，填入真实的配置信息：

```python
DB_CONFIG = {
    'host': 'your_real_host',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_strong_password',  # ⚠️ 使用强密码
    'database': 'maccms',
    'charset': 'utf8mb4'
}
```

### 步骤3：验证 .gitignore

确保 `.gitignore` 包含以下内容：

```gitignore
# 配置文件（包含敏感信息）
*config.py
!.gitignore
# 保留示例配置文件
!*example*.py
```

### 步骤4：提交代码

```bash
git add .gitignore
git add douban_fetcher/config_example.py
git add selenium_fetcher/config_example.py
git commit -m "chore: 添加配置模板并忽略敏感配置文件"
git push
```

**⚠️ 重要**：永远不要提交 `config.py` 文件！

## 🔐 密码安全最佳实践

### 1. 使用强密码

```
✅ 推荐：X9#kL2$mP7@nQ4&vR8!wT5
❌ 避免：123456、password、admin
```

### 2. 定期更换密码

- 每 3-6 个月更换一次
- 怀疑泄露时立即更换
- 使用密码管理器生成和存储密码

### 3. 使用环境变量（更安全的方案）

创建 `.env` 文件（已在 .gitignore 中）：

```bash
# .env 文件
DB_HOST=mylove.fenghuo1943.cn
DB_PORT=13307
DB_USER=maccms
DB_PASSWORD=your_password_here
DB_NAME=maccms
```

在代码中读取：

```python
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8mb4'
}
```

安装依赖：
```bash
pip install python-dotenv
```

## 🛡️ 安全检查清单

在每次提交代码前，检查：

- [ ] 没有硬编码的密码
- [ ] 没有真实的 API 密钥
- [ ] 没有数据库连接字符串
- [ ] config.py 没有被提交
- [ ] .env 文件没有被提交
- [ ] 使用的是配置模板（config_example.py）

## 🔍 检测敏感信息泄露

### 使用 GitGuardian CLI

```bash
# 安装
pip install gitguardian-cli

# 扫描当前仓库
ggshield scan repo .
```

### 使用 truffleHog

```bash
# 安装
pip install trufflehog

# 扫描
trufflehog filesystem .
```

### 手动检查

```bash
# 搜索可能的密码
grep -r "password.*=" --include="*.py" .
grep -r "passwd.*=" --include="*.py" .
grep -r "secret.*=" --include="*.py" .
grep -r "api_key.*=" --include="*.py" .
```

## 📞 如果已经泄露

1. **立即更改密码**
2. **从 Git 历史中删除**（见上方步骤）
3. **联系 GitHub 支持**（如果已公开）
4. **监控数据库访问日志**
5. **考虑启用双因素认证**
6. **审查所有访问权限**

## 📚 相关资源

- [GitHub 安全最佳实践](https://docs.github.com/en/code-security/getting-started/github-security-best-practices)
- [GitGuardian 文档](https://docs.gitguardian.com/)
- [12-Factor App: Config](https://12factor.net/config)

---

**记住：安全第一！永远不要将敏感信息提交到版本控制系统。**
