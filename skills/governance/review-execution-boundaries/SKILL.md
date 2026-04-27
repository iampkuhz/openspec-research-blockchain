---
name: governance-review-boundaries
description: 当新增或重构 skill 后需要确认分类合理性与 hook 覆盖完整性，或发现多个 skill 职责重叠时使用。
---

# 审查执行层边界

## 适用场景

- 新增或重构 skill 后，需要确认分类是否合理
- 新增 change profile、operation 或 artifact 类型后，需要确认 hook 覆盖是否完整
- 发现多个 skill 职责重叠、分类不清

## 输入

- `skills/` 目录与每个 skill 的 `SKILL.md`
- `scripts/hooks/` 目录
- `openspec/schemas/blockchain-research/` schema 文件

## 输出

- 边界问题清单（重叠 skill、错分类别、命名不一致、未覆盖的生命阶段、缺失的 validator）
- 重构建议

## 读取文件

- `skills/*/SKILL.md` 与 `skills/README.md`
- `scripts/hooks/` 下的所有脚本
- `openspec/schemas/blockchain-research/schema.yaml` 及 profiles/operations

## 写入文件

- 治理评审报告（由调用方决定写入位置）

## 禁止事项

- 不得直接修改 hook 脚本，只输出审查报告与修复建议
- 不得直接重构 skill 文件，只输出审查报告与重构建议

## 自检

- 每个 skill 的 description 是否与其他 skill 有实质性重叠？
- skill 的分类目录是否与 description 中的使用场景一致？
- 每个 profile 是否有对应的 hook validator？
- 新增的 artifact 类型是否被现有 hook 覆盖？
