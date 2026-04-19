# Claude Routing Index

Claude 侧的入口索引。先看这里，再下钻到具体 command、agent、rule 或本地设置文件。

---

## 1. 入口顺序

1. `../CLAUDE.md`：Claude 场景下的轻量入口与共享约束
2. `../AGENTS.md`：仓库总导航、分层和 workflow 路由
3. 本文件：Claude 侧命令、agent、语言规则和本地设置索引

---

## 2. Commands

| Command | 场景 | 读取入口 |
|---------|------|----------|
| `spec-research.md` | 端到端 research pipeline | `harness/workflows/research-pipeline.md` |
| `spec-request.md` | 只做 request 阶段 | `harness/rules/_phase_index.yaml` 的 `request` |
| `spec-plan.md` | 只做 plan 阶段 | `harness/rules/_phase_index.yaml` 的 `plan` |
| `spec-draft.md` | 只做 draft 阶段 | `harness/rules/_phase_index.yaml` 的 `draft` |
| `spec-artifact.md` | 只做 artifact / publish 阶段 | `harness/rules/_phase_index.yaml` 的 `artifact` |
| `spec-governance-review.md` | 规约、路由、仓库架构治理任务 | `harness/workflows/governance-review-workflow.md` |
| `spec-system-audit.md` | 仓库规约体系周期性审计与清理 | `harness/workflows/spec-system-audit-workflow.md` |

**读取顺序**：
- 先用 command 判断场景
- 再回到 `harness/workflows/_index.yaml` 识别 workflow
- 阶段型 command 再按 `harness/rules/_phase_index.yaml` 加载叶子 rules/specs/workflow

---

## 3. Agents

| 文件 | 角色 | 何时加载 |
|------|------|----------|
| `agents/CONTRACT.md` | agent 合同基线 | 创建/修改任一 agent 前必读 |
| `agents/primitive-author.md` | primitive 主链写作 | `research_type=primitive` |
| `agents/synthesis-author.md` | synthesis 横向合成 | `research_type=synthesis` |
| `agents/decision-author.md` | decision 场景判断 | `research_type=decision` |
| `agents/source-evidence-agent.md` | `sources/` 采集与验证 | plan/draft 需要补来源 |
| `agents/diagram-agent.md` | `diagrams/` 生成与验证 | 需要正式图表时 |
| `agents/review-critic-agent.md` | 独立评审 | draft 冻结后 |
| `agents/publish-agent.md` | artifact 提炼与 apply 前检查 | review 通过后 |
| `agents/governance-review-agent.md` | 边界与一致性评审 | governance 任务 |
| `agents/spec-system-audit-agent.md` | 规约体系体检、孤岛/死引用清理 | repo hygiene audit |

**调度原则**：
- 主会话 orchestrator 统一调度 specialist agent。
- author agent 只负责主链写作，不嵌套拉起其他 subagent。

---

## 4. Rules

| 文件 | 用途 | 何时读取 |
|------|------|----------|
| `rules/language-output.md` | Claude 过程输出语言约束 | 任何 Claude 可见输出前 |

---

## 5. Settings

| 文件 | 性质 | 用途 |
|------|------|------|
| `settings.json` | 仓库共享设置 | 默认语言与共享基础配置 |
| `settings.local.json` | 本地覆盖设置 | 仅在排查本机代理、权限、Beta 开关时读取；不是 workflow/source-of-truth |

**注意**：
- `settings.local.json` 是低耦合本地文件，不参与研究 workflow 的 canonical 加载链。
- 若修改本地设置，应同步检查是否需要更新本文件的用途说明。
