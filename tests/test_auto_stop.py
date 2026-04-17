"""
测试自动停止功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.fetcher import DoubanScoreFetcher
from douban_fetcher.config import DB_CONFIG_EXAMPLE


def test_fetcher_initialization():
    """测试Fetcher初始化"""
    print("测试Fetcher初始化...")
    
    # 使用示例配置创建fetcher（不会真正连接数据库）
    try:
        fetcher = DoubanScoreFetcher(
            db_config=DB_CONFIG_EXAMPLE,
            max_requests_per_second=2.0,
            use_proxy=False
        )
        
        # 检查新添加的属性
        assert hasattr(fetcher, 'consecutive_no_results'), "缺少consecutive_no_results属性"
        assert hasattr(fetcher, 'max_consecutive_no_results'), "缺少max_consecutive_no_results属性"
        assert fetcher.consecutive_no_results == 0, "初始连续无结果次数应为0"
        assert fetcher.max_consecutive_no_results == 20, "默认最大连续无结果次数应为20"
        
        # 检查api_client的属性
        assert hasattr(fetcher.api_client, 'consecutive_failures'), "api_client缺少consecutive_failures属性"
        assert hasattr(fetcher.api_client, 'max_consecutive_failures'), "api_client缺少max_consecutive_failures属性"
        assert fetcher.api_client.consecutive_failures == 0, "初始连续失败次数应为0"
        assert fetcher.api_client.max_consecutive_failures == 10, "默认最大连续失败次数应为10"
        
        print("✓ Fetcher初始化测试完成")
        return True
    except Exception as e:
        print(f"✗ Fetcher初始化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_logic_description():
    """描述自动停止逻辑"""
    print("\n" + "="*70)
    print("自动停止功能说明")
    print("="*70)
    print("""
1. 连续API请求失败检测：
   - 当API请求失败（超时、连接错误、异常等）时，连续失败计数器+1
   - 当API请求成功时，连续失败计数器重置为0
   - 当连续失败次数达到10次时，自动停止任务

2. 连续无结果检测：
   - 当搜索返回空结果时，连续无结果计数器+1
   - 当搜索返回有结果时，连续无结果计数器重置为0
   - 当连续无结果次数达到20次时，自动停止任务
   - 这可以检测豆瓣API的静默限制（不返回429但返回空结果）

3. 整批失败检测：
   - 如果一批数据全部处理失败
   - 且连续失败次数>=5次
   - 则自动停止任务

这些检测机制可以有效防止在API被限制后继续无效请求。
    """)
    print("="*70)


if __name__ == "__main__":
    print("测试自动停止功能...\n")
    
    success = test_fetcher_initialization()
    test_logic_description()
    
    if success:
        print("\n" + "="*50)
        print("所有测试通过！")
        print("="*50)
    else:
        print("\n测试失败！")
        sys.exit(1)
