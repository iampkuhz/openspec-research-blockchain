---
name: build-plan
description: 用于在 request.md 已经成型后，生成和修订 plan.md；适合把研究计划与来源规划合并为一次集中 review。
---

# 生成研究计划

## 规则来源

本 skill 执行 plan 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `openspec/schemas/blockchain-research/templates/plan.md` —— plan 模板
- `openspec/specs/plan-generation/spec.md` —— plan 阶段规范（入口）
- 相关上位规范（见 `plan-generation/spec.md` 中"与上位规范的关系"）

本 skill 不复制上位规范正文，仅负责 Qoder 的触发入口、使用时机与输入输出。

若 `plan-generation/spec.md` 与其引用的上位规范存在差异，以相关上位规范为准。

## 何时使用（Qoder 特定）

- `request.md` 已经写好
- 需要把问题收紧为可执行计划
- 需要一次性生成预算、来源规划、证据缺口与后续确认问题

## 输入输出（Qoder 特定）

**输入：**
- 目标 change 目录路径

**输出：**
- `plan.md`（写入目标 change 目录下）
- 如确有必要，再补 `decision-criteria.md`（仅 decision 类型）
