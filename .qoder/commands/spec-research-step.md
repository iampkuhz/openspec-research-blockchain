---
name: spec-research-step
description: 推进当前 change 的下一步，自动检测缺失产物并执行 sources / draft / review / publish 阶段。
---

# spec-research-step

推进单个 change 的下一步。阶段状态机入口。

## 语言

所有过程说明、阶段汇报默认使用简体中文。

## Action Scope

- 定位一个现有 change
- 读取 schema / phase index / workflow
- 检测下一项缺失 artifact
- 调用对应 capsule 或 agent
- review 通过后继续 publish 到 `knowledge/**`

## 必读文件

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | 仓库导航、任务路由 |
| `openspec/config.yaml` | change root、knowledge root、publish 约束 |
| `openspec/schemas/blockchain-research/schema.yaml` | artifact flow、requires、templates |
| 当前 change 的 `change.yaml` | `task_type`、`change_operation`、artifacts、publish_targets |
| `harness/rules/_phase_index.yaml` | 按阶段加载必要 rules / specs / workflows |
| `harness/governance/agent-boundaries.md` | agent 调度、调用与等待策略 |
| `harness/workflows/research-step-execution.md` | 阶段执行真源 |

工具差异见 `harness/adapters/tool-capability-matrix.md`。

## Artifact Flow

```
request.md -> plan.md -> sources/source-pack.md -> sources/evidence-map.md -> [notes/*.md] / [claims/*.md] -> [diagrams/]* -> draft.md -> review.md -> publish.md -> knowledge/**
```

硬性约束：
- 当前 change 必须已有 `change.yaml`
- `draft.md` 是唯一主候选产物
- 只有 publish 阶段可以写 `knowledge/**`

## 自动下一步判断

完整状态机以 `harness/workflows/research-step-execution.md` 和 `harness/rules/_phase_index.yaml` 为准。
下表是简化版判断逻辑：

| 状态 | 下一步 | 调用对象 |
|------|--------|---------|
| 缺少 `request.md` 或 `plan.md` | 返回 intake 缺失，建议 spec-research | 不在 step 内补 intake |
| 缺少 `sources/source-pack.md` | source capsule | `source-evidence-agent` |
| 缺少 `sources/evidence-map.md` | source capsule | `source-evidence-agent` |
| decision 缺少 `decision-criteria.md` | decision intake support | `decision-author` 或 `research-build-decision-criteria` |
| plan 要求正式图表且 `diagrams/` 缺失 | diagram capsule | `diagram-agent` |
| 缺少 `draft.md` | draft capsule | 对应 author agent（mode=draft） |
| 缺少 `review.md` | review capsule | `review-critic-agent` |
| review 未通过 | 停止 | 返回 repair blocker |
| 缺少 `publish.md` | publish capsule | `publish-agent` |
| 全部完成 | 汇报完成 | 无 |

## 禁止事项

- 不要跳过 `review.md` 直接 publish
- 不要跳过 `publish.md` 直接写 `knowledge/**`
- 不要从 `request.md` 或 `plan.md` 直接生成 `knowledge/**`

## 完成总结

汇报：
- 当前 change 路径
- 本次执行阶段
- 生成或更新的文件
- review verdict（如涉及）
- 写入的 `knowledge/**` 路径（如涉及 publish）
- 下一步建议或 blocker
