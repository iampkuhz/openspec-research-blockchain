---
name: render-decision-verdict
description: 将 decision 类型的 draft.md 中的 Verdict Draft 提炼为 knowledge/decisions/**/verdict.md。
---

# 渲染决策裁决

## 适用场景

- 研究类型为 `decision`，需要将最终判断沉淀为长期资产。
- `publish.md` 已定义 verdict 的 publish target。

## 输入

- `draft.md`（包含 Verdict Draft 章节）。
- `decision-criteria.md`。
- `publish.md`。

## 输出

- `knowledge/decisions/<domain_id>/<topic_slug>/verdict.md`

## 读取文件

- `draft.md`、`decision-criteria.md`、`publish.md`。
- `openspec/schemas/blockchain-research/templates/decision-verdict.md`（如存在）。

## 写入文件

- `knowledge/decisions/<domain_id>/<topic_slug>/verdict.md`

## 禁止事项

- 不得跳过 publish.md 直接写入 verdict。
- 不得从未经 review 的 draft 生成 verdict。

## 自检

- verdict 的判断是否基于 decision-criteria 中的维度？
- 输出路径是否与 schema.yaml 的 decision artifact 模型一致？
