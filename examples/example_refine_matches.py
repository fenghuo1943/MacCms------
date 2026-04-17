"""
多结果二次确认功能使用示例
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.api_client import ApiClient


def example_basic_usage():
    """基本使用示例"""
    print("=" * 70)
    print("示例1：基本用法")
    print("=" * 70)
    
    api_client = ApiClient()
    
    # 搜索视频
    video_name = "流浪地球"
    print(f"\n搜索视频: {video_name}")
    
    search_results = api_client.search_douban(video_name)
    
    if not search_results:
        print("搜索失败或无结果")
        return
    
    print(f"找到 {len(search_results)} 个搜索结果\n")
    
    # 显示前3个结果
    for i, result in enumerate(search_results[:3], 1):
        print(f"{i}. {result.get('title', '')} ({result.get('year', '')}) - ID: {result.get('id', '')}")
    
    # 匹配视频（启用二次确认）
    print("\n开始匹配（启用二次确认）...")
    matched = DataProcessor.match_douban_search_results(
        search_results,
        target_name="流浪地球",
        target_year="2019",
        target_area="中国大陆",
        target_director="郭帆",
        api_client=api_client
    )
    
    if matched == 'multiple':
        print("结果: 仍然有多个匹配结果")
    elif matched is None:
        print("结果: 未找到匹配")
    else:
        print(f"✓ 匹配成功!")
        print(f"  标题: {matched.get('title', '')}")
        print(f"  年份: {matched.get('year', '')}")
        print(f"  ID: {matched.get('id', '')}")
    
    print()


def example_without_api_client():
    """不使用api_client的示例（向后兼容）"""
    print("=" * 70)
    print("示例2：不传入api_client（向后兼容模式）")
    print("=" * 70)
    
    api_client = ApiClient()
    
    video_name = "复仇者联盟"
    print(f"\n搜索视频: {video_name}")
    
    search_results = api_client.search_douban(video_name)
    
    if not search_results:
        print("搜索失败或无结果")
        return
    
    print(f"找到 {len(search_results)} 个搜索结果\n")
    
    # 不传入api_client，如果匹配到多个结果会直接返回'multiple'
    print("开始匹配（不传入api_client）...")
    matched = DataProcessor.match_douban_search_results(
        search_results,
        target_name="复仇者联盟",
        target_year="",
        target_area="",
        target_director=""
        # 注意：没有传入 api_client
    )
    
    if matched == 'multiple':
        print("结果: 多个匹配（未进行二次确认）")
    elif matched is None:
        print("结果: 未找到匹配")
    else:
        print(f"✓ 匹配成功!")
        print(f"  标题: {matched.get('title', '')}")
        print(f"  ID: {matched.get('id', '')}")
    
    print()


def example_with_partial_info():
    """部分信息示例"""
    print("=" * 70)
    print("示例3：仅提供部分信息")
    print("=" * 70)
    
    api_client = ApiClient()
    
    video_name = "盗梦空间"
    print(f"\n搜索视频: {video_name}")
    print("提供信息: 仅提供名称和年份，不提供地区和导演")
    
    search_results = api_client.search_douban(video_name)
    
    if not search_results:
        print("搜索失败或无结果")
        return
    
    print(f"找到 {len(search_results)} 个搜索结果\n")
    
    # 仅提供部分信息
    print("开始匹配（仅名称+年份）...")
    matched = DataProcessor.match_douban_search_results(
        search_results,
        target_name="盗梦空间",
        target_year="2010",
        target_area="",  # 不提供地区
        target_director="",  # 不提供导演
        api_client=api_client
    )
    
    if matched == 'multiple':
        print("结果: 仍然有多个匹配结果")
    elif matched is None:
        print("结果: 未找到匹配")
    else:
        print(f"✓ 匹配成功!")
        print(f"  标题: {matched.get('title', '')}")
        print(f"  年份: {matched.get('year', '')}")
        print(f"  ID: {matched.get('id', '')}")
    
    print()


if __name__ == '__main__':
    try:
        example_basic_usage()
        example_without_api_client()
        example_with_partial_info()
        
        print("=" * 70)
        print("所有示例运行完成！")
        print("=" * 70)
    except Exception as e:
        print(f"\n✗ 运行失败: {str(e)}")
        import traceback
        traceback.print_exc()
