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
- `harness/rules/_phase_index.yaml`
- 各阶段对应的 OpenSpec spec 与 template
- `.claude/agents/` 中相关 agent contract
- `.claude/agents/CONTRACT.md`（agent 合同校验规范）

## Subagent 使用规则

| 阶段 | 必须使用的 subagent | 禁止行为 |
|------|-------------------|----------|
| 研究写作（primitive） | `primitive-author` | 主会话自行写 request/plan/draft |
| 研究写作（synthesis） | `synthesis-author` | 主会话自行写 request/plan/draft |
| 研究写作（decision） | `decision-author` | 主会话自行写 request/plan/draft |
| sources/ 创建 | `source-evidence-agent` | author agent 自行创建 inbox.yaml / source-review.md |
| sources/ 补证据 | `source-evidence-agent` | 主会话绕过 `sources/` handoff 直接写正文 |
| 架构图 | `diagram-agent` | author agent 手写 PlantUML 或直接改 diagram package |
| draft 评审 | `review-critic-agent` | 主会话/author agent 自我评审或跳过评审 |
| artifact 提炼 | `publish-agent` | 主会话自行写入 knowledge/ |

**Fallback 约束**：禁止直接 fallback。必须先尝试调用 subagent，确认失败后向用户请求二次确认，用户明确同意后才可按相同 contract 串行执行。详见第 3 节 Fallback。

## Concurrency 控制

当阶段 1（依赖发现）需要启动多个 author agent 时，主会话必须控制并发量，防止超过 LLM server 的 TPS 限制：

| 参数 | 值 | 说明 |
|------|-----|------|
| `MAX_CONCURRENT` | 3 | 任何时刻正在运行的 agent 总数不得超过 3 |

**调度规则**：

1. **分批启动**：使用 `Agent(run_in_background=true)` 启动 author agent 时，每批不超过 `MAX_CONCURRENT`（3）个；等整批全部完成后，再启动下一批
2. **绝对上限**：任何时刻正在运行的 agent 总数不得超过 `MAX_CONCURRENT`（3）
3. **阶段 1.5 quality gate**（review + publish）：串行执行，不按并发规则处理
4. **汇报**：完成总结中必须列出各批次的调度顺序与并发数，例如：
   ```
   并发调度：第1批 [primitive-a, primitive-b, primitive-c] → 第2批 [primitive-d, primitive-e]
   ```

**示例**（5 个 primitive 依赖）：
```
批 1: primitive-author(A), primitive-author(B), primitive-author(C)  ← 3 个并发
等待批 1 全部完成
批 2: primitive-author(D), primitive-author(E)                      ← 2 个
```

## Research Flow

### 0. request.md 约束（二次研究来源保护）

在创建或校验 request.md 时，必须检查"范围与非目标"段：

- **二次研究禁止切断来源验证**：request.md 的"非目标"中**不得**包含"不扩展研究新来源"、"不引入新外部来源"、"基于既有分析已确认的事实"等切断来源搜索的表述。
- **既有 artifact 是起点，不是天花板**：二次研究的 request 必须明确既有 artifact 仅作为参考基线，仍需回源到原始项目仓库、文档、commit 历史等验证和补充信息。
- 如发现 request.md 已包含此类自我设限表述，**必须先修正 request.md 再继续**。

### 1. Change 初始化

如果 `$ARGUMENTS` 是研究主题而不是现有 change 路径：

- 创建 change 目录
- 从 `request.md` 开始推进

如果 `$ARGUMENTS` 指向现有 change，则复用现有 change packet。

创建或读取 `request.md` 后，**立即读取其中的 `research_type` 和 `research_path` 字段**，根据类型路由到对应 author agent：

### 2a. primitive 模式

路由到 `primitive-author`：

```
主会话 → primitive-author（request / plan / draft 主链）
主会话 → source-evidence-agent（sources/ 支撑轨）
主会话 → diagram-agent（如需正式图表）
主会话 → review-critic-agent
主会话 → publish-agent
```

1. 主会话调用 `primitive-author`，传入 change 路径
2. primitive-author 负责 `request.md` / `plan.md` / `draft.md` 主链写作
3. 如作者返回来源需求单，主会话调用 `source-evidence-agent` 创建或补充 `sources/`
4. 如作者返回图表需求单，主会话调用 `diagram-agent` 生成和验证 `diagrams/`
5. primitive-author 消费 `sources/` 与 `diagrams/` 后完成 `draft.md`
6. **review gate**：draft 冻结后，主会话**必须**调用 `review-critic-agent` 评审，**不得跳过**
7. **publish gate**：review 通过后，主会话**必须**调用 `publish-agent` 提炼 artifact 到 `knowledge/`，**不得跳过**

### 2b. synthesis 模式（三阶段）

**阶段 1 — 依赖发现**：

1. 读取 synthesis `request.md` 中的 `依赖声明` 段
2. 列出所有依赖的 primitive（每个对应一个 `primitive-*` change）
3. 对每个 primitive：
   - 如果 change 不存在：创建 change 目录
   - 调用 `primitive-author` 为该 primitive 执行全链路写作
4. 等待所有 primitive-author 完成（按 Concurrency 控制分批执行）

**阶段 1.5 — primitive quality gate（不可跳过）**：

1. 对阶段 1 产生的**每个** primitive change，主会话必须依次执行：
   - 调用 `review-critic-agent` 评审该 primitive 的 `draft.md`
   - review 通过后，调用 `publish-agent` 提炼该 primitive 的 artifact 到 `knowledge/`
2. **只有当所有 primitive 均通过 review + publish 后**，才允许进入阶段 2

**阶段 2 — synthesis 合成**：

1. 主会话调用 `synthesis-author`，传入 synthesis change 路径
2. synthesis-author 从各 primitive `draft.md`（以及已 publish 的 `knowledge/` artifact）中提取信息进行横向对比
3. 如 synthesis-author 返回来源或图表需求单，主会话调用 `source-evidence-agent` / `diagram-agent`
4. synthesis-author 消费补充产物后完成 `draft.md`
5. **review gate**：主会话**必须**调用 `review-critic-agent` 评审，**不得跳过**
6. **publish gate**：review 通过后，主会话**必须**调用 `publish-agent` 提炼 artifact 到 `knowledge/`，**不得跳过**

**约束**：阶段 2 禁止在阶段 1.5 所有 primitive 的 review + publish 完成前开始。

### 2c. decision 模式

路由到 `decision-author`：

```
主会话 → decision-author（request / plan / decision-criteria / draft）
主会话 → source-evidence-agent（sources/ 支撑轨）
主会话 → diagram-agent（如需正式图表）
主会话 → review-critic-agent
主会话 → publish-agent
```

**阶段 1 — 依赖发现**：

1. 读取 decision `request.md` 中的 `依赖声明` 段
2. 列出所有依赖的 primitive 和 synthesis
3. 对每个缺失的 primitive/synthesis：创建 change 目录 + 调用对应 author agent 执行全链路写作
4. 等待所有 author agent 完成（按 Concurrency 控制分批执行）

**阶段 1.5 — 依赖 quality gate（不可跳过）**：

1. 对阶段 1 产生的**每个** primitive 和 synthesis change，主会话必须依次执行：
   - 调用 `review-critic-agent` 评审该 change 的 `draft.md`
   - review 通过后，调用 `publish-agent` 提炼该 change 的 artifact 到 `knowledge/`
2. **只有当所有依赖 change 均通过 review + publish 后**，才允许进入阶段 2

**阶段 2 — decision 合成**：

1. 主会话调用 `decision-author`，传入 decision change 路径
2. decision-author 从各 primitive/synthesis `draft.md`（以及已 publish 的 `knowledge/` artifact）中提取信息进行场景决策分析
3. 如 decision-author 返回来源或图表需求单，主会话调用 `source-evidence-agent` / `diagram-agent`
4. decision-author 消费补充产物后完成 `draft.md`
5. **review gate**：主会话**必须**调用 `review-critic-agent` 评审，**不得跳过**
6. **publish gate**：review 通过后，主会话**必须**调用 `publish-agent` 提炼 artifact + verdict 到 `knowledge/`，**不得跳过**

**约束**：阶段 2 禁止在阶段 1.5 所有依赖 change 的 review + publish 完成前开始。

### 3. Fallback

**禁止直接 fallback**。必须按以下三步执行：

1. **先尝试调用 subagent**：不得跳过 subagent 直接由主会话代写
2. **确认失败后上报**：subagent 调用失败（报错/超时/无响应）时，向主会话返回失败详情（agent 名称、失败原因、已完成的产物），并向用户请求二次确认是否 fallback
3. **用户确认后执行**：只有用户明确同意 fallback 后，主会话才可按相同 contract 串行继续，必须在完成总结中说明哪个 subagent 被 fallback 了、fallback 原因、用户确认时间

- 如果网络限制阻塞来源收集，记录 evidence gap，不要伪造确定性。
- 如果 required PlantUML package 未通过 validation，不要声称 draft 已完成。

## 完成总结

汇报：

- 当前任务最终走的是 research flow 还是 governance routing
- 路由到的 author agent 类型（primitive-author / synthesis-author / decision-author）
- 使用了哪些 specialist subagent
- 各阶段状态
- 最终使用的 change 路径（如有 synthesis，列出所有 primitive change 路径）
- **每个 change 的 review 状态**：是否调用了 review-critic-agent、评审结论（approved / needs revision）
- **每个 change 的 publish 状态**：是否调用了 publish-agent、artifact 提升路径（knowledge/ 下的具体路径）
- **每个 change 的 archive 状态**：是否已归档到 openspec/archive/ / 延迟归档（原因）/ 归档前智能决策内容（哪些沉淀为 openspec/specs、哪些合并到 knowledge/）
- **并发调度情况**：分了几批、每批并发数、是否有 agent 等待
- 是否生成了 `sources/`、`diagrams/`、`review/` 与 artifact 文件
- 是否还有 fridge items / evidence gap 未关闭

**强制检查**：在输出完成总结前，必须确认每个 change 均已通过 review gate + publish gate + archive gate。如有 change 未完成 review/publish/archive，必须在总结中明确列出，不得隐去。
