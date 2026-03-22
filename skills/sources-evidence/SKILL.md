---
name: sources-evidence
description: 用于为本仓库的 change packet 生成和修订 sources.md、dependency-map.md、evidence-matrix.md，适合做证据规划、依赖声明和证据分级时使用。
---

# 来源与证据

## 何时使用

- request / brief 已经成型
- 需要补齐来源、证据等级、依赖对象、evidence gap

## 输出要求

- `sources.md`
- `dependency-map.md`（如适用）
- `evidence-matrix.md`（如适用）

## 强约束

- 结论优先依赖 `L1/L2`
- 明确区分协议原生、官方生态、第三方能力
- 明确区分已上线、规划中、宣传性表述
- 必须标记 evidence gaps 和 unresolved ambiguities
