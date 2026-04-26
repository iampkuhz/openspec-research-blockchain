---
description: 为 research change 生成或修订 plan.md
argument-hint: "[change-path | change-name]"
---

# spec-plan

`plan` 阶段的主会话 orchestrator 入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 主会话所有过程说明、阶段汇报与完成总结默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## 执行模型

- 本 command 是**渐进式执行**模式下的 plan 阶段入口，保持在主会话执行。
- 适用于用户只想先完成 plan 阶段、暂不推进完整 pipeline 的场景。
- 如果需要端到端执行（request → plan → draft → review → artifact），应使用 `/spec-research` 而非本 command。
- 主会话负责路由、handoff 回收与最终质量门控。
- `plan.md` 的主链写作保留在主会话；不要再额外拆出 author subagent。
- 需要来源收集、链接验证或 evidence gap 分析时，由主会话显式调用 `source-evidence-agent` subagent。
- 如果当前任务实际属于 governance / routing / repository architecture 变更，切换到 governance review 路由，并显式调用 `governance-review-agent`。治理路由判断以 `docs/governance/openspec-harness-boundary.md` 为准。
- 不要让一个 subagent 去继续调用另一个 subagent。所有 specialist 都由主会话调度。

## 规则来源

执行前读取并遵循：

- `harness/rules/_phase_index.yaml`（读取 `plan` 阶段依赖）
- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/plan.md`
- `harness/workflows/plan-phase.md`
- 需要来源支持时读取 `harness/workflows/source-workflow.md`

## 执行步骤

1. 从 `$ARGUMENTS`、当前工作目录或上下文中解析目标 change 目录。
2. 先读取 `request.md`、plan template 与 stage spec。
3. 由主会话直接生成或修订 `plan.md`，先完成问题拆解、范围、来源规划与完成标准。
4. 如需补来源、验证链接或补 evidence gap，由主会话显式调用 `source-evidence-agent`，再把结果并回 `plan.md`。
5. 只有当 `plan.md` 满足 canonical section、来源规划、evidence gap 与 completion criteria 要求时，才能声称该阶段完成。

## 完成总结

汇报：

- 最终使用的 change 路径
- 更新了哪些 section
- 是否创建或更新了 `sources/`
- 仍然冻结中的 source / dependency gap
- 进入 `/spec-draft` 前建议用户重点 review 的部分

## Validation 自检

- [ ] `plan.md` 的 study_depth / source_plan 与 `request.md` 的 `research_type` 匹配
- [ ] 来源规划包含 L1/L2/L3/L4 分级
- [ ] evidence gap 已显式记录
- [ ] 图表范围（如需要）已声明
- [ ] 完成标准与 `request.md` 的核心问题一一对应
- [ ] 文件符合 `openspec/schemas/blockchain-research/templates/plan.md` 模板结构
