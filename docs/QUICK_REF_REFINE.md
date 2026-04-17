# 多结果二次确认功能 - 快速参考

## 一句话说明
当匹配到多个豆瓣结果时，自动通过Subject API获取详细信息重新匹配，提高准确性。

## 核心API

```python
matched = DataProcessor.match_douban_search_results(
    search_results, 
    target_name, target_year, target_area, target_director,
    api_client=api_client  # ← 关键：传入以启用二次确认
)
```

## 返回值

| 返回值 | 含义 |
|--------|------|
| `dict` | 匹配成功，包含视频信息 |
| `'multiple'` | 仍然有多个结果 |
| `None` | 未找到匹配 |

## 三级匹配策略

```
第一级（严格）→ 第二级（宽松）→ 第三级（二次确认⭐）
```

### 触发条件

- **第一级**：名称精确 + 年份 + 地区/导演 → 多结果时进入第三级
- **第二级**：名称相似度 + 年份/导演必须 → 多结果时进入第三级  
- **第三级**：通过Subject API获取详情重新匹配

## 快速测试

```bash
# 运行测试
python tests/test_refine_multiple_matches.py

# 运行示例
python examples/example_refine_matches.py
```

## 日志关键字

搜索日志中的这些关键字监控功能：

- `检测到 X 个候选结果，开始通过Subject API进行二次确认`
- `获取豆瓣ID XXX 的详细信息`
- `匹配结果: 名称=X, 年份=X, 地区=X, 导演=X`
- `✓ 匹配成功` / `✗ 匹配失败`
- `二次确认完成：精确匹配到 1 个结果`

## 性能提示

- ⚠️ 每个候选结果需要1次额外的API调用
- ✅ 仅在多结果时触发（不常见）
- ✅ 已有速率控制和重试机制
- 📊 监控 `douban_score_fetch.log` 观察触发频率

## 常见问题

**Q: 如何禁用此功能？**  
A: 调用时不传 `api_client` 参数即可

**Q: 会影响现有功能吗？**  
A: 不会，完全向后兼容

**Q: 在哪里查看效果？**  
A: 查看日志文件和统计文件

## 相关文件

- 核心代码：`douban_fetcher/data_processor.py`
- 集成位置：`douban_fetcher/fetcher.py`, `selenium_fetcher/fetcher.py`
- 详细文档：`docs/REFINE_MULTIPLE_MATCHES.md`
- 修改总结：`docs/MODIFICATION_SUMMARY.md`

---
快速参考 | v1.0 | 2026-04-17
