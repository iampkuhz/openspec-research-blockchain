---
description: 技术调研总入口，接收自然语言需求、路由研究类型、初始化 change，并按 research pipeline 调度 capsule 直到 Knowledge artifact
argument-hint: "<research-topic>"
---

# spec-research

技术调研端到端入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 所有过程说明、阶段汇报默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## Command 定位

`/spec-research` 负责**整体编排**：

- 接收自然语言研究需求
- 路由 `task_type` 与 `change_operation`
- 初始化一个或多个 child changes
- 按 `research-pipeline.md` 调度 intake / source / draft / review / publish capsule
- 在每个 change 完成后汇报最终 `knowledge/**` 写入路径或 blocker

本 command 不展开 subagent 内部 workflow，不复制 request / source / draft / review / publish 的质量规则。具体规则由 Harness workflow、phase index、agent contract 和 OpenSpec schema 承担。

## 必读文件

### 启动时读取

| 文件 | 作用 |
|---|---|
| `openspec/config.yaml` | 确认 change root、knowledge root、apply / publish 约束 |
| `openspec/schemas/blockchain-research/schema.yaml` | 确认 artifact flow、requires、templates、profiles、operations |
| `harness/workflows/_index.yaml` | 找到 active workflow |
| `harness/workflows/research-pipeline.md` | 端到端编排真源 |
| `harness/governance/agent-boundaries.md` | capsule 边界与 agent 调度原则 |

### 按阶段读取

| 阶段 | 读取入口 | 目的 |
|---|---|---|
| route / intake | `harness/workflows/research-intake-routing.md` | 判断 task_type、拆 child changes、初始化 change |
| phase dependencies | `harness/rules/_phase_index.yaml` | 在进入具体阶段时加载必要 rules / specs / workflows |
| task type | `harness/workflows/<task-type>-workflow.md` | 确认 primitive / synthesis / decision / source_reading 的类型边界 |
| agent dispatch | `.claude/agents/CONTRACT.md` + 对应 agent 文件 | 确认 subagent 输入、写入范围和完成信号 |

## Artifact Flow

正式 artifact 依赖以 schema 为准，command 只按状态推进：

```text
request.md
  -> plan.md
  -> sources/source-pack.md
  -> sources/evidence-map.md
  -> [notes/*.md] / [claims/*.md]
  -> draft.md
  -> review.md
  -> publish.md
  -> knowledge/**
```

硬性约束：

- `draft.md` 是当前 change 的唯一主候选产物。
- 不得生成 `work-products/*.md`。
- 不得在 review gate 和 publish mapping 之前写 `knowledge/**`。
- 复杂任务必须拆成多个 child changes。
- decision 任务必须保留 `decision-criteria.md -> draft.md#Verdict Draft -> knowledge/decisions/**/verdict.md` 的追溯链。

## 执行过程

### 1. 接收与路由

1. 读取用户研究需求。
2. 参考 `openspec-route-research-change` skill 与 `research-intake-routing.md` 判断 `task_type`：
   - 单个机制 / 协议 / 产品深度研究 → `primitive`
   - 多对象横向对比 / 演进分析 → `synthesis`
   - 场景驱动选型或推荐 → `decision`
   - 仅阅读和消化来源 → `source_reading`
3. 判断 `change_operation`：`create` 或 `update`。
4. 如果任务覆盖多个最终 Knowledge artifact，拆成 child changes。

### 2. 初始化 change

对每个 change：

1. 创建或定位 `openspec/changes/<change-id>/`。
2. 生成 `change.yaml`。
3. 创建必要 staging 目录。
4. 不在主会话直接写 `request.md`、`plan.md`、`draft.md`。

### 3. 调度 capsule

主会话只调度到 capsule 粒度：

| capsule | 调用对象 | 主要输出 | command 只关心 |
|---|---|---|---|
| intake | 对应 author agent，`mode=intake` | `request.md`、`plan.md`、按需 `decision-criteria.md` | 产物路径、依赖 handoff、blocker |
| source | `source-evidence-agent` | `sources/source-pack.md`、`sources/evidence-map.md`、按需 `notes/*.md`、`claims/*.md` | sources 是否就绪 |
| draft | 对应 author agent，`mode=draft` | `draft.md`、按需 `diagrams/**` | draft 是否就绪；diagram 由 author agent 作为 draft 子步骤直接调用 |
| review | `review-critic-agent` | `review.md` | verdict 与 high severity blocker |
| publish | `publish-agent` | `publish.md`、合法 `knowledge/**` targets | 写入路径、归档状态、blocker |

不要把 subagent 的 evidence gap 细节、评分过程、traceability 审计过程或图表内部生成步骤返回主会话；这些内容应写入对应 artifact。

### 4. 推进状态机

对每个 change 重复：

1. 检测缺失的下一项 artifact。
2. 按 `research-pipeline.md` 选择 capsule。
3. 调用对应 agent 或复用 `/spec-research-step` 推进单 change。
4. 检查产物存在且符合 schema artifact flow。
5. 遇到 blocker、review `needs revision` 或 publish target 不合法时停止。
6. `knowledge/**` 写入完成后结束该 change。

### 5. 依赖型任务

- synthesis：依赖 primitive draft 未完成时，先推进 primitive child changes。
- decision：候选方案 primitive / synthesis 未完成时，先补齐依赖；不得让 decision author 独立评估候选方案。

## 完成总结

汇报：

- 当前任务拆解为几个 changes
- 每个 change 的 `task_type`
- 每个 change 的路径
- 每个 change 的 capsule 完成状态
- 最终写入的 `knowledge/**` 路径
- 遇到的 blocker（如有）
