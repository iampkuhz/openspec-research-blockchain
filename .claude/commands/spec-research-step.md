---
description: 推进当前 change 的下一步，自动检测缺失产物并执行 sources / draft / review / publish 阶段
argument-hint: "[change-id | change-path]"
---

# spec-research-step

推进单个 change 的下一步。这个 command 是阶段状态机入口，包含 publish 阶段；不再需要单独的发布 command。

用户传入参数：`$ARGUMENTS`（change-id 或 change 路径，可选）

## 语言输出约束

- 所有过程说明、阶段汇报默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## Command 定位

`/spec-research-step` 负责**单 change 状态推进**：

- 定位一个现有 change
- 读取 schema / phase index / workflow
- 检测下一项缺失 artifact
- 调用对应 capsule 或 skill
- 在 review 通过后继续 publish 到 `knowledge/**`

本 command 不展开 source / author / review / publish agent 的内部工作流，只说明何时调用它们、需要哪些阶段级输入、产出什么文件。

## 必读文件

### 启动时读取

| 文件 | 作用 |
|---|---|
| `openspec/config.yaml` | 确认 active change root、archive root、knowledge root 和 publish 约束 |
| `openspec/schemas/blockchain-research/schema.yaml` | 确认 artifact flow、requires、templates、profiles、operations |
| 当前 change 的 `change.yaml` | 确认 `task_type`、`change_operation`、artifacts、publish_targets |
| `harness/rules/_phase_index.yaml` | 按阶段加载必要 rules / specs / workflows |

### 按阶段读取

| 阶段 | 读取入口 | 目的 |
|---|---|---|
| sources | `harness/workflows/source-workflow.md` | 指导 source capsule，不展开来源抓取细节 |
| draft | `harness/workflows/research-step-execution.md` + task workflow | 确认 draft 前置和 task_type 边界 |
| review | `harness/workflows/research-step-execution.md` | 确认 review 产物和 verdict |
| publish | `harness/workflows/research-publish-flow.md` | 确认 publish gate、publish.md、knowledge target |
| agent | `.claude/agents/CONTRACT.md` + 对应 agent 文件 | 确认 agent 写入范围和完成信号 |

## Artifact Flow

按 schema 顺序推进：

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

- 当前 change 必须已有 `change.yaml`。
- `draft.md` 是唯一主候选产物。
- 不得生成 `work-products/*.md`。
- 只有 publish 阶段可以写 `knowledge/**`，且必须通过 `review.md` 与 `publish.md`。
- 如果发现当前 change 实际需要多个最终 Knowledge artifact，停止并建议拆 child changes。

## 自动下一步判断

按以下优先级检测当前 change 缺少的产物：

| 状态 | 下一步 | 调用对象 |
|---|---|---|
| 缺少 `request.md` 或 `plan.md` | 返回 intake 缺失，建议 `/spec-research` 或 author `mode=intake` | 不在 step 内补 intake |
| 缺少 `sources/source-pack.md` | source capsule | `source-evidence-agent` |
| 缺少 `sources/evidence-map.md` | source capsule | `source-evidence-agent` |
| plan 要求 notes 且缺少 `notes/*.md` | source capsule | `source-evidence-agent` 或 source note skill |
| plan 要求 claims 且缺少 `claims/*.md` | source capsule | `source-evidence-agent` 或 evidence skill |
| decision 缺少 `decision-criteria.md` | decision intake support | `decision-author mode=intake` 或 `research-build-decision-criteria` |
| 缺少 `draft.md` | draft capsule | 对应 author agent `mode=draft` |
| 缺少 `review.md` | review capsule | `review-critic-agent` |
| review 未通过 | 停止 | 返回 repair blocker |
| 缺少 `publish.md` | publish capsule | `publish-agent` 或 publish skills |
| publish targets 未写入 `knowledge/**` | publish capsule | `publish-agent` 或 publish skills |
| 全部完成 | 汇报完成 | 无 |

## 阶段执行

### sources

只把来源阶段调度给 `source-evidence-agent` 或等价 skill。command 只检查：

- `sources/source-pack.md` 是否存在
- `sources/evidence-map.md` 是否存在
- blocker 是否影响 draft

### draft

按 `task_type` 调用对应 author agent 的 `mode=draft`：

- `primitive` → `primitive-author`
- `synthesis` → `synthesis-author`
- `decision` → `decision-author`

command 只检查 `draft.md` 是否生成、是否返回补 sources / diagrams handoff。

### review

调用 `review-critic-agent`。command 只读取 verdict：

- `approved`
- `approved with minor fixes`
- `needs revision`

`needs revision` 时停止，不进入 publish。

### publish

调用 `publish-agent` 或以下 publish skills：

- `openspec-build-publish-plan`
- `publish-validate-targets`
- `publish-render-artifact`
- `publish-render-verdict`
- `publish-merge-knowledge`

publish 阶段必须：

1. 检查 `draft.md` 存在。
2. 检查 `review.md` verdict 为 `approved` 或 `approved with minor fixes`。
3. 生成或校验 `publish.md`。
4. 校验 publish targets 符合 schema 与 `openspec/config.yaml`。
5. 写入合法 `knowledge/**/artifact.md` 和 decision `verdict.md`（如适用）。

## 禁止事项

- 不要跳过 `review.md` 直接 publish。
- 不要跳过 `publish.md` 直接写 `knowledge/**`。
- 不要从 `request.md` 或 `plan.md` 直接生成 `knowledge/**`。
- 不要在 step command 内展开 subagent 的内部分析细节。

## 完成总结

汇报：

- 当前 change 路径
- 本次执行的阶段
- 生成或更新的文件
- review verdict（如本次涉及 review / publish）
- 写入的 `knowledge/**` 路径（如本次涉及 publish）
- 下一步建议或 blocker
