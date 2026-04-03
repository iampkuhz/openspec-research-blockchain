# AGENTS.md

OpenSpec 区块链研究协作的导航入口。

**核心理念**：知道去哪里找知识，而不是把所有知识加载进来。

---

## 一、系统架构分层

```
┌─────────────────────────────────────────────────────────┐
│  入口层 (Entry Point)                                   │
│  → AGENTS.md (本文件)                                    │
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
│  → harness/rules/_index.yaml  - 规则域索引               │
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
| 4 | 识别任务类型 | 路由到对应 workflow |
| 5 | 按需加载规则 | `harness/rules/_index.yaml` |
| 6 | 结合联网搜索 | 补充本地知识缺口 |

**Source of Truth**：`openspec/config.yaml` + `openspec/schemas/blockchain-research/schema.yaml`

---

## 三、任务与路由

| 任务类型 | 触发条件 | Workflow | 产出位置 |
|----------|----------|----------|----------|
| `new-research` | 创建新研究 | `harness/workflows/intake-workflow.md` | `openspec/changes/` |
| `update-research` | 更新现有研究 | `harness/workflows/update-existing-knowledge.md` | `openspec/changes/` |
| `review` | 评审研究产出 | `harness/workflows/review-workflow.md` | `openspec/changes/<id>/review/` |
| `apply` | 应用到 knowledge | `openspec/config.yaml` apply 段 | `knowledge/analysis/` 或 `knowledge/decisions/` |

---

## 四、资产模型（单一事实源）

**长期资产只存在于两处**：

| 资产类型 | 路径 | 产出物 | 用途 |
|----------|------|--------|------|
| **事实分析** | `knowledge/analysis/` | `artifact.md` | 技术机制、演进关系、域定义 |
| **场景决策** | `knowledge/decisions/` | `artifact.md` + `verdict.md` | 场景比较、选型判断 |

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
| **primitive** | 单个协议/EIP/机制 | eip-4337, consensus-qbft | `knowledge/analysis/primitives/` |
| **synthesis** | 关系/演进/分类分析 | aa-eip-evolution, bft-comparison | `knowledge/analysis/synthesis/` |
| **domain** | 主题域定义 | account-abstraction | `knowledge/analysis/domains/` |
| **decision** | 场景决策 | agentic-payment | `knowledge/decisions/` |

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

### General Rules (`harness/rules/general/`)

| 规则 | 用途 |
|------|------|
| `repo-governance.md` | 仓库治理（变更必须走 OpenSpec） |
| `evidence-policy.md` | 证据政策（L1/L2/L3/L4 等级定义） |
| `terminology-policy.md` | 术语治理（复用 glossary taxonomy） |
| `traceability-policy.md` | 可追溯性（claim→source 映射） |
| `update-policy.md` | 更新政策（向后兼容处理） |

### Research Rules (`harness/rules/research/`)

| 规则 | 用途 |
|------|------|
| `definition-rules.md` | 定义写作 |
| `mechanism-rules.md` | 机制分析 |
| `evolution-rules.md` | 演进分析 |
| `comparison-rules.md` | 比较分析 |
| `source-validation-rules.md` | 来源验证 |
| `uncertainty-rules.md` | 不确定性处理 |

### Diagram Rules (`harness/rules/diagrams/`)

| 规则 | 用途 |
|------|------|
| `diagram-selection-matrix.md` | 图类型选择 |
| `brief-quality-rules.md` | Brief 质量评估 |
| `relationship-rules.md` | 关系语义 |
| `annotation-rules.md` | 注释规范 |
| `simplification-policy.md` | 简化政策 |
| `diagram-review-checklist.md` | 评审清单 |

### Writing Rules (`harness/rules/writing/`)

| 规则 | 用途 |
|------|------|
| `structure-rules.md` | 结构规范 |
| `table-rules.md` | 表格规范 |
| `summary-rules.md` | 摘要规范 |

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
| `openspec-research-promote-canonical/` | 辅助提升到 canonical 资产 |

### 用户级 Skills（全局）

以下 skills 配置在 `~/.claude/skills/`，优先使用：

| Skill | 用途 | 输入 |
|-------|------|------|
| `feipi-gen-plantuml-arch-diagram` | 生成 PlantUML 架构图 | `architecture-brief.yaml` |
| `feipi-gen-plantuml-sequence-diagram` | 生成 PlantUML 时序图 | `sequence-brief.yaml` |

**详情**：`skills/README.md`

---

## 八、Scripts 索引

### General Scripts (`scripts/general/`)

| 脚本 | 用途 | 用法 |
|------|------|------|
| `init_research_item.py` | 初始化研究项目 | `--topic <topic> --type <type>` |
| `build_index.py` | 构建 topic 索引 | `--output <path>` |
| `check_frontmatter.py` | 检查 frontmatter | `[file\|directory]` |
| `check_traceability.py` | 检查可追溯性 | `--topic <topic>` |

### Research Scripts (`scripts/research/`)

| 脚本 | 用途 | 用法 |
|------|------|------|
| `normalize_claims.py` | 标准化 claims | `--topic <topic>` |
| `build_comparison_matrix.py` | 构建比较矩阵 | `--topics <list> --output <path>` |
| `validate_sources.py` | 验证来源 | `--topic <topic>` |
| `find_term_drift.py` | 查找术语漂移 | `--term <term>` |

### Publish Scripts (`scripts/publish/`)

| 脚本 | 用途 | 用法 |
|------|------|------|
| `move_change_outputs.py` | 移动 change 到 knowledge | `--change <id> --topic <topic> --domain <domain>` |
| `generate_topic_index.py` | 生成 topic 索引 | `--output <path>` |

### Diagram Scripts（备选）

**注意**：架构图和时序图优先使用用户级 skills。以下脚本仅在手动创建图表时使用：

| 脚本 | 用途 | 用法 |
|------|------|------|
| `check_plantuml.sh` | 校验 PlantUML 语法 | `<file.puml> [--svg-output <output>]` |
| `diagrams/render.sh` | 渲染 PlantUML | `<file.puml>` |
| `diagrams/validate_diagram_model.py` | 验证 diagram model | `<model.yaml>` |

**详情**：`scripts/README.md`

---

## 九、核心约束速查

| 约束 | 来源 |
|------|------|
| 禁止直接修改 `knowledge/` 主线 | `openspec/config.yaml` / `repo-governance.md` |
| 长期资产只在 `analysis/` 和 `decisions/` | `openspec/schemas/blockchain-research/schema.yaml` |
| 过程文件保留在 `openspec/changes/` | `openspec/changes/README.md` |
| 证据等级 L1/L2 用于核心技术主张 | `evidence-policy.md` |
| 术语复用 glossary taxonomy | `terminology-policy.md` |
| 每个 claim 必须绑定 source id | `traceability-policy.md` |

---

## 十、遇到问题时

| 问题类型 | 查看位置 |
|----------|----------|
| 系统约束（artifact 模型、工作流） | `openspec/config.yaml` + `openspec/schemas/blockchain-research/schema.yaml` |
| 流程问题（下一步做什么） | `harness/workflows/` |
| 规范问题（如何写/约束） | `harness/rules/` |
| 操作问题（具体执行） | `skills/` |
| 自动化需求（脚本） | `scripts/` |
