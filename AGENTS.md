# AGENTS.md

OpenSpec 区块链研究协作的导航入口。

**核心理念**：知道去哪里找知识，而不是把所有知识加载进来。

---

## 一、系统架构分层

```
┌─────────────────────────────────────────────────────────┐
│  入口层 (Entry Point)                                   │
│  → AGENTS.md (本文件)                                    │
│  → CLAUDE.md              - Claude 侧轻量入口             │
│  → .claude/README.md      - Claude 路由与命令索引         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  系统约束层 (Source of Truth)                            │
│  → openspec/config.yaml      - OpenSpec 工作流配置        │
│  → openspec/schemas/.../schema.yaml - 研究对象模型        │
│  → openspec/specs/...        - 研究系统规范 (规划中)       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  路由层 (Routing / Harness)                              │
│  → harness/workflows/_index.yaml - workflow 索引         │
│  → harness/rules/_phase_index.yaml - 阶段依赖索引        │
│  → harness/rules/_index.yaml  - 规则域索引               │
│  → .claude/agents/...        - Agent 角色合同            │
│  → harness/workflows/...     - 工作流程                 │
│  → harness/rules/...         - 规则详情                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  过程层 (Process)                                        │
│  → openspec/changes/...      - 研究改动包                │
│  → skills/...                - 可复用操作                │
│  → scripts/...               - 自动化工具                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  资产层 (Canonical Assets)                               │
│  → knowledge/analysis/...    - 事实分析资产              │
│  → knowledge/decisions/...   - 场景决策资产              │
└─────────────────────────────────────────────────────────┘
```

---

## 二、启动行为

| 步骤 | 操作 | 来源 |
|------|------|------|
| 1 | 读取本文件 (AGENTS.md) | 获取系统架构概览 |
| 2 | 读取 OpenSpec 配置 | `openspec/config.yaml` - 工作流定义 |
| 3 | 读取对象模型 | `openspec/schemas/blockchain-research/schema.yaml` |
| 4 | 读取 workflow 索引并识别任务类型 | `harness/workflows/_index.yaml` |
| 5 | 按阶段加载依赖 | `harness/rules/_phase_index.yaml` |
| 6 | 按规则域补充叶子规则 | `harness/rules/_index.yaml` |
| 7 | Claude 场景下读取命令/agent 索引 | `CLAUDE.md` + `.claude/README.md` |
| 8 | 结合联网搜索 | 补充本地知识缺口；如需联网搜索，优先使用 `fastmcp-gateway` 暴露的 `searxng_search_web` MCP 工具 |
| 9 | 网页内容提取 | 需要提取网页详情时使用 `crawl4ai` MCP 的 `md` 工具 |

**联网搜索约束**：
- 当任务明确要求”联网搜索 / 在线检索 / web search / search”时，默认使用 `fastmcp-gateway` 提供的 `searxng_search_web`。
- `searxng_search_web` 为 SearXNG 元搜索工具，输入支持 `query`，可选 `category`、`max_results`、`language`、`time_range`。
- 若该 MCP 在当前会话不可用，应先明确说明，再选择替代搜索方式；不要无提示地切换到其他搜索通道。

**网页内容提取约束**：
- 当需要提取网页内容、获取网页详情、将网页转换为 Markdown 时，使用 `crawl4ai` MCP 服务器提供的工具。
- `crawl4ai` 提供以下工具：
  - `md`：将网页转换为 Markdown（默认使用 fit 模式，支持 raw/bm25/llm 过滤）
  - `html`：获取并清理网页 HTML 结构
  - `screenshot`：获取网页截图
  - `pdf`：生成网页 PDF
  - `execute_js`：在浏览器上下文中执行 JavaScript
  - `crawl`：完整的网页爬取（支持 hooks 配置）
  - `ask`：查询 Crawl4AI 库的使用文档
- 提取网页内容时优先使用 `md` 工具，参数包括：
  - `url`：目标网页 URL（必填）
  - `f`：过滤模式，可选 `fit`（默认）、`raw`、`bm25`、`llm`
  - `q`：查询字符串（用于 bm25/llm 模式）
  - `provider`：LLM provider 覆盖（可选）
  - `temperature`：LLM temperature（可选）

**Source of Truth**：`openspec/config.yaml` + `openspec/schemas/blockchain-research/schema.yaml`

---

## 三、任务与路由

| 任务类型 | 触发条件 | Workflow | 产出位置 |
|----------|----------|----------|----------|
| `new-research` | 创建新研究 | `harness/workflows/intake-workflow.md` | `openspec/changes/` |
| `source` | 来源收集与验证 | `harness/workflows/source-workflow.md` | `openspec/changes/<id>/sources/` |
| `update-research` | 更新现有研究 | `harness/workflows/update-existing-knowledge.md` | `openspec/changes/` |
| `review` | 评审研究产出 | `harness/workflows/review-workflow.md` | `openspec/changes/<id>/review/` |
| `apply` | 应用到 knowledge | `openspec/config.yaml` apply 段 | `knowledge/analysis/` 或 `knowledge/decisions/` |
| `governance-review` | 修改 OpenSpec / Harness / AGENTS 路由 | `harness/workflows/governance-review-workflow.md` | `openspec/changes/<id>/review/` |
| `spec-system-audit` | 定期审查规约体系触发链、索引链与死引用 | `harness/workflows/spec-system-audit-workflow.md` | 会话总结 / `harness/reports/`（可选） |

### v1 Multi-Agent 执行（条件加载）

当 workflow 明确支持 multi-agent 执行时，从 `.claude/agents/` 读取角色合同。

**主会话不直接写 `request.md`、`plan.md`、`draft.md`**，这些由 author agent 负责。
主会话充当 orchestrator，按 `research_type` 路由到对应 author agent，并统一调度 specialist agent。

**Author Agents（研究型）**：

| Agent | 职责 |
|-------|------|
| @primitive-author | 单个 primitive 的主链写作（request → plan → draft） |
| @synthesis-author | 多 primitive 的横向对比合成（读取各 primitive draft，做对比矩阵） |
| @decision-author | 场景决策分析写作（场景定义、决策标准、verdict） |

**Specialist Agents（专长型）**：

| Agent | 职责 |
|-------|------|
| @source-evidence-agent | `sources/` 收集、链接验证、source review |
| @diagram-agent | 图表生成与验证 |
| @review-critic-agent | 独立技术评审、traceability audit |
| @publish-agent | artifact 提炼与 update impact scan |
| @spec-system-audit-agent | 仓库规约体系审计、孤岛文件与死引用清理 |

**多 agent 边界**：
- 只允许主会话 orchestrator 调用 specialist agent；author agent 不再嵌套拉起其他 subagent。
- `sources/`、`diagrams/`、`review/`、`knowledge/` 分属不同上下文，避免主链写作与辅助产物互相污染。
- 每次阶段切换优先回到索引：先查 `harness/workflows/_index.yaml`，再按 `harness/rules/_phase_index.yaml` 加载叶子规则。

**条件角色**：

| Agent | 激活条件 |
|-------|----------|
| @governance-review-agent | 修改 `openspec/**`、`harness/**`、`AGENTS.md`、`docs/governance/**` |
| @spec-system-audit-agent | 需要做 repo-wide 规约体系周期性清理或卫生审计 |

**Agent 合同规范**：`.claude/agents/CONTRACT.md`

---

## 四、资产模型（单一事实源）

**长期资产只存在于两处**：

| 资产类型 | 路径 | 产出物 | 用途 |
|----------|------|--------|------|
| **事实分析** | `knowledge/analysis/` | `artifact.md` | 技术机制、演进关系（primitives 按 domain_id 分组，synthesis 扁平化） |
| **场景决策** | `knowledge/decisions/` | `artifact.md` + `verdict.md` | 场景比较、选型判断（按 domain_id 分组） |

**domain 是分组概念**，不作为独立的 `object_type`，不提供独立的 `artifact.md`。

**过程产物（不进入长期目录）**：

| 产物 | 位置 | 用途 |
|------|------|------|
| `request.md` | `openspec/changes/<id>/` | 研究问题定义 |
| `plan.md` | `openspec/changes/<id>/` | 研究计划与来源规划 |
| `draft.md` | `openspec/changes/<id>/` | 集中 review 稿 |
| `decision-criteria.md` | `openspec/changes/<id>/` | 决策标准（可选） |

**详情**：`openspec/schemas/blockchain-research/schema.yaml`

---

## 五、研究对象模型

| 类型 | 描述 | 示例 | 产出位置 |
|------|------|------|----------|
| **primitive** | 单个协议/EIP/机制 | eip-4337, consensus-qbft | `knowledge/analysis/primitives/<domain_id>/<topic>/artifact.md` |
| **synthesis** | 关系/演进/分类分析 | aa-eip-evolution, bft-comparison | `knowledge/analysis/synthesis/<topic>/artifact.md` |
| **decision** | 场景决策 | agentic-payment | `knowledge/decisions/<domain_id>/<topic>/artifact.md` + `verdict.md` |

**研究路径**：

| 路径 | 用途 | 适用类型 |
|------|------|----------|
| `deep-dive` | 深度分析单个对象 | primitive |
| `evolution` | 演进历史分析 | synthesis |
| `scenario` | 场景驱动分析 | decision |

**详情**：`openspec/schemas/blockchain-research/schema.yaml` (context 段)

---

## 六、规则索引

**总索引**：`harness/rules/_index.yaml`

**阶段依赖索引**：`harness/rules/_phase_index.yaml`

### General Rules (`harness/rules/general/`)

| 规则 | 用途 |
|------|------|
| `repo-governance.md` | 仓库治理（变更必须走 OpenSpec） |
| `terminology-policy.md` | 术语治理（复用 glossary taxonomy） |
| `traceability-policy.md` | 可追溯性（claim→source 映射） |
| `update-policy.md` | 更新政策（向后兼容处理） |

### Research Rules (`harness/rules/research/`)

| 规则 | 用途 |
|------|------|
| `atom-definition-rules.md` | 定义原子写作 |
| `atom-mechanism-rules.md` | 机制分析写作 |
| `atom-evolution-rules.md` | 演进分析写作 |
| `note-comparison-rules.md` | 比较分析写作 |
| `source-validation-rules.md` | 来源验证 |
| `uncertainty-rules.md` | 不确定性处理 |
| `component-quality-rules.md` | 组件分析与性能质量要求 |
| `consensus-depth-rules.md` | 共识算法分析深度要求 |

### Diagram Rules (`harness/rules/diagrams/`)

| 规则 | 用途 |
|------|------|
| `diagram-policy.md` | 图表总政策（正式规则来源） |
| `diagram-selection-matrix.md` | 图类型选择 |
| `brief-quality-rules.md` | Brief 质量评估 |
| `relationship-rules.md` | 关系语义 |
| `annotation-rules.md` | 注释规范 |
| `simplification-policy.md` | 简化政策 |
| `diagram-review-checklist.md` | 评审清单 |
| `architecture-quality-rules.md` | 架构图质量规约 |
| `component-abstraction-rules.md` | 组件抽象层级规约 |

### Writing Rules (`harness/rules/writing/`)

| 规则 | 用途 |
|------|------|
| `structure-rules.md` | 结构规范 |
| `table-rules.md` | 表格规范 |
| `summary-rules.md` | 摘要规范 |
| `language-rules.md` | 语言与写作风格 |

---

## 七、Skills 索引

### Research Skills (`skills/research/`)

| Skill | 用途 |
|-------|------|
| `create-research-item/` | 初始化研究项目结构 |
| `extract-source-pack/` | 从 URL 提取来源包 |
| `write-definition-atom/` | 编写定义类型笔记 |
| `write-mechanism-atom/` | 编写机制类型笔记 |
| `write-evolution-atom/` | 编写演进类型笔记 |
| `write-comparison-note/` | 编写比较分析笔记 |
| `review-knowledge-item/` | 评审知识产出物 |

### Maintenance Skills (`skills/maintenance/`)

| Skill | 用途 |
|-------|------|
| `refresh-existing-topic/` | 刷新现有主题 |
| `merge-change-into-knowledge/` | 合并 change 到 knowledge |

### OpenSpec Research Skills (`skills/openspec-research-*/`)

| Skill | 用途 |
|-------|------|
| `openspec-research-build-plan/` | 辅助生成 plan.md |
| `openspec-research-build-draft/` | 辅助生成 draft.md |
| `openspec-research-build-artifact/` | 辅助提升到 canonical 资产 |
| `openspec-research-build-request/` | 辅助生成 request.md |
| `openspec-research-build-research/` | 辅助执行端到端 research |

### 用户级 Skills（全局）

以下 skills 配置在 `~/.claude/skills/`，优先使用：

| Skill | 用途 | 输入 |
|-------|------|------|
| `feipi-plantuml-generate-architecture-diagram` | 生成 PlantUML 架构图 | `architecture-brief.yaml` |
| `feipi-plantuml-generate-sequence-diagram` | 生成 PlantUML 时序图 | `sequence-brief.yaml` |

**详情**：`skills/README.md`

---

## 八、Scripts 索引

### General Scripts (`scripts/general/`)

| 脚本 | 用途 | 用法 |
|------|------|------|
| `init_research_item.py` | 初始化研究项目 | `--topic <topic> --type <type>` |
| `check_frontmatter.py` | 检查 `knowledge/` 长期资产 frontmatter | `[knowledge/\|artifact.md\|verdict.md]` |
| `check_traceability.py` | 检查可追溯性 | `--topic <topic>` |
| `validate_knowledge_tree.py` | 检查长期资产目录树 | `[directory]` |

### Research Scripts (`scripts/research/`)

| 脚本 | 用途 | 用法 |
|------|------|------|
| `normalize_claims.py` | 标准化 claims | `--topic <topic>` |
| `build_comparison_matrix.py` | 构建比较矩阵 | `--topics <list> --output <path>` |
| `validate_sources.py` | 验证来源 | `--topic <topic>` |
| `find_term_drift.py` | 查找术语漂移 | `--term <term>` |
| `check_artifact_contract.py` | 校验 artifact 最小章节合同 | `[knowledge-dir]` |
| `validate_draft_diagram_contract.py` | 校验 draft 中的 diagram contract | `--draft <path>` |

### Publish Scripts (`scripts/publish/`)

| 脚本 | 用途 | 用法 |
|------|------|------|
| `move_change_outputs.py` | 手动 apply 时移动 change 到 knowledge（备选，主路径是 publish-agent） | `--change <id> --topic <slug> --type <type> --domain <domain_id>` |

### Diagram Scripts（备选）

**注意**：架构图和时序图优先使用用户级 skills。以下脚本仅在手动创建图表时使用：

| 脚本 | 用途 | 用法 |
|------|------|------|
| `check_plantuml.sh` | 校验 PlantUML 语法 | `<file.puml> [--svg-output <output>]` |
| `maintenance/render.sh` | 渲染 PlantUML / SVG 对比 | `<file.puml>` |
| `diagrams/validate_diagram_model.py` | 验证 diagram model | `<model.yaml>` |

**详情**：`scripts/README.md`

---

## 九、核心约束速查

| 约束 | 来源 |
|------|------|
| 禁止直接修改 `knowledge/` 主线 | `openspec/config.yaml` / `repo-governance.md` |
| 长期资产只在 `analysis/` 和 `decisions/` | `openspec/schemas/blockchain-research/schema.yaml` |
| 过程文件保留在 `openspec/changes/` | `openspec/changes/README.md` |
| 证据等级 L1/L2 用于核心技术主张 | `openspec/specs/evidence-policy/spec.md` |
| 术语复用 glossary taxonomy | `terminology-policy.md` |
| 每个 claim 必须绑定 source id | `traceability-policy.md` |
| 联网搜索默认走 `fastmcp-gateway` 的 `searxng_search_web` | 本文件（启动行为 / 联网搜索约束） |

---

## 十、OpenSpec / Harness 边界（条件加载）

**任务语义优先，路径辅助**：不要因为文件位于某个路径下就自动加载边界规范，只有当任务语义涉及规约/架构调整时才加载。

**必须读取** `docs/governance/openspec-harness-boundary.md`：
- 调整 OpenSpec / Harness 职责边界
- 修改 schema / specs / templates / governance / repository architecture
- 修改用于定义或评审规约分层的 workflow / rules / skills
- 修改 `.claude/commands/` 或 `.claude/agents/` 中与仓库路由、角色合同、阶段编排相关的内容
- 修改 AGENTS.md 中与仓库路由、治理、分层相关的段落
- 评审上述类型的变更

**不要默认读取**：
- 普通技术调研、知识条目更新
- 来源收集与验证、图表生成
- 一般性的 research workflow 微调
- 与仓库分层无关的 skills 优化

**详情**：`docs/governance/openspec-harness-boundary.md`

**治理索引**：`docs/governance/README.md`

---

## 十一、遇到问题时

| 问题类型 | 查看位置 |
|----------|----------|
| 系统约束（artifact 模型、工作流） | `openspec/config.yaml` + `openspec/schemas/blockchain-research/schema.yaml` |
| 流程问题（下一步做什么） | `harness/workflows/_index.yaml` → 对应 workflow |
| 阶段加载问题（当前该读哪些规范） | `harness/rules/_phase_index.yaml` |
| 执行角色问题（谁来做、怎么分工） | `.claude/README.md` → `.claude/agents/` |
| 规约体系体检（孤岛、死引用、触发链） | `.claude/commands/spec-system-audit.md` → `harness/workflows/spec-system-audit-workflow.md` |
| 规范问题（如何写/约束） | `harness/rules/_index.yaml` → 对应规则域 |
| 操作问题（具体执行） | `skills/` |
| 自动化需求（脚本） | `scripts/` |
