"""
测试数据库更新字段过滤功能
"""


def test_filter_empty_values():
    """测试过滤空值"""
    
    # 模拟原始数据
    info = {
        'doubanRating': 8.5,
        'doubanVotes': 12345,
        'doubanDirector': '张三',
        'doubanWriter': '',  # 空字符串，应该被过滤
        'doubanCast': '',    # 空字符串，应该被过滤
        'doubanGenre': '剧情,爱情',
        'doubanCountry': '',  # 空字符串，应该被过滤
        'doubanLanguage': '汉语',
        'doubanReleaseDate': '',
        'doubanEpisodes': 0,  # 0，应该被过滤
        'doubanDuration': 45,
        'doubanSummary': '',
        'imdb_id': '',
    }
    
    # 执行过滤
    filtered_info = {
        key: value for key, value in info.items()
        if value != 0 and value != 0.0 and value != '' and value is not None
    }
    
    print("原始数据:")
    for key, value in info.items():
        print(f"  {key}: {repr(value)}")
    
    print("\n过滤后的数据:")
    for key, value in filtered_info.items():
        print(f"  {key}: {repr(value)}")
    
    print("\n被过滤的字段:")
    filtered_out = set(info.keys()) - set(filtered_info.keys())
    for key in filtered_out:
        print(f"  {key}: {repr(info[key])}")
    
    # 验证结果
    assert 'doubanWriter' not in filtered_info, "空字符串应该被过滤"
    assert 'doubanCast' not in filtered_info, "空字符串应该被过滤"
    assert 'doubanCountry' not in filtered_info, "空字符串应该被过滤"
    assert 'doubanEpisodes' not in filtered_info, "0应该被过滤"
    assert 'doubanReleaseDate' not in filtered_info, "空字符串应该被过滤"
    assert 'doubanSummary' not in filtered_info, "空字符串应该被过滤"
    assert 'imdb_id' not in filtered_info, "空字符串应该被过滤"
    
    # 验证保留的字段
    assert 'doubanRating' in filtered_info, "非零数字应该保留"
    assert 'doubanVotes' in filtered_info, "非零数字应该保留"
    assert 'doubanDirector' in filtered_info, "非空字符串应该保留"
    assert 'doubanGenre' in filtered_info, "非空字符串应该保留"
    assert 'doubanLanguage' in filtered_info, "非空字符串应该保留"
    assert 'doubanDuration' in filtered_info, "非零数字应该保留"
    
    print("\n✅ 所有验证通过！")
    print(f"\n原始字段数: {len(info)}")
    print(f"过滤后字段数: {len(filtered_info)}")
    print(f"被过滤字段数: {len(filtered_out)}")


def test_all_empty():
    """测试所有字段都为空的情况"""
    
    info = {
        'doubanRating': 0.0,
        'doubanVotes': 0,
        'doubanDirector': '',
        'doubanWriter': '',
    }
    
    filtered_info = {
        key: value for key, value in info.items()
        if value != 0 and value != 0.0 and value != '' and value is not None
    }
    
    print("\n测试所有字段为空:")
    print(f"  原始字段数: {len(info)}")
    print(f"  过滤后字段数: {len(filtered_info)}")
    
    assert len(filtered_info) == 0, "所有字段为空时应该返回空字典"
    print("  ✓ 通过")


def test_none_values():
    """测试None值的过滤"""
    
    info = {
        'doubanRating': 8.5,
        'doubanDirector': None,
        'doubanWriter': '李四',
    }
    
    filtered_info = {
        key: value for key, value in info.items()
        if value != 0 and value != 0.0 and value != '' and value is not None
    }
    
    print("\n测试None值过滤:")
    print(f"  过滤后: {list(filtered_info.keys())}")
    
    assert 'doubanDirector' not in filtered_info, "None应该被过滤"
    assert 'doubanRating' in filtered_info, "非零数字应该保留"
    assert 'doubanWriter' in filtered_info, "非空字符串应该保留"
    print("  ✓ 通过")


if __name__ == '__main__':
    print("="*70)
    print("数据库更新字段过滤测试")
    print("="*70)
    print()
    
    try:
        test_filter_empty_values()
        test_all_empty()
        test_none_values()
        
        print("\n" + "="*70)
        print("✅ 所有测试通过！")
        print("="*70)
    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ 测试失败: {str(e)}")
        print("="*70)
        import traceback
        traceback.print_exc()
