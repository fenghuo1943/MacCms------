"""
测试 RLock 修复 - 验证死锁问题已解决
"""
import sys
sys.path.insert(0, '.')

from douban_fetcher.rate_limiter import RateLimitMonitor
import json
import time

print("=" * 60)
print("测试 RLock 修复")
print("=" * 60)

# 创建监控器
monitor = RateLimitMonitor()

# 模拟一些请求
print("\n1. 模拟请求...")
for i in range(10):
    monitor.record_request(success=(i % 3 != 0))
    time.sleep(0.01)
print("✓ 请求记录完成")

# 测试 get_current_rate
print("\n2. 测试 get_current_rate()...")
try:
    rate = monitor.get_current_rate()
    print(f"✓ 当前速率: {rate:.2f} req/s")
except Exception as e:
    print(f"✗ 失败: {e}")
    sys.exit(1)

# 测试 get_stats（这会调用 get_current_rate，之前会导致死锁）
print("\n3. 测试 get_stats()（包含嵌套锁调用）...")
try:
    stats = monitor.get_stats()
    print(f"✓ 统计数据获取成功:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")
except Exception as e:
    print(f"✗ 失败: {e}")
    sys.exit(1)

# 测试 JSON 序列化
print("\n4. 测试 JSON 序列化...")
try:
    stats_json = json.dumps(stats, ensure_ascii=False)
    print(f"✓ JSON 序列化成功:")
    print(f"  {stats_json}")
except Exception as e:
    print(f"✗ 失败: {e}")
    sys.exit(1)

# 多次调用测试
print("\n5. 多次调用测试（压力测试）...")
try:
    for i in range(100):
        stats = monitor.get_stats()
        rate = monitor.get_current_rate()
    print(f"✓ 成功执行 100 次调用，无死锁")
except Exception as e:
    print(f"✗ 失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ 所有测试通过！RLock 修复成功！")
print("=" * 60)
print("\n说明:")
print("- 使用 RLock 后，get_stats() 可以安全地调用 get_current_rate()")
print("- 不会再出现死锁问题")
print("- 程序可以正常运行")
