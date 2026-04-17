"""
测试视频名称空格匹配优化
"""
import sys
sys.path.insert(0, 'e:/python/MacCms自动获取评分')

from douban_fetcher.data_processor import DataProcessor

def test_name_normalization():
    """测试名称标准化功能"""
    print("=" * 70)
    print("测试名称标准化功能")
    print("=" * 70)
    
    test_cases = [
        ("博斯第二季", "博斯 第二季"),
        ("权力的游戏 第一季", "权力的游戏第一季"),
        ("绝命毒师  第五季", "绝命毒师第五季"),  # 多个空格
        ("黑客帝国", "黑客帝国"),  # 无空格
        ("  西部世界  第一季  ", "西部世界第一季"),  # 首尾空格+中间空格
    ]
    
    for target, api_result in test_cases:
        normalized_target = DataProcessor.normalize_name(target)
        normalized_api = DataProcessor.normalize_name(api_result)
        match = normalized_target == normalized_api
        
        print(f"\n原始: '{target}' vs '{api_result}'")
        print(f"标准化: '{normalized_target}' vs '{normalized_api}'")
        print(f"匹配结果: {'✓ 匹配' if match else '✗ 不匹配'}")

def test_match_with_spaces():
    """测试带空格的名称匹配"""
    print("\n" + "=" * 70)
    print("测试带空格的名称匹配")
    print("=" * 70)
    
    # 模拟搜索结果
    search_results = [
        {
            'id': '12345',
            'title': '博斯 第二季',
            'year': '2016',
            'country': '美国'
        },
        {
            'id': '67890',
            'title': '博斯第三季',
            'year': '2017',
            'country': '美国'
        }
    ]
    
    # 测试1: 数据库名称无空格，API结果有空格
    print("\n测试1 - 数据库:'博斯第二季' vs API:'博斯 第二季'")
    result = DataProcessor.match_douban_search_results(
        search_results, 
        '博斯第二季',  # 数据库中无空格
        '2016',
        ''
    )
    if result and result.get('id') == '12345':
        print("  ✓ 成功匹配到正确结果")
        print(f"  匹配ID: {result['id']}, 标题: {result['title']}")
    else:
        print("  ✗ 匹配失败")
    
    # 测试2: 数据库名称有空格，API结果无空格
    print("\n测试2 - 数据库:'权力的游戏 第一季' vs API:'权力的游戏第一季'")
    search_results2 = [
        {
            'id': '11111',
            'title': '权力的游戏第一季',
            'year': '2011',
            'country': '美国'
        }
    ]
    result = DataProcessor.match_douban_search_results(
        search_results2, 
        '权力的游戏 第一季',  # 数据库中有空格
        '2011',
        ''
    )
    if result and result.get('id') == '11111':
        print("  ✓ 成功匹配到正确结果")
        print(f"  匹配ID: {result['id']}, 标题: {result['title']}")
    else:
        print("  ✗ 匹配失败")
    
    # 测试3: 确保不会错误匹配不同剧集
    print("\n测试3 - 确保不会错误匹配不同季")
    result = DataProcessor.match_douban_search_results(
        search_results, 
        '博斯第二季',
        '2016',
        ''
    )
    if result and result.get('id') == '12345':
        print("  ✓ 正确匹配第二季（不是第三季）")
    else:
        print("  ✗ 匹配错误")

def test_edge_cases():
    """测试边界情况"""
    print("\n" + "=" * 70)
    print("测试边界情况")
    print("=" * 70)
    
    # 测试多个连续空格
    print("\n测试多个连续空格:")
    name1 = "绝命毒师    第五季"  # 4个空格
    name2 = "绝命毒师第五季"
    normalized1 = DataProcessor.normalize_name(name1)
    normalized2 = DataProcessor.normalize_name(name2)
    print(f"  '{name1}' -> '{normalized1}'")
    print(f"  '{name2}' -> '{normalized2}'")
    print(f"  匹配: {'✓' if normalized1 == normalized2 else '✗'}")
    
    # 测试制表符和换行符
    print("\n测试制表符和换行符:")
    name3 = "西部世界\t第一季"  # 制表符
    name4 = "西部世界\n第一季"  # 换行符
    name5 = "西部世界第一季"
    normalized3 = DataProcessor.normalize_name(name3)
    normalized4 = DataProcessor.normalize_name(name4)
    normalized5 = DataProcessor.normalize_name(name5)
    print(f"  制表符: '{name3}' -> '{normalized3}'")
    print(f"  换行符: '{name4}' -> '{normalized4}'")
    print(f"  正常: '{name5}' -> '{normalized5}'")
    print(f"  三者相同: {'✓' if normalized3 == normalized4 == normalized5 else '✗'}")

if __name__ == '__main__':
    test_name_normalization()
    test_match_with_spaces()
    test_edge_cases()
    print("\n" + "=" * 70)
    print("所有测试完成！")
    print("=" * 70)
