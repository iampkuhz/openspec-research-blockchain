# Note Rules

## 适用文件

`openspec/changes/<id>/notes/*.md`

## 必须包含

- 来源引用（URL 或来源 ID）
- 核心信息摘录
- 与 research question 的关联

## 不应包含

- 正式分析结论
- 跨来源的综合判断（属于 synthesis）

## 质量标准

- 摘录准确反映原文
- 区分原文引用和笔记作者的理解
- 原文引用使用 blockquote 格式

## Traceability 要求

- 每条笔记可追溯到至少一个 source

## 推荐 Validator

- `markdown_sections`（base）：检查必要结构

## 失败处理

- 返回格式不合规的笔记清单
