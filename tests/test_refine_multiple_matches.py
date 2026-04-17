"""
测试多结果二次确认功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.api_client import ApiClient


def test_refine_multiple_matches():
    """测试通过Subject API对多个候选结果进行二次确认"""
    
    # 创建API客户端
    api_client = ApiClient()
    
    # 模拟多个候选结果（以"蜘蛛侠"为例）
    candidates = [
        {
            'id': '26374149',
            'title': '蜘蛛侠：英雄归来',
            'year': '2017',
            'type': 'movie'
        },
        {
            'id': '3048829',
            'title': '蜘蛛侠',
            'year': '2002',
            'type': 'movie'
        },
        {
            'id': '1308753',
            'title': '蜘蛛侠2',
            'year': '2004',
            'type': 'movie'
        }
    ]
    
    # 目标视频信息
    target_name = "蜘蛛侠：英雄归来"
    target_year = "2017"
    target_area = "美国"
    target_director = "乔·沃茨"
    
    print("=" * 70)
    print("测试：多结果二次确认功能")
    print("=" * 70)
    print(f"\n目标视频: {target_name}")
    print(f"年份: {target_year}")
    print(f"地区: {target_area}")
    print(f"导演: {target_director}")
    print(f"\n候选结果数量: {len(candidates)}")
    
    for i, candidate in enumerate(candidates, 1):
        print(f"  {i}. {candidate['title']} ({candidate['year']}) - ID: {candidate['id']}")
    
    print("\n开始二次确认...")
    print("-" * 70)
    
    # 调用二次确认方法
    result = DataProcessor._refine_multiple_matches(
        candidates, target_name, target_year, target_area, target_director, api_client
    )
    
    print("-" * 70)
    print("\n最终结果:")
    if result == 'multiple':
        print("  ✗ 仍然匹配到多个结果")
    elif result is None:
        print("  ✗ 未找到匹配结果")
    else:
        print(f"  ✓ 精确匹配到 1 个结果:")
        print(f"    标题: {result.get('title', '')}")
        print(f"    年份: {result.get('year', '')}")
        print(f"    ID: {result.get('id', '')}")
    
    print("=" * 70)


def test_match_with_api_client():
    """测试完整的匹配流程（包含api_client）"""
    
    api_client = ApiClient()
    
    # 搜索一个可能产生多个结果的影片
    video_name = "复仇者联盟"
    
    print("\n" + "=" * 70)
    print("测试：完整匹配流程（带api_client）")
    print("=" * 70)
    print(f"\n搜索视频: {video_name}")
    
    # 使用API搜索
    search_results = api_client.search_douban(video_name)
    
    if not search_results:
        print("  ✗ 搜索失败或无结果")
        return
    
    print(f"  搜索结果数量: {len(search_results)}")
    
    # 显示前5个结果
    for i, result in enumerate(search_results[:5], 1):
        title = result.get('title', '')
        year = result.get('year', '')
        douban_id = result.get('id', '')
        print(f"    {i}. {title} ({year}) - ID: {douban_id}")
    
    if len(search_results) > 5:
        print(f"    ... 还有 {len(search_results) - 5} 个结果")
    
    # 尝试匹配（不提供年份、地区、导演，应该会返回多个结果）
    print("\n尝试匹配（不提供额外信息）...")
    matched = DataProcessor.match_douban_search_results(
        search_results, video_name, "", "", "", api_client
    )
    
    if matched == 'multiple':
        print("  结果: 多个匹配")
    elif matched is None:
        print("  结果: 未找到匹配")
    else:
        print(f"  结果: 精确匹配到 1 个")
        print(f"    标题: {matched.get('title', '')}")
        print(f"    ID: {matched.get('id', '')}")
    
    print("=" * 70)


if __name__ == '__main__':
    try:
        # 测试1：直接测试二次确认功能
        test_refine_multiple_matches()
        
        # 测试2：测试完整匹配流程
        test_match_with_api_client()
        
        print("\n✓ 测试完成")
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
