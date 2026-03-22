---
name: promote-canonical
description: 用于把 change packet 中的 durable 结果提炼进 knowledge/analysis/ 或 knowledge/decisions/，适合一轮研究完成后整理长期资产时使用。
---

# 提炼长期产物

## 何时使用

- change packet 已经完成本轮研究
- 需要把长期值得保留的内容提炼进 canonical 目录

## 输出要求

- `knowledge/analysis/...` 或 `knowledge/decisions/...` 下的长期文件

## 强约束

- 不把 `request.md`、`plan.md` 直接复制进长期目录
- 只保留 durable 结果
- 不把 `evidence-matrix.md` 直接复制进长期目录
- `knowledge/analysis/` 默认只保留 `reference.md`，必要时保留 `dependencies.md`
- glossary 层默认折叠进 `reference.md` 的“关键术语”区
- `knowledge/decisions/` 保留 `reference.md`、`criteria.md`、`dependencies.md`、`verdict.md`
