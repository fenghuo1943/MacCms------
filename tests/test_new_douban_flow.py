"""
测试新的豆瓣API流程：搜索 -> Subject详情
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.api_client import ApiClient
from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.config import logger


def test_new_douban_flow():
    """测试新的豆瓣API流程"""
    logger.info("=" * 70)
    logger.info("开始测试新的豆瓣API流程")
    logger.info("=" * 70)
    
    # 初始化API客户端
    api_client = ApiClient(use_proxy=False)
    
    # 测试视频
    test_videos = [
        {'name': '爱情公寓', 'year': '2009'},
        {'name': 'The Drama', 'year': '2026'},
    ]
    
    for video in test_videos:
        logger.info(f"\n{'='*70}")
        logger.info(f"测试视频: {video['name']} ({video['year']})")
        logger.info("=" * 70)
        
        # 步骤1: 使用豆瓣搜索API
        logger.info(f"\n步骤1: 使用豆瓣搜索API搜索 '{video['name']}'")
        search_results = api_client.search_douban(video['name'])
        
        if not search_results:
            logger.error("豆瓣搜索失败或无结果")
            continue
        
        logger.info(f"找到 {len(search_results)} 个搜索结果")
        
        # 打印前几个结果
        for i, result in enumerate(search_results[:3]):
            title = result.get('title', '')
            year = result.get('year', '')
            douban_id = result.get('id', '')
            logger.info(f"  {i+1}. {title} ({year}) - ID: {douban_id}")
        
        # 步骤2: 匹配视频
        logger.info(f"\n步骤2: 匹配目标视频")
        matched = DataProcessor.match_douban_search_results(
            search_results, 
            video['name'], 
            video['year']
        )
        
        if matched == 'multiple':
            logger.warning("匹配到多个结果")
            continue
        elif matched is None:
            logger.warning("未找到匹配的视频")
            continue
        
        logger.info(f"✓ 匹配成功")
        logger.info(f"  标题: {matched.get('title', '')}")
        logger.info(f"  年份: {matched.get('year', '')}")
        logger.info(f"  豆瓣ID: {matched.get('id', '')}")
        
        # 步骤3: 使用Subject API获取详细信息
        douban_id = matched.get('id', '')
        logger.info(f"\n步骤3: 通过豆瓣ID {douban_id} 获取详细信息")
        
        subject_data = api_client.get_douban_subject(douban_id)
        
        if not subject_data:
            logger.error("获取Subject详情失败")
            continue
        
        logger.info("✓ 成功获取Subject详情")
        
        # 步骤4: 提取信息
        logger.info(f"\n步骤4: 提取详细信息")
        info = DataProcessor.extract_douban_subject_info(subject_data)
        
        logger.info(f"  豆瓣ID: {info.get('doubanId', 'N/A')}")
        logger.info(f"  标题: {info.get('title', 'N/A')}")
        logger.info(f"  原标题: {info.get('originalTitle', 'N/A')}")
        logger.info(f"  年份: {info.get('year', 'N/A')}")
        logger.info(f"  豆瓣评分: {info.get('doubanRating', 'N/A')}")
        logger.info(f"  评分人数: {info.get('doubanVotes', 'N/A')}")
        logger.info(f"  类型: {info.get('tags', 'N/A')}")
        logger.info(f"  导演: {info.get('directors', 'N/A')}")
        logger.info(f"  别名: {info.get('alias', 'N/A')}")
        logger.info(f"  国家: {info.get('country', 'N/A')}")
        logger.info(f"  子类型: {info.get('subtype', 'N/A')}")
        
        if info.get('episodes_count'):
            logger.info(f"  集数: {info.get('episodes_count', 'N/A')}")
        if info.get('seasons_count'):
            logger.info(f"  季数: {info.get('seasons_count', 'N/A')}")
        if info.get('current_season'):
            logger.info(f"  当前季: {info.get('current_season', 'N/A')}")
        
        logger.info(f"\n  简介 (前100字符): {info.get('description', 'N/A')[:100]}...")
        
        logger.info("\n" + "=" * 70)
        logger.info("✓ 测试完成！")
        logger.info("=" * 70)


if __name__ == '__main__':
    try:
        test_new_douban_flow()
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
        sys.exit(1)
