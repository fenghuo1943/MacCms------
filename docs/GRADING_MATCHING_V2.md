# 分级匹配策略 v2 - 最终版本

## 概述

优化后的**两级分级匹配策略**，明确区分严格匹配和宽松匹配的条件：

1. **第一级（严格匹配）**：名称精确匹配 + 年份 + 地区 + 导演
2. **第二级（宽松匹配）**：名称包含关系/相似度 + 年份(必填) + 地区(必填) + 导演(必填)

## 核心改进

### ✅ 严格匹配（第一级）
- **名称**：只使用**精确匹配**（去除空格后完全相同）
- **年份**：必须匹配（可选字段）
- **地区**：必须匹配（可选字段）
- **导演**：必须匹配（可选字段）
- **返回**：
  - 1个结果 → 返回该结果
  - 多个结果 → 返回 `'multiple'`
  - 0个结果 → 进入第二级

### ✅ 宽松匹配（第二级）
- **触发条件**：第一级结果为0
- **名称**：包含关系 OR 相似度 >= 0.5
- **年份**：**必须非空且匹配**（否则跳过）
- **地区**：**必须非空且匹配**（否则跳过）
- **导演**：**必须非空且匹配**（否则跳过）
- **返回**：
  - 1个结果 → 返回该结果
  - 多个结果 → 返回 `'multiple'`（不再选择最相似的）
  - 0个结果 → 返回 `None`

## 匹配流程

```
开始
  ↓
第一级：严格匹配
  - 名称：精确匹配
  - 年份：匹配（可选）
  - 地区：匹配（可选）
  - 导演：匹配（可选）
  ↓
结果数量 = 1? → 返回该结果 ✅
  ↓
结果数量 > 1? → 返回 'multiple' ⚠️
  ↓
结果数量 = 0? → 进入第二级
  ↓
第二级：宽松匹配
  - 名称：包含关系 OR 相似度>=0.5
  - 年份：必须非空且匹配 ❗
  - 地区：必须非空且匹配 ❗
  - 导演：必须非空且匹配 ❗
  ↓
结果数量 = 1? → 返回该结果 ✅
  ↓
结果数量 > 1? → 返回 'multiple' ⚠️
  ↓
结果数量 = 0? → 返回 None ❌
```

## 关键变化

### v1 vs v2 对比

| 特性 | v1 | v2（当前） |
|------|----|-----------|
| **严格匹配-名称** | 精确+包含+相似度 | **仅精确匹配** |
| **宽松匹配-年份** | 可选 | **必须非空且匹配** |
| **宽松匹配-地区** | 可选 | **必须非空且匹配** |
| **宽松匹配-导演** | 可选 | **必须非空且匹配** |
| **宽松多结果** | 返回最相似的 | **返回'multiple'** |

## 代码实现

### 严格匹配逻辑

```python
# 第一级：只检查精确匹配
normalized_target = DataProcessor.normalize_name(target_name)
normalized_result = DataProcessor.normalize_name(result_name)
exact_match = normalized_target == normalized_result

# 其他字段可选匹配
year_match = DataProcessor._check_year_match(target_year, result_year)
area_match = DataProcessor._check_area_match(target_area, result)
director_match = DataProcessor._check_director_match(target_director, result)

# 所有条件都必须满足
if exact_match and year_match and area_match and director_match:
    strict_matched.append(result)
```

### 宽松匹配逻辑

```python
# 第二级：名称使用包含关系或相似度
containment_match = DataProcessor.check_name_containment(target_name, result_name)
similarity = DataProcessor.calculate_similarity(target_name, result_name)
loose_name_match = containment_match or (similarity >= 0.5)

# 关键：年份、地区、导演必须非空且匹配
if not target_year or not target_year.strip():
    continue  # 年份为空，跳过
year_match = DataProcessor._check_year_match(target_year, result_year)
if not year_match:
    continue

if not target_area or not target_area.strip():
    continue  # 地区为空，跳过
area_match = DataProcessor._check_area_match(target_area, result)
if not area_match:
    continue

if not target_director or not target_director.strip():
    continue  # 导演为空，跳过
director_match = DataProcessor._check_director_match(target_director, result)
if not director_match:
    continue

# 名称可以宽松，但其他字段必须非空且匹配
if loose_name_match:
    loose_matched.append(result)

# 处理结果
if len(loose_matched) == 1:
    return loose_matched[0]
elif len(loose_matched) > 1:
    return 'multiple'  # 多个结果直接返回'multiple'
```

## 实际案例

### 案例1：严格匹配成功

**数据库信息**：
- 名称：伟大的觉醒
- 年份：2026
- 地区：美国
- 导演：约书亚·恩克

**豆瓣结果**：
- 名称：伟大的觉醒（精确匹配）
- 年份：2026
- 国家：美国
- 导演：约书亚·恩克

**匹配过程**：
1. 第一级：名称（精确✓）+ 年份（✓）+ 地区（✓）+ 导演（✓）
2. 结果数量：1个
3. **结果**：✅ 返回该结果

### 案例2：回退到宽松匹配

**数据库信息**：
- 名称：伟大的觉醒
- 年份：2026
- 地区：美国
- 导演：约书亚·恩克

**豆瓣结果**：
- 名称：大觉醒（包含关系："觉醒"在"伟大的觉醒"中）
- 年份：2026
- 国家：美国
- 导演：约书亚·恩克

**匹配过程**：
1. 第一级：名称（不精确✗）→ 0个结果
2. 第二级：
   - 名称（包含关系✓）
   - 年份（非空且匹配✓）
   - 地区（非空且匹配✓）
   - 导演（非空且匹配✓）
3. 结果数量：1个
4. **结果**：✅ 返回该结果

### 案例3：宽松匹配多个结果

**数据库信息**：
- 名称：伟大的觉醒
- 年份：2026
- 地区：美国
- 导演：约书亚·恩克

**豆瓣结果**：
- 结果1：大觉醒（包含关系），2026，美国，约书亚·恩克
- 结果2：觉醒（包含关系），2026，美国，约书亚·恩克

**匹配过程**：
1. 第一级：无精确匹配 → 0个结果
2. 第二级：两个结果都满足条件
3. 结果数量：2个
4. **结果**：⚠️ 返回 `'multiple'`

### 案例4：缺少必需字段

**数据库信息**：
- 名称：伟大的觉醒
- 年份：2026
- 地区：（空）
- 导演：约书亚·恩克

**豆瓣结果**：
- 名称：大觉醒（包含关系）
- 年份：2026
- 国家：美国
- 导演：约书亚·恩克

**匹配过程**：
1. 第一级：名称不精确 → 0个结果
2. 第二级：地区为空 → **跳过此结果**
3. **结果**：❌ 返回 `None`

## 优势

1. **严格的准确性控制**：
   - 严格模式只用精确匹配，避免误判
   - 宽松模式要求年份、地区、导演必须非空且匹配

2. **明确的降级策略**：
   - 第一级失败后才尝试第二级
   - 第二级有严格的前置条件

3. **透明的多结果处理**：
   - 多个结果统一返回 `'multiple'`
   - 不再自动选择"最相似"的，让用户决定

4. **防止空字段导致的误匹配**：
   - 宽松模式下，年份、地区、导演为空时直接跳过
   - 避免因缺少关键信息而错误匹配

## 测试验证

运行测试套件：

```bash
python tests/test_grading_matching.py
```

测试结果：
- ✅ 测试1: 严格匹配 - 名称精确匹配时返回
- ✅ 测试2: 严格匹配 - 多个精确匹配结果时返回'multiple'
- ✅ 测试3: 回退到宽松匹配
- ✅ 测试4: 完全无匹配结果
- ✅ 测试5: 只有宽松匹配存在的场景
- ✅ 测试6: 宽松匹配 - 多个结果时返回'multiple'

## 参数调整

如需调整匹配严格度：

### 调整宽松模式名称相似度阈值

```python
# data_processor.py 第483行左右
similarity_match = similarity >= 0.5  # 提高→更严格，降低→更宽松
```

**建议**：
- 默认0.5已平衡准确性和召回率
- 如果误匹配多 → 提高到0.6或0.7
- 如果漏匹配多 → 降低到0.4

## 总结

v2版本的分级匹配策略通过以下改进提升了匹配质量：

1. **严格模式更严格**：只使用精确匹配
2. **宽松模式有条件**：年份、地区、导演必须非空且匹配
3. **多结果处理更透明**：统一返回'multiple'
4. **防止空字段误匹配**：宽松模式下跳过缺少关键信息的记录

这个策略在保证准确性的前提下，最大化了匹配成功率，同时避免了因数据不完整导致的错误匹配。
