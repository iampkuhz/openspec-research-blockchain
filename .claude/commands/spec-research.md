---
description: 技术调研总入口，接收自然语言需求、路由研究类型、初始化 change 并生成 request.md 与 plan.md
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

## 参考 Skills

本命令的参考 skill 包如下。优先参考对应 skill 的执行逻辑；如果 Claude Code 未自动加载 skill，则按本命令内联步骤执行。

| Capability | Skill name | Skill path | Fallback |
|---|---|---|---|
| 路由研究任务 | `openspec-route-research-change` | `skills/openspec-flow/route-research-change/SKILL.md` | 使用本命令的 Routing Rules |
| 初始化 change | `openspec-init-change` | `skills/openspec-flow/init-change/SKILL.md` | 使用本命令的 Init Steps |
| 生成请求与计划 | `openspec-build-request-plan` | `skills/openspec-flow/build-request-plan/SKILL.md` | 使用本命令的 Build Steps |

如果 Claude Code 未自动加载上述 skill，必须按本命令内联步骤执行，不得中止。

## 执行步骤

### 1. 接收需求

用户以自然语言传入研究需求（`$ARGUMENTS`）。

### 2. 路由研究类型

参考 `openspec-route-research-change` skill（`skills/openspec-flow/route-research-change/SKILL.md`）。

**Routing Rules（Fallback）**：

- 定义/描述某个机制、组件、协议、工具 → `primitive`
- 横向对比多个方案/技术/框架 → `synthesis`
- 在多个候选方案中做选择 → `decision`
- 仅回源阅读验证来源 → `source_reading`

如果任务复杂（涉及多个最终 Knowledge artifact 或覆盖 3+ 独立主题域），拆成多个 child changes。

### 3. 初始化 change

参考 `init-change` skill（`skills/openspec-flow/init-change/SKILL.md`）。

- 创建 `openspec/changes/<change-id>/` 目录
- 生成 `change.yaml`（含 `task_type`、`profile`、`operation`）
- 创建 `sources/`、`notes/`、`claims/` 空目录

### 4. 生成 request.md

参考 `build-request-plan` skill（`skills/openspec-flow/build-request-plan/SKILL.md`）。

- 明确研究目标、范围边界、非目标
- 填写研究对象类型、研究路径、核心问题、触发原因
- 不得包含切断来源验证的表述（参见下方二次研究来源保护）

### 5. 生成 plan.md

参考 `build-request-plan` skill。

- 规划研究路径、关键来源、预期产出
- plan 完成后停止，**不直接生成 draft.md**

### 6. 二次研究来源保护

在创建或校验 `request.md` 时，必须检查"范围与非目标"段：

- **二次研究禁止切断来源验证**：request.md 的"非目标"中**不得**包含"不扩展研究新来源"、"不引入新外部来源"、"基于既有分析已确认的事实"等切断来源搜索的表述。
- **既有 artifact 是起点，不是天花板**：二次研究的 request 必须明确既有 artifact 仅作为参考基线，仍需回源到原始项目仓库、文档、commit 历史等验证和补充信息。
- 如发现 request.md 已包含此类自我设限表述，**必须先修正 request.md 再继续**。

## 完成总结

汇报：

- 当前任务拆解为几个 changes
- 每个 change 的 `task_type`（primitive / synthesis / decision）
- 每个 change 的路径
- request.md 与 plan.md 的生成状态
- 是否建议用户调用 `/spec-research-step` 推进下一步
