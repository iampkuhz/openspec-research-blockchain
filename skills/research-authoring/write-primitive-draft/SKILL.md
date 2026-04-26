---
name: write-primitive-draft
description: 基于 claims 与证据，编写 primitive 类型的 draft.md 正文。
---

# 编写 Primitive 型草稿

## 适用场景

- 研究类型为 `primitive`，需要定义某个概念/机制/组件。
- 适用 `primitive` profile。

## 输入

- `sources/claims/*.md` 提取的 claims。
- `sources/evidence-map.md`。
- `request.md` / `plan.md`。

## 输出

- `draft.md`（写入当前 change 目录下）。

## 读取文件

- `request.md`、`plan.md`。
- `sources/claims/*.md`、`sources/evidence-map.md`。
- `openspec/schemas/blockchain-research/templates/draft.md`。

## 写入文件

- `openspec/changes/<change-id>/draft.md`

## 禁止事项

- 不得生成 `work-products/*.md`。
- 不得跳过 claims 直接写结论。
- 不得直接写 `knowledge/**`。

## 自检

- draft 是否包含角色的定义、边界与信任假设？
- 每个 claim 是否可追溯到来源？
