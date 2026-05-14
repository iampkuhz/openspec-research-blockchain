# OpenSpec / Harness 边界（Harness 侧索引）

> **非规范版本**。本文件仅作为 Harness 侧的快速索引。
> **Canonical source**: [`docs/governance/openspec-harness-boundary.md`](../../docs/governance/openspec-harness-boundary.md)
>
> 边界判断、冲突处理、文件归属规则以 canonical 文件为准。

## 一句话边界

- **OpenSpec** 管"什么算正式、产物长什么样、何时可沉淀"。
- **Harness** 管"AI 怎么干、怎么查、怎么修、怎么协作"。
- **Skill / command** 管"这次动作怎么触发、怎么接线"。

## Harness 侧职责

Harness 只负责执行步骤、质量门禁、artifact 规则与多 agent 协作边界，不重新定义 artifact graph。与 `openspec/schemas/**/schema.yaml` 冲突时，以后者为准。
