# Harness Directory

`harness/` 目录包含研究系统的规则索引和工作流定义。

## 结构

```
harness/
├── rules/                # 规则文件
│   ├── _index.yaml       # 规则域索引
│   ├── general/          # 通用规则
│   ├── research/         # 研究规则
│   ├── diagrams/         # 图表规则
│   └── writing/          # 写作规则
├── workflows/            # 工作流定义
└── README.md             # 本文件
```

## 与 OpenSpec 的关系

`harness/` 是**路由层**，不是系统约束的定义位置。

| 层级 | 文件 | 职责 |
|------|------|------|
| **系统约束层** | `openspec/config.yaml` | OpenSpec 工作流配置（source of truth） |
| **系统约束层** | `openspec/schemas/.../schema.yaml` | 研究对象模型（source of truth） |
| **系统约束层** | `openspec/specs/` | 研究系统规范正文 |
| **路由层** | `harness/` | 导航、规则索引、轻量 workflow 说明 |

## 规则索引

完整规则列表见 [rules/_index.yaml](./rules/_index.yaml)。

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
| `definition-rules.md` | 定义写作规范 |
| `mechanism-rules.md` | 机制分析规范 |
| `evolution-rules.md` | 演进分析规范 |
| `comparison-rules.md` | 比较分析规范 |
| `source-validation-rules.md` | 来源验证规范 |
| `uncertainty-rules.md` | 不确定性处理规范 |

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

## 工作流

| 工作流 | 用途 | 产物位置 |
|--------|------|----------|
| `intake-workflow.md` | 研究请求接入 | `openspec/changes/` |
| `source-workflow.md` | 来源处理 | `openspec/changes/<id>/sources/` |
| `principle-atom-workflow.md` | 知识笔记写作 | `openspec/changes/<id>/notes/` |
| `comparison-workflow.md` | 比较分析 | `openspec/changes/<id>/comparisons/` |
| `diagram-workflow.md` | 图表创建 | `openspec/changes/<id>/diagrams/` |
| `review-workflow.md` | 知识评审 | `openspec/changes/<id>/review/` |
| `merge-workflow.md` | 应用到 knowledge | `knowledge/analysis/` 或 `knowledge/decisions/` |
| `update-existing-knowledge.md` | 更新现有知识 | `openspec/changes/` → `knowledge/` |

## 使用方法

### 加载规则

规则按需加载，不默认全部加载。

从 `rules/_index.yaml` 中查找对应 domain 的规则列表。

### 执行工作流

按照工作流文件中的 step-by-step procedure 执行。

工作流中的产物默认落在 `openspec/changes/<change-id>/`，通过评审后通过 `apply` 提升到 `knowledge/`。

## 更新规则

更新规则需要：

1. 创建 change 记录变更
2. 评审变更
3. 更新 `_index.yaml`（如需要）
