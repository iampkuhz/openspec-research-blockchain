# Synthesis Workflow

**task_type**：`synthesis`
**对应 Workflow**：`harness/workflows/synthesis-workflow.md`

---

## 适用场景

- 多个 primitive 的横向对比
- 演进脉络梳理
- 分类分析

## 输入

- `request.md`（声明比较对象、比较目的）
- `plan.md`（声明比较维度、依赖的 primitive）

## 输出

- `sources/source-pack.md`
- `sources/evidence-map.md`
- `draft.md`（包含对比表格、横向分析、趋势判断）
- `review.md`

## 推荐 child change 拆分方式

- synthesis change 依赖其引用的所有 primitive changes
- 如依赖的 primitive 不存在，先创建 primitive changes
- synthesis 独立一个 change

## draft.md 写作重点

- 比较维度固定（3-5 个核心维度）
- 每个维度下逐项对比
- 区分事实和观点
- 标注证据等级
- 列出适用场景与不适用场景
- 给出 bounded conclusions，不做绝对化判断

## review 重点

- 比较维度是否合理
- 数据是否来自可靠的 primitive artifacts
- 结论是否有证据支撑
- 是否有遗漏的重要比较对象

## Publish target

```text
knowledge/analysis/synthesis/<topic_slug>/artifact.md
```

## 禁止事项

- 不深入每个 primitive 的完整机制（那是 primitive 的职责）
- 不做场景决策（那是 decision 的职责）
- 维度不固定就做不了有效对比
- 不生成 work-products/*.md
