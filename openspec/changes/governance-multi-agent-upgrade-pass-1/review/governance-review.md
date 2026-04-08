# Governance Review

## 变更概述

本次变更把仓库执行面升级为第一版 multi-agent 模式，主要包含：

- 新增 `harness/agents/` 作为 agent contract 真源
- 更新 `research-pipeline` 与相关 workflow，使其显式声明执行角色
- 更新 `.claude/commands/spec-*.md`，使其从单 agent 阶段命令转为 agent-aware 编排入口
- 修正 `AGENTS.md`、`README.md` 以及关键 rules / skills 中的旧资产模型与旧路径残留
- 为 `.qoder/agents/` 补充基础骨架说明

## 职责边界检查

| 检查项 | 结果 | 说明 |
|--------|------|------|
| OpenSpec 修改是否符合其职责 | pass | 未把 multi-agent 运行细节提升到 OpenSpec 正式规则层 |
| Harness 修改是否符合其职责 | pass | agent roster、workflow 编排、review / publish 协议均位于 Harness |
| 是否存在职责越界 | pass | 命令层只消费 workflow + agent contract，没有重写 artifact contract |
| 是否存在重复定义 | pass | 角色合同集中到 `harness/agents/`，未在多个入口重复定义完整 contract |

## 影响范围

- 受影响 workflows：
  - `harness/workflows/research-pipeline.md`
  - `harness/workflows/source-workflow.md`
  - `harness/workflows/review-workflow.md`
  - `harness/workflows/merge-workflow.md`
  - `harness/workflows/governance-review-workflow.md`
- 受影响 rules：
  - `harness/rules/general/traceability-policy.md`
  - `harness/rules/general/update-policy.md`
  - `harness/rules/general/terminology-policy.md`
- 受影响 skills：
  - `skills/maintenance/*`
  - `skills/openspec-research-build-draft/SKILL.md`
  - `skills/openspec-research-build-research/SKILL.md`
- 受影响入口：
  - `AGENTS.md`
  - `README.md`
  - `.claude/commands/spec-*.md`

## 一致性检查

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 与 `openspec/config.yaml` 一致 | pass | 长期资产模型仍为 `knowledge/analysis` + `knowledge/decisions` |
| 与 `schema.yaml` 一致 | pass | request / plan / draft 主链未改变 |
| 与 boundary 文档一致 | pass | multi-agent 约定全部放在执行层 |
| 与当前命令入口一致 | pass | Claude 命令已切到 agent-aware 模式 |

## 必须修复的问题

无。

## 建议后续处理

| ID | 严重性 | 描述 |
|----|--------|------|
| FOLLOWUP-001 | low | `.qoder/commands/` 仍未完全对齐新 contract，本轮只补了 `.qoder/agents/` skeleton |
| FOLLOWUP-002 | low | 仍有部分非关键 legacy 文档保留旧 topic / atom 术语，建议后续单独 cleanup |

## 评审结论

- [ ] approved - 可直接合并
- [x] approved with minor fixes - 已完成本轮目标，保留少量低优先级 follow-up
- [ ] needs revision - 需要重大修改后重新评审
