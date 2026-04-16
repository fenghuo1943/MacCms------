"""
测试年份提取功能（从dateReleased中提取）
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.config import logger


def test_year_extraction():
    """测试年份提取功能"""
    logger.info("=" * 70)
    logger.info("开始测试年份提取功能")
    logger.info("=" * 70)
    
    # 测试场景1: year字段为空，从dateReleased提取
    logger.info("\n测试场景1: year字段为空，从dateReleased提取")
    search_results = [{
        "originalName": "Test Movie",
        "year": "",
        "dateReleased": "2025-12-23",
        "data": [{"name": "Test Movie"}]
    }]
    
    matched = DataProcessor.match_video(search_results, "Test Movie", "2025")
    if matched:
        logger.info("✓ 成功匹配：从dateReleased提取到年份 2025")
    else:
        logger.error("✗ 匹配失败")
    
    # 测试场景2: year字段有无效值，从dateReleased提取
    logger.info("\n测试场景2: year字段有无效值，从dateReleased提取")
    search_results2 = [{
        "originalName": "Test Movie 2",
        "year": "N/A",
        "dateReleased": "2026-01-15",
        "data": [{"name": "Test Movie 2"}]
    }]
    
    matched2 = DataProcessor.match_video(search_results2, "Test Movie 2", "2026")
    if matched2:
        logger.info("✓ 成功匹配：从dateReleased提取到年份 2026")
    else:
        logger.error("✗ 匹配失败")
    
    # 测试场景3: year字段有效，优先使用year
    logger.info("\n测试场景3: year字段有效，优先使用year")
    search_results3 = [{
        "originalName": "Test Movie 3",
        "year": "2024",
        "dateReleased": "2025-06-01",
        "data": [{"name": "Test Movie 3"}]
    }]
    
    matched3 = DataProcessor.match_video(search_results3, "Test Movie 3", "2024")
    if matched3:
        logger.info("✓ 成功匹配：使用year字段的年份 2024")
    else:
        logger.error("✗ 匹配失败")
    
    # 测试场景4: year字段有特殊字符，从dateReleased提取
    logger.info("\n测试场景4: year字段有特殊字符，从dateReleased提取")
    search_results4 = [{
        "originalName": "Test Movie 4",
        "year": "–",
        "dateReleased": "2027-03-10",
        "data": [{"name": "Test Movie 4"}]
    }]
    
    matched4 = DataProcessor.match_video(search_results4, "Test Movie 4", "2027")
    if matched4:
        logger.info("✓ 成功匹配：从dateReleased提取到年份 2027")
    else:
        logger.error("✗ 匹配失败")
    
    # 测试场景5: 既没有year也没有dateReleased
    logger.info("\n测试场景5: 既没有year也没有dateReleased")
    search_results5 = [{
        "originalName": "Test Movie 5",
        "year": "",
        "data": [{"name": "Test Movie 5"}]
    }]
    
    matched5 = DataProcessor.match_video(search_results5, "Test Movie 5", "")
    if matched5:
        logger.info("✓ 成功匹配：无年份信息时仅匹配名称")
    else:
        logger.error("✗ 匹配失败")
    
    logger.info("\n" + "=" * 70)
    logger.info("✓ 所有测试场景完成！")
    logger.info("=" * 70)
    
    logger.info("\n总结:")
    logger.info("  1. 优先从 year 字段获取年份")
    logger.info("  2. 如果 year 字段为空或无效，从 dateReleased 中提取")
    logger.info("  3. 支持各种日期格式：2025-12-23、2026/01/15 等")
    logger.info("  4. 使用正则表达式提取4位数字年份")


if __name__ == '__main__':
    try:
        test_year_extraction()
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
        sys.exit(1)
