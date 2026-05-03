# Agent 协作边界

**主定义位置**：本文件
**用途**：定义本仓库 multi-agent 协作的分类、职责边界与调度规则。
**引用方**：`.claude/agents/CONTRACT.md`、`AGENTS.md`

---

## Author Agents（研究型）

| Agent | 职责 | 调用方 |
|-------|------|--------|
| `primitive-author` | 单个 primitive 的 intake / draft capsule 写作 | 主会话 orchestrator |
| `synthesis-author` | 多 primitive 的 intake / draft capsule 写作 | 主会话 orchestrator |
| `decision-author` | 场景决策的 intake / draft capsule 写作 | 主会话 orchestrator |

Author agents 的特点：
- 可以被多次独立调用，但每次调用必须声明 capsule mode
- `mode=intake` 只写 `request.md`、`plan.md`，完成后停止
- `mode=draft` 只写 `draft.md`，前置条件是 `sources/` 已就绪
- 如需 `sources/`，向主会话返回明确 handoff 需求
- 如需正式图表，向主会话返回明确 handoff 需求；由主会话调用 `diagram-agent`
- 完成后将 draft 交回主会话，由主会话决定是否调用 review-critic-agent

## Specialist Agents（专长型）

| Agent | 职责 | 可写 | 不写 |
|-------|------|------|------|
| `source-evidence-agent` | sources/ 创建、链接验证、evidence gap | `sources/`、`notes/`、`claims/` | `draft.md`、`knowledge/**` |
| `diagram-agent` | 图表生成与验证 | `diagrams/` supporting artifacts | `knowledge/**`（除非通过 draft/publish） |
| `review-critic-agent` | 独立技术评审 | `review.md` | 不改 `draft.md` 正文（除非任务明确要求修复） |
| `publish-agent` | 长期 artifact 提炼 | `publish.md`、publish gate 后的 `knowledge/**` | 不改 `request.md` / `plan.md` 的语义 |
| `governance-review-agent` | 治理边界评审 | openspec/harness/commands/skills 规约文件 | 默认不改 `knowledge/**` |
| `spec-system-audit-agent` | 仓库规约体系审计 | 审计报告 | 不改正式 policy 或 knowledge 正文 |

Specialist agents 的特点：
- 不负责 `request.md` / `plan.md` / `draft.md` 的写作
- 输出结构化产物（inbox.yaml、diagram package、review checklist 等）
- **不得调用其他 subagent**

## 调度原则

- 主会话 orchestrator 统一调度 specialist agent
- Author agent 只负责主链写作，不嵌套拉起其他 subagent
- 主会话决定路由、目标路径、是否进入下一阶段；agent 自主决定具体实现细节
- 失败降级：若运行环境不支持真实 subagent，仍按 contract 顺序串行执行，不得跳过 handoff artifact 与 quality gate

## 调用与等待策略

- 单个 capsule 默认使用前台调用，也就是不设置 `run_in_background` 或显式设为 `false`；调用本身应阻塞到 agent 返回完成信号。
- 只有存在多个相互独立的 child changes / capsule，且主会话确实需要并行推进时，才使用后台调用。
- 后台调用必须在同一轮调度中批量发出，并在发出后停止主动等待；主会话只响应系统推送的完成通知，不发送"继续等待"、"检查状态"等 busy-wait 消息。
- 如果后台 agent 运行期间还有不依赖其结果的本地工作，主会话可以继续处理该工作；如果下一步完全依赖后台结果，则结束当前轮次或安静等待系统通知，不用自然语言占用新的 LLM 调用。
- 只有当当前工具列表明确提供延迟唤醒 / scheduler 能力时，才可设置单次延迟唤醒；不得编造不存在的等待工具，也不得用反复自我续写替代系统通知。

## Capsule 隔离原则

- multi-agent 的首要目的不是并发，而是让复杂任务拆成边界清晰、上下文干净、可停止和可审计的子任务。
- 按"会污染后续判断的认知边界"切分 capsule，不按文件数量机械切分。
- `request.md` 与 `plan.md` 默认属于同一个 intake capsule，因为 scope、来源策略和完成标准强耦合。
- `sources/`、`draft.md`、`review.md`、`publish.md` 必须分属不同 capsule。
- 默认不新增常驻 `request-planner` agent；只有当 request 生成需要独立治理、反复修订或跨研究类型复用时，才升级为独立 agent。
- 主会话只消费 agent 的完成状态、产出路径和 blocker；中间分析细节应沉淀在对应 artifact 内。
