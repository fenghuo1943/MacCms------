"""
测试地区别名匹配功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from douban_fetcher.data_processor import DataProcessor


def test_normalize_area():
    """测试地区标准化功能"""
    print("=" * 70)
    print("测试1：地区标准化功能")
    print("=" * 70)
    
    test_cases = [
        ('大陆', '中国大陆'),
        ('中国', '中国大陆'),
        ('内地', '中国大陆'),
        ('CN', '中国大陆'),
        ('中国大陆', '中国大陆'),  # 已经是标准形式
        ('USA', '美国'),
        ('US', '美国'),
        ('United States', '美国'),
        ('美国', '美国'),
        ('UK', '英国'),
        ('Britain', '英国'),
        ('台湾', '中国台湾'),
        ('Taiwan', '中国台湾'),
        ('香港', '中国香港'),
        ('Hong Kong', '中国香港'),
        ('日本', '日本'),  # 没有别名，保持不变
        ('韩国', '韩国'),
    ]
    
    print("\n测试地区标准化映射：\n")
    all_passed = True
    
    for input_area, expected in test_cases:
        result = DataProcessor._normalize_area(input_area)
        passed = result == expected
        status = "✓" if passed else "✗"
        
        if not passed:
            all_passed = False
        
        print(f"  {status} '{input_area}' → '{result}' (期望: '{expected}')")
    
    print(f"\n{'='*70}")
    if all_passed:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败")
    print("=" * 70)
    
    return all_passed


def test_area_match_with_aliases():
    """测试地区匹配（支持别名）"""
    print("\n" + "=" * 70)
    print("测试2：地区匹配功能（支持别名）")
    print("=" * 70)
    
    test_cases = [
        # (目标地区, 结果地区, 期望结果, 说明)
        ('大陆', '中国大陆', True, '大陆 → 中国大陆'),
        ('中国大陆', '大陆', True, '中国大陆 → 大陆'),
        ('中国', '中国大陆', True, '中国 → 中国大陆'),
        ('内地', '中国大陆', True, '内地 → 中国大陆'),
        ('CN', '中国大陆', True, 'CN → 中国大陆'),
        ('中国大陆', '中国大陆', True, '中国大陆 → 中国大陆（精确匹配）'),
        ('USA', '美国', True, 'USA → 美国'),
        ('US', '美国', True, 'US → 美国'),
        ('United States', '美国', True, 'United States → 美国'),
        ('台湾', '中国台湾', True, '台湾 → 中国台湾'),
        ('Taiwan', '中国台湾', True, 'Taiwan → 中国台湾'),
        ('香港', '中国香港', True, '香港 → 中国香港'),
        ('Hong Kong', '中国香港', True, 'Hong Kong → 中国香港'),
        ('日本', '日本', True, '日本 → 日本（无别名）'),
        ('韩国', '韩国', True, '韩国 → 韩国（无别名）'),
        ('美国', '日本', False, '美国 → 日本（不匹配）'),
        ('大陆', '美国', False, '大陆 → 美国（不匹配）'),
    ]
    
    print("\n测试地区匹配：\n")
    all_passed = True
    
    for target_area, result_area, expected, description in test_cases:
        # 构造模拟的搜索结果
        result = {'country': result_area}
        
        match_result = DataProcessor._check_area_match(target_area, result)
        passed = match_result == expected
        status = "✓" if passed else "✗"
        
        if not passed:
            all_passed = False
        
        print(f"  {status} {description:30s} → {match_result} (期望: {expected})")
    
    print(f"\n{'='*70}")
    if all_passed:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败")
    print("=" * 70)
    
    return all_passed


def test_area_match_with_multiple_countries():
    """测试多国家/地区的匹配"""
    print("\n" + "=" * 70)
    print("测试3：多国家/地区匹配")
    print("=" * 70)
    
    # 模拟二次确认中的多国家情况
    test_cases = [
        # (目标地区, 国家列表, 期望结果, 说明)
        ('大陆', ['中国大陆', '美国'], True, '大陆在[中国大陆, 美国]中'),
        ('中国', ['美国', '中国大陆'], True, '中国在[美国, 中国大陆]中'),
        ('美国', ['中国大陆', '美国'], True, '美国在[中国大陆, 美国]中'),
        ('日本', ['中国大陆', '美国'], False, '日本不在[中国大陆, 美国]中'),
        ('台湾', ['中国台湾', '日本'], True, '台湾在[中国台湾, 日本]中'),
        ('香港', ['中国大陆', '中国香港'], True, '香港在[中国大陆, 中国香港]中'),
    ]
    
    print("\n测试多国家匹配：\n")
    all_passed = True
    
    for target_area, countries, expected, description in test_cases:
        # 模拟二次确认中的匹配逻辑
        normalized_target = DataProcessor._normalize_area(target_area)
        area_match = False
        
        for country in countries:
            normalized_country = DataProcessor._normalize_area(country)
            
            # 1. 精确匹配（标准化后）
            if normalized_target == normalized_country:
                area_match = True
                break
            
            # 2. 包含关系匹配（原始值）
            if target_area.strip() in country or country in target_area.strip():
                area_match = True
                break
            
            # 3. 标准化后的包含关系
            if normalized_target in normalized_country or normalized_country in normalized_target:
                area_match = True
                break
        
        passed = area_match == expected
        status = "✓" if passed else "✗"
        
        if not passed:
            all_passed = False
        
        countries_str = ', '.join(countries)
        print(f"  {status} {description:40s} → {area_match} (期望: {expected})")
    
    print(f"\n{'='*70}")
    if all_passed:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败")
    print("=" * 70)
    
    return all_passed


def test_real_world_scenarios():
    """测试真实场景"""
    print("\n" + "=" * 70)
    print("测试4：真实场景测试")
    print("=" * 70)
    
    scenarios = [
        {
            'name': '流浪地球（中国大陆电影）',
            'target_area': '大陆',
            'result': {'country': '中国大陆'},
            'expected': True
        },
        {
            'name': '复仇者联盟（美国电影）',
            'target_area': 'USA',
            'result': {'country': '美国'},
            'expected': True
        },
        {
            'name': '寄生虫（韩国电影）',
            'target_area': 'Korea',
            'result': {'country': '韩国'},
            'expected': True
        },
        {
            'name': '你的名字（日本动画）',
            'target_area': '日本',
            'result': {'country': 'Japan'},
            'expected': True
        },
        {
            'name': '中美合拍片',
            'target_area': '大陆',
            'result': {'country': '中国大陆, 美国'},
            'expected': True
        },
    ]
    
    print("\n测试真实场景：\n")
    all_passed = True
    
    for scenario in scenarios:
        match_result = DataProcessor._check_area_match(
            scenario['target_area'], 
            scenario['result']
        )
        passed = match_result == scenario['expected']
        status = "✓" if passed else "✗"
        
        if not passed:
            all_passed = False
        
        print(f"  {status} {scenario['name']:30s}")
        print(f"      目标: '{scenario['target_area']}' vs 结果: '{scenario['result']['country']}'")
        print(f"      结果: {match_result} (期望: {scenario['expected']})")
        print()
    
    print(f"{'='*70}")
    if all_passed:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败")
    print("=" * 70)
    
    return all_passed


if __name__ == '__main__':
    try:
        results = []
        
        # 运行所有测试
        results.append(("地区标准化", test_normalize_area()))
        results.append(("地区匹配", test_area_match_with_aliases()))
        results.append(("多国家匹配", test_area_match_with_multiple_countries()))
        results.append(("真实场景", test_real_world_scenarios()))
        
        # 总结
        print("\n" + "=" * 70)
        print("测试总结")
        print("=" * 70)
        
        for test_name, passed in results:
            status = "✓ 通过" if passed else "✗ 失败"
            print(f"  {status} - {test_name}")
        
        all_passed = all(result[1] for result in results)
        
        print(f"\n{'='*70}")
        if all_passed:
            print("🎉 所有测试全部通过！")
        else:
            print("⚠️  部分测试失败，请检查")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
