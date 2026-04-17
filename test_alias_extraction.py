"""
测试别名提取功能
"""
from selenium_fetcher.extractor import DoubanPageExtractor


def test_alias_extraction():
    """测试别名提取"""
    html = '''
    <div id="info">
        <span class="pl">又名:</span> 爱情公寓-回归季 / 爱情公寓 第三季 / IPARTMENT Season3<br>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试1: 别名提取")
    print(f"  别名: {info.get('alias')}")
    expected = "爱情公寓-回归季 / 爱情公寓 第三季 / IPARTMENT Season3"
    assert info['alias'] == expected, f"应该是 '{expected}'，实际是 '{info['alias']}'"
    print("  ✓ 通过\n")


def test_alias_with_br():
    """测试带br标签的别名"""
    html = '''
    <div id="info">
        <span class="pl">又名:</span> 测试别名1 / 测试别名2<br>
        <span class="pl">导演:</span> 张三
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试2: 带br标签的别名")
    print(f"  别名: {repr(info.get('alias'))}")
    # br标签应该被清理
    assert '<br>' not in info['alias'], "br标签应该被清理"
    assert info['alias'] == "测试别名1 / 测试别名2", f"别名不正确: {info['alias']}"
    print("  ✓ 通过\n")


def test_no_alias():
    """测试没有别名的情况"""
    html = '''
    <div id="info">
        <span class="pl">导演:</span> 张三
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试3: 没有别名")
    print(f"  别名: {repr(info.get('alias'))}")
    assert info['alias'] == '', f"没有别名应该返回空字符串，实际是 '{info['alias']}'"
    print("  ✓ 通过\n")


def test_alias_with_alternative_label():
    """测试使用'别名'标签"""
    html = '''
    <div id="info">
        <span class="pl">别名:</span> 测试别名<br>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试4: 使用'别名'标签")
    print(f"  别名: {info.get('alias')}")
    assert info['alias'] == "测试别名", f"应该是 '测试别名'，实际是 '{info['alias']}'"
    print("  ✓ 通过\n")


if __name__ == '__main__':
    print("="*70)
    print("别名提取功能测试")
    print("="*70)
    print()
    
    try:
        test_alias_extraction()
        test_alias_with_br()
        test_no_alias()
        test_alias_with_alternative_label()
        
        print("="*70)
        print("✅ 所有测试通过！")
        print("="*70)
    except Exception as e:
        print("="*70)
        print(f"❌ 测试失败: {str(e)}")
        print("="*70)
        import traceback
        traceback.print_exc()
