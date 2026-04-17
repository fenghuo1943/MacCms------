# 测试文件

本目录包含项目的所有测试脚本。

## 🧪 测试分类

### Selenium 相关测试
- `test_selenium_basic.py` - Selenium 基础功能测试
- `test_alias_extraction.py` - 别名提取功能测试
- `test_duration_extraction.py` - 片长提取功能测试
- `test_rating_extraction.py` - 评分提取容错测试
- `test_filter_update.py` - 数据库更新过滤测试

### API 相关测试
- `test_douban_api.py` - 豆瓣 API 测试
- `test_douban_search.py` - 豆瓣搜索 API 测试
- `test_douban_search_post.py` - 豆瓣 POST 搜索测试
- `test_douban_subject_api.py` - 豆瓣 Subject API 测试
- `test_douban_by_id.py` - 按 ID 获取豆瓣数据测试

### 集成测试
- `test_full_integration.py` - 完整集成测试
- `test_complete_douban_flow.py` - 完整豆瓣流程测试
- `test_new_douban_flow.py` - 新豆瓣流程测试
- `test_dual_api.py` - 双 API 测试
- `test_dual_api_fallback.py` - 双 API 降级测试

### 功能测试
- `test_auto_stop.py` - 自动停止功能测试
- `test_consecutive_failures.py` - 连续失败测试
- `test_year_extraction.py` - 年份提取测试
- `test_rlock_fix.py` - RLock 修复测试

### 配置测试
- `test_config.py` - 配置测试
- `test_module.py` - 模块测试

### 网页爬取测试
- `test_douban_webpage.py` - 豆瓣网页爬取测试

## 🚀 运行测试

### 运行单个测试
```bash
python tests/test_alias_extraction.py
```

### 运行所有测试
```bash
python -m pytest tests/ -v
```

### 运行特定类别的测试
```bash
# 只运行 Selenium 相关测试
python -m pytest tests/ -k "selenium or alias or duration or rating" -v

# 只运行 API 相关测试
python -m pytest tests/ -k "douban_api or douban_search" -v
```

## 📝 编写新测试

1. 文件名以 `test_` 开头
2. 函数名以 `test_` 开头
3. 使用 assert 进行断言
4. 添加清晰的文档字符串
5. 包含必要的测试数据

示例：
```python
def test_feature_name():
    """测试功能说明"""
    # 准备测试数据
    # 执行测试
    # 验证结果
    assert result == expected
```

## 🔧 测试依赖

确保已安装测试所需的依赖：
```bash
pip install pytest
```

## 📊 测试覆盖

- ✅ 核心功能测试
- ✅ 边界条件测试
- ✅ 异常处理测试
- ✅ 集成测试

## ⚠️ 注意事项

1. 测试不应修改生产数据库
2. 使用测试配置或 Mock 数据
3. 保持测试独立性
4. 清理测试产生的临时文件
