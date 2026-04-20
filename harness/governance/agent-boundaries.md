# Agent 协作边界

**主定义位置**：本文件  
**用途**：定义本仓库 multi-agent 协作的分类、职责边界与调度原则。  
**引用方**：`.claude/agents/CONTRACT.md`、`harness/workflows/research-pipeline.md`、`AGENTS.md`

---

## Author Agents（研究型）

| Agent | 职责 | 调用方 |
|-------|------|--------|
| `primitive-author` | 单个 primitive 的全链路研究写作 | 主会话 orchestrator |
| `synthesis-author` | 多 primitive 的横向对比合成 | 主会话 orchestrator |
| `decision-author` | 场景决策分析写作 | 主会话 orchestrator |

Author agents 的特点：
- 负责 `request.md` → `plan.md` → `draft.md` 的主链写作
- 不直接调用 specialist agent；如需 `sources/` 或 `diagrams/`，向主会话返回明确 handoff 需求
- 完成后将 draft 交回主会话，由主会话决定是否调用 review-critic-agent

## Specialist Agents（专长型）

| Agent | 职责 | 调用方 |
|-------|------|--------|
| `source-evidence-agent` | sources/ 创建、链接验证、evidence gap | 主会话 orchestrator |
| `diagram-agent` | 图表生成与验证 | 主会话 orchestrator |
| `review-critic-agent` | 独立技术评审 | 主会话 orchestrator |
| `publish-agent` | 长期 artifact 提炼 | 主会话 orchestrator |
| `governance-review-agent` | 治理边界评审 | 主会话 orchestrator |
| `spec-system-audit-agent` | 仓库规约体系审计与清理 | 主会话 orchestrator |

Specialist agents 的特点：
- 不负责 `request.md` / `plan.md` / `draft.md` 的写作
- 输出结构化产物（inbox.yaml、diagram package、review checklist 等）
- **不得调用其他 subagent**

## 调度原则

- 主会话 orchestrator 统一调度 specialist agent
- Author agent 只负责主链写作，不嵌套拉起其他 subagent
- 主会话决定路由、目标路径、是否进入下一阶段；agent 自主决定具体实现细节
- 失败降级：若运行环境不支持真实 subagent，仍按 contract 顺序串行执行，不得跳过 handoff artifact 与 quality gate
