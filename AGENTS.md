# AGENTS.md - OpenSpec 区块链研究协作索引

你是这个仓库的区块链技术调研协作助手。

**核心理念：知道去哪里找知识，而不是把所有知识加载进来。**

---

## 一、启动时的自动行为

### 1. 读取规则索引

首先读取 `harness/rules/_index.yaml`，了解可用的规则域。

**禁止**默认加载所有 rules 正文。

### 2. 判断任务类型

根据用户问题识别任务类型：

| 任务类型 | 触发条件 | 路由 workflow |
|----------|----------|---------------|
| `new-topic` | 创建新主题研究 | `harness/workflows/intake-workflow.md` |
| `update-topic` | 更新现有主题 | `harness/workflows/update-existing-knowledge.md` |
| `source-extraction` | 提取来源 | `harness/workflows/source-workflow.md` |
| `atom-writing` | 编写知识原子 | `harness/workflows/principle-atom-workflow.md` |
| `comparison` | 比较分析 | `harness/workflows/comparison-workflow.md` |
| `diagram` | 创建图表 | `harness/workflows/diagram-workflow.md` |
| `review` | 评审 | `harness/workflows/review-workflow.md` |
| `merge` | 合并到 knowledge | `harness/workflows/merge-workflow.md` |

### 3. 渐进加载规则

根据任务类型，按需加载对应 rules：

```yaml
# 从 harness/rules/_index.yaml 加载

intake → [repo-governance.md, terminology-policy.md, definition-rules.md]
source → [evidence-policy.md, traceability-policy.md, source-validation-rules.md]
definition → [terminology-policy.md, traceability-policy.md, definition-rules.md]
mechanism → [evidence-policy.md, traceability-policy.md, mechanism-rules.md]
# ...
```

### 4. 读取本地 knowledge

当用户提出研究相关问题时：

1. 先判断问题类型（primitive / synthesis / domain / decision）
2. 读取对应 `knowledge/` 目录中的文件

| 问题类型 | 读取路径 |
|----------|----------|
| primitive | `knowledge/topics/<domain>/<topic>/atoms/*.md` |
| synthesis | `knowledge/topics/<domain>/<topic>/atoms/module-evolution.md` |
| domain | `knowledge/domains/<domain>/` |
| decision | `knowledge/decisions/<domain>/<topic>/` |

### 5. 结合联网搜索

- 本地知识完整 → 基于本地知识回答
- 本地知识有缺口 → 结合联网搜索补充
- 本地知识可能过时（>6 个月）→ 必须联网验证

---

## 二、核心原则

### 原则 1: 所有知识变更都必须走 OpenSpec

**禁止**直接修改 `knowledge/` 下的主线知识。

**必须**通过以下流程：
1. 在 `openspec/changes/` 创建 change
2. 完成研究并产出 draft
3. 通过 review 后 merge 到 knowledge

### 原则 2: 原子化知识

**禁止**将不同主题混在同一文件。

**必须**：
- 每个 topic 有独立的目录
- 支持拆分为多个 atoms（definition / mechanism / evolution）
- claims 与 atoms 一一对应

### 原则 3: 证据可追溯

**禁止**无来源的主张。

**必须**：
- 每个 claim 绑定到 source id
- 区分 L1/L2/L3/L4 证据等级
- 记录 evidence gaps

### 原则 4: 术语一致性

**禁止**在同一 topic 内混用不同术语指代同一概念。

**必须**：
- 使用 `knowledge/glossary/meta/` 定义的 taxonomy
- 新建术语时声明 category 和 layer
- 复用已有术语时检查边界

---

## 三、工作流程快速导航

### 开始新研究

```
1. harness/workflows/intake-workflow.md
   → 判断对象类型、创建 change

2. harness/workflows/source-workflow.md
   → 收集来源、提取 claims

3. harness/workflows/principle-atom-workflow.md
   → 编写 atoms

4. harness/workflows/review-workflow.md
   → 评审

5. harness/workflows/merge-workflow.md
   → 合并到 knowledge
```

### 更新现有知识

```
1. harness/workflows/update-existing-knowledge.md
   → 评估影响范围、创建 change

2. harness/workflows/review-workflow.md
   → 评审

3. harness/workflows/merge-workflow.md
   → 合并
```

### 创建图表

```
1. harness/workflows/diagram-workflow.md
   → 创建 model → 渲染 → 验证 → 评审
```

---

## 四、规则索引

完整规则位于 `harness/rules/` 目录，按域组织：

### General Rules (`harness/rules/general/`)

| 规则 | 用途 |
|------|------|
| [repo-governance.md](./harness/rules/general/repo-governance.md) | 仓库治理 |
| [evidence-policy.md](./harness/rules/general/evidence-policy.md) | 证据政策 |
| [terminology-policy.md](./harness/rules/general/terminology-policy.md) | 术语治理 |
| [traceability-policy.md](./harness/rules/general/traceability-policy.md) | 可追溯性 |
| [update-policy.md](./harness/rules/general/update-policy.md) | 更新政策 |

### Research Rules (`harness/rules/research/`)

| 规则 | 用途 |
|------|------|
| [definition-rules.md](./harness/rules/research/definition-rules.md) | 定义写作 |
| [mechanism-rules.md](./harness/rules/research/mechanism-rules.md) | 机制分析 |
| [evolution-rules.md](./harness/rules/research/evolution-rules.md) | 演进分析 |
| [comparison-rules.md](./harness/rules/research/comparison-rules.md) | 比较分析 |
| [source-validation-rules.md](./harness/rules/research/source-validation-rules.md) | 来源验证 |
| [uncertainty-rules.md](./harness/rules/research/uncertainty-rules.md) | 不确定性 |

### Diagram Rules (`harness/rules/diagrams/`)

| 规则 | 用途 |
|------|------|
| [diagram-selection-matrix.md](./harness/rules/diagrams/diagram-selection-matrix.md) | 图选择 |
| [abstraction-boundaries.md](./harness/rules/diagrams/abstraction-boundaries.md) | 抽象边界 |
| [relationship-rules.md](./harness/rules/diagrams/relationship-rules.md) | 关系语义 |
| [annotation-rules.md](./harness/rules/diagrams/annotation-rules.md) | 注释规范 |
| [simplification-policy.md](./harness/rules/diagrams/simplification-policy.md) | 简化政策 |
| [diagram-review-checklist.md](./harness/rules/diagrams/diagram-review-checklist.md) | 评审清单 |

### Writing Rules (`harness/rules/writing/`)

| 规则 | 用途 |
|------|------|
| [structure-rules.md](./harness/rules/writing/structure-rules.md) | 结构规范 |
| [table-rules.md](./harness/rules/writing/table-rules.md) | 表格规范 |
| [summary-rules.md](./harness/rules/writing/summary-rules.md) | 摘要规范 |

---

## 五、Skills 索引

Skills 位于 `skills/` 目录，按类型组织：

### Research Skills

| Skill | 用途 |
|-------|------|
| `research/create-research-item/` | 创建研究项目 |
| `research/extract-source-pack/` | 提取来源包 |
| `research/write-definition-atom/` | 编写定义 atom |
| `research/write-mechanism-atom/` | 编写机制 atom |
| `research/write-evolution-atom/` | 编写演进 atom |
| `research/write-comparison-note/` | 编写比较分析 |
| `research/review-knowledge-item/` | 评审知识 |

### Diagram Skills

| Skill | 用途 |
|-------|------|
| `diagrams/create-diagram-model-from-atom/` | 创建 diagram model |
| `diagrams/render-plantuml/` | 渲染 PlantUML |
| `diagrams/review-diagram/` | 评审图表 |
| `diagrams/simplify-diagram/` | 简化图表 |

### Maintenance Skills

| Skill | 用途 |
|-------|------|
| `maintenance/refresh-existing-topic/` | 刷新现有主题 |
| `maintenance/merge-change-into-knowledge/` | 合并 change |

---

## 六、Scripts 索引

Scripts 位于 `scripts/` 目录：

### General Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/general/init_research_item.py` | 初始化研究项目 |
| `scripts/general/build_index.py` | 构建 topic 索引 |
| `scripts/general/check_frontmatter.py` | 检查 frontmatter |
| `scripts/general/check_traceability.py` | 检查可追溯性 |

### Research Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/research/normalize_claims.py` | 标准化 claims |
| `scripts/research/build_comparison_matrix.py` | 构建比较矩阵 |
| `scripts/research/validate_sources.py` | 验证来源 |
| `scripts/research/find_term_drift.py` | 查找术语漂移 |

### Diagram Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/diagrams/render.sh` | 渲染 PlantUML |
| `scripts/diagrams/validate_diagram_model.py` | 验证 diagram model |
| `scripts/diagrams/check_diagram_references.py` | 检查 diagram 引用 |
| `scripts/diagrams/compare_svg.sh` | 比较 SVG 差异 |

### Publish Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/publish/move_change_outputs.py` | 移动 change 到 knowledge |
| `scripts/publish/generate_topic_index.py` | 生成 topic 索引 |

---

## 七、知识目录导航

```
knowledge/
├── glossary/meta/        # 术语元数据
│   ├── concept-categories.yaml
│   ├── layer-taxonomy.yaml
│   ├── relation-types.yaml
│   └── evidence-status.yaml
├── domains/              # 域知识
│   └── <domain>/
├── topics/               # 主题知识（primitives / synthesis）
│   └── <domain>/<topic>/
│       ├── overview.md
│       ├── atoms/
│       ├── claims/
│       ├── comparisons/
│       ├── diagrams/
│       ├── sources/
│       └── changelog.md
├── indexes/              # 索引文件
│   ├── topic-index.md
│   ├── concept-index.md
│   ├── diagram-index.md
│   └── comparison-index.md
└── templates/            # 模板
    └── topic-template/
```

---

## 八、OpenSpec Change 流程

所有知识变更必须在 `openspec/changes/` 中创建 change：

```
openspec/changes/<change-id>/
├── request.md       # 问题定义
├── plan.md          # 研究计划
├── draft.md         # 分析草稿
├── evidence-matrix.md
├── sources/
│   ├── inbox.yaml
│   ├── fetched/
│   └── excerpts/
└── .openspec.yaml
```

### Change 类型

| 类型 | 用途 | 模板 |
|------|------|------|
| `new-topic` | 新增主题 | `openspec/templates/change/new-topic/` |
| `update-topic` | 更新现有 | `openspec/templates/change/update-topic/` |
| `refactor-topic` | 重构 | `openspec/templates/change/refactor-topic/` |

---

## 九、证据等级

| 等级 | 来源 | 用途 |
|------|------|------|
| L1 | 官方规范/EIP/白皮书 | 核心技术主张 |
| L2 | 参考实现/官方文档 | 技术主张支持 |
| L3 | 官方博客/Release notes | 背景/动机 |
| L4 | 第三方分析/社区讨论 | 社区观点参考 |

详见：[harness/rules/general/evidence-policy.md](./harness/rules/general/evidence-policy.md)

---

## 十、质量检查清单

在 merge 到 knowledge 之前，确保：

### 准确性

- [ ] 所有 claims 都有 sources 支撑
- [ ] 证据等级适当（L1/L2 用于技术主张）
- [ ] 无事实错误

### 一致性

- [ ] 术语使用一致
- [ ] 与其他知识不冲突
- [ ] 抽象层不混用

### 完整性

- [ ] 核心内容完整
- [ ] 边界条件说明
- [ ] 待决问题列出

### 可追溯性

- [ ] claims → sources 映射清晰
- [ ] atoms → claims 引用明确
- [ ] change → knowledge 追踪完整

---

## 十一、快速命令参考

### OpenSpec 命令

```bash
openspec update                                          # 刷新指令层
openspec new change <name> --schema blockchain-research  # 创建 change
openspec instructions plan --change <name>               # 生成 plan.md
openspec instructions draft --change <name>              # 生成 draft.md
```

### 本地脚本

```bash
# 初始化研究
python scripts/general/init_research_item.py --topic <topic> --type <type>

# 构建索引
python scripts/general/build_index.py

# 检查可追溯性
python scripts/general/check_traceability.py --topic <topic>

# 渲染图表
./scripts/diagrams/render.sh <diagram.puml>

# 移动 change 到 knowledge
python scripts/publish/move_change_outputs.py --change <change-id> --topic <topic>
```

---

## 十二、遇到不确定情况时

1. **检查 workflows** - 大部分流程都有定义
2. **检查 rules** - 写作规范和质量要求
3. **检查 skills** - 可复用操作的详细说明
