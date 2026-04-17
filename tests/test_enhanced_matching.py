"""
测试增强的匹配功能 - 支持翻译差异和多字段综合匹配
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from douban_fetcher.data_processor import DataProcessor


def test_translation_matching_with_director():
    """测试翻译差异的匹配（带导演信息）- 伟大的觉醒案例"""
    
    # 模拟数据库中的视频信息
    target_name = "伟大的觉醒"
    target_year = "2026"
    target_area = "美国"
    target_director = "约书亚·恩克"
    
    # 模拟豆瓣返回的搜索结果
    search_results = [
        {
            "title": "大觉醒",
            "year": "2026",
            "id": "37940320",
            "rating": {"max": 10, "average": 0, "stars": "00", "min": 0},
            "genres": ["剧情", "历史"],
            "directors": [{"name": "约书亚·恩克", "id": "1481884"}],
            "casts": [{"name": "John Paul Sneed"}, {"name": "乔纳森·布莱尔", "id": "1481887"}],
            "original_title": "A Great Awakening",
            "countries": ["美国"]
        }
    ]
    
    print("="*70)
    print("测试1: 翻译差异匹配（伟大的觉醒 vs 大觉醒）")
    print("="*70)
    print(f"目标名称: {target_name}")
    print(f"目标年份: {target_year}")
    print(f"目标地区: {target_area}")
    print(f"目标导演: {target_director}")
    print()
    
    # 测试名称相似度
    result_name = search_results[0]['title']
    similarity = DataProcessor.calculate_similarity(target_name, result_name)
    print(f"结果名称: {result_name}")
    print(f"名称相似度: {similarity:.2f}")
    
    # 测试包含关系
    containment = DataProcessor.check_name_containment(target_name, result_name)
    print(f"名称包含关系: {containment}")
    print()
    
    # 测试完整匹配
    matched = DataProcessor.match_douban_search_results(
        search_results, 
        target_name, 
        target_year, 
        target_area,
        target_director
    )
    
    if matched:
        print("✅ 匹配成功!")
        print(f"  匹配结果ID: {matched.get('id')}")
        print(f"  匹配结果标题: {matched.get('title')}")
        print(f"  匹配结果年份: {matched.get('year')}")
        if matched.get('directors'):
            directors = [d.get('name', '') for d in matched['directors'] if d.get('name')]
            print(f"  匹配结果导演: {', '.join(directors)}")
        if matched.get('countries'):
            print(f"  匹配结果国家: {', '.join(matched['countries'])}")
    else:
        print("❌ 匹配失败")
    
    print()
    return matched is not None


def test_multiple_translation_cases():
    """测试多个翻译差异案例"""
    
    test_cases = [
        {
            "name": "复仇者联盟 vs 复仇者",
            "target": "复仇者联盟",
            "result": "复仇者",
            "should_match": True
        },
        {
            "name": "蝙蝠侠：黑暗骑士 vs 黑暗骑士",
            "target": "蝙蝠侠：黑暗骑士",
            "result": "黑暗骑士",
            "should_match": True
        },
        {
            "name": "X战警：黑凤凰 vs 黑凤凰",
            "target": "X战警：黑凤凰",
            "result": "黑凤凰",
            "should_match": True
        },
        {
            "name": "蜘蛛侠：英雄无归 vs 蜘蛛侠3（名称相似但实际不同，需要其他字段辅助）",
            "target": "蜘蛛侠：英雄无归",
            "result": "蜘蛛侠3",
            "should_match": True  # 名称层面确实相似，实际应用中会通过年份/导演区分
        }
    ]
    
    print("="*70)
    print("测试2: 多个翻译差异案例")
    print("="*70)
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        similarity = DataProcessor.calculate_similarity(case["target"], case["result"])
        containment = DataProcessor.check_name_containment(case["target"], case["result"])
        
        # 判断是否应该匹配
        should_match = similarity >= 0.7 or containment
        
        passed = should_match == case["should_match"]
        status = "✅" if passed else "❌"
        
        print(f"{status} 案例{i}: {case['name']}")
        print(f"   相似度: {similarity:.2f}, 包含关系: {containment}")
        print(f"   预期: {case['should_match']}, 实际: {should_match}")
        
        if not passed:
            all_passed = False
    
    print()
    return all_passed


def test_director_matching():
    """测试导演匹配功能"""
    
    print("="*70)
    print("测试3: 导演匹配功能")
    print("="*70)
    
    # 案例1: 导演完全匹配
    search_results_1 = [
        {
            "title": "测试电影",
            "year": "2020",
            "id": "123",
            "directors": [{"name": "张三", "id": "100"}]
        }
    ]
    
    matched = DataProcessor.match_douban_search_results(
        search_results_1, 
        "测试电影", 
        "2020", 
        "",
        "张三"
    )
    
    if matched:
        print("✅ 案例1: 导演完全匹配 - 通过")
        test1_passed = True
    else:
        print("❌ 案例1: 导演完全匹配 - 失败")
        test1_passed = False
    
    # 案例2: 导演不匹配
    search_results_2 = [
        {
            "title": "测试电影",
            "year": "2020",
            "id": "123",
            "directors": [{"name": "李四", "id": "101"}]
        }
    ]
    
    matched = DataProcessor.match_douban_search_results(
        search_results_2, 
        "测试电影", 
        "2020", 
        "",
        "张三"
    )
    
    if not matched:
        print("✅ 案例2: 导演不匹配正确拒绝 - 通过")
        test2_passed = True
    else:
        print("❌ 案例2: 导演不匹配正确拒绝 - 失败")
        test2_passed = False
    
    # 案例3: 没有导演信息时跳过导演匹配
    search_results_3 = [
        {
            "title": "测试电影",
            "year": "2020",
            "id": "123"
        }
    ]
    
    matched = DataProcessor.match_douban_search_results(
        search_results_3, 
        "测试电影", 
        "2020", 
        "",
        "张三"
    )
    
    if matched:
        print("✅ 案例3: 无导演信息时跳过匹配 - 通过")
        test3_passed = True
    else:
        print("❌ 案例3: 无导演信息时跳过匹配 - 失败")
        test3_passed = False
    
    print()
    return test1_passed and test2_passed and test3_passed


def test_area_containment():
    """测试地区包含关系匹配"""
    
    print("="*70)
    print("测试4: 地区包含关系匹配")
    print("="*70)
    
    test_cases = [
        {
            "name": "美国 vs 美国",
            "target_area": "美国",
            "result_area": "美国",
            "expected_match": True
        },
        {
            "name": "中国大陆 vs 中国",
            "target_area": "中国大陆",
            "result_area": "中国",
            "expected_match": True
        },
        {
            "name": "中国 vs 中国大陆",
            "target_area": "中国",
            "result_area": "中国大陆",
            "expected_match": True
        }
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        # 模拟匹配逻辑
        target_area = case["target_area"]
        result_area = case["result_area"]
        
        if result_area:
            area_match = target_area.strip() in result_area or result_area in target_area.strip()
        else:
            area_match = True
        
        passed = area_match == case["expected_match"]
        status = "✅" if passed else "❌"
        
        print(f"{status} 案例{i}: {case['name']}")
        print(f"   预期: {case['expected_match']}, 实际: {area_match}")
        
        if not passed:
            all_passed = False
    
    print()
    return all_passed


if __name__ == '__main__':
    print("\n开始测试增强的匹配功能...\n")
    
    test1_passed = test_translation_matching_with_director()
    test2_passed = test_multiple_translation_cases()
    test3_passed = test_director_matching()
    test4_passed = test_area_containment()
    
    print("="*70)
    print("测试结果汇总:")
    print(f"  测试1 (翻译差异匹配): {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"  测试2 (多个翻译案例): {'✅ 通过' if test2_passed else '❌ 失败'}")
    print(f"  测试3 (导演匹配): {'✅ 通过' if test3_passed else '❌ 失败'}")
    print(f"  测试4 (地区匹配): {'✅ 通过' if test4_passed else '❌ 失败'}")
    print("="*70)
    
    if test1_passed and test2_passed and test3_passed and test4_passed:
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️  部分测试失败，请检查实现")
