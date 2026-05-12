# Qoder 路由索引

Qoder 侧的入口索引。先看这里，再下钻到具体 command、agent、skill 或本地设置文件。

---

## 1. 入口顺序

1. `../QODER.md`：Qoder 场景下的轻量入口与共享约束
2. `../AGENTS.md`：仓库总导航、分层和 workflow 路由
3. 本文件：Qoder 侧命令、agent、技能和本地设置索引

---

## 2. Commands

**Active commands（3 个）：**

| Command | 场景 | 必读文件 |
|---------|------|----------|
| `spec-research.md` | 技术调研总入口，按 research pipeline 调度 agents 推进到 Knowledge artifact | `harness/workflows/research-pipeline.md` |
| `spec-research-step.md` | 推进当前 change 的下一步，覆盖 sources / draft / review / publish | `harness/rules/_phase_index.yaml` |
| `spec-governance-review.md` | 规约治理入口，审查 openspec / commands / skills / harness 一致性 | `docs/governance/openspec-harness-boundary.md` |

Commands 负责入口，Skills 负责能力包。Commands 不依赖 skill 自动加载，每个 command 都有内联 fallback steps。

**读取顺序**：
- 先用 active command 判断场景
- 再回到 `harness/workflows/_index.yaml` 识别 workflow
- 阶段型任务再按 `harness/rules/_phase_index.yaml` 加载叶子 rules/specs/workflow

---

## 3. Agents

| 文件 | 角色 | 何时加载 |
|------|------|----------|
| `agents/CONTRACT.md` | agent 合同基线（03 阶段创建，当前不存在） | 创建/修改任一 agent 前必读 |
| `agents/primitive-author.md` | primitive 主链写作 | `task_type=primitive` |
| `agents/synthesis-author.md` | synthesis 横向合成 | `task_type=synthesis` |
| `agents/decision-author.md` | decision 场景判断 | `task_type=decision` |
| `agents/source-evidence-agent.md` | `sources/` 采集与验证 | plan/draft 需要补来源 |
| `agents/diagram-agent.md` | `diagrams/` 生成与验证 | 需要正式图表时 |
| `agents/review-critic-agent.md` | 独立评审 | draft 冻结后 |
| `agents/publish-agent.md` | artifact 提炼与 apply 前检查 | review 通过后 |
| `agents/governance-review-agent.md` | 边界与一致性评审 | governance 任务 |
| `agents/spec-system-audit-agent.md` | 规约体系体检 | repo hygiene audit |

**Agent 源文件**：所有 agent 的完整合同定义在 `.claude/agents/*.md`。
`.qoder/agents/*.md` 尚未创建（03 阶段），将采用薄 wrapper 方式，frontmatter 适配 Qoder 格式，
正文中显式要求启动时读取 `.claude/agents/*.md` 源文件。
当前以 `harness/adapters/agent-adapter-contract.md` + `.claude/agents/CONTRACT.md` 为准。

**调度原则**：
- 主会话 orchestrator 统一调度 specialist agent。
- author agent 只负责主链写作，不嵌套拉起其他 subagent。
- source 阶段直接调度 `source-evidence-agent`。

---

## 4. Skills

Skill 真源在 `skills/` 目录下，`.claude/skills/` 是 Claude Code 的 symlink 暴露层。
Qoder 侧的 `.qoder/skills/` 应优先通过 symlink 或薄 wrapper 引用 `skills/` 真源。

详细分类与路由表见 `skills/README.md`。

---

## 5. Settings / Local Override

| 文件 | 性质 | 用途 |
|------|------|------|
| `.qoder/settings.json` | 项目级共享设置 | permissions + hooks 配置 |
| `.qoder/settings.local.json` | 本地覆盖设置 | 仅在排查本机代理、权限时读取；不参与研究 workflow 的 canonical 加载链 |

Qoder settings 字段与 Claude Code 不同，详见 `harness/adapters/tool-capability-matrix.md`。

---

## 6. 与 `.claude/README.md` 的关系

`.claude/README.md` 与 `.qoder/README.md` 是同一套路由语义的两个 adapter 实现。
两者都不是正式规则源，正式规则以 `openspec/**`、`harness/workflows/**`、`harness/rules/**` 为准。

当 Qoder 不支持某项 Claude Code 能力时，降级路径记录在 `harness/adapters/tool-capability-matrix.md`。
