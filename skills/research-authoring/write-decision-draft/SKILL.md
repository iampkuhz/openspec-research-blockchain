---
name: write-decision-draft
description: 基于决策标准与对比分析，编写 decision 类型的 draft.md 正文，包含 Verdict Draft。
---

# 编写 Decision 型草稿

## 适用场景

- 研究类型为 `decision`，需要在多个方案之间做选择判断。
- 适用 `decision` profile。

## 输入

- `decision-criteria.md`。
- `sources/claims/*.md` 提取的 claims。
- `request.md` / `plan.md`。

## 输出

- `draft.md`（写入当前 change 目录下），包含 Verdict Draft 章节。

## 读取文件

- `request.md`、`plan.md`、`decision-criteria.md`。
- `sources/claims/*.md`、`sources/evidence-map.md`。
- `openspec/schemas/blockchain-research/templates/draft.md`。

## 写入文件

- `openspec/changes/<change-id>/draft.md`

## 禁止事项

- 必须先有 `decision-criteria.md` 再写 draft。
- 不得生成 `work-products/*.md`。
- 不得直接写 `knowledge/**`。

## 自检

- draft 是否包含明确的 Verdict Draft 章节？
- 判断是否基于已定义的决策标准？
