# Knowledge Indexes

本目录包含知识库的索引文件。

## 文件说明

| 文件 | 用途 |
|------|------|
| [`topic-index.md`](./topic-index.md) | 主题索引 |
| [`concept-index.md`](./concept-index.md) | 概念索引 |
| [`diagram-index.md`](./diagram-index.md) | 图表索引 |
| [`comparison-index.md`](./comparison-index.md) | 比较索引 |

## 自动生成

部分索引文件可通过脚本自动生成：

```bash
# 生成 topic 索引
python scripts/publish/generate_topic_index.py --output knowledge/indexes/topic-index.md

# 构建完整索引
python scripts/general/build_index.py --output knowledge/indexes/topic-index.md
```

## 更新时机

索引在以下时机更新：

1. **Merge change 时** - 自动更新 topic-index.md
2. **手动运行脚本** - 执行 generate_topic_index.py
3. **发布流程** - CI/CD 自动更新

## 手动维护

部分索引需要手动维护：

- `concept-index.md` - 按概念组织的索引
- `diagram-index.md` - 图表索引（可从 diagram models 生成）
- `comparison-index.md` - 比较分析索引
