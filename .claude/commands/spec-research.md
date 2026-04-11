---
description: 由主会话 orchestrator 执行端到端 research pipeline
argument-hint: "[change-path | research-topic]"
---

# spec-research

本仓库的端到端 command 入口。

用户传入参数：`$ARGUMENTS`

## 路由守卫

执行前先判断任务类型：

- 如果是普通 research change，按下方 research pipeline 执行。
- 如果任务会修改 `openspec/**`、`harness/**`、`.claude/**`、`AGENTS.md`、`docs/governance/**`，且影响 routing、governance、schema、spec、template、workflow、rule 或 repository architecture，则**不要**走 research pipeline，改走 governance review 路由，并显式调用 `governance-review-agent`。

## 执行模型

- 保持在主会话执行；这个 command 本身就是 orchestrator。
- 主会话负责：
  - 路由判断
  - 阶段推进
  - `request.md`、`plan.md`、`draft.md` 主链写作与增量修订
  - subagent 选择
  - handoff 回收
  - 质量门控
- 所有 specialist subagent 都由主会话显式调用：
  - `source-evidence-agent`：负责 `sources/`、链接验证与 evidence gap 分析
  - `diagram-agent`：负责 diagram decision tree、brief、diagram package 与 contract 支持
  - `review-critic-agent`：负责独立 review
  - `publish-agent`：负责 canonical artifact 提炼
- 不要让一个 subagent 再去调用另一个 subagent。所有 delegation 都留在主会话。

## 规则来源

执行前读取并遵循：

- `harness/workflows/research-pipeline.md`
- 各阶段对应的 OpenSpec spec 与 template
- `.claude/agents/` 中相关 subagent contract

## Research Flow

### 1. Change 初始化

如果 `$ARGUMENTS` 是研究主题而不是现有 change 路径：

- 创建 change 目录
- 初始化 change packet
- 从 `request.md` 开始推进

如果 `$ARGUMENTS` 指向现有 change，则复用现有 change packet。

### 2. 阶段编排

- `request`：主会话直接生成或修订 `request.md`
- `plan`：主会话直接生成或修订 `plan.md`；需要来源支持时再显式调用 `source-evidence-agent`
- `draft`：主会话直接生成或修订 `draft.md`；需要图表时调用 `diagram-agent`；遇到定向 evidence gap 时调用 `source-evidence-agent`
- `review`：在 draft 冻结后，主会话显式调用 `review-critic-agent`
- `artifact`：只有 review 通过后，主会话才显式调用 `publish-agent`

### 3. Fallback

- 如果某个适合的 subagent 当前不可用，主会话可以按相同 contract 串行继续，但必须在总结中说明。
- 如果网络限制阻塞来源收集，记录 evidence gap，不要伪造确定性。
- 如果 required PlantUML package 未通过 validation，不要声称 draft 已完成。

## 完成总结

汇报：

- 当前任务最终走的是 research flow 还是 governance routing
- 使用了哪些 subagent
- 哪些阶段已完成
- 最终使用的 change 路径
- 是否生成了 `sources/`、`diagrams/`、`review/` 与 artifact 文件
- 是否还有 fridge items / evidence gap 未关闭
