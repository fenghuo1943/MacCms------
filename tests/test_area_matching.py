"""
测试地区匹配和新状态功能
"""
import sys
sys.path.insert(0, 'e:/python/MacCms自动获取评分')

from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.models import FetchStatus

def test_area_matching():
    """测试地区匹配功能"""
    print("=" * 70)
    print("测试地区匹配功能")
    print("=" * 70)
    
    # 模拟搜索结果
    search_results = [
        {
            'id': '12345',
            'title': '测试电影',
            'year': '2020',
            'country': '中国大陆'
        },
        {
            'id': '67890',
            'title': '测试电影',
            'year': '2020',
            'country': '美国'
        }
    ]
    
    # 测试1: 名称+年份+地区匹配（中国）
    result = DataProcessor.match_douban_search_results(
        search_results, 
        '测试电影', 
        '2020', 
        '中国大陆'
    )
    print(f"\n测试1 - 名称+年份+地区(中国大陆):")
    print(f"  结果: {result}")
    if result and result.get('id') == '12345':
        print("  ✓ 正确匹配到中国版本")
    else:
        print("  ✗ 匹配失败")
    
    # 测试2: 名称+年份+地区匹配（美国）
    result = DataProcessor.match_douban_search_results(
        search_results, 
        '测试电影', 
        '2020', 
        '美国'
    )
    print(f"\n测试2 - 名称+年份+地区(美国):")
    print(f"  结果: {result}")
    if result and result.get('id') == '67890':
        print("  ✓ 正确匹配到美国版本")
    else:
        print("  ✗ 匹配失败")
    
    # 测试3: 不提供地区信息（应该返回多个结果）
    result = DataProcessor.match_douban_search_results(
        search_results, 
        '测试电影', 
        '2020', 
        ''
    )
    print(f"\n测试3 - 名称+年份（无地区）:")
    print(f"  结果: {result}")
    if result == 'multiple':
        print("  ✓ 正确识别为多个结果")
    else:
        print("  ✗ 应该返回'multiple'")
    
    # 测试4: 地区不匹配
    result = DataProcessor.match_douban_search_results(
        search_results, 
        '测试电影', 
        '2020', 
        '日本'
    )
    print(f"\n测试4 - 名称+年份+地区(日本，应无匹配):")
    print(f"  结果: {result}")
    if result is None:
        print("  ✓ 正确返回None（无匹配）")
    else:
        print("  ✗ 应该返回None")

def test_new_status():
    """测试新的状态常量"""
    print("\n" + "=" * 70)
    print("测试新状态常量")
    print("=" * 70)
    
    print(f"\nNO_SEARCH_RESULT (搜索结果为空): {FetchStatus.NO_SEARCH_RESULT}")
    print(f"  描述: {FetchStatus.STATUS_MAP[FetchStatus.NO_SEARCH_RESULT]}")
    
    print(f"\nNO_MATCH_RESULT (匹配结果为空): {FetchStatus.NO_MATCH_RESULT}")
    print(f"  描述: {FetchStatus.STATUS_MAP[FetchStatus.NO_MATCH_RESULT]}")
    
    print(f"\n所有状态映射:")
    for status_code, status_name in FetchStatus.STATUS_MAP.items():
        print(f"  {status_code}: {status_name}")

if __name__ == '__main__':
    test_area_matching()
    test_new_status()
    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
