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
| 8 | 结合联网搜索 | 补充本地知识缺口；详见 `.claude/tools/mcp-tools.md` |
| 9 | 网页内容提取 | 提取网页详情；详见 `.claude/tools/mcp-tools.md` |

**Source of Truth**：`openspec/config.yaml` + `openspec/schemas/blockchain-research/schema.yaml`

---

## 三、任务与路由

| 任务类型 | 触发条件 | Workflow |
|----------|----------|----------|
| `new-research` | 创建新研究 | `harness/workflows/intake-workflow.md` |
| `source` | 来源收集与验证 | `harness/workflows/source-workflow.md` |
| `update-research` | 更新现有研究 | `harness/workflows/update-existing-knowledge.md` |
| `review` | 评审研究产出 | `harness/workflows/review-workflow.md` |
| `apply` | 应用到 knowledge | `openspec/config.yaml` apply 段 |
| `governance-review` | 修改 OpenSpec / Harness / AGENTS 路由 | `harness/workflows/governance-review-workflow.md` |
| `spec-system-audit` | 定期审查规约体系触发链、索引链与死引用 | `harness/workflows/spec-system-audit-workflow.md` |

> 各任务产出位置见「四、资产模型」。

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

| 类型 | 描述 | 示例 |
|------|------|------|
| **primitive** | 单个协议/EIP/机制 | eip-4337, consensus-qbft |
| **synthesis** | 关系/演进/分类分析 | aa-eip-evolution, bft-comparison |
| **decision** | 场景决策 | agentic-payment |

> 各类型产出位置见「四、资产模型」。

**研究路径**：

| 路径 | 用途 | 适用类型 |
|------|------|----------|
| `deep-dive` | 深度分析单个对象 | primitive |
| `evolution` | 演进历史分析 | synthesis |
| `scenario` | 场景驱动分析 | decision |

**详情**：`openspec/schemas/blockchain-research/schema.yaml` (context 段)

---

## 六、规则索引

规则按域分为四类，各域包含的具体规则文件、适用阶段与加载时机见：
- **总索引**：`harness/rules/_index.yaml`
- **阶段依赖索引**：`harness/rules/_phase_index.yaml`

| 规则域 | 用途摘要 |
|--------|----------|
| **General** (`harness/rules/general/`) | 仓库治理、术语治理、可追溯性、更新政策 |
| **Research** (`harness/rules/research/`) | 原子写作（定义/机制/演进）、比较分析、来源验证、不确定性处理、组件分析与共识深度 |
| **Diagram** (`harness/rules/diagrams/`) | 图表政策、类型选择、brief 质量、关系语义、注释规范、架构图与时序图质量 |
| **Writing** (`harness/rules/writing/`) | 结构、表格、摘要规范与语言风格 |

---

## 七、Skills 索引

| 分类 | 路径 | 用途摘要 |
|------|------|----------|
| **Research** | `skills/research/` | 创建研究项目、提取来源、编写原子笔记（定义/机制/演进/比较）、评审知识产出 |
| **Maintenance** | `skills/maintenance/` | 刷新现有主题、合并 change 到 knowledge |
| **OpenSpec Research** | `skills/openspec-research-*/` | 辅助生成 request/plan/draft/artifact、端到端 research 执行 |
| **用户级（全局）** | `~/.claude/skills/` | PlantUML 架构图与时序图生成（`feipi-plantuml-*`） |

**详情**：`skills/README.md`

---

## 八、Scripts 索引

| 分类 | 路径 | 用途摘要 |
|------|------|----------|
| **General** | `scripts/general/` | 初始化研究项目、检查 frontmatter、可追溯性校验、知识树验证 |
| **Research** | `scripts/research/` | claims 标准化、比较矩阵构建、来源验证、术语漂移检测、artifact/diagram contract 校验 |
| **Publish** | `scripts/publish/` | 手动 apply 时移动 change 到 knowledge（备选，主路径是 publish-agent） |
| **Diagram（备选）** | `scripts/diagrams/`、`scripts/maintenance/` | PlantUML 语法校验与渲染；优先使用用户级 skills |

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
| 联网搜索默认走 `fastmcp-gateway` 的 `searxng_search_web` | 本文件（启动行为）、`.claude/tools/mcp-tools.md` |

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

按问题类型对照 `CLAUDE.md` 中的「快速索引」表查找对应入口。常见路径：

| 问题类型 | 入口 |
|----------|------|
| 系统约束（artifact 模型、工作流） | `openspec/config.yaml` + `openspec/schemas/blockchain-research/schema.yaml` |
| 流程问题（下一步做什么） | `harness/workflows/_index.yaml` |
| 阶段加载问题 | `harness/rules/_phase_index.yaml` |
| 执行角色问题 | `.claude/README.md` → `.claude/agents/` |
| 规约体系体检 | `.claude/commands/spec-system-audit.md` |
| 操作与自动化 | `skills/` + `scripts/` |
