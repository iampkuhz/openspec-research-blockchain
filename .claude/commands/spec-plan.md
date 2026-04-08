---
description: 为 research change 生成或修订 plan.md
argument-hint: "[change-path | change-name]"
---

# spec-plan

`plan` 阶段的主会话 orchestrator 入口。

用户传入参数：`$ARGUMENTS`

## 执行模型

- 保持在主会话执行。主会话负责路由、handoff 回收与最终质量门控。
- `plan.md` 的主写作者由主会话显式调用 `research-author-agent` subagent。
- 需要来源收集、链接验证或 evidence gap 分析时，由主会话显式调用 `source-evidence-agent` subagent。
- 如果当前任务实际属于 governance / routing / repository architecture 变更，切换到 governance review 路由，并显式调用 `governance-review-agent`。
- 不要让一个 subagent 去继续调用另一个 subagent。所有 specialist 都由主会话调度。

## 规则来源

执行前读取并遵循：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/plan.md`
- `openspec/specs/plan-generation/spec.md`
- 需要来源支持时读取 `harness/workflows/source-workflow.md`

## 执行步骤

1. 从 `$ARGUMENTS`、当前工作目录或上下文中解析目标 change 目录。
2. 先读取 `request.md`、plan template 与 stage spec。
3. 由主会话显式调用 `research-author-agent` subagent 生成或修订 `plan.md`。
4. 如需补来源、验证链接或补 evidence gap，由主会话显式调用 `source-evidence-agent`，再把结果并回 `plan.md`。
5. 只有当 `plan.md` 满足 canonical section、来源规划、evidence gap 与 completion criteria 要求时，才能声称该阶段完成。

## 完成总结

汇报：

- 最终使用的 change 路径
- 更新了哪些 section
- 是否创建或更新了 `sources/`
- 仍然冻结中的 source / dependency gap
- 进入 `/spec-draft` 前建议用户重点 review 的部分
