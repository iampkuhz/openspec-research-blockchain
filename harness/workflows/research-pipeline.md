# Research Pipeline

**用途**：端到端研究编排真源，供 `/spec-research` 和主会话 orchestrator 引用。

本文件只描述从自然语言需求到最终 Knowledge artifact 的执行编排。正式 artifact 依赖以 `openspec/schemas/blockchain-research/schema.yaml` 的 `artifacts[].requires` 为准；正式 apply / publish 规则以 `openspec/config.yaml` 为准。

---

## 输入与输出

输入：

- 用户自然语言研究需求
- 可选的既有 `knowledge/**/artifact.md`
- 可选的现有 `openspec/changes/<change-id>/`

输出：

- `openspec/changes/<change-id>/change.yaml`
- `request.md`
- `plan.md`
- `sources/source-pack.md`
- `sources/evidence-map.md`
- `notes/*.md`（按需）
- `claims/*.md`（按需）
- `draft.md`
- `review.md`
- `publish.md`
- `knowledge/**/artifact.md` 或 `knowledge/decisions/**/verdict.md`

---

## 入口关系

| 入口 | 职责 | 引用的 workflow |
|---|---|---|
| `/spec-research` | 端到端 orchestrator | 本文件 |
| `/spec-research-step` | 单 change 下一阶段推进，含 publish | `research-step-execution.md` + `research-publish-flow.md` |

`/spec-research` 可以自动串起 intake、step 和 publish capsule；具体阶段规则仍由被引用 workflow 和 phase rules 承担。

---

## 主流程

1. **读取总导航**
   - `AGENTS.md`
   - `openspec/config.yaml`
   - `openspec/schemas/blockchain-research/schema.yaml`
   - `harness/workflows/_index.yaml`
   - `harness/rules/_phase_index.yaml`
   - `harness/governance/agent-boundaries.md`

2. **Intake / routing**
   - 按 `harness/workflows/research-intake-routing.md` 判断 `task_type`、`change_operation` 与 child changes。
   - 创建或定位 `openspec/changes/<change-id>/`。
   - 初始化 `change.yaml` 与必要 staging 目录。

3. **Intake capsule**
   - 主会话调用对应 author agent，声明 `mode=intake`。
   - 该 capsule 只生成或修订 `request.md`、`plan.md`。
   - 完成后立即停止，返回来源 handoff。

4. **Source capsule**
   - 主会话调用 `source-evidence-agent`。
   - 按 `harness/workflows/source-workflow.md` 生成或补充 `sources/source-pack.md`、`sources/evidence-map.md`、`notes/*.md`、`claims/*.md`。
   - 完成后立即停止。

5. **Diagram capsule（draft 的前置子步骤）**
   - 在进入 draft capsule 之前，主会话检查 `plan.md` 中的图表规划。
   - 如果 plan 声明了正式 PlantUML 类型图表（Architecture Diagram / Sequence Diagram），主会话必须先调用 `diagram-agent` 生成图表 package。
   - diagram-agent 完成后，图表产物位于 `openspec/changes/<change-id>/diagrams/`。
   - **计划要求的正式图表未完成、`validation.json` 未通过或 draft 仍含图表 TODO 占位时，draft capsule 不得开始写作。**
   - 如果 plan 声明了 fallback 类型图表（Mermaid / 表格 / ASCII），author agent 在 draft 中直接写入即可。

6. **Draft capsule**
   - 主会话再次调用对应 author agent，声明 `mode=draft`。
   - 该 capsule 读取 `request.md`、`plan.md`、`sources/` 和 `diagrams/`，只生成或修订 `draft.md`。
   - 如果发现需要更多来源或正式图表，返回 handoff，不自行调用 specialist。

7. **Review capsule**
   - draft 冻结后，主会话调用 `review-critic-agent`。
   - 评审结果写入 `review.md`，可按需附带 `review/checklist.yaml`、`review/issues.md`。
   - verdict 为 `needs revision` 时停止并回报 blocker。
   - 如果 plan 要求的正式图表缺失或 draft 中仍有图表 TODO，占位问题必须按 blocker / high severity 处理，不得作为 medium severity 放行。

8. **Publish capsule**
   - review verdict 为 `approved` 或 `approved with minor fixes` 后，主会话调用 `publish-agent` 或 `/spec-research-step` 的 publish 阶段。
   - 按 `research-publish-flow.md` 生成 `publish.md` 并写入合法 `knowledge/**` 目标。

---

## Capsule 切分原则

- 按"会污染后续判断的认知边界"切分，而不是按文件数量机械切分。
- `request.md` 与 `plan.md` 默认属于同一个 intake capsule。
- `sources/`、`draft.md`、`review.md`、`publish.md` 必须分属不同 capsule。
- 子任务必须能独立读取输入、独立写入产物、独立停止并返回 handoff。
- 不为了并发而拆分；并发只是 child changes 或独立来源验证的副作用。

---

## Agent 调度

| capsule | 默认 agent | 写入范围 |
|---|---|---|
| intake | `primitive-author` / `synthesis-author` / `decision-author` | `request.md`、`plan.md`、`decision-criteria.md`（仅 decision 按需） |
| source | `source-evidence-agent` | `sources/`、`notes/`、`claims/` |
| diagram | `diagram-agent` | `diagrams/` |
| draft | `primitive-author` / `synthesis-author` / `decision-author` | `draft.md` |
| review | `review-critic-agent` | `review.md`，按需 `review/` supporting files |
| publish | `publish-agent` | `publish.md`、合法 `knowledge/**` targets |

Author agent 可以被多次调用，但每次调用必须是独立上下文，并由主会话声明 capsule mode。
Author agent 不调用 specialist agent；需要来源或正式图表时返回 handoff，由主会话调度对应 specialist。

---

## Child Changes

复杂任务必须拆成多个 child changes：

- 每个 primitive 独立一个 change。
- synthesis 依赖其引用的 primitive changes。
- decision 依赖其引用的 primitive / synthesis changes。
- synthesis / decision 不得在依赖 draft 缺失时自行补写依赖内容。

---

## 停止条件

遇到以下情况必须停止并向主会话返回 blocker：

- task 实际需要多个最终 Knowledge artifact，但尚未拆 child changes。
- sources 无法支撑高确定性 claim，且无可接受降级策略。
- plan 要求正式图表但 `diagrams/` 未生成、校验未通过，或 draft 中仍保留图表 TODO。
- review verdict 为 `needs revision`。
- publish target 不符合 `openspec/config.yaml` 或 schema asset model。
- agent 需要写入自身 capsule 范围之外的文件。

---

## Agent 后台等待保护

**背景**：当主 orchestrator 使用 `run_in_background: true` 启动 subagent 后，不得在主会话中进行 busy-wait 轮询（反复检查 agent 是否完成）。每次轮询都是一次完整的 LLM API 调用，属于严重浪费。

本节是 `harness/governance/agent-boundaries.md` 中"调用与等待策略"在 `/spec-research` 端到端流程里的落地说明。

**强制规则**：

1. **单个 capsule 默认前台调用**：只要当前关键路径上只有一个 agent 需要执行，就使用 `run_in_background: false`（即 `Agent` tool 的默认行为）。Agent tool 调用本身会阻塞直到 subagent 完成，主会话自动收到结果，零额外调用。

2. **后台只用于真实并行**：只有多个 child changes 或多个彼此独立的 capsule 可以并行推进时，才使用 `run_in_background: true`。不得因为单个 agent 预计耗时较长就改成后台调用再轮询。

3. **并行时批量发出**：当多个 child changes 需要并行运行独立 agent 时，必须在**同一轮调度**中发出所有 `Agent` 调用。Claude Code 会并发执行这些 agents，并在每个完成时自动向主会话推送通知。主会话收到所有完成通知后自然继续，**不得主动轮询**。

4. **禁止 busy-wait 轮询**：主会话不得反复发送 "继续等待"、"检查 agent 状态"、"agent 完成了吗" 等消息。收到 subagent 完成通知是被动事件，不需要主动检查。

5. **无可推进工作时停止发言**：如果所有下一步都依赖后台 agent 的结果，主会话最多汇报一次"后台任务已启动，等待完成通知"，随后结束当前轮次或安静等待系统通知，不得继续生成等待消息。

6. **长时间等待的降级**：只有当前工具列表明确提供延迟唤醒 / scheduler 能力时，才可设置单次延迟唤醒；否则保持后台任务运行并等待系统完成通知。不得编造 `ScheduleWakeup` 等不存在的工具。

**错误示例**（禁止）：
```
主会话: "继续等待后台 source-evidence-agent 完成。"
主会话: "继续等待。"        ← 浪费调用 #1
主会话: "继续等待。"        ← 浪费调用 #2
...（重复 50+ 次）
```

**正确示例 1**（单个 agent，前台）：
```
主会话: Agent(source-evidence-agent, run_in_background: false)
        ← 自动阻塞，agent 完成后直接收到结果
```

**正确示例 2**（多个 agent 并行）：
```
主会话: 同时发出 2 个 Agent 调用（都 run_in_background: true）
        ← Claude Code 并发执行，自动推送完成通知
        ← 收到通知 A
        ← 收到通知 B
        ← 两个都完成，自然继续下一步
```

---

## 完成信号

端到端完成时，主会话汇报：

- change 拆分列表
- 每个 change 的 `task_type`
- 每个 change 的路径
- 每个 capsule 的完成状态
- 正式图表 gate 状态（如 plan 声明了 diagram）
- 写入的最终 `knowledge/**` 路径
