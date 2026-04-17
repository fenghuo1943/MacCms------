"""
测试分级匹配策略 - 严格匹配和宽松匹配
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from douban_fetcher.data_processor import DataProcessor


def test_strict_matching():
    """测试严格匹配（名称精确匹配+年份+导演+地区）"""
    
    print("="*70)
    print("测试1: 严格匹配 - 名称精确匹配时返回")
    print("="*70)
    
    # 模拟搜索结果：有精确匹配
    search_results = [
        {
            "title": "伟大的觉醒",  # 精确匹配
            "year": "2026",
            "id": "37940320",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        },
        {
            "title": "不相关的电影",
            "year": "2020",
            "id": "37940321",
            "directors": [{"name": "其他导演", "id": "1481885"}],
            "countries": ["日本"]
        }
    ]
    
    # 测试：名称精确匹配
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",  # 精确匹配
        target_year="2026",
        target_area="美国",
        target_director="约书亚·恩克"
    )
    
    if matched:
        print(f"✅ 严格匹配成功! 匹配到: {matched.get('title')}")
        print(f"   ID: {matched.get('id')}, 年份: {matched.get('year')}")
        test1_passed = True
    else:
        print("❌ 严格匹配失败")
        test1_passed = False
    
    print()
    return test1_passed


def test_multiple_strict_results():
    """测试严格匹配返回多个结果的情况"""
    
    print("="*70)
    print("测试2: 严格匹配 - 多个精确匹配结果时返回'multiple'")
    print("="*70)
    
    # 模拟搜索结果：有多个精确匹配项
    search_results = [
        {
            "title": "伟大的觉醒",  # 精确匹配
            "year": "2026",
            "id": "37940320",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        },
        {
            "title": "伟大的觉醒",  # 精确匹配（同名不同ID）
            "year": "2026",
            "id": "37940322",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        }
    ]
    
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",
        target_year="2026",
        target_area="美国",
        target_director="约书亚·恩克"
    )
    
    if matched == 'multiple':
        print("✅ 正确返回 'multiple' 表示多个结果")
        test2_passed = True
    else:
        print("❌ 应该返回 'multiple' 但返回了其他结果")
        test2_passed = False
    
    print()
    return test2_passed


def test_fallback_to_loose_matching():
    """测试回退到宽松匹配（名称包含关系/相似度 + 年份/地区/导演必须非空且匹配）"""
    
    print("="*70)
    print("测试3: 回退到宽松匹配 - 严格匹配无结果时使用宽松匹配")
    print("="*70)
    
    # 模拟搜索结果：严格匹配无结果，但宽松匹配有结果
    search_results = [
        {
            "title": "大觉醒",  # 名称有包含关系（“觉醒”在“伟大的觉醒”中）
            "year": "2026",
            "id": "37940323",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        },
        {
            "title": "另一个无关电影",  # 名称不匹配
            "year": "2020",  # 年份不匹配
            "id": "37940324",
            "directors": [{"name": "其他导演", "id": "1481885"}],
            "countries": ["日本"]
        }
    ]
    
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",  # 和第一个结果的名称有包含关系
        target_year="2026",       # 年份必须非空且匹配
        target_area="美国",       # 地区必须非空且匹配
        target_director="约书亚·恩克"  # 导演必须非空且匹配
    )
    
    if matched:
        print(f"✅ 回退到宽松匹配成功! 匹配到: {matched.get('title')}")
        print(f"   ID: {matched.get('id')}, 年份: {matched.get('year')}")
        print(f"   导演: {[d.get('name') for d in matched.get('directors', [])]}")
        test3_passed = True
    else:
        print("❌ 宽松匹配失败，没有找到任何匹配")
        test3_passed = False
    
    print()
    return test3_passed


def test_no_results_at_all():
    """测试完全没有匹配结果的情况"""
    
    print("="*70)
    print("测试4: 完全无匹配结果")
    print("="*70)
    
    # 模拟搜索结果：没有任何匹配
    search_results = [
        {
            "title": "完全无关电影",
            "year": "2020",
            "id": "37940325",
            "directors": [{"name": "其他导演", "id": "1481885"}],
            "countries": ["日本"]
        }
    ]
    
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",
        target_year="2026",
        target_area="美国",
        target_director="约书亚·恩克"
    )
    
    if matched is None:
        print("✅ 正确返回 None 表示无匹配")
        test4_passed = True
    else:
        print("❌ 应该返回 None 但返回了其他结果")
        test4_passed = False
    
    print()
    return test4_passed


def test_only_loose_match_exists():
    """测试只有宽松匹配存在的场景"""
    
    print("="*70)
    print("测试5: 只有宽松匹配存在的场景")
    print("="*70)
    
    # 模拟搜索结果：严格匹配无结果，但有一个接近的匹配
    search_results = [
        {
            "title": "觉醒",  # 名称有包含关系（翻译差异）
            "year": "2026",           # 年份匹配
            "id": "37940326",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],  # 导演匹配
            "countries": ["美国"]      # 地区匹配
        }
    ]
    
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",
        target_year="2026",
        target_area="美国",
        target_director="约书亚·恩克"
    )
    
    if matched:
        print(f"✅ 宽松匹配成功! 匹配到: {matched.get('title')}")
        print(f"   ID: {matched.get('id')}, 年份: {matched.get('year')}")
        test5_passed = True
    else:
        print("❌ 宽松匹配失败")
        test5_passed = False
    
    print()
    return test5_passed


def test_loose_matching_multiple_results():
    """测试宽松匹配多个结果时返回'multiple'"""
    
    print("="*70)
    print("测试6: 宽松匹配 - 多个结果时返回'multiple'")
    print("="*70)
    
    # 模拟搜索结果：严格匹配无结果，宽松匹配有多个结果
    search_results = [
        {
            "title": "大觉醒",  # 名称有包含关系
            "year": "2026",
            "id": "37940327",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        },
        {
            "title": "觉醒",  # 名称有包含关系
            "year": "2026",
            "id": "37940328",
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "countries": ["美国"]
        }
    ]
    
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name="伟大的觉醒",
        target_year="2026",
        target_area="美国",
        target_director="约书亚·恩克"
    )
    
    if matched == 'multiple':
        print("✅ 正确返回 'multiple' 表示多个宽松匹配结果")
        test6_passed = True
    else:
        print(f"❌ 应该返回 'multiple' 但返回了: {matched}")
        test6_passed = False
    
    print()
    return test6_passed


if __name__ == '__main__':
    print("\n开始测试分级匹配策略...\n")
    
    test1_passed = test_strict_matching()
    test2_passed = test_multiple_strict_results()
    test3_passed = test_fallback_to_loose_matching()
    test4_passed = test_no_results_at_all()
    test5_passed = test_only_loose_match_exists()
    test6_passed = test_loose_matching_multiple_results()
    
    print("="*70)
    print("测试结果汇总:")
    print(f"  测试1 (严格匹配): {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"  测试2 (多结果处理): {'✅ 通过' if test2_passed else '❌ 失败'}")
    print(f"  测试3 (回退匹配): {'✅ 通过' if test3_passed else '❌ 失败'}")
    print(f"  测试4 (无结果): {'✅ 通过' if test4_passed else '❌ 失败'}")
    print(f"  测试5 (宽松匹配): {'✅ 通过' if test5_passed else '❌ 失败'}")
    print(f"  测试6 (宽松多结果): {'✅ 通过' if test6_passed else '❌ 失败'}")
    print("="*70)
    
    if all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed, test6_passed]):
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️  部分测试失败，请检查实现")

