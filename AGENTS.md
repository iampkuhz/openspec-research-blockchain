# AGENTS.md

OpenSpec 区块链研究协作的轻量导航入口。

**本文件是 cross-client navigation entry**，不是 policy / schema / workflow / rules 事实源。遇到冲突以正式文件为准。

**核心原则**：先判任务，再读索引，最后只读必要叶子文件。不要把本文件当规则全集，也不要在启动时展开整个仓库。

---

## 1. Source of Truth by Decision Type

| Decision type | Source of truth |
|---|---|
| Formal policy / invariant | `openspec/specs/**` |
| Artifact graph / object model / publish constraints | `openspec/schemas/blockchain-research/schema.yaml` |
| Root directories / lifecycle roots | `openspec/config.yaml` |
| Workflow selection | `harness/workflows/_index.yaml` |
| Phase dependency | `harness/rules/_phase_index.yaml` |
| Concrete phase rules | `harness/rules/**` |
| Mechanical validation | `harness/gates/registry.yaml` + `scripts/hooks/validators/registry.yaml` |
| Claude Code adapter | `CLAUDE.md` + `.claude/**` |
| Qoder adapter | `QODER.md` + `.qoder/**` if present |
| Skill behavior | `skills/**/SKILL.md` |
| Script behavior | `scripts/**` |

Adapter 不重新定义 research policy / artifact schema / workflow semantics。与 OpenSpec / Harness 冲突时，后者胜出。

---

## 2. Routing Discriminators

基于用户输入选择 workflow，不要猜阶段：

- 端到端从需求到 publish → `harness/workflows/research-pipeline.md`
- 没有 `change-id`，要创建/初始化研究 → `harness/workflows/research-intake-routing.md`
- 已有 `change-id`，未指定阶段 → 先做 **Change State Detection**（§5），再读 `harness/workflows/research-step-execution.md`
- 只要来源、证据、claim mapping → `harness/workflows/source-workflow.md`
- 只要 diagram package → `harness/workflows/diagram-workflow.md`
- 要求 publish 到长期知识 → `harness/workflows/research-publish-flow.md`
- 修改 spec / schema / harness / command / agent / skill / hook / governance → `harness/workflows/governance-review-workflow.md`

不复制 workflow 步骤细节。需要具体规则时按 §1 的决策类型索引下钻。

---

## 3. Conditional Loading

| 场景 | 读取入口 |
|---|---|
| Claude Code command / agent | `CLAUDE.md` → `.claude/README.md` |
| Qoder 入口 | `QODER.md`；仅当 `.qoder/` 存在时再读 `.qoder/README.md` |
| 治理修改 | `docs/governance/openspec-harness-boundary.md` + `harness/workflows/governance-review-workflow.md` |
| Hook / gate / validator | `harness/hooks/README.md`、`harness/gates/registry.yaml`、`scripts/hooks/validators/registry.yaml` |
| Skills / scripts | `skills/README.md` / `scripts/README.md`，再读目标 `SKILL.md` 或脚本 |
| 联网 / MCP | `.claude/tools/mcp-tools.md`；仅在需要外部事实、source evidence、claim verification 或用户明确要求时加载，不绑定到单一阶段 |
| Multi-Agent | `harness/governance/agent-boundaries.md` + `.claude/agents/CONTRACT.md`，再读目标 agent |

---

## 4. Change State Detection

用户提供或上下文出现 `change-id` 时：

1. 检查 `openspec/changes/<change-id>/` 中现有 artifact 文件
2. 用文件存在性识别阶段：`change.yaml`、`request.md`、`plan.md`、`sources/`、`claims/`、`draft.md`、`review.md`、`publish.md`、`validation/`
3. 不只根据用户口头描述推断阶段
4. 只加载当前或下一阶段需要的 workflow / phase index / rule leaves
5. change 目录不存在或 artifact 状态不一致时，先进入 intake / repair / governance 检查，不继续推进

---

## 5. Write Safety

写入前必须确认 task type、change-id、current stage、target artifact、governing workflow/rules/schema。

- 普通研究默认只写 `openspec/changes/<change-id>/`
- 不得直接写 `knowledge/**`，除非通过 publish workflow 且满足 review / validation 要求
- 修改 OpenSpec / Harness / command / agent / skill / hook / governance 文件，必须走 governance review
- validator 失败时不得继续生命周期推进，除非 workflow 明确允许 waiver
- 删除、迁移、批量重命名文件前必须先输出 plan 或 diff，不静默执行

---

## 6. Validation Protocol

1. 先读 gate / validator registry（§1）
2. 根据 changed files、current stage、target artifact 选择 validator
3. deterministic validator 先于 semantic review
4. 校验结果写入 `openspec/changes/<change-id>/validation/`（需持久化时）
5. validator 失败时停止 lifecycle advancement
6. 没有 applicable validator 时记录未运行原因

---

## 7. Multi-Agent Boundary

只有 workflow 明确授权或用户明确要求时才加载 `.claude/agents/**`。

- 不得虚构 agent；agent 文件必须真实存在
- 主会话负责 orchestrate；author agent 只写 intake / draft capsule，不调用其他 subagent
- specialist agent 只产出 scoped artifact：`sources/`、`diagrams/`、`review.md`、`publish.md`
- 默认前台串行；不鼓励后台 agent 或 busy-wait 轮询
- subagent 不默认拥有 publish / apply / archive 权限

| `task_type` | Author Agent |
|---|---|
| `primitive` | `.claude/agents/primitive-author.md` |
| `synthesis` | `.claude/agents/synthesis-author.md` |
| `decision` | `.claude/agents/decision-author.md` |

Specialist agent（按需加载）：`source-evidence-agent`、`diagram-agent`、`review-critic-agent`、`publish-agent`、`governance-review-agent`、`spec-system-audit-agent`。

---

## 8. Low Token Reading Protocol

- 文件发现用 `rg --files`，内容定位用 `rg -n`
- 大文件用 `wc -l`、`sed -n '<start>,<end>p'`、`rg -n '<pattern>'` 分段读取
- 不 `cat` 整个目录，不无目的全文读取 `openspec/changes/`、`knowledge/`、`harness/rules/diagrams/`
- 读索引时只输出"下一步读哪个文件"，不复制索引全文
- 单线程顺序执行；不为了提速并行调用 agent 或批量展开无关文件

---

## 9. Quick Lookup

| 问题 | 先看 |
|---|---|
| 当前任务走哪个 workflow | `harness/workflows/_index.yaml` |
| 当前阶段需要哪些规则 | `harness/rules/_phase_index.yaml` |
| artifact 形状与依赖 | `openspec/schemas/blockchain-research/schema.yaml` |
| publish / apply / archive 根目录 | `openspec/config.yaml` |
| 规约修改是否越界 | `docs/governance/openspec-harness-boundary.md` |
| hook 覆盖哪些检查 | `harness/gates/registry.yaml` + `scripts/hooks/validators/registry.yaml` |
