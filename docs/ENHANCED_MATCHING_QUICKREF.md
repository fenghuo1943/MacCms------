# 增强匹配功能 - 快速参考

## 核心特性

✅ **翻译差异处理**: 自动识别"伟大的觉醒"和"大觉醒"为同一作品  
✅ **多字段综合匹配**: 名称 + 年份 + 地区 + 导演  
✅ **智能容错**: 支持部分匹配和包含关系  
✅ **防止误匹配**: 多字段联合验证  

## 修改的文件

| 文件 | 修改内容 |
|------|---------|
| `douban_fetcher/data_processor.py` | 新增相似度计算、包含关系检查、增强匹配逻辑 |
| `douban_fetcher/fetcher.py` | 获取并传递导演信息 |
| `douban_fetcher/database.py` | 查询中添加 vod_director 字段 |
| `tests/test_enhanced_matching.py` | 新增测试套件 |

## 关键方法

### 1. calculate_similarity(str1, str2)
计算两个字符串的编辑距离相似度（0-1）

### 2. check_name_containment(name1, name2)
检查名称是否存在包含关系或核心词匹配

### 3. match_douban_search_results(..., target_director='')
增强的匹配方法，支持导演参数

## 使用示例

```python
from douban_fetcher.data_processor import DataProcessor

# 匹配视频（带导演信息）
matched = DataProcessor.match_douban_search_results(
    search_results, 
    target_name="伟大的觉醒",
    target_year="2026",
    target_area="美国",
    target_director="约书亚·恩克"  # 新增参数
)
```

## 匹配策略

### 名称匹配（三层）
1. **精确匹配**: 去除空格后完全相同
2. **包含关系**: "复仇者" ⊂ "复仇者联盟"
3. **相似度**: 编辑距离相似度 >= 0.7

### 其他字段
- **年份**: 支持范围匹配
- **地区**: 包含关系（"中国" ↔ "中国大陆"）
- **导演**: 包含关系，可选字段

## 测试

```bash
python tests/test_enhanced_matching.py
```

## 调整参数

如需调整匹配严格度：

```python
# data_processor.py 第395行左右
if (match_ratio >= 0.8) or (len(shorter_no_num) >= 4 and match_ratio >= 0.7):
    # 降低阈值 → 更宽松
    # 提高阈值 → 更严格

# data_processor.py 第460行左右
similarity_match = similarity >= 0.7  # 调整0.7
```

## 注意事项

⚠️ 确保数据库中有 `vod_director` 数据  
⚠️ 导演名称使用标准译名效果更佳  
⚠️ 定期监控匹配成功率  

## 成功案例

- ✅ "伟大的觉醒" → "大觉醒"
- ✅ "复仇者联盟" → "复仇者"
- ✅ "蝙蝠侠：黑暗骑士" → "黑暗骑士"
- ✅ "X战警：黑凤凰" → "黑凤凰"
