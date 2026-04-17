# 片长提取功能说明

## ✅ 功能概述

已成功添加**单集片长**和**电影片长**的自动提取功能，支持两种豆瓣页面格式。

## 📋 支持的格式

### 1. 电视剧单集片长
```html
<span class="pl">单集片长:</span> 45分钟<br>
```
- 提取结果：`duration = 45`（分钟）

### 2. 电影片长
```html
<span property="v:runtime" content="103">103分钟</span>
```
- 提取结果：`duration = 103`（分钟）

## 🎯 提取逻辑

### 优先级规则
1. **优先提取单集片长**（电视剧）
2. **如果没有单集片长，则提取电影片长**
3. **如果都没有，返回 0**

### 代码实现

```python
# 先尝试提取单集片长
episode_duration_span = info_div.find('span', class_='pl', 
                                      string=lambda text: text and '单集片长' in text)
if episode_duration_span:
    next_text = episode_duration_span.next_sibling
    if next_text:
        duration_text = next_text.strip()
        duration_match = re.search(r'(\d+)', duration_text)
        info['duration'] = int(duration_match.group(1)) if duration_match else 0
else:
    # 如果没有单集片长，尝试提取电影片长
    runtime_tag = info_div.find('span', property='v:runtime')
    if runtime_tag:
        runtime_text = runtime_tag.get_text().strip()
        runtime_match = re.search(r'(\d+)', runtime_text)
        info['duration'] = int(runtime_match.group(1)) if runtime_match else 0
    else:
        info['duration'] = 0
```

## 📊 数据库字段

### 字段映射
```python
info = {
    'doubanDuration': movie_info.get('duration', 0),  # 单位：分钟
}
```

### 字段说明
- **字段名**: `doubanDuration`
- **类型**: Integer
- **单位**: 分钟
- **默认值**: 0
- **含义**: 
  - 对于电视剧：单集片长（分钟）
  - 对于电影：总片长（分钟）

## 🔍 日志输出

处理视频时会在日志中显示片长信息：

```
豆瓣:8.5(12345人) 类型:剧情,爱情 集数:24 片长:45分钟
```

## ✅ 测试用例

已创建完整的测试文件 [test_duration_extraction.py](file:///e:/python/MacCms自动获取评分/test_duration_extraction.py)，包含5个测试场景：

### 测试1: 单集片长（电视剧）
```python
输入: <span class="pl">单集片长:</span> 45分钟<br>
输出: duration = 45
结果: ✓ 通过
```

### 测试2: 电影片长
```python
输入: <span property="v:runtime" content="103">103分钟</span>
输出: duration = 103
结果: ✓ 通过
```

### 测试3: 优先级测试
```python
输入: 同时有单集片长(30分钟)和电影片长(120分钟)
输出: duration = 30 (优先使用单集片长)
结果: ✓ 通过
```

### 测试4: 没有片长信息
```python
输入: 没有片长相关标签
输出: duration = 0
结果: ✓ 通过
```

### 测试5: 短时长
```python
输入: <span class="pl">单集片长:</span> 2分钟<br>
输出: duration = 2
结果: ✓ 通过
```

所有测试均已通过！✅

## 💡 使用示例

### 在代码中使用
```python
from selenium_fetcher import SeleniumDoubanFetcher
from selenium_fetcher.config import DB_CONFIG_EXAMPLE

fetcher = SeleniumDoubanFetcher(DB_CONFIG_EXAMPLE)

# 处理视频后，duration字段会自动填充
# 电视剧: doubanDuration = 单集片长（如 45）
# 电影: doubanDuration = 总片长（如 103）
```

### 查询数据库
```sql
-- 查询所有有片长信息的视频
SELECT vod_id, vod_name, doubanDuration 
FROM mac_vod 
WHERE doubanDuration > 0;

-- 查询电视剧（有集数和单集片长）
SELECT vod_id, vod_name, doubanEpisodes, doubanDuration 
FROM mac_vod 
WHERE doubanEpisodes > 0 AND doubanDuration > 0;

-- 查询电影（有片长但无集数）
SELECT vod_id, vod_name, doubanDuration 
FROM mac_vod 
WHERE doubanEpisodes = 0 AND doubanDuration > 0;
```

## 🎬 应用场景

### 1. 电视剧分类
```python
if doubanEpisodes > 0 and doubanDuration > 0:
    # 这是电视剧，doubanDuration是单集片长
    total_duration = doubanEpisodes * doubanDuration
```

### 2. 电影分类
```python
if doubanEpisodes == 0 and doubanDuration > 0:
    # 这是电影，doubanDuration是总片长
    print(f"电影时长: {doubanDuration}分钟")
```

### 3. 时长筛选
```sql
-- 查找90-120分钟的电影
SELECT * FROM mac_vod 
WHERE doubanEpisodes = 0 
  AND doubanDuration BETWEEN 90 AND 120;

-- 查找单集30-60分钟的电视剧
SELECT * FROM mac_vod 
WHERE doubanEpisodes > 0 
  AND doubanDuration BETWEEN 30 AND 60;
```

## 🔧 技术细节

### 正则表达式提取
```python
# 从 "45分钟" 或 "103分钟" 中提取数字
duration_match = re.search(r'(\d+)', duration_text)
duration = int(duration_match.group(1)) if duration_match else 0
```

### 容错处理
- ✅ 标签不存在 → 返回 0
- ✅ 文本为空 → 返回 0
- ✅ 无法提取数字 → 返回 0
- ✅ 非数字内容 → 返回 0

## 📝 修改的文件

1. **[selenium_fetcher/extractor.py](file:///e:/python/MacCms自动获取评分/selenium_fetcher/extractor.py)**
   - 添加单集片长提取逻辑
   - 添加电影片长提取逻辑
   - 实现优先级判断

2. **[selenium_fetcher/fetcher.py](file:///e:/python/MacCms自动获取评分/selenium_fetcher/fetcher.py)**
   - 添加 `doubanDuration` 字段映射
   - 在日志中显示片长信息

3. **[test_duration_extraction.py](file:///e:/python/MacCms自动获取评分/test_duration_extraction.py)**
   - 新建测试文件
   - 5个完整测试用例

## ⚠️ 注意事项

1. **单位统一**: 所有片长都以**分钟**为单位
2. **电视剧**: `doubanDuration` 表示单集片长，不是总时长
3. **电影**: `doubanDuration` 表示总片长
4. **缺失处理**: 如果豆瓣页面没有片长信息，返回 0

## 🚀 未来优化

可能的改进方向：
- [ ] 添加总时长计算（电视剧：集数 × 单集片长）
- [ ] 支持小时:分钟格式（如 "1:45"）
- [ ] 添加片长范围筛选功能
- [ ] 统计平均片长

---

**更新时间**: 2026-04-17  
**版本**: v1.2.0  
**分支**: selenium-webpage-fetcher
