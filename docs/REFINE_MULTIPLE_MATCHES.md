# 多结果二次确认功能说明

## 功能概述

当通过 `match_douban_search_results` 匹配豆瓣搜索结果时，如果匹配到多个候选结果，系统会自动通过豆瓣 Subject API 获取每个候选结果的详细信息（包括准确的标题、年份、导演、地区等），然后基于这些更精确的信息重新进行匹配，以提高匹配的准确性。

## 工作流程

### 1. 第一级匹配（严格模式）
- 名称精确匹配（去除空格后完全相同）
- 年份匹配
- 地区匹配（可选）
- 导演匹配（可选）

**结果处理：**
- 如果只有 1 个结果 → 直接返回
- 如果有多个结果 → 进入第三级（二次确认）
- 如果没有结果 → 进入第二级（宽松模式）

### 2. 第二级匹配（宽松模式）
- 名称使用包含关系或相似度（≥0.7）
- 年份必须非空且匹配
- 导演必须非空且匹配
- 地区可选

**结果处理：**
- 如果只有 1 个结果 → 直接返回
- 如果有多个结果 → 进入第三级（二次确认）
- 如果没有结果 → 返回 None（未找到匹配）

### 3. 第三级匹配（多结果二次确认）✨ 新增
当第一级或第二级匹配到多个结果时触发：

1. **获取详细信息**：对每个候选结果，通过 Subject API 获取完整信息
   - 准确标题（title / original_title）
   - 年份（year）
   - 导演列表（directors）
   - 国家/地区列表（countries）

2. **重新匹配**：使用更精确的信息进行匹配
   - 名称匹配：优先使用原标题，支持精确匹配和包含关系
   - 年份匹配：使用提取的年份信息
   - 地区匹配：检查目标地区是否在国家的列表中
   - 导演匹配：检查目标导演是否在导演列表中

3. **返回结果**：
   - 如果精炼后只有 1 个结果 → 返回该结果
   - 如果仍然有多个结果 → 返回 `'multiple'`
   - 如果没有结果 → 返回 `None`

## 代码示例

### 基本用法

```python
from douban_fetcher.data_processor import DataProcessor
from douban_fetcher.api_client import ApiClient

# 创建API客户端
api_client = ApiClient()

# 搜索视频
search_results = api_client.search_douban("复仇者联盟")

# 匹配视频（传入api_client以启用二次确认功能）
matched = DataProcessor.match_douban_search_results(
    search_results, 
    target_name="复仇者联盟",
    target_year="2018",
    target_area="美国",
    target_director="安东尼·罗素",
    api_client=api_client  # 关键：传入api_client
)

if matched == 'multiple':
    print("仍然匹配到多个结果")
elif matched is None:
    print("未找到匹配")
else:
    print(f"匹配成功: {matched['title']} (ID: {matched['id']})")
```

### 在 Fetcher 中的使用

已在 `douban_fetcher/fetcher.py` 和 `selenium_fetcher/fetcher.py` 中自动集成：

```python
# 自动传入 api_client，无需手动修改
matched = DataProcessor.match_douban_search_results(
    search_results, vod_name, vod_year, vod_area, vod_director, self.api_client
)
```

## 日志输出示例

```
检测到 3 个候选结果，开始通过Subject API进行二次确认...
  [1/3] 获取豆瓣ID 26374149 的详细信息...
    标题: 蜘蛛侠：英雄归来, 年份: 2017, 导演: 乔·沃茨, 地区: 美国
    匹配结果: 名称=True, 年份=True, 地区=True, 导演=True
    ✓ 匹配成功
  [2/3] 获取豆瓣ID 3048829 的详细信息...
    标题: 蜘蛛侠, 年份: 2002, 导演: 山姆·雷米, 地区: 美国
    匹配结果: 名称=False, 年份=False, 地区=True, 导演=False
    ✗ 匹配失败
  [3/3] 获取豆瓣ID 1308753 的详细信息...
    标题: 蜘蛛侠2, 年份: 2004, 导演: 山姆·雷米, 地区: 美国
    匹配结果: 名称=False, 年份=False, 地区=True, 导演=False
    ✗ 匹配失败
二次确认完成：精确匹配到 1 个结果
```

## 优势

1. **提高准确性**：通过 Subject API 获取更详细、更准确的信息
2. **减少误匹配**：即使搜索结果的元数据不完整，也能通过详细信息精确匹配
3. **自动化处理**：无需人工干预，系统自动处理多结果情况
4. **透明化**：详细的日志输出，便于调试和监控

## 注意事项

1. **性能影响**：二次确认需要对每个候选结果调用 Subject API，会增加请求次数和时间
   - 建议：仅在必要时使用（已自动判断）
   
2. **API限制**：频繁调用 Subject API 可能触发频率限制
   - 系统已有速率控制和重试机制
   
3. **向后兼容**：如果不传入 `api_client` 参数，功能会退化为原来的行为（直接返回 `'multiple'`）

## 测试

运行测试文件验证功能：

```bash
python tests/test_refine_multiple_matches.py
```

## 相关文件

- `douban_fetcher/data_processor.py` - 核心匹配逻辑
- `douban_fetcher/fetcher.py` - API方案主获取器（已集成）
- `selenium_fetcher/fetcher.py` - Selenium方案主获取器（已集成）
- `tests/test_refine_multiple_matches.py` - 测试文件
