---
name: build-draft
description: 用于在 plan.md review 通过后，生成和修订 draft.md；适合把 glossary、analysis、verdict 合并为一次集中 review。
---

# 生成研究草稿

## 规则来源

本 skill 执行 draft 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `openspec/schemas/blockchain-research/templates/draft.md` —— draft 模板
- `openspec/specs/draft-generation/spec.md` —— draft 阶段规范（入口）
- `openspec/specs/diagram-policy/spec.md` —— 图表政策
- 相关上位规范（见 `draft-generation/spec.md` 中"与上位规范的关系"）

本 skill 不复制上位规范正文，仅负责 Qoder 的触发入口、使用时机与输入输出。

若 `draft-generation/spec.md` 与其引用的上位规范存在差异，以相关上位规范为准。

## 何时使用（Qoder 特定）

- `plan.md` 已经通过 review
- 来源规划已经足以支撑第一轮正文
- 需要把术语、分析、有限结论合并为一次 review

## 输入输出（Qoder 特定）

**输入：**
- 目标 change 目录路径

**输出：**
- `draft.md`（写入目标 change 目录下）

## 依赖

- PlantUML 生成工具：所有 PlantUML 图必须通过相应工具生成和校验
