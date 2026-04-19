# AGENTS.md

OpenSpec 区块链研究协作的导航入口。

**定位**：本文件只负责回答三件事。
- 先读什么
- 任务该路由到哪里
- 哪些约束必须优先记住

**不是这里的职责**：
- 不在这里重写 `openspec/config.yaml`、`openspec/schemas/blockchain-research/schema.yaml`、`openspec/specs/**` 的正式规则
- 不在这里展开 `harness/workflows/**`、`harness/rules/**`、`.claude/agents/**` 的执行细节
- 不把所有索引和政策复制一遍

**冲突处理**：如果本文件与真源不一致，以真源为准。真源优先级从高到低：
1. `openspec/specs/**`（正式政策）
2. `openspec/config.yaml` + `openspec/schemas/blockchain-research/schema.yaml`（模型与规则）
3. `harness/workflows/_index.yaml` + `harness/rules/_phase_index.yaml`（执行路由）

**核心原则**：知道去哪里找知识，而不是把所有知识加载进来。

---

## 一、必读顺序

### 默认顺序

| 步骤 | 读取文件 | 目的 |
|------|----------|------|
| 1 | `AGENTS.md` | 获取导航、路由和最小硬约束 |
| 2 | `openspec/config.yaml` | 确认 workflow 配置、artifact 依赖与 apply 规则 |
| 3 | `openspec/schemas/blockchain-research/schema.yaml` | 确认研究对象模型、资产模型与产物路径 |
| 4 | `harness/workflows/_index.yaml` | 识别当前任务属于哪类 workflow |
| 5 | `harness/rules/_phase_index.yaml` | 在阶段明确后按需加载 specs / rules / workflows |
| 6 | `harness/rules/_index.yaml` | 只有需要继续下钻叶子规则时才读 |

### 条件加载

| 场景 | 追加读取 |
|------|----------|
| Claude 场景 | `CLAUDE.md` → `.claude/README.md` |
| 治理型任务（修改 OpenSpec / Harness / 治理结构） | `docs/governance/openspec-harness-boundary.md` |
| 需要联网搜索或网页提取 | `.claude/tools/mcp-tools.md` |
| 需要查看 change 目录结构或现有样例 | `openspec/changes/` |
| 需要技能或脚本支持 | `skills/README.md`、`scripts/README.md` |
| Multi-Agent 执行 | `.claude/agents/CONTRACT.md` → 按 `research_type` 加载对应 author agent |

**加载原则**：
- 先读索引，再读叶子文件
- 先按任务路由，再按阶段加载
- 只加载当前任务需要的最小上下文

---

## 二、任务路由

| 任务 | 主入口 | 主要产出 |
|------|--------|----------|
| 端到端研究（request → plan → draft → review → apply） | `harness/workflows/research-pipeline.md` | 完整 change 产物链 + 长期 artifact |
| 创建新研究 | `harness/workflows/intake-workflow.md` | `openspec/changes/<id>/request.md` |
| 收集与验证来源 | `harness/workflows/source-workflow.md` | `openspec/changes/<id>/sources/` |
| 正式图表 | `harness/workflows/diagram-workflow.md` | `openspec/changes/<id>/diagrams/` |
| 评审研究产出 | `harness/workflows/review-workflow.md` | `openspec/changes/<id>/review/` |
| Apply 到长期知识 | `openspec/config.yaml` apply 段 + `harness/workflows/merge-workflow.md` | `knowledge/analysis/**` 或 `knowledge/decisions/**` |
| 更新现有知识 | `harness/workflows/update-existing-knowledge.md` | `knowledge/` 增量更新 |
| 修改规约分层或治理结构 | `docs/governance/openspec-harness-boundary.md` + `harness/workflows/governance-review-workflow.md` | `review/governance-review.md` |
| 规约体系卫生审计 | `harness/workflows/spec-system-audit-workflow.md` | 审计总结或报告 |

**阶段型任务的统一做法**：
1. 先在 `harness/workflows/_index.yaml` 确认任务类型
2. 再在 `harness/rules/_phase_index.yaml` 找当前阶段依赖
3. 最后按索引加载必要的 spec、rule、workflow 叶子文件

---

## 三、单一事实源

### OpenSpec 是正式规则层

以下内容以 OpenSpec 为准：
- artifact 依赖链、研究对象模型、长期资产模型
- apply 准入规则、evidence / output model 等正式政策

对应入口：`openspec/config.yaml`、`openspec/schemas/blockchain-research/schema.yaml`、`openspec/specs/**`

### Harness 是执行手册层

以下内容以 Harness 索引和 workflow/rule 文件为准：
- 任务如何路由、阶段如何切换、规则如何按需加载
- review / repair / merge 的执行步骤

对应入口：`harness/workflows/_index.yaml`、`harness/rules/_phase_index.yaml`、`harness/rules/_index.yaml`

**边界原则**：OpenSpec 定义正式规则；Harness 负责把正式规则落实成执行步骤。不要在 `AGENTS.md` 或 Harness 中重新定义 OpenSpec 的正式语义。

---

## 四、研究模型速查

### 长期产物

| 类型 | 研究路径 | 产物位置 |
|------|----------|----------|
| `primitive` | `deep-dive` | `knowledge/analysis/primitives/<domain_id>/<topic_slug>/artifact.md` |
| `synthesis` | `evolution` | `knowledge/analysis/synthesis/<topic_slug>/artifact.md` |
| `decision` | `scenario` | `knowledge/decisions/<domain_id>/<topic_slug>/artifact.md` + `verdict.md` |

### 过程产物

以下文件留在 `openspec/changes/<change-id>/`，不直接进入长期目录：
`request.md`、`plan.md`、`draft.md`、`decision-criteria.md`（可选）、`sources/`、`diagrams/`、`review/`

**补充说明**：
- `domain` 是 taxonomy / 浏览分组概念，不是独立 `object_type`
- `knowledge/topics/` 是遗留目录，不再作为主线 canonical 资产目标

---

## 五、最小硬约束

- 禁止直接修改 `knowledge/` 主线；研究过程文件进入 `openspec/changes/`
- 长期资产只沉淀到 `knowledge/analysis/` 和 `knowledge/decisions/`
- 核心技术主张遵守证据等级约束，每个 claim 必须可追溯到 source
- 术语优先复用既有 glossary / taxonomy
- 涉及仓库治理、分层、路由或规约边界的修改，必须进入 governance review 路由

> 证据等级与可追溯性细节见 `openspec/specs/evidence-policy/spec.md`；术语与 traceability 执行细节见 `harness/rules/general/` 下的对应 policy。

---

## 六、Claude 与 Multi-Agent（条件加载）

### Claude 场景

追加读取 `CLAUDE.md` → `.claude/README.md`，按当前任务涉及的 command / agent / rule 文件下钻。具体路由提醒以 CLAUDE.md 为准。

### Multi-Agent 场景

只有当 workflow 或 Claude 路由明确需要 multi-agent 时，才加载 `.claude/agents/**`。

必须先读 `.claude/agents/CONTRACT.md`，再按 `research_type` 路由：

| 研究类型 | Author Agent |
|----------|-------------|
| `primitive` | primitive-author |
| `synthesis` | synthesis-author |
| `decision` | decision-author |

Specialist agent 按需加载：`source-evidence-agent`、`diagram-agent`、`review-critic-agent`、`publish-agent`、`governance-review-agent`、`spec-system-audit-agent`。

**协作边界**：
- 主会话负责 orchestrate
- author agent 负责主链写作（request → plan → draft）
- specialist agent 负责 `sources/`、`diagrams/`、`review/`、`publish` 等专项上下文
- 不允许 author agent 嵌套拉起 subagent

---

## 七、索引入口

| 需求 | 入口 |
|------|------|
| Workflow 总索引 | `harness/workflows/_index.yaml` |
| 阶段依赖索引 | `harness/rules/_phase_index.yaml` |
| 规则域索引 | `harness/rules/_index.yaml` |
| Change 目录与样例 | `openspec/changes/` |
| Governance 索引 | `docs/governance/README.md` |
| Skills 索引 | `skills/README.md` |
| Scripts 索引 | `scripts/README.md` |
| Claude 侧路由 | `CLAUDE.md`、`.claude/README.md` |
| MCP 工具指南 | `.claude/tools/mcp-tools.md` |

---

## 八、遇到问题时

| 问题 | 先看哪里 |
|------|----------|
| 不知道当前任务该走哪个 workflow | `harness/workflows/_index.yaml` |
| 不知道当前阶段还要加载哪些规则 | `harness/rules/_phase_index.yaml` |
| 不知道长期产物应该落在哪里 | `openspec/schemas/blockchain-research/schema.yaml` |
| 不知道 apply 是否允许 | `openspec/config.yaml` |
| 不知道治理型修改是否越界 | `docs/governance/openspec-harness-boundary.md` |
| 不知道 Claude 侧该调哪个 command / agent | `.claude/README.md` |
