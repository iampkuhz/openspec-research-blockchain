---
name: openspec-route-research-change
description: 当用户给出自然语言研究需求，需要判断属于 primitive / synthesis / decision / source_reading 类型，并在复杂需求时拆分 child changes 时使用。
---

# 路由研究需求

## 适用场景

- 用户给出自然语言研究需求，需要判断属于哪种研究类型。
- 需要为 change 选择正确的 profile（`primitive` / `synthesis` / `decision`）。
- 复杂需求需要拆成多个 child changes 时，确定拆分策略。

## 输入

- 用户研究需求的自然语言描述。

## 输出

- 确定的 `task_type`（`primitive` / `synthesis` / `decision`）。
- 对应的 `change.yaml` 中的 `profile` 与 `operation` 值。
- 如需拆分，给出 change graph 建议。

## 读取文件

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/profiles/*.schema.yaml`
- 已有的 `openspec/changes/` 目录，避免重复创建。

## 写入文件

不直接写入文件，仅输出路由判断结果。由 `init-change` skill 负责写入。

## 路由规则（Fallback Execution）

当 Skill 工具不可用时，按以下规则手动判断：

### task_type 判断

| 需求特征 | task_type | 示例 |
|----------|-----------|------|
| 定义/描述某个机制、组件、协议、工具 | `primitive` | "调研 EIP-4337 的机制" |
| 横向对比多个方案/技术/框架的异同与演进 | `synthesis` | "对比 5 个 AI code review 框架" |
| 在多个候选方案中做选择判断 | `decision` | "选择用 OpenTelemetry 还是 Prometheus" |
| 仅回源阅读并验证来源，不生成新分析 | `source_reading` | "验证既有 artifact 中的来源" |

### 复杂任务拆分规则

满足以下任一条件时，拆成多个 child changes：

1. 涉及多个最终 Knowledge artifact（如同时需要 primitive + decision）
2. 研究对象覆盖 3 个以上独立主题域（如同时调研链、共识、DEX、Token 经济模型）
3. 需要对比的主题超过 5 个，且每个需要深度分析

拆分格式：

```yaml
parent: <parent-change-id>
children:
  - id: <child-1-id>
    task_type: primitive
    instruction: "..."
    publish_target: knowledge/...
  - id: <child-2-id>
    task_type: decision
    instruction: "..."
    publish_target: knowledge/decisions/...
```

### change graph 依赖

如果拆分为多个 child changes，必须声明依赖：

```yaml
# child 2 依赖 child 1 的 draft
child-2:
  blocked_by: [child-1]
  # child-2 需要 child-1 的对比分析结果作为输入
```

## 禁止事项

- 不得跳过类型判断直接创建 change。
- 不得将单一复杂需求硬塞进一个 change。
- 不得引用 `work-products/*.md`。
- 不得直接写 draft.md。
- 不得直接写 knowledge/**。

## 自检

- 研究类型是否与 `schema.yaml` 中定义的 profile 一致？
- 如果拆分为多个 changes，每个 change 是否对应一个独立 publish target？
- 是否需要既有 artifact 作为参考基线？如有，标记为二次研究。
