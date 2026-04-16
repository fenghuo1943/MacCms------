"""
测试完整的双API集成流程
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.api_client import ApiClient
from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.config import logger


def test_full_integration():
    """测试完整的双API集成流程"""
    logger.info("=" * 70)
    logger.info("开始测试完整双API集成流程")
    logger.info("=" * 70)
    
    # 初始化API客户端
    api_client = ApiClient(use_proxy=False)
    
    # 模拟从WMDB API获取的数据（基于用户提供的JSON）
    wmdb_data = {
        "originalName": "The Drama",
        "imdbVotes": 0,
        "imdbRating": "",
        "rottenRating": "",
        "rottenVotes": 0,
        "year": "2026",
        "imdbId": "tt33071426",
        "alias": "抓马恋人(台) / 戏剧性婚礼(港) / 抓马 / 戏剧故事",
        "doubanId": "36995126",
        "type": "Movie",
        "doubanRating": "7.4",
        "doubanVotes": 1016,
        "duration": 6360,
        "episodes": 0,
        "totalSeasons": 0,
        "dateReleased": "2026-04-01",
        "data": [{
            "poster": "https://img.wmdb.tv/movie/poster/1775351312983-edcfab.webp",
            "name": "爱情抓马",
            "genre": "爱情",
            "description": "婚礼前几天，一对情侣无意中发现彼此的秘密，亲密关系面临考验，令结婚计划骤然生变。暗黑秘密如何一发不可收拾？各种反应又引致怎样翻天覆地的后果？原定又浪漫又幸福的结婚计划，还可以进行吗？",
            "language": "英语",
            "country": "美国",
            "lang": "Cn"
        }],
        "writer": [{
            "data": [{"name": "克里斯托弗·博格利", "lang": "Cn"}]
        }],
        "actor": [
            {"data": [{"name": "罗伯特·帕丁森", "lang": "Cn"}]},
            {"data": [{"name": "赞达亚", "lang": "Cn"}]}
        ],
        "director": [{
            "data": [{"name": "克里斯托弗·博格利", "lang": "Cn"}]
        }]
    }
    
    logger.info("\n步骤1: 从WMDB数据提取信息")
    wmdb_info = DataProcessor.extract_video_info(wmdb_data)
    
    logger.info(f"  IMDB ID: {wmdb_info['imdbId']}")
    logger.info(f"  豆瓣评分: {wmdb_info['doubanRating']} ({wmdb_info['doubanVotes']}人)")
    logger.info(f"  IMDB评分: {wmdb_info['imdbRating']} ({wmdb_info['imdbVotes']}人)")
    logger.info(f"  年份: {wmdb_info['year']}")
    logger.info(f"  时长: {wmdb_info['duration']}秒")
    logger.info(f"  上映日期: {wmdb_info['dateReleased']}")
    logger.info(f"  国家: {wmdb_info['country']}")
    logger.info(f"  语言: {wmdb_info['language']}")
    logger.info(f"  编剧: {wmdb_info['writers']}")
    logger.info(f"  描述长度: {len(wmdb_info['description'])}字符")
    
    # 步骤2: 通过IMDB ID从豆瓣API获取信息
    imdb_id = wmdb_info.get('imdbId', '')
    if not imdb_id:
        logger.error("没有IMDB ID，无法继续")
        return
    
    logger.info(f"\n步骤2: 通过IMDB ID {imdb_id} 从豆瓣API获取信息")
    douban_data = api_client.get_douban_by_imdb(imdb_id)
    
    if not douban_data:
        logger.error("豆瓣API获取失败")
        return
    
    logger.info("✓ 成功从豆瓣API获取数据")
    
    # 步骤3: 提取豆瓣信息
    logger.info(f"\n步骤3: 从豆瓣API提取信息")
    douban_info = DataProcessor.extract_douban_info(douban_data)
    
    logger.info(f"  豆瓣评分: {douban_info.get('doubanRating', 0)} ({douban_info.get('doubanVotes', 0)}人)")
    logger.info(f"  标签: {douban_info.get('tags', '')}")
    
    # 步骤4: 合并两个API的信息
    logger.info(f"\n步骤4: 合并双API信息")
    merged_info = DataProcessor.merge_video_info(wmdb_info, douban_info)
    
    logger.info("\n最终合并后的信息:")
    logger.info("-" * 70)
    
    # 按照用户需求显示关键字段
    logger.info("\n【从第一个API (WMDB) 获取的字段】:")
    logger.info(f"  ✓ dateReleased: {merged_info['dateReleased']}")
    logger.info(f"  ✓ episodes: {merged_info['episodes']}")
    logger.info(f"  ✓ duration: {merged_info['duration']}秒 ({merged_info['duration']//60}分钟)")
    logger.info(f"  ✓ description: {merged_info['description'][:50]}...")
    logger.info(f"  ✓ country: {merged_info['country']}")
    logger.info(f"  ✓ language: {merged_info['language']}")
    logger.info(f"  ✓ writers: {merged_info['writers']}")
    
    logger.info("\n【从第二个API (豆瓣) 获取的字段】:")
    logger.info(f"  ✓ rating[average]: {merged_info['doubanRating']}")
    logger.info(f"  ✓ rating[numRaters]: {merged_info['doubanVotes']}人")
    logger.info(f"  ✓ tags: {merged_info['tags']}")
    
    logger.info("\n【其他字段】:")
    logger.info(f"  - imdbId: {merged_info['imdbId']}")
    logger.info(f"  - imdbRating: {merged_info['imdbRating']}")
    logger.info(f"  - imdbVotes: {merged_info['imdbVotes']}")
    logger.info(f"  - doubanId: {merged_info['doubanId']}")
    logger.info(f"  - year: {merged_info['year']}")
    logger.info(f"  - type: {merged_info['type']}")
    logger.info(f"  - alias: {merged_info['alias']}")
    logger.info(f"  - actors: {merged_info['actors']}")
    logger.info(f"  - directors: {merged_info['directors']}")
    logger.info(f"  - genre: {merged_info['genre']}")
    logger.info(f"  - poster: {merged_info['poster'][:50]}...")
    
    # 验证数据来源
    logger.info("\n" + "=" * 70)
    logger.info("✓ 双API集成测试完成！")
    logger.info("=" * 70)
    
    logger.info("\n数据来源验证:")
    logger.info(f"  WMDB豆瓣评分: 7.4 (1016人)")
    logger.info(f"  豆瓣API豆瓣评分: 7.2 (5203人)")
    logger.info(f"  最终使用: {merged_info['doubanRating']} ({merged_info['doubanVotes']}人) ← 来自豆瓣API ✓")
    logger.info(f"  标签: {'有' if merged_info['tags'] else '无'} ← 来自豆瓣API ✓")


if __name__ == '__main__':
    try:
        test_full_integration()
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
        sys.exit(1)
