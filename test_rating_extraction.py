"""
测试评分提取的容错处理
"""
from selenium_fetcher.extractor import DoubanPageExtractor


def test_empty_rating():
    """测试空评分的情况"""
    html = '''
    <div class="rating_self clearfix" typeof="v:Rating">
        <strong class="ll rating_num" property="v:average"></strong>
        <span property="v:best" content="10.0"></span>
        <div class="rating_right not_showed">
            <div class="ll bigstar bigstar00"></div>
            <div class="rating_sum">暂无评分</div>
        </div>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试1: 空评分")
    print(f"  评分: {info.get('rating')}")
    print(f"  评分人数: {info.get('votes')}")
    assert info['rating'] == 0.0, "空评分应该返回0.0"
    assert info['votes'] == 0, "空评分人数应该返回0"
    print("  ✓ 通过\n")


def test_valid_rating():
    """测试正常评分"""
    html = '''
    <div class="rating_self clearfix" typeof="v:Rating">
        <strong class="ll rating_num" property="v:average">8.5</strong>
        <span property="v:best" content="10.0"></span>
        <div class="rating_right">
            <div class="ll bigstar bigstar45"></div>
            <div class="rating_sum">
                <span property="v:votes">12345</span>人评价
            </div>
        </div>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试2: 正常评分")
    print(f"  评分: {info.get('rating')}")
    print(f"  评分人数: {info.get('votes')}")
    assert info['rating'] == 8.5, f"评分应该是8.5，实际是{info['rating']}"
    assert info['votes'] == 12345, f"评分人数应该是12345，实际是{info['votes']}"
    print("  ✓ 通过\n")


def test_no_rating_tag():
    """测试没有评分标签"""
    html = '''
    <div class="rating_self clearfix" typeof="v:Rating">
        <div class="rating_right">
            <div class="rating_sum">暂无评分</div>
        </div>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试3: 没有评分标签")
    print(f"  评分: {info.get('rating')}")
    print(f"  评分人数: {info.get('votes')}")
    assert info['rating'] == 0.0, "没有评分标签应该返回0.0"
    assert info['votes'] == 0, "没有评分人数标签应该返回0"
    print("  ✓ 通过\n")


if __name__ == '__main__':
    print("="*70)
    print("评分提取容错测试")
    print("="*70)
    print()
    
    try:
        test_empty_rating()
        test_valid_rating()
        test_no_rating_tag()
        
        print("="*70)
        print("✅ 所有测试通过！")
        print("="*70)
    except Exception as e:
        print("="*70)
        print(f"❌ 测试失败: {str(e)}")
        print("="*70)
        import traceback
        traceback.print_exc()
