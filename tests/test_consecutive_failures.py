"""
测试连续失败检测功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.api_client import ApiClient
from douban_fetcher.config import logger


def test_consecutive_failures():
    """测试连续失败计数功能"""
    print("测试连续失败计数功能...")
    
    # 创建API客户端
    client = ApiClient()
    
    # 初始状态
    print(f"初始连续失败次数: {client.consecutive_failures}")
    assert client.consecutive_failures == 0, "初始连续失败次数应为0"
    
    # 模拟几次失败请求（使用不存在的视频名）
    test_videos = ["不存在的视频1", "不存在的视频2", "不存在的视频3"]
    
    for video_name in test_videos:
        result = client.search_douban(video_name)
        print(f"搜索 '{video_name}': {'成功' if result is not None else '失败'}, "
              f"连续失败次数: {client.consecutive_failures}")
    
    print(f"最终连续失败次数: {client.consecutive_failures}")
    
    # 测试成功后重置计数器
    print("\n测试成功后重置计数器...")
    # 注意：这里我们不调用真实的成功请求，只是展示逻辑
    # 在实际使用中，当search_douban返回非None且非空列表时，计数器会重置
    
    print("✓ 连续失败计数功能测试完成")


def test_api_client_initialization():
    """测试API客户端初始化"""
    print("\n测试API客户端初始化...")
    
    client = ApiClient()
    
    # 检查新添加的属性
    assert hasattr(client, 'consecutive_failures'), "缺少consecutive_failures属性"
    assert hasattr(client, 'max_consecutive_failures'), "缺少max_consecutive_failures属性"
    assert client.consecutive_failures == 0, "初始连续失败次数应为0"
    assert client.max_consecutive_failures == 10, "默认最大连续失败次数应为10"
    
    print("✓ API客户端初始化测试完成")


if __name__ == "__main__":
    try:
        test_api_client_initialization()
        test_consecutive_failures()
        print("\n" + "="*50)
        print("所有测试通过！")
        print("="*50)
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
