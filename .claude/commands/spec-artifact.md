---
description: 将通过评审的 draft 提升为 canonical artifact
argument-hint: "[change-path | change-name]"
---

# spec-artifact

`artifact / publish` 阶段的主会话 orchestrator 入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 主会话所有过程说明、阶段汇报与完成总结默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## 执行模型

- 本 command 是**渐进式执行**模式下的 artifact/publish 阶段入口，保持在主会话执行。
- 适用于用户只想完成 artifact 提炼、暂不推进其他阶段的场景。
- 如果需要端到端执行（request → plan → draft → review → artifact），应使用 `/spec-research` 而非本 command。
- 主会话负责 review gate 检查、目标路径确认与最终写入。
- durable 内容提炼由主会话显式调用 `publish-agent` subagent 负责。
- 如果当前任务实际属于 governance / routing / repository architecture 变更，切换到 governance review 路由，并显式调用 `governance-review-agent`。治理路由判断以 `docs/governance/openspec-harness-boundary.md` 为准。
- 不要让一个 subagent 继续调用其他 subagent。所有 specialist 都由主会话协调。

## 规则来源

执行前读取并遵循：

- `harness/rules/_phase_index.yaml`（读取 `artifact` 阶段依赖）
- `openspec/schemas/blockchain-research/schema.yaml`
- `harness/workflows/artifact-phase.md`
- `openspec/specs/canonical-output-model/spec.md`
- `harness/workflows/merge-workflow.md`

## 执行步骤

1. 从 `$ARGUMENTS`、当前工作目录或上下文中解析目标 change 目录。
2. 读取 `request.md`、`plan.md`、`draft.md` 与 `review/review-summary.md`。
3. 确认 review 结论为 `approved` 或 `approved with minor fixes`，且不存在未关闭的 high-severity issue。
4. 由主会话显式调用 `publish-agent` subagent 提炼 canonical artifact 输出。
5. 完成前检查输出路径是否符合 OpenSpec 规定的 `knowledge/analysis/` / `knowledge/decisions/` canonical layout。

## 完成总结

汇报：

- 最终使用的 change 路径
- 写入了哪些长期文件
- 是否执行了 update impact scan
- apply / merge 前是否仍有 blocker
