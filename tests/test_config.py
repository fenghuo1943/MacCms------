"""
配置验证脚本 - 检查配置是否正确
"""
import sys
sys.path.insert(0, '.')

print("=" * 60)
print("配置验证")
print("=" * 60)

# 测试1: 导入配置模块
try:
    from douban_fetcher.config import DB_CONFIG_EXAMPLE, DEFAULT_RUN_CONFIG
    print("\n✓ 配置模块导入成功")
except Exception as e:
    print(f"\n✗ 配置模块导入失败: {e}")
    sys.exit(1)

# 测试2: 检查数据库配置
print("\n【数据库配置】")
print(f"  主机: {DB_CONFIG_EXAMPLE['host']}")
print(f"  端口: {DB_CONFIG_EXAMPLE['port']}")
print(f"  用户: {DB_CONFIG_EXAMPLE['user']}")
print(f"  密码: {'*' * len(DB_CONFIG_EXAMPLE['password'])}")
print(f"  数据库: {DB_CONFIG_EXAMPLE['database']}")

# 测试3: 检查运行配置
print("\n【运行配置】")
print(f"  批处理大小: {DEFAULT_RUN_CONFIG['batch_size']}")
print(f"  请求速率: {DEFAULT_RUN_CONFIG['max_requests_per_second']} req/s")
print(f"  自动调速: {DEFAULT_RUN_CONFIG['adjust_rate']}")
print(f"  使用代理: {DEFAULT_RUN_CONFIG['use_proxy']}")
print(f"  代理列表: {DEFAULT_RUN_CONFIG['proxy_list']}")

# 测试4: 验证配置完整性
required_db_keys = ['host', 'port', 'user', 'password', 'database']
missing_keys = [key for key in required_db_keys if key not in DB_CONFIG_EXAMPLE]
if missing_keys:
    print(f"\n✗ 数据库配置缺少字段: {missing_keys}")
else:
    print("\n✓ 数据库配置完整")

required_run_keys = ['batch_size', 'max_requests_per_second', 'adjust_rate', 'use_proxy', 'proxy_list']
missing_keys = [key for key in required_run_keys if key not in DEFAULT_RUN_CONFIG]
if missing_keys:
    print(f"✗ 运行配置缺少字段: {missing_keys}")
else:
    print("✓ 运行配置完整")

# 测试5: 验证 main.py 能否正确引用配置
print("\n【main.py 配置引用检查】")
try:
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'DB_CONFIG_EXAMPLE' in content:
            print("✓ main.py 使用了 DB_CONFIG_EXAMPLE")
        else:
            print("✗ main.py 未使用 DB_CONFIG_EXAMPLE")
        
        if 'DEFAULT_RUN_CONFIG' in content:
            print("✓ main.py 使用了 DEFAULT_RUN_CONFIG")
        else:
            print("✗ main.py 未使用 DEFAULT_RUN_CONFIG")
            
        # 检查是否还有硬编码配置
        if "'host': '192.168.114.4'" in content and 'DB_CONFIG_EXAMPLE' not in content.split("'host': '192.168.114.4'")[0][-50:]:
            print("⚠ main.py 中可能存在硬编码的数据库配置")
        else:
            print("✓ main.py 中没有硬编码配置")
except Exception as e:
    print(f"✗ 检查失败: {e}")

print("\n" + "=" * 60)
print("配置验证完成！")
print("=" * 60)
print("\n提示: 如需修改配置，请编辑 douban_fetcher/config.py")
