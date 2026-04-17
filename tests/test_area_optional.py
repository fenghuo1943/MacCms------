"""
测试宽松匹配中地区可以为空的场景
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from douban_fetcher.data_processor import DataProcessor


def test_loose_matching_with_empty_area():
    """测试宽松匹配中地区为空时仍能匹配"""
    
    print("="*70)
    print("测试: 宽松匹配 - 地区为空时仍能匹配")
    print("="*70)
    
    # 模拟搜索结果
    search_results = [
        {
            "title": "大觉醒",  # 名称有包含关系
            "year": "2026",
            "id": "37940320",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        }
    ]
    
    # 测试：地区为空，但年份和导演非空且匹配
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",
        target_year="2026",       # 年份非空且匹配
        target_area="",           # 地区为空
        target_director="约书亚·恩克"  # 导演非空且匹配
    )
    
    if matched:
        print(f"✅ 匹配成功! 匹配到: {matched.get('title')}")
        print(f"   ID: {matched.get('id')}, 年份: {matched.get('year')}")
        print(f"   导演: {[d.get('name') for d in matched.get('directors', [])]}")
        print(f"   地区: {matched.get('countries', [])}")
        test_passed = True
    else:
        print("❌ 匹配失败，地区为空时应该仍能匹配")
        test_passed = False
    
    print()
    return test_passed


def test_loose_matching_with_none_area():
    """测试宽松匹配中地区为None时仍能匹配"""
    
    print("="*70)
    print("测试: 宽松匹配 - 地区为None时仍能匹配")
    print("="*70)
    
    # 模拟搜索结果
    search_results = [
        {
            "title": "觉醒",  # 名称有包含关系
            "year": "2026",
            "id": "37940321",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        }
    ]
    
    # 测试：地区为None，但年份和导演非空且匹配
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",
        target_year="2026",       # 年份非空且匹配
        target_area=None,         # 地区为None
        target_director="约书亚·恩克"  # 导演非空且匹配
    )
    
    if matched:
        print(f"✅ 匹配成功! 匹配到: {matched.get('title')}")
        print(f"   ID: {matched.get('id')}, 年份: {matched.get('year')}")
        print(f"   导演: {[d.get('name') for d in matched.get('directors', [])]}")
        test_passed = True
    else:
        print("❌ 匹配失败，地区为None时应该仍能匹配")
        test_passed = False
    
    print()
    return test_passed


def test_loose_matching_without_year_should_fail():
    """测试宽松匹配中年份为空时应该失败"""
    
    print("="*70)
    print("测试: 宽松匹配 - 年份为空时应该失败")
    print("="*70)
    
    # 模拟搜索结果
    search_results = [
        {
            "title": "大觉醒",  # 名称有包含关系
            "year": "2026",
            "id": "37940322",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        }
    ]
    
    # 测试：年份为空，应该跳过
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",
        target_year="",           # 年份为空
        target_area="美国",       # 地区非空
        target_director="约书亚·恩克"  # 导演非空
    )
    
    if matched is None:
        print("✅ 正确返回 None，年份为空时应该失败")
        test_passed = True
    else:
        print(f"❌ 应该返回 None 但匹配到了: {matched.get('title')}")
        test_passed = False
    
    print()
    return test_passed


def test_loose_matching_without_director_should_fail():
    """测试宽松匹配中导演为空时应该失败"""
    
    print("="*70)
    print("测试: 宽松匹配 - 导演为空时应该失败")
    print("="*70)
    
    # 模拟搜索结果
    search_results = [
        {
            "title": "大觉醒",  # 名称有包含关系
            "year": "2026",
            "id": "37940323",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        }
    ]
    
    # 测试：导演为空，应该跳过
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",
        target_year="2026",       # 年份非空
        target_area="美国",       # 地区非空
        target_director=""        # 导演为空
    )
    
    if matched is None:
        print("✅ 正确返回 None，导演为空时应该失败")
        test_passed = True
    else:
        print(f"❌ 应该返回 None 但匹配到了: {matched.get('title')}")
        test_passed = False
    
    print()
    return test_passed


if __name__ == '__main__':
    print("\n开始测试宽松匹配中地区可选的功能...\n")
    
    test1_passed = test_loose_matching_with_empty_area()
    test2_passed = test_loose_matching_with_none_area()
    test3_passed = test_loose_matching_without_year_should_fail()
    test4_passed = test_loose_matching_without_director_should_fail()
    
    print("="*70)
    print("测试结果汇总:")
    print(f"  测试1 (地区为空): {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"  测试2 (地区为None): {'✅ 通过' if test2_passed else '❌ 失败'}")
    print(f"  测试3 (年份为空): {'✅ 通过' if test3_passed else '❌ 失败'}")
    print(f"  测试4 (导演为空): {'✅ 通过' if test4_passed else '❌ 失败'}")
    print("="*70)
    
    if all([test1_passed, test2_passed, test3_passed, test4_passed]):
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️  部分测试失败，请检查实现")
