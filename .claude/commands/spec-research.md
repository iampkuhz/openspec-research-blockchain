---
description: 由主会话 orchestrator 执行端到端 research pipeline，按 research_type 路由到对应 author agent
argument-hint: "[change-path | research-topic]"
---

# spec-research

本仓库的端到端 command 入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 主会话所有过程说明、阶段汇报与完成总结默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## 路由守卫

执行前先判断任务类型：

- 如果是普通 research change，按下方 research pipeline 执行。
- 如果任务会修改 `openspec/**`、`harness/**`、`.claude/**`、`AGENTS.md`、`docs/governance/**`，且影响 routing、governance、schema、spec、template、workflow、rule 或 repository architecture，则**不要**走 research pipeline，改走 governance review 路由，并显式调用 `governance-review-agent`。

## 执行模型

- 保持在主会话执行；这个 command 本身就是 **orchestrator**。
- **主会话不直接写 `request.md` / `plan.md` / `draft.md`**，这些由 author agent 负责。
- 主会话负责：
  - 路由判断（根据 research_type 选择 author agent）
  - 阶段推进
  - subagent 调度
  - handoff 回收
  - 质量门控

## 规则来源

执行前读取并遵循：

- `harness/workflows/research-pipeline.md`
- 各阶段对应的 OpenSpec spec 与 template
- `.claude/agents/` 中相关 agent contract
- `.claude/agents/CONTRACT.md`（agent 合同校验规范）

## Subagent 使用规则

| 阶段 | 必须使用的 subagent | 禁止行为 |
|------|-------------------|----------|
| 研究写作（primitive） | `primitive-author` | 主会话自行写 request/plan/draft |
| 研究写作（synthesis） | `synthesis-author` | 主会话自行写 request/plan/draft |
| 研究写作（decision） | `decision-author` | 主会话自行写 request/plan/draft |
| sources/ 创建 | `source-evidence-agent` | 主会话/author agent 自行创建 inbox.yaml |
| sources/ 补证据 | `source-evidence-agent` | 主会话自行抓取网页写入 excerpts |
| 架构图 | `diagram-agent` | 主会话/author agent 手写 PlantUML/Mermaid |
| draft 评审 | `review-critic-agent` | 主会话/author agent 自我评审或跳过评审 |
| artifact 提炼 | `publish-agent` | 主会话自行写入 knowledge/ |

**例外**：如果 subagent 确实不可用（报错/超时），主会话可以按相同 contract 串行执行，但必须在完成总结中说明哪个 subagent 被 fallback 了。

## Research Flow

### 1. Change 初始化

如果 `$ARGUMENTS` 是研究主题而不是现有 change 路径：

- 创建 change 目录
- 从 `request.md` 开始推进

如果 `$ARGUMENTS` 指向现有 change，则复用现有 change packet。

创建或读取 `request.md` 后，**立即读取其中的 `research_type` 和 `research_path` 字段**，根据类型路由到对应 author agent：

### 2a. primitive 模式

路由到 `primitive-author`：

```
主会话 → primitive-author →（并行调用 source-evidence-agent）
                         → draft 完成
                         → 主会话调用 review-critic-agent
                         → 主会话调用 publish-agent
```

1. 主会话调用 `primitive-author`，传入 change 路径
2. primitive-author 自行完成 request → plan → draft
3. primitive-author 在 plan 阶段调用 `source-evidence-agent` 创建 sources/
4. primitive-author 在需要时调用 `diagram-agent`
5. primitive-author 完成后，主会话调用 `review-critic-agent` 评审
6. review 通过后，主会话调用 `publish-agent` 提炼 artifact

### 2b. synthesis 模式（三阶段）

**阶段 1 — 依赖发现**：

1. 读取 synthesis `request.md` 中的 `依赖声明` 段
2. 列出所有依赖的 primitive（每个对应一个 `primitive-*` change）
3. 对每个 primitive：
   - 如果 change 不存在：创建 change 目录
   - 调用 `primitive-author` 为该 primitive 执行全链路写作
4. 等待所有 primitive-author 完成（并行执行）

**阶段 2 — synthesis 合成**：

1. 主会话调用 `synthesis-author`，传入 synthesis change 路径
2. synthesis-author 从各 primitive `draft.md` 中提取信息进行横向对比
3. synthesis-author 在需要时调用 `diagram-agent` 或 `source-evidence-agent`
4. synthesis-author 完成后，主会话调用 `review-critic-agent` 评审
5. review 通过后，主会话调用 `publish-agent` 提炼 artifact

**约束**：阶段 2 禁止在阶段 1 所有 primitive 的 draft 完成前开始。

### 2c. decision 模式

路由到 `decision-author`：

```
主会话 → decision-author →（并行调用 source-evidence-agent）
                        → draft 完成
                        → 主会话调用 review-critic-agent
                        → 主会话调用 publish-agent
```

流程同 2a，但 decision-author 输出带 verdict 的决策建议。

### 3. Fallback

- 如果某个适合的 subagent 当前不可用，主会话可以按相同 contract 串行继续，但必须在总结中说明。
- 如果网络限制阻塞来源收集，记录 evidence gap，不要伪造确定性。
- 如果 required PlantUML package 未通过 validation，不要声称 draft 已完成。

## 完成总结

汇报：

- 当前任务最终走的是 research flow 还是 governance routing
- 路由到的 author agent 类型（primitive-author / synthesis-author / decision-author）
- 使用了哪些 specialist subagent
- 各阶段状态
- 最终使用的 change 路径（如有 synthesis，列出所有 primitive change 路径）
- 是否生成了 `sources/`、`diagrams/`、`review/` 与 artifact 文件
- 是否还有 fridge items / evidence gap 未关闭
