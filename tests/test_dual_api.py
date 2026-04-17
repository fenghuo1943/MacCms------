"""
测试双API获取功能
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.api_client import ApiClient
from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.config import logger


def test_dual_api():
    """测试双API获取流程"""
    logger.info("=" * 70)
    logger.info("开始测试双API获取功能")
    logger.info("=" * 70)
    
    # 初始化API客户端（不使用代理）
    api_client = ApiClient(use_proxy=False)
    
    # 测试视频名称
    test_video_name = "The Drama"
    test_year = "2026"
    
    logger.info(f"\n步骤1: 使用WMDB API搜索视频: {test_video_name} ({test_year})")
    
    # 1. 使用WMDB API搜索
    search_results = api_client.search_video(test_video_name)
    
    if not search_results:
        logger.error("WMDB API搜索失败或无结果")
        return
    
    logger.info(f"找到 {len(search_results)} 个搜索结果")
    
    # 打印搜索结果详情用于调试
    for i, result in enumerate(search_results):
        logger.info(f"  结果{i+1}: name={result.get('originalName', '')}, year={result.get('year', '')}")
        if 'data' in result and isinstance(result['data'], list) and len(result['data']) > 0:
            first_data = result['data'][0]
            if isinstance(first_data, dict):
                logger.info(f"    data[0].name={first_data.get('name', '')}")
    
    # 2. 匹配视频
    matched = DataProcessor.match_video(search_results, test_video_name, test_year)
    
    if matched == 'multiple':
        logger.warning("匹配到多个结果")
        return
    elif matched is None:
        logger.warning("未找到匹配的视频")
        return
    
    logger.info(f"✓ 成功匹配视频")
    
    # 3. 提取WMDB信息
    wmdb_info = DataProcessor.extract_video_info(matched)
    logger.info(f"\n步骤2: 从WMDB API提取的信息:")
    logger.info(f"  IMDB ID: {wmdb_info['imdbId']}")
    logger.info(f"  豆瓣评分: {wmdb_info['doubanRating']} ({wmdb_info['doubanVotes']}人)")
    logger.info(f"  IMDB评分: {wmdb_info['imdbRating']} ({wmdb_info['imdbVotes']}人)")
    logger.info(f"  年份: {wmdb_info['year']}")
    logger.info(f"  类型: {wmdb_info['type']}")
    logger.info(f"  时长: {wmdb_info['duration']}秒")
    logger.info(f"  上映日期: {wmdb_info['dateReleased']}")
    logger.info(f"  国家: {wmdb_info['country']}")
    logger.info(f"  语言: {wmdb_info['language']}")
    logger.info(f"  描述: {wmdb_info['description'][:50]}...")
    
    # 4. 使用豆瓣API获取更多信息
    imdb_id = wmdb_info.get('imdbId', '')
    if not imdb_id:
        logger.warning("\n没有IMDB ID，无法调用豆瓣API")
        return
    
    logger.info(f"\n步骤3: 使用豆瓣API通过IMDB ID获取信息: {imdb_id}")
    
    douban_data = api_client.get_douban_by_imdb(imdb_id)
    
    if not douban_data:
        logger.warning("豆瓣API获取失败")
        logger.info("\n最终信息（仅WMDB）:")
        for key, value in wmdb_info.items():
            if value:
                logger.info(f"  {key}: {value}")
        return
    
    logger.info(f"✓ 成功从豆瓣API获取数据")
    
    # 5. 提取豆瓣信息
    douban_info = DataProcessor.extract_douban_info(douban_data)
    logger.info(f"\n步骤4: 从豆瓣API提取的信息:")
    logger.info(f"  豆瓣评分: {douban_info.get('doubanRating', 0)} ({douban_info.get('doubanVotes', 0)}人)")
    logger.info(f"  标签: {douban_info.get('tags', '')}")
    
    # 6. 合并信息
    merged_info = DataProcessor.merge_video_info(wmdb_info, douban_info)
    
    logger.info(f"\n步骤5: 合并后的最终信息:")
    logger.info("-" * 70)
    for key, value in merged_info.items():
        if value:
            # 对长文本进行截断
            if isinstance(value, str) and len(value) > 100:
                value = value[:100] + "..."
            logger.info(f"  {key}: {value}")
    
    logger.info("\n" + "=" * 70)
    logger.info("✓ 双API测试完成！")
    logger.info("=" * 70)
    
    # 验证关键字段
    logger.info("\n关键字段验证:")
    logger.info(f"  ✓ dateReleased: {merged_info.get('dateReleased', 'N/A')}")
    logger.info(f"  ✓ episodes: {merged_info.get('episodes', 'N/A')}")
    logger.info(f"  ✓ duration: {merged_info.get('duration', 'N/A')}")
    logger.info(f"  ✓ description: {'有' if merged_info.get('description') else '无'}")
    logger.info(f"  ✓ country: {merged_info.get('country', 'N/A')}")
    logger.info(f"  ✓ language: {merged_info.get('language', 'N/A')}")
    logger.info(f"  ✓ writers: {merged_info.get('writers', 'N/A')}")
    logger.info(f"  ✓ doubanRating (from Douban API): {merged_info.get('doubanRating', 'N/A')}")
    logger.info(f"  ✓ doubanVotes (from Douban API): {merged_info.get('doubanVotes', 'N/A')}")
    logger.info(f"  ✓ tags (from Douban API): {'有' if merged_info.get('tags') else '无'}")


if __name__ == '__main__':
    try:
        test_dual_api()
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
        sys.exit(1)
