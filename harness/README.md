# Harness Directory

`harness/` 目录包含研究系统的规则和工作流定义。

## 结构

```
harness/
├── rules/                # 规则文件
│   ├── _index.yaml       # 规则索引（轻量级）
│   ├── general/          # 通用规则
│   ├── research/         # 研究规则
│   ├── diagrams/         # 图表规则
│   └── writing/          # 写作规则
├── workflows/            # 工作流定义
└── README.md             # 本文件
```

## 规则索引

完整规则列表见 [rules/_index.yaml](./rules/_index.yaml)。

### General Rules (`harness/rules/general/`)

- `repo-governance.md` - 仓库治理
- `evidence-policy.md` - 证据政策
- `terminology-policy.md` - 术语治理
- `traceability-policy.md` - 可追溯性
- `update-policy.md` - 更新政策

### Research Rules (`harness/rules/research/`)

- `definition-rules.md` - 定义写作
- `mechanism-rules.md` - 机制分析
- `evolution-rules.md` - 演进分析
- `comparison-rules.md` - 比较分析
- `source-validation-rules.md` - 来源验证
- `uncertainty-rules.md` - 不确定性处理

### Diagram Rules (`harness/rules/diagrams/`)

- `diagram-selection-matrix.md` - 图选择矩阵
- `abstraction-boundaries.md` - 抽象边界
- `relationship-rules.md` - 关系语义
- `annotation-rules.md` - 注释规范
- `simplification-policy.md` - 简化政策
- `diagram-review-checklist.md` - 评审清单

### Writing Rules (`harness/rules/writing/`)

- `structure-rules.md` - 结构规范
- `table-rules.md` - 表格规范
- `summary-rules.md` - 摘要规范

## 工作流

| 工作流 | 用途 |
|--------|------|
| `intake-workflow.md` | 研究请求接入 |
| `source-workflow.md` | 来源处理 |
| `principle-atom-workflow.md` | 笔记写作 |
| `comparison-workflow.md` | 比较分析 |
| `diagram-workflow.md` | 图表创建 |
| `review-workflow.md` | 知识评审 |
| `merge-workflow.md` | 应用到 knowledge |
| `update-existing-knowledge.md` | 更新现有知识 |

## 使用方法

### 加载规则

规则按需加载，不默认全部加载。

从 `rules/_index.yaml` 中查找对应 domain 的规则列表。

### 执行工作流

按照工作流文件中的 step-by-step procedure 执行。

## 与 OpenSpec 的关系

`harness/` 是路由层和规则索引层，真正的系统约束定义在：

- `openspec/config.yaml` - OpenSpec 工作流配置
- `openspec/schemas/blockchain-research/schema.yaml` - 研究对象模型
- `openspec/specs/` - 研究系统规范（规划中）

## 更新规则

更新规则需要：

1. 创建 change 记录变更
2. 评审变更
3. 更新 `_index.yaml`（如需要）
