"""
测试通过豆瓣ID从豆瓣API获取信息
"""
import sys
import os
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.api_client import ApiClient
from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.config import logger


def test_douban_by_id():
    """测试通过豆瓣ID获取信息"""
    logger.info("=" * 70)
    logger.info("开始测试通过豆瓣ID获取信息")
    logger.info("=" * 70)
    
    # 初始化API客户端
    api_client = ApiClient(use_proxy=False)
    
    # 使用用户提供的豆瓣ID
    douban_id = "36995126"
    
    logger.info(f"\n通过豆瓣ID获取信息: {douban_id}")
    
    # 调用豆瓣API
    douban_data = api_client.get_douban_by_id(douban_id)
    
    if not douban_data:
        logger.error("豆瓣API获取失败")
        return
    
    logger.info(f"✓ 成功从豆瓣API获取数据")
    logger.info(f"\n完整JSON数据:")
    logger.info(json.dumps(douban_data, ensure_ascii=False, indent=2))
    
    # 提取信息
    logger.info(f"\n提取豆瓣信息:")
    douban_info = DataProcessor.extract_douban_info(douban_data)
    
    for key, value in douban_info.items():
        logger.info(f"  {key}: {value}")
    
    logger.info("\n" + "=" * 70)
    logger.info("✓ 豆瓣ID API测试完成！")
    logger.info("=" * 70)


if __name__ == '__main__':
    try:
        test_douban_by_id()
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
        sys.exit(1)
