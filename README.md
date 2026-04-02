# 基于 OpenSpec 的区块链技术调研工作台

这个仓库用于长期维护区块链技术调研资产，区别于一次性报告。研究流程沉淀为可复用的研究系统。

## 仓库定位

六类资产及其位置：

| 资产类型 | 目录 | 说明 |
|---------|------|------|
| 长期知识 | `knowledge/topics/` | atoms / claims / sources / diagrams |
| 域知识 | `knowledge/domains/` | 主题域知识组织 |
| 场景决策 | `knowledge/decisions/` | decision 及其依赖 |
| 变更包 | `openspec/changes/` | 进行中的研究 |
| 研究系统 specs | `openspec/config.yaml` + `openspec/templates/` | OpenSpec 配置和模板 |
| 规则和工作流 | `harness/` | rules / workflows / prompts / evals |
| 可复用技能 | `skills/` | 研究 / 图表 / 维护技能 |
| 脚本工具 | `scripts/` | 通用 / 研究 / 图表 / 发布脚本 |

## 核心能力

这个仓库同时具备以下能力：

1. **OpenSpec 变更管理** - 所有知识更新都走 change 流程
2. **Harness 规则系统** - 规则、工作流、评审、提示词
3. **原子化知识管理** - atoms / claims / sources / terms / diagrams / reviews
4. **Skills + Scripts** - 稳定的、可复用的操作能力
5. **质量优先** - 准确性、术语边界、来源可追溯、图质量

## 目录结构

```
.
├── AGENTS.md                 # 协作索引（必读）
├── README.md                 # 本文件
├── CLAUDE.md                 # Claude 特定指令
├── Makefile                  # 构建自动化
├── pyproject.toml            # Python 项目配置
├── package.json              # Node.js 配置（如需要）
│
├── harness/                  # 规则和工作流
│   ├── rules/                # 规则文件
│   │   ├── _index.yaml       # 规则索引
│   │   ├── general/          # 通用规则
│   │   ├── research/         # 研究规则
│   │   ├── diagrams/         # 图表规则
│   │   └── writing/          # 写作规则
│   ├── workflows/            # 工作流定义
│   ├── prompts/              # 提示词模板
│   ├── evals/                # 评估材料
│   └── adapters/             # 适配器配置
│
├── skills/                   # 可复用技能
│   ├── README.md
│   ├── research/             # 研究技能
│   ├── diagrams/             # 图表技能
│   └── maintenance/          # 维护技能
│
├── scripts/                  # 脚本工具
│   ├── README.md
│   ├── general/              # 通用脚本
│   ├── research/             # 研究脚本
│   ├── diagrams/             # 图表脚本
│   └── publish/              # 发布脚本
│
├── knowledge/                # 知识库
│   ├── README.md
│   ├── glossary/meta/        # 术语元数据
│   ├── domains/              # 域知识
│   ├── topics/               # 主题知识
│   ├── indexes/              # 索引文件
│   └── templates/            # 知识模板
│
├── openspec/                 # OpenSpec 配置
│   ├── README.md
│   ├── config.yaml           # OpenSpec 配置
│   ├── templates/            # Change 模板
│   ├── changes/              # 进行中的 changes
│   └── archive/              # 已归档 changes
│
├── shared/                   # 共享资源
│   ├── README.md
│   ├── skills/
│   └── prompts/
│
└── tests/                    # 测试
    ├── fixtures/
    ├── unit/
    └── snapshots/
```

## 研究主链

区别于默认 OpenSpec 的 `proposal/spec/design/tasks`，本仓库使用 research-driven 主链：

```
request.md -> plan.md -> draft.md -> promote -> knowledge/
```

| 文件 | 作用 | 位置 |
|------|------|------|
| `request.md` | 定义问题、范围、非目标 | `openspec/changes/<change-id>/` |
| `plan.md` | 研究计划 + 来源规划 | `openspec/changes/<change-id>/` |
| `draft.md` | 术语 + 机制分析 + 有限结论 | `openspec/changes/<change-id>/` |
| `promote` | 提炼到 `knowledge/` | `knowledge/topics/...` |

## 对象模型

技术分析主链：`primitive -> [synthesis] -> domain`

- `primitive`：单个协议、EIP、机制
- `synthesis`：多个对象的关系分析（可选）
- `domain`：主题域知识组织层
- `decision`：场景决策（独立层）

约束：`synthesis` 非强制；`domain` 不是 `primitive` 的父目录；一个 primitive 可被多个 domain 复用。

## 知识更新流程

**重要**：所有知识更新都必须走 OpenSpec change 流程。

```
1. 创建 change
   openspec new change <name> --schema blockchain-research

2. 编写 request.md
   定义问题、范围、非目标

3. 生成 plan.md
   研究计划 + 来源规划

4. 收集来源
   获取 L1/L2/L3/L4 来源，提取 excerpts

5. 提取 claims
   从来源提取 facts/inferences/estimates

6. 编写 atoms
   definition / mechanism / evolution

7. 创建 diagrams（如需要）
   model -> PlantUML -> render -> validate -> review

8. 评审
   technical review + readability review

9. Merge
   通过评审后 merge 到 knowledge/
```

## 常用命令

### OpenSpec 原生命令

```bash
openspec update                                          # 刷新指令层
openspec new change <name> --schema blockchain-research  # 创建 change
openspec instructions plan --change <name>               # 生成 plan.md
openspec instructions draft --change <name>              # 生成 draft.md
```

### 本地脚本

```bash
# 初始化研究项目
python scripts/general/init_research_item.py --topic <topic> --type <primitive|synthesis|domain|decision>

# 构建 topic 索引
python scripts/general/build_index.py

# 检查 frontmatter
python scripts/general/check_frontmatter.py [file|directory]

# 检查可追溯性
python scripts/general/check_traceability.py --topic <topic>

# 标准化 claims
python scripts/research/normalize_claims.py --topic <topic>

# 构建比较矩阵
python scripts/research/build_comparison_matrix.py --topics topic1,topic2,topic3 --output matrix.yaml

# 验证来源
python scripts/research/validate_sources.py --topic <topic>

# 查找术语漂移
python scripts/research/find_term_drift.py --term <term>

# 渲染 PlantUML
./scripts/diagrams/render.sh <diagram.puml>

# 验证 diagram model
python scripts/diagrams/validate_diagram_model.py <model.yaml>

# 检查 diagram 引用
python scripts/diagrams/check_diagram_references.py <diagram-id> --topic <topic>

# 移动 change 到 knowledge
python scripts/publish/move_change_outputs.py --change <change-id> --topic <topic> --domain <domain>

# 生成 topic 索引
python scripts/publish/generate_topic_index.py --output knowledge/indexes/topic-index.md
```

## 使用流程示例

### 示例 1: 新 Primitive 研究

```bash
# 1. 创建 change
openspec new change primitive-eip-4337-deep-dive-pass-1 --schema blockchain-research

# 2. 编写 request.md（或使用 /spec-request 辅助）
# 编辑 openspec/changes/primitive-eip-4337-deep-dive-pass-1/request.md

# 3. 生成 plan.md
openspec instructions plan --change primitive-eip-4337-deep-dive-pass-1

# 4. 收集来源、提取 claims、编写 atoms
# 按照 harness/workflows/ 中的流程执行

# 5. 评审后 merge 到 knowledge/
python scripts/publish/move_change_outputs.py --change primitive-eip-4337-deep-dive-pass-1 --topic eip-4337 --domain account-abstraction
```

### 示例 2: 更新现有主题

```bash
# 1. 创建 update change
openspec new change update-eip-4337-spec-v07-pass-1 --schema blockchain-research

# 2. 在 request.md 说明更新原因和范围

# 3. 对比新旧内容，执行更新

# 4. 更新 changelog.md

# 5. 评审后 merge
```

### 示例 3: 创建图表

```bash
# 1. 创建 diagram model
# 编辑 diagrams/models/<diagram-id>-model.yaml

# 2. 编写 PlantUML source
# 编辑 diagrams/source/<diagram-id>.puml

# 3. 渲染
./scripts/diagrams/render.sh diagrams/source/<diagram-id>.puml

# 4. 验证
python scripts/diagrams/validate_diagram_model.py diagrams/models/<diagram-id>-model.yaml

# 5. 评审
# 按照 harness/workflows/diagram-workflow.md 执行 review
```

## 证据等级

| 等级 | 来源 | 用途 |
|------|------|------|
| L1 | 官方规范 / EIP / 白皮书 | 核心技术主张 |
| L2 | 参考实现 / 官方文档 | 技术主张支持 |
| L3 | 官方博客 / Release notes | 背景/动机 |
| L4 | 第三方分析 / 社区讨论 | 社区观点参考 |

详见：[harness/rules/general/evidence-policy.md](./harness/rules/general/evidence-policy.md)

## 先看哪里

- **快速开始**：[AGENTS.md](./AGENTS.md) - 协作索引和导航
- **研究系统规范**：[harness/rules/](./harness/rules/) - 规则和约束
- **工作流程**：[harness/workflows/](./harness/workflows/) - 操作流程
- **技能**：[skills/](./skills/) - 可复用操作
- **脚本**：[scripts/](./scripts/) - 自动化工具
- **模板**：[knowledge/templates/](./knowledge/templates/) - 知识模板

## 协作

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)（待更新）。

## 许可证

[待添加]
