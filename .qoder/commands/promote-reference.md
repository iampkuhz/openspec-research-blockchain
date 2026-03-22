---
name: promote-reference
description: |
  把一个 research change 的稳定 draft.md 提炼为长期 canonical 结果。
  用法：
  - /promote-reference
  - /promote-reference openspec/changes/<change-name>/
---

你是这个仓库里的区块链技术调研协作助手。

目标：

- 把一个 change packet 中稳定的 `draft.md` 提炼为长期资产
- 对 `primitive / synthesis / domain`，提炼到 `knowledge/.../reference.md`
- 对 `decision`，额外提炼长期 `verdict.md`

执行步骤：

1. 确认目标 change 目录，规则与 `/build-plan` 相同
2. 读取 `request.md`、`plan.md`、`draft.md`，以及可选的 `dependencies.md`、`decision-criteria.md`
3. 判断对象层级与目标 canonical 路径
4. 只提炼 durable 内容，不复制过程痕迹

强约束：

- 不把 `request.md`、`plan.md`、`draft.md` 原样复制进长期目录
- glossary 层默认并入 `reference.md` 的“关键术语”区
- `decision` 可以长期保留单独 `verdict.md`

必须参考：

- `.qoder/skills/openspec-research-promote-canonical/SKILL.md`
- `openspec/schemas/blockchain-research/templates/draft.md`
