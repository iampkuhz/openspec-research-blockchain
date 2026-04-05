---
name: build-draft
description: 用于在 plan.md review 通过后，生成和修订 draft.md；适合把 glossary、analysis、verdict 合并为一次集中 review。
---

# 生成研究草稿

## 真理之源

**本 skill 的核心约束和规则统一由以下规范定义**：

- `openspec/specs/draft-generation/spec.md` —— Draft 生成规范（真理之源）

本 adapter 仅定义 Qoder 平台特定的使用时机和输出要求。

## 何时使用（Qoder 特定）

- `plan.md` 已经通过 review
- 来源规划已经足以支撑第一轮正文
- 需要把术语、分析、有限结论合并为一次 review

## 输出要求（Qoder 特定）

- `draft.md`
- 严格遵守 `openspec/specs/draft-generation/spec.md` 中的所有约束

## 依赖

- `feipi-gen-plantuml-code` skill：所有 PlantUML 图必须通过此 skill 生成和校验
