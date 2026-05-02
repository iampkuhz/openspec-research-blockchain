---
description: 技术调研总入口，接收自然语言需求、路由研究类型、初始化 change，并按独立 capsule 调度 agents 推进到最终 Knowledge artifact
argument-hint: "<research-topic>"
---

# spec-research

技术调研总入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 所有过程说明、阶段汇报默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## OpenSpec Research Flow Contract

本命令必须遵守当前仓库的 `blockchain-research` schema。

主流程：

```text
request.md -> plan.md -> sources/source-pack.md -> sources/evidence-map.md -> [notes/<source-slug>.md]* -> [claims/<claim-slug>.md]* -> draft.md -> review.md -> publish.md -> knowledge/**
```

执行前必须读取：

- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/schema.yaml`
- 当前 change 的 `change.yaml`
- `openspec/schemas/blockchain-research/profiles/<task_type>.schema.yaml`
- `openspec/schemas/blockchain-research/operations/<change_operation>.schema.yaml`

硬性约束：

- `draft.md` 是当前 change 的唯一主候选产物。
- 不得生成 `work-products/*.md`。
- 不得直接写 `knowledge/**`，除非当前命令是 `/spec-research-publish`，且 `publish.md` 已定义合法映射。
- 复杂任务必须拆成多个 child changes。
- decision 任务必须明确 `decision-criteria.md -> draft.md#Verdict Draft -> decision-verdict.md -> knowledge/decisions/**/verdict.md` 的关系。

## 参考 Skills / Stage Commands

本命令是 orchestrator 入口，只直接处理路由、初始化和 agent / stage command 调度。具体 artifact 生成优先交给对应 capsule 的 agent 或阶段 command。

| Capability | Skill name | Skill path | Fallback |
|---|---|---|---|
| 路由研究任务 | `openspec-route-research-change` | `skills/openspec-flow/route-research-change/SKILL.md` | 使用本命令的 Routing Rules |
| 初始化 change | `openspec-init-change` | `skills/openspec-flow/init-change/SKILL.md` | 使用本命令的 Init Steps |
| 单 change 阶段推进 | `/spec-research-step` | `.claude/commands/spec-research-step.md` | 按 `research-step-execution.md` 调用对应 capsule |
| 发布到 Knowledge | `/spec-research-publish` | `.claude/commands/spec-research-publish.md` | 按 `research-publish-flow.md` 调用 publish capsule |

如果 Claude Code 未自动加载 skill，仍按本命令引用的 Harness workflow 和 agent contract 执行，不得中止。

## 执行步骤

### 1. 接收需求

用户以自然语言传入研究需求（`$ARGUMENTS`）。

### 2. 读取编排真源

按顺序读取：

- `harness/workflows/_index.yaml`
- `harness/workflows/research-pipeline.md`
- `harness/rules/_phase_index.yaml`
- `harness/governance/agent-boundaries.md`

本 command 只作为 orchestrator 入口，不在本文件重写 pipeline、agent 边界、request 规则、sources 规则、review 规则或 publish 规则。

### 3. 路由研究类型与 change

参考：

- `openspec-route-research-change` skill（`skills/openspec-flow/route-research-change/SKILL.md`）
- `harness/workflows/research-intake-routing.md`
- `harness/workflows/primitive-workflow.md`
- `harness/workflows/synthesis-workflow.md`
- `harness/workflows/decision-workflow.md`
- `harness/workflows/source-reading-workflow.md`

Fallback routing：

- 定义/描述某个机制、组件、协议、工具 → `primitive`
- 横向对比多个方案/技术/框架 → `synthesis`
- 在多个候选方案中做选择 → `decision`
- 仅回源阅读验证来源 → `source_reading`

如果任务复杂（涉及多个最终 Knowledge artifact 或覆盖 3+ 独立主题域），按 `research-pipeline.md` 拆成 child changes。

### 4. 初始化 change

参考 `openspec-init-change` skill（`skills/openspec-flow/init-change/SKILL.md`）和 `research-intake-routing.md`：

- 创建或定位 `openspec/changes/<change-id>/`
- 生成 `change.yaml`
- 创建 staging 目录
- 不在主会话中直接写 `request.md`、`plan.md`、`draft.md`

### 5. 按 capsule 调度 agents

按照 `harness/workflows/research-pipeline.md` 和 `harness/governance/agent-boundaries.md` 推进：

| capsule | 调用对象 | 主要输出 |
|---|---|---|
| intake | 对应 author agent，`mode=intake` | `request.md`、`plan.md` |
| source | `source-evidence-agent` | `sources/source-pack.md`、`sources/evidence-map.md`、按需 `notes/*.md`、`claims/*.md` |
| draft | 对应 author agent，`mode=draft` | `draft.md` |
| review | `review-critic-agent` | `review.md` |
| publish | `publish-agent` 或 `/spec-research-publish` | `publish.md`、合法 `knowledge/**` targets |

每次 agent 调用只消费最小输入，返回完成状态、产物路径和 blocker。主会话不接收或复述中间分析细节。

### 6. 状态循环

主会话按 artifact 状态循环：

1. 检测当前 change 缺少的下一项 artifact。
2. 根据 `research-pipeline.md` 选择 capsule。
3. 调用对应 agent 或阶段 command。
4. 检查产物是否存在且符合 OpenSpec artifact flow。
5. 遇到 blocker、`needs revision` 或 publish target 不合法时停止。
6. 所有 publish targets 写入后结束。

### 7. 特殊路由

- synthesis：必须先确保依赖 primitive 的 `draft.md` 就绪。
- decision：必须确保候选方案依赖的 primitive / synthesis artifacts 就绪；`decision-criteria.md` 按 decision workflow 生成或校验。
- diagram：需要正式图表时，由主会话调用 `diagram-agent`，不得由 author agent 嵌套调用。

## 完成总结

汇报：

- 当前任务拆解为几个 changes
- 每个 change 的 `task_type`（primitive / synthesis / decision）
- 每个 change 的路径
- 每个 change 的 pipeline 完成状态（成功 / 遇到 blocker）
- 最终 Knowledge artifact 的写入路径
