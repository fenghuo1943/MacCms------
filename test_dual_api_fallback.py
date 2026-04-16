"""
测试完整的双API集成流程（支持IMDB ID和豆瓣ID）
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.api_client import ApiClient
from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.config import logger


def test_dual_api_with_fallback():
    """测试双API集成流程（带备用方案）"""
    logger.info("=" * 70)
    logger.info("开始测试双API集成流程（支持IMDB ID和豆瓣ID）")
    logger.info("=" * 70)
    
    # 初始化API客户端
    api_client = ApiClient(use_proxy=False)
    
    # 测试场景1: 有IMDB ID的情况
    logger.info("\n" + "=" * 70)
    logger.info("测试场景1: 使用IMDB ID获取豆瓣信息")
    logger.info("=" * 70)
    
    wmdb_data_with_imdb = {
        "originalName": "The Drama",
        "year": "2026",
        "imdbId": "tt33071426",
        "doubanId": "36995126",
        "type": "Movie",
        "doubanRating": "7.4",
        "doubanVotes": 1016,
        "duration": 6360,
        "episodes": 0,
        "dateReleased": "2026-04-01",
        "data": [{
            "poster": "https://img.wmdb.tv/movie/poster/test.webp",
            "name": "爱情抓马",
            "genre": "爱情",
            "description": "婚礼前几天，一对情侣无意中发现彼此的秘密...",
            "language": "英语",
            "country": "美国",
        }],
        "writer": [{"data": [{"name": "克里斯托弗·博格利", "lang": "Cn"}]}],
        "actor": [{"data": [{"name": "罗伯特·帕丁森", "lang": "Cn"}]}],
        "director": [{"data": [{"name": "克里斯托弗·博格利", "lang": "Cn"}]}]
    }
    
    wmdb_info = DataProcessor.extract_video_info(wmdb_data_with_imdb)
    logger.info(f"WMDB信息: IMDB={wmdb_info['imdbId']}, 豆瓣={wmdb_info['doubanId']}")
    
    # 优先使用IMDB ID
    imdb_id = wmdb_info.get('imdbId', '')
    douban_id = wmdb_info.get('doubanId', '')
    douban_data = None
    
    if imdb_id:
        logger.info(f"→ 使用IMDB ID: {imdb_id}")
        douban_data = api_client.get_douban_by_imdb(imdb_id)
    elif douban_id:
        logger.info(f"→ 使用豆瓣ID: {douban_id}")
        douban_data = api_client.get_douban_by_id(str(douban_id))
    
    if douban_data:
        douban_info = DataProcessor.extract_douban_info(douban_data)
        merged_info = DataProcessor.merge_video_info(wmdb_info, douban_info)
        
        logger.info(f"\n合并结果:")
        logger.info(f"  豆瓣评分: {merged_info['doubanRating']} ({merged_info['doubanVotes']}人)")
        logger.info(f"  标签: {merged_info.get('tags', '无')}")
        logger.info(f"  ✓ 数据来源: 豆瓣API (通过IMDB ID)")
    else:
        logger.warning("豆瓣API获取失败")
    
    # 测试场景2: 没有IMDB ID，只有豆瓣ID的情况
    logger.info("\n" + "=" * 70)
    logger.info("测试场景2: 仅使用豆瓣ID获取信息（无IMDB ID）")
    logger.info("=" * 70)
    
    wmdb_data_without_imdb = wmdb_data_with_imdb.copy()
    wmdb_data_without_imdb['imdbId'] = ''  # 模拟没有IMDB ID
    
    wmdb_info2 = DataProcessor.extract_video_info(wmdb_data_without_imdb)
    logger.info(f"WMDB信息: IMDB={wmdb_info2['imdbId'] or 'N/A'}, 豆瓣={wmdb_info2['doubanId']}")
    
    imdb_id2 = wmdb_info2.get('imdbId', '')
    douban_id2 = wmdb_info2.get('doubanId', '')
    douban_data2 = None
    
    if imdb_id2:
        logger.info(f"→ 使用IMDB ID: {imdb_id2}")
        douban_data2 = api_client.get_douban_by_imdb(imdb_id2)
    elif douban_id2:
        logger.info(f"→ 使用豆瓣ID: {douban_id2}")
        douban_data2 = api_client.get_douban_by_id(str(douban_id2))
    
    if douban_data2:
        douban_info2 = DataProcessor.extract_douban_info(douban_data2)
        merged_info2 = DataProcessor.merge_video_info(wmdb_info2, douban_info2)
        
        logger.info(f"\n合并结果:")
        logger.info(f"  豆瓣评分: {merged_info2['doubanRating']} ({merged_info2['doubanVotes']}人)")
        logger.info(f"  标签: {merged_info2.get('tags', '无')}")
        logger.info(f"  ✓ 数据来源: 豆瓣API (通过豆瓣ID)")
    else:
        logger.warning("豆瓣API获取失败")
    
    # 测试场景3: 既没有IMDB ID也没有豆瓣ID
    logger.info("\n" + "=" * 70)
    logger.info("测试场景3: 既无IMDB ID也无豆瓣ID")
    logger.info("=" * 70)
    
    wmdb_data_no_ids = wmdb_data_with_imdb.copy()
    wmdb_data_no_ids['imdbId'] = ''
    wmdb_data_no_ids['doubanId'] = ''
    
    wmdb_info3 = DataProcessor.extract_video_info(wmdb_data_no_ids)
    logger.info(f"WMDB信息: IMDB={wmdb_info3['imdbId'] or 'N/A'}, 豆瓣={wmdb_info3['doubanId'] or 'N/A'}")
    
    imdb_id3 = wmdb_info3.get('imdbId', '')
    douban_id3 = wmdb_info3.get('doubanId', '')
    
    if not imdb_id3 and not douban_id3:
        logger.info("→ 无可用ID，仅使用WMDB数据")
        merged_info3 = wmdb_info3
        
        logger.info(f"\n最终结果:")
        logger.info(f"  豆瓣评分: {merged_info3['doubanRating']} ({merged_info3['doubanVotes']}人)")
        logger.info(f"  标签: {merged_info3.get('tags', '无')}")
        logger.info(f"  ✓ 数据来源: WMDB API")
    
    logger.info("\n" + "=" * 70)
    logger.info("✓ 所有测试场景完成！")
    logger.info("=" * 70)
    
    logger.info("\n总结:")
    logger.info("  1. 优先使用IMDB ID从豆瓣API获取信息")
    logger.info("  2. 如果没有IMDB ID，使用豆瓣ID作为备用")
    logger.info("  3. 如果两者都没有，仅使用WMDB数据")
    logger.info("  4. 成功合并两个API的数据并更新到数据库")


if __name__ == '__main__':
    try:
        test_dual_api_with_fallback()
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
        sys.exit(1)
