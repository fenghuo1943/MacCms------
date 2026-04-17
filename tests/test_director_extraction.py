"""
测试导演信息提取和匹配
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from douban_fetcher.data_processor import DataProcessor


def test_director_extraction_from_api():
    """测试从API返回的数据中提取导演信息"""
    
    print("="*70)
    print("测试: 从API返回数据中提取导演信息")
    print("="*70)
    
    # 模拟豆瓣搜索API返回的数据（包含完整的导演信息）
    search_results = [
        {
            "title": "大觉醒",
            "year": "2026",
            "id": "37940320",
            "rating": {"max": 10, "average": 0, "stars": "00", "min": 0},
            "genres": ["剧情", "历史"],
            "directors": [
                {
                    "alt": "https://movie.douban.com/celebrity/1481884/",
                    "avatars": {
                        "small": "https://img1.doubanio.com/view/personage/m/public/7d9c6ecea6c1b1f5a48d519d87824c80.jpg",
                        "large": "https://img1.doubanio.com/view/personage/m/public/7d9c6ecea6c1b1f5a48d519d87824c80.jpg",
                        "medium": "https://img1.doubanio.com/view/personage/m/public/7d9c6ecea6c1b1f5a48d519d87824c80.jpg"
                    },
                    "name": "约书亚·恩克",
                    "id": "1481884"
                }
            ],
            "casts": [
                {
                    "alt": None,
                    "avatars": None,
                    "name": "John Paul Sneed",
                    "id": None
                }
            ],
            "collect_count": 11,
            "original_title": "A Great Awakening",
            "subtype": "movie",
            "images": {
                "small": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2928328867.jpg",
                "large": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2928328867.jpg",
                "medium": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2928328867.jpg"
            },
            "alt": "https://movie.douban.com/subject/37940320/",
            "countries": ["美国"]
        }
    ]
    
    # 测试导演匹配
    target_director = "约书亚·恩克"
    result = search_results[0]
    
    # 检查是否能正确提取导演信息
    if 'directors' in result and isinstance(result['directors'], list):
        result_directors = [d.get('name', '') for d in result['directors'] if d.get('name')]
        print(f"✅ 成功提取导演信息: {result_directors}")
        
        # 测试导演匹配
        director_match = any(target_director.strip() in director or director in target_director.strip() 
                           for director in result_directors)
        
        if director_match:
            print(f"✅ 导演匹配成功: '{target_director}' 匹配到 '{result_directors[0]}'")
            test_passed = True
        else:
            print(f"❌ 导演匹配失败: '{target_director}' 无法匹配到 {result_directors}")
            test_passed = False
    else:
        print("❌ 未能从结果中提取导演信息")
        test_passed = False
    
    print()
    return test_passed


def test_full_matching_with_director():
    """测试完整的匹配流程（包含导演信息）"""
    
    print("="*70)
    print("测试: 完整匹配流程（包含导演信息）")
    print("="*70)
    
    # 模拟豆瓣搜索API返回的数据
    search_results = [
        {
            "title": "大觉醒",
            "year": "2026",
            "id": "37940320",
            "directors": [
                {
                    "alt": "https://movie.douban.com/celebrity/1481884/",
                    "avatars": {
                        "small": "https://img1.doubanio.com/view/personage/m/public/7d9c6ecea6c1b1f5a48d519d87824c80.jpg",
                        "large": "https://img1.doubanio.com/view/personage/m/public/7d9c6ecea6c1b1f5a48d519d87824c80.jpg",
                        "medium": "https://img1.doubanio.com/view/personage/m/public/7d9c6ecea6c1b1f5a48d519d87824c80.jpg"
                    },
                    "name": "约书亚·恩克",
                    "id": "1481884"
                }
            ],
            "countries": ["美国"]
        }
    ]
    
    # 测试完整匹配
    matched = DataProcessor.match_douban_search_results(
        search_results,
        target_name="伟大的觉醒",
        target_year="2026",
        target_area="美国",
        target_director="约书亚·恩克"
    )
    
    if matched:
        print(f"✅ 匹配成功!")
        print(f"   标题: {matched.get('title')}")
        print(f"   ID: {matched.get('id')}")
        print(f"   年份: {matched.get('year')}")
        
        # 检查导演信息
        if 'directors' in matched:
            directors = [d.get('name', '') for d in matched['directors'] if d.get('name')]
            print(f"   导演: {directors}")
        
        test_passed = True
    else:
        print("❌ 匹配失败")
        test_passed = False
    
    print()
    return test_passed


if __name__ == '__main__':
    print("\n开始测试导演信息提取和匹配...\n")
    
    test1_passed = test_director_extraction_from_api()
    test2_passed = test_full_matching_with_director()
    
    print("="*70)
    print("测试结果汇总:")
    print(f"  测试1 (导演信息提取): {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"  测试2 (完整匹配): {'✅ 通过' if test2_passed else '❌ 失败'}")
    print("="*70)
    
    if all([test1_passed, test2_passed]):
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️  部分测试失败，请检查实现")
