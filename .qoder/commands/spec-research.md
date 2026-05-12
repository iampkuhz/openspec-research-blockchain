---
name: spec-research
description: 技术调研总入口，接收自然语言需求、路由研究类型（primitive/synthesis/decision/source_reading）、初始化 change，并按 research pipeline 调度 capsule 直到 Knowledge artifact。
---

# spec-research

技术调研端到端入口。

## 语言

所有过程说明、阶段汇报默认使用简体中文。术语、路径、文件名与关键技术标识符优先保留英文。

## Action Scope

- 接收自然语言研究需求
- 路由 `task_type` 与 `change_operation`
- 初始化一个或多个 child changes
- 按 research pipeline 调度 capsule 直到 `knowledge/**` 写入完成

## 必读文件

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | 仓库导航、任务路由 |
| `openspec/config.yaml` | change root、knowledge root、publish 约束 |
| `openspec/schemas/blockchain-research/schema.yaml` | artifact flow、requires、templates、profiles |
| `harness/workflows/_index.yaml` | 识别 active workflow |
| `harness/workflows/research-pipeline.md` | 端到端编排真源 |
| `harness/governance/agent-boundaries.md` | capsule 边界与 agent 调度原则 |

按阶段还需读取 `harness/rules/_phase_index.yaml`，见 `harness/adapters/tool-capability-matrix.md` 的工具差异说明。

## Artifact Flow

```
request.md -> plan.md -> sources/source-pack.md -> sources/evidence-map.md -> [notes/*.md] / [claims/*.md] -> [diagrams/]* -> draft.md -> review.md -> publish.md -> knowledge/**
```

硬性约束：
- `draft.md` 是当前 change 的唯一主候选产物
- 不得在 review gate 和 publish mapping 之前写 `knowledge/**`
- 复杂任务必须拆成多个 child changes

## 何时调用哪些 Agents

| capsule | 调用对象 | 主要输出 |
|---------|---------|---------|
| intake | `primitive-author` / `synthesis-author` / `decision-author`（mode=intake） | `request.md`、`plan.md` |
| source | `source-evidence-agent` | `sources/source-pack.md`、`sources/evidence-map.md` |
| diagram | `diagram-agent` | `diagrams/**` |
| draft | 对应 author agent（mode=draft） | `draft.md` |
| review | `review-critic-agent` | `review.md` |
| publish | `publish-agent` | `publish.md`、`knowledge/**` |

Agent 调用规则见 `harness/governance/agent-boundaries.md` 的"调用与等待策略"。前台调用为主，禁止 busy-wait。

## 完成总结

汇报：
- 当前任务拆解为几个 changes
- 每个 change 的 `task_type` 与路径
- 每个 change 的 capsule 完成状态
- 最终写入的 `knowledge/**` 路径
- 遇到的 blocker（如有）
