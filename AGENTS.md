# AGENTS.md

OpenSpec 区块链研究协作的导航入口。

**核心理念**：知道去哪里找知识，而不是把所有知识加载进来。

---

## 一、启动行为

| 步骤 | 操作 | 来源 |
|------|------|------|
| 1 | 读取规则域索引 | `harness/rules/_index.yaml` |
| 2 | 识别任务类型并路由 | `harness/workflows/` |
| 3 | 按需加载规则 | `_index.yaml` 中对应 domain 的规则列表 |
| 4 | 读取本地 knowledge | `knowledge/` 按问题类型定位 |
| 5 | 结合联网搜索 | 补充缺口或验证 >6 个月前的信息 |

**详情**：`harness/workflows/intake-workflow.md`

---

## 二、任务与路由

| 任务类型 | 触发条件 | Workflow | 主要规则域 |
|----------|----------|----------|------------|
| `new-topic` | 创建新主题研究 | `intake-workflow.md` | intake |
| `update-topic` | 更新现有主题 | `update-existing-knowledge.md` | merge |
| `source-extraction` | 提取来源 | `source-workflow.md` | source |
| `atom-writing` | 编写知识原子 | `principle-atom-workflow.md` | definition/mechanism/evolution |
| `comparison` | 比较分析 | `comparison-workflow.md` | comparison |
| `diagram` | 创建图表 | `diagram-workflow.md` | diagram |
| `review` | 评审 | `review-workflow.md` | review |
| `merge` | 合并到 knowledge | `merge-workflow.md` | merge |

---

## 三、规则索引

**总索引**：`harness/rules/_index.yaml`

### General Rules (`harness/rules/general/`)

| 规则 | 用途 | 约束 |
|------|------|------|
| `repo-governance.md` | 仓库治理 | 变更必须走 OpenSpec |
| `evidence-policy.md` | 证据政策 | L1/L2/L3/L4 等级定义 |
| `terminology-policy.md` | 术语治理 | 复用 glossary taxonomy |
| `traceability-policy.md` | 可追溯性 | claim→source 映射 |
| `update-policy.md` | 更新政策 | 知识更新流程 |

### Research Rules (`harness/rules/research/`)

| 规则 | 用途 | 约束 |
|------|------|------|
| `definition-rules.md` | 定义写作 | primitive 结构规范 |
| `mechanism-rules.md` | 机制分析 | 机制拆解方法 |
| `evolution-rules.md` | 演进分析 | 时间线/里程碑 |
| `comparison-rules.md` | 比较分析 | 维度/矩阵 |
| `source-validation-rules.md` | 来源验证 | 来源可信度评估 |
| `uncertainty-rules.md` | 不确定性 | 置信度标注 |

### Diagram Rules (`harness/rules/diagrams/`)

| 规则 | 用途 |
|------|------|
| `diagram-selection-matrix.md` | 图类型选择 |
| `abstraction-boundaries.md` | 抽象边界 |
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

## 四、Skills 索引

### Research Skills (`skills/research/`)

| Skill | 用途 |
|-------|------|
| `create-research-item/` | 初始化研究项目结构 |
| `extract-source-pack/` | 从 URL 提取来源包 |
| `write-definition-atom/` | 编写定义类型 atom |
| `write-mechanism-atom/` | 编写机制类型 atom |
| `write-evolution-atom/` | 编写演进类型 atom |
| `write-comparison-note/` | 编写比较分析笔记 |
| `review-knowledge-item/` | 评审知识产出物 |

### Maintenance Skills (`skills/maintenance/`)

| Skill | 用途 |
|-------|------|
| `refresh-existing-topic/` | 刷新现有主题（检查更新） |
| `merge-change-into-knowledge/` | 将 change 合并到 knowledge |

**详情**：`skills/README.md`

---

## 五、用户级 Skills（全局）

以下 skills 配置在 `~/.claude/skills/`，优先使用：

| Skill | 用途 | 输入 |
|-------|------|------|
| `feipi-gen-plantuml-arch-diagram` | 生成 PlantUML 架构图 | `architecture-brief.yaml` |
| `feipi-gen-plantuml-sequence-diagram` | 生成 PlantUML 时序图 | `sequence-brief.yaml` |

**工作流程**：brief 校验 → 覆盖校验 → 布局校验 → 渲染校验

**详情**：`~/.claude/skills/feipi-gen-plantuml-*/SKILL.md`

---

## 六、Scripts 索引

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

**详情**：`scripts/README.md`

---

## 七、目录结构

### Knowledge 目录

| 目录 | 用途 |
|------|------|
| `knowledge/glossary/meta/` | 术语元数据（categories/taxonomy/relations） |
| `knowledge/domains/` | 域级知识 |
| `knowledge/topics/` | 主题知识（primitives / synthesis） |
| `knowledge/decisions/` | 场景决策知识 |
| `knowledge/indexes/` | 索引文件 |
| `knowledge/templates/` | 写作模板 |

### OpenSpec Changes 目录

| 路径 | 用途 |
|------|------|
| `openspec/changes/<change-id>/request.md` | 问题定义 |
| `openspec/changes/<change-id>/plan.md` | 研究计划 |
| `openspec/changes/<change-id>/draft.md` | 分析草稿 |
| `openspec/changes/<change-id>/evidence-matrix.md` | 证据矩阵 |
| `openspec/changes/<change-id>/sources/` | 来源文件 |

**详情**：`openspec/changes/README.md`

---

## 八、核心约束速查

| 约束 | 来源 |
|------|------|
| 禁止直接修改 `knowledge/` 主线 | `repo-governance.md` |
| 每个 claim 必须绑定 source id | `traceability-policy.md` |
| 证据等级 L1/L2 用于核心技术主张 | `evidence-policy.md` |
| 术语复用 `knowledge/glossary/meta/` taxonomy | `terminology-policy.md` |
| 每个 topic 独立目录，atoms 与 claims 对应 | `definition-rules.md` |

---

## 九、遇到问题时

| 问题类型 | 查看位置 |
|----------|----------|
| 流程问题（下一步做什么） | `harness/workflows/` |
| 规范问题（如何写/约束） | `harness/rules/` |
| 操作问题（具体执行） | `skills/` |
| 自动化需求（脚本） | `scripts/` |
