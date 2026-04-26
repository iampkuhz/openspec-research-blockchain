# Source Reading Workflow

**task_type**：`source_reading`
**对应 Workflow**：`harness/workflows/source-reading-workflow.md`

---

## 适用场景

- 阅读并消化一个或多个来源
- 不生成完整的 primitive/synthesis/decision 分析
- 产出为来源笔记的整理版

## 输入

- `request.md`（声明要阅读的来源）
- `plan.md`（声明阅读范围和来源分层）

## 输出

- `sources/source-pack.md`
- `sources/evidence-map.md`
- `notes/*.md`
- `draft.md`（整理后的来源笔记汇总）
- `review.md`

## 推荐 child change 拆分方式

- 如果来源数量超过 5 个，按来源组拆分多个 source_reading changes
- 每组 sources 独立一个 change

## draft.md 写作重点

- 按来源组织笔记，不做深度分析
- 每条来源标注 URL、类型、分层、验证状态
- 提取核心信息，保留原文引用
- 列出证据缺口

## review 重点

- 来源覆盖是否完整
- 来源分层是否合理
- 摘录是否准确反映原文

## Publish target

```text
knowledge/analysis/source-notes/**/artifact.md
```

## 禁止事项

- 不做深度机制分析（那是 primitive 的职责）
- 不做横向对比（那是 synthesis 的职责）
- 不做场景决策（那是 decision 的职责）
- 不生成 work-products/*.md
