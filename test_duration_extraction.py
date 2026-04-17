"""
测试片长提取功能
"""
from selenium_fetcher.extractor import DoubanPageExtractor


def test_episode_duration():
    """测试单集片长提取（电视剧）"""
    html = '''
    <div id="info">
        <span class="pl">单集片长:</span> 45分钟<br>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试1: 单集片长（电视剧）")
    print(f"  片长: {info.get('duration')} 分钟")
    assert info['duration'] == 45, f"应该是45分钟，实际是{info['duration']}"
    print("  ✓ 通过\n")


def test_movie_runtime():
    """测试电影片长提取"""
    html = '''
    <div id="info">
        <span property="v:runtime" content="103">103分钟</span>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试2: 电影片长")
    print(f"  片长: {info.get('duration')} 分钟")
    assert info['duration'] == 103, f"应该是103分钟，实际是{info['duration']}"
    print("  ✓ 通过\n")


def test_priority_episode_duration():
    """测试优先级：单集片长优先于电影片长"""
    html = '''
    <div id="info">
        <span class="pl">单集片长:</span> 30分钟<br>
        <span property="v:runtime" content="120">120分钟</span>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试3: 优先级测试（单集片长优先）")
    print(f"  片长: {info.get('duration')} 分钟")
    assert info['duration'] == 30, f"应该优先使用单集片长30分钟，实际是{info['duration']}"
    print("  ✓ 通过\n")


def test_no_duration():
    """测试没有片长信息"""
    html = '''
    <div id="info">
        <span class="pl">导演:</span> 张三
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试4: 没有片长信息")
    print(f"  片长: {info.get('duration')} 分钟")
    assert info['duration'] == 0, f"没有片长应该返回0，实际是{info['duration']}"
    print("  ✓ 通过\n")


def test_duration_with_text():
    """测试带文本的片长"""
    html = '''
    <div id="info">
        <span class="pl">单集片长:</span> 2分钟<br>
    </div>
    '''
    
    extractor = DoubanPageExtractor()
    info = extractor.extract_movie_info(html)
    
    print("测试5: 短时长（2分钟）")
    print(f"  片长: {info.get('duration')} 分钟")
    assert info['duration'] == 2, f"应该是2分钟，实际是{info['duration']}"
    print("  ✓ 通过\n")


if __name__ == '__main__':
    print("="*70)
    print("片长提取功能测试")
    print("="*70)
    print()
    
    try:
        test_episode_duration()
        test_movie_runtime()
        test_priority_episode_duration()
        test_no_duration()
        test_duration_with_text()
        
        print("="*70)
        print("✅ 所有测试通过！")
        print("="*70)
    except Exception as e:
        print("="*70)
        print(f"❌ 测试失败: {str(e)}")
        print("="*70)
        import traceback
        traceback.print_exc()
