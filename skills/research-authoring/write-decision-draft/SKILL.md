---
name: research-write-decision-draft
description: 当研究类型为 decision 且 decision-criteria.md 已定义完成，需要基于决策标准与对比分析生成包含 Verdict Draft 章节的 draft.md 时使用。
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
