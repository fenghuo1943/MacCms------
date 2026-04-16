"""
测试豆瓣API通过IMDB ID获取信息
"""
import sys
import os
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.api_client import ApiClient
from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.config import logger


def test_douban_api():
    """测试豆瓣API"""
    logger.info("=" * 70)
    logger.info("开始测试豆瓣API")
    logger.info("=" * 70)
    
    # 初始化API客户端
    api_client = ApiClient(use_proxy=False)
    
    # 使用用户提供的IMDB ID
    imdb_id = "tt33071426"
    
    logger.info(f"\n通过IMDB ID获取豆瓣信息: {imdb_id}")
    
    # 调用豆瓣API
    douban_data = api_client.get_douban_by_imdb(imdb_id)
    
    if not douban_data:
        logger.error("豆瓣API获取失败")
        return
    
    logger.info(f"✓ 成功从豆瓣API获取数据")
    logger.info(f"\n原始JSON数据:")
    logger.info(json.dumps(douban_data, ensure_ascii=False, indent=2))
    
    # 提取信息
    logger.info(f"\n提取豆瓣信息:")
    douban_info = DataProcessor.extract_douban_info(douban_data)
    
    for key, value in douban_info.items():
        logger.info(f"  {key}: {value}")
    
    # 测试Unicode解码
    logger.info(f"\n测试Unicode解码:")
    if 'author' in douban_data:
        for author in douban_data['author']:
            if 'name' in author:
                original = author['name']
                decoded = DataProcessor.decode_unicode_string(original)
                logger.info(f"  原始: {original}")
                logger.info(f"  解码: {decoded}")
    
    if 'attrs' in douban_data:
        attrs = douban_data['attrs']
        if 'writer' in attrs:
            for writer in attrs['writer']:
                decoded = DataProcessor.decode_unicode_string(writer)
                logger.info(f"  编剧: {decoded}")
        
        if 'country' in attrs:
            for country in attrs['country']:
                decoded = DataProcessor.decode_unicode_string(country)
                logger.info(f"  国家: {decoded}")
        
        if 'language' in attrs:
            for lang in attrs['language']:
                decoded = DataProcessor.decode_unicode_string(lang)
                logger.info(f"  语言: {decoded}")
    
    logger.info("\n" + "=" * 70)
    logger.info("✓ 豆瓣API测试完成！")
    logger.info("=" * 70)


if __name__ == '__main__':
    try:
        test_douban_api()
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
        sys.exit(1)
