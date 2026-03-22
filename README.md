# 基于 OpenSpec 的区块链技术调研工作台

这个仓库不是业务应用仓库，不是博客仓库，也不是一次性报告仓库。它的目标是把重复出现的区块链技术调研流程，沉淀成一套可长期维护、可复用、可演进的研究系统。

## 仓库定位

这个仓库长期区分六类资产：

1. 长期事实分析资产
2. 长期场景决策资产
3. 当前研究改动包
4. 长期研究系统 specs
5. 工作流定义资产
6. 支撑方法与 AI 协作资产

对应位置：

- `knowledge/analysis/`：长期事实分析资产
- `knowledge/decisions/`：长期场景决策资产
- `openspec/changes/`：当前研究改动包
- `openspec/specs/`：长期研究系统 specs
- `openspec/config.yaml` + `openspec/schemas/...`：工作流定义层
- `support/` + `skills/`：支撑方法与 AI 协作层

## 为什么不是默认 spec-driven 仓库

默认 OpenSpec 更适合“我要实现一个功能”的软件变更流程。本仓库解决的是：

- 如何长期积累事实分析资产
- 如何把事实分析资产应用到具体场景判断
- 如何把本轮调研中的纠偏过程，与长期保留的知识结果分开
- 如何把跨 case 的研究准则沉淀成长期 specs

所以这里不能直接沿用 `proposal / spec / design / tasks` 语义，而是使用 research-driven 的 artifact 链。

## 对象模型

技术分析主链：

`primitive -> [optional synthesis] -> domain`

- `primitive`：单个协议、单个 EIP、单个机制、单个链能力点
- `synthesis`：多个对象之间的关系、演进、分类、框架分析
- `domain`：长期主题域与知识组织层

独立的场景应用层：

- `decision`

关键约束：

- `synthesis` 是可选层，不是强制层
- `domain` 不是 `primitive` 的父目录，只是长期知识组织层
- 一个 `primitive` 或 `synthesis` 可以被多个 `domain` 复用
- `decision` 消费前三类资产，但不属于纯技术分析主链

## 仓库里到底有几类东西

| 资产类别 | 位置 | 作用 |
| --- | --- | --- |
| 工作流定义资产 | `openspec/config.yaml`、`openspec/schemas/...` | 定义 schema、artifact 图、模板与规则 |
| 当前改动资产 | `openspec/changes/<change-name>/` | 承载本轮研究过程 |
| 研究系统 specs | `openspec/specs/` | 沉淀跨多次调研复用的长期规则 |
| 长期技术分析资产 | `knowledge/analysis/...` | 长期事实分析知识底座 |
| 长期场景决策资产 | `knowledge/decisions/...` | 把知识底座应用到具体场景 |
| 支撑方法资产 | `support/`、`skills/` | 方法论、模板、提示词与 AI 协作入口 |

## `support/docs/` 和 `openspec/specs/` 怎么区分

- `openspec/specs/`：规范版，写“必须怎么做”
- `support/docs/`：说明版，写“为什么这么做、怎么落地、怎么自检”

## 目录结构

```text
.
├── AGENTS.md
├── CONTRIBUTING.md
├── Makefile
├── README.md
├── knowledge/                                       # 【最终产物】长期正式产出
│   ├── README.md
│   ├── analysis/                                    # 【最终产物】长期事实分析
│   │   ├── README.md
│   │   ├── domains/                                 # 【最终产物】主题域知识组织
│   │   ├── primitives/                              # 【最终产物】单对象机制分析
│   │   └── synthesis/                               # 【最终产物】关系与演进分析
│   └── decisions/                                   # 【最终产物】长期场景决策
│       ├── README.md
│       └── agentic-payment/                         # 【最终产物】场景族目录
├── openspec/                                        # 【流程配置】OpenSpec 工作流层
│   ├── changes/                                     # 【临时改动】当前研究工作区
│   ├── schemas/                                     # 【流程配置】研究驱动 schema
│   └── specs/                                       # 【长期规约】研究系统 specs
├── scripts/                                         # 【命令入口】本地脚本
├── skills/                                          # 【固定结构】仓库内置 skills
│   ├── analysis-writing/
│   ├── decision-verdict/
│   ├── promote-canonical/
│   ├── request-brief/
│   └── sources-evidence/
└── support/                                         # 【支撑资产】说明、模板、提示词
    ├── docs/                                        # 【人工参考】操作说明与清单
    ├── prompts/                                     # 【AI 入口】提示词
    └── templates/                                   # 【人工参考】模板与表格骨架
```

## `knowledge/` 里到底保留什么

| 文件 | 放在 `openspec/changes/` | 放在 `knowledge/analysis/` | 放在 `knowledge/decisions/` | 说明 |
| --- | --- | --- | --- | --- |
| `request.md` | 是 | 否 | 否 | 问题定义文件，属于过程 |
| `brief.md` | 是 | 否 | 否 | 计划与预算文件，属于过程 |
| `sources.md` | 是 | 否 | 否 | 证据规划与补证日志，默认属于过程 |
| `evidence-matrix.md` | 是 | 否 | 否 | 证据约束矩阵，默认属于过程 |
| `analysis.md` | 是 | 否 | 否 | 研究过程中的分析稿 |
| `reference.md` | 否 | 是 | 是 | 长期正式参考稿 |
| `glossary.md` | 是 | 是 | 是 | 长期术语卡 |
| `dependencies.md` | 是 | 视需要保留 | 是 | 统一的依赖声明文件，兼容 budget / strength / extraction |
| `decision-criteria.md` | 是 | 否 | 否 | change 阶段的决策标准原件 |
| `criteria.md` | 否 | 否 | 是 | 提炼后的长期决策标准 |
| `verdict.md` | 是 | 默认否 | 是 | `primitive / synthesis / domain` 默认并入 `reference.md`；`decision` 长期保留 |
| case 级 `README.md` | 否 | 否 | 否 | 目录说明应上收，不作为知识正文 |

## 执行入口

### 推荐主链

假设你已经安装好 `openspec`，推荐顺序是：

1. `openspec update`
2. `openspec new change <change-name> --schema blockchain-research`
3. `openspec status --change <change-name>`
4. `openspec instructions request --change <change-name>`
5. `openspec instructions brief --change <change-name>`
6. `openspec instructions sources --change <change-name>`
7. `openspec instructions analysis --change <change-name>`
8. `openspec instructions verdict --change <change-name>`
9. `openspec validate --changes`
10. `openspec schema validate blockchain-research`

职责分别是：

- `openspec update`：刷新客户端 AI 指令文件，让 slash command 和仓库配置保持一致
- `openspec new change ...`：创建 `openspec/changes/<change-name>/`
- `openspec status --change ...`：按 schema 依赖图显示已完成、待完成、被阻塞的 artifact
- `openspec instructions <artifact> --change ...`：读取仓库 context、schema、模板和已存在 artifact，输出当前该写什么的指令
- `openspec validate --changes`：校验当前 change

### `/opsx:propose` 到底怎么起作用

`/opsx:propose` 能用，不代表它适合这个仓库。

它的工作方式是：

1. 先执行 `openspec update`
2. OpenSpec 把 AI 指令写进客户端支持的指令文件
3. 客户端再把 `/opsx:propose "your idea"` 解释成 OpenSpec 默认 `core` profile 的 spec-driven 流程

按 OpenSpec 官方 README，这条命令默认生成的是：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/specs/`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`

这正是它不适合本仓库的原因。我们的 schema 要生成的是：

- `request.md`
- `brief.md`
- `sources.md`
- `glossary.md`
- `analysis.md`
- `verdict.md`

以及按需出现的：

- `dependencies.md`
- `decision-criteria.md`
- `evidence-matrix.md`

所以这里不要把 `/opsx:propose` 当主入口。更稳的做法是：

- 用 `openspec new change ... --schema blockchain-research` 开 change
- 用 `openspec instructions ...` 驱动每个 artifact

### slash command 在这个仓库里的正确理解

如果你的客户端支持自定义 slash command，更合理的映射是：

- `/opsx:request-brief` -> `skills/request-brief/`
- `/opsx:sources-evidence` -> `skills/sources-evidence/`
- `/opsx:analysis-writing` -> `skills/analysis-writing/`
- `/opsx:decision-verdict` -> `skills/decision-verdict/`
- `/opsx:promote-canonical` -> `skills/promote-canonical/`

这层属于客户端映射，不是仓库 schema 自动生成的能力。

### 仓库包装入口

仓库里仍保留一层本地 wrapper，但它只是便捷层，不是主语义：

- `./scripts/new_change.sh <domain|primitive|synthesis|decision> <change-name>`
- `make change-domain NAME=<change-name>`
- `make change-primitive NAME=<change-name>`
- `make change-synthesis NAME=<change-name>`
- `make change-decision NAME=<change-name>`
- `make install-skills`
- `make scan-language`
- `make validate-schema`

## 使用步骤

| 步骤 | 执行 | 人工检查 | 输入 / 依赖 | 产物 |
| --- | --- | --- | --- | --- |
| 0. 刷新指令层 | `openspec update` | 检查客户端已加载最新仓库指令 | `openspec/config.yaml`、`openspec/schemas/...`、客户端集成 | 最新 AI 指令与 slash command 入口 |
| 1. 安装技能 | `make install-skills` | 确认 `${CODEX_HOME}/skills/` 下已出现仓库 skills | 仓库内 `skills/` | 可被 Codex 直接调用的本地 skills |
| 2. 开研究改动包 | 首选 `openspec new change <change-name> --schema blockchain-research`；若要一步补齐骨架，用 `./scripts/new_change.sh primitive <change-name>` | 检查 change 名是否稳定、对象层是否判断正确 | 研究对象名称、对象层级、研究路径 | `openspec/changes/<change-name>/` |
| 3. 看依赖图 | `openspec status --change <change-name>` | 检查哪些 artifact 已完成、哪些被阻塞 | 已创建的 change、schema 依赖图 | 当前 change 的完成状态 |
| 4. 收紧问题 | `openspec instructions request --change <change-name>` 与 `openspec instructions brief --change <change-name>`，再配合 `skills/request-brief/` | 人工收紧范围、非目标、budget、依赖对象 | change、schema、对象背景、已有问题清单 | `request.md`、`brief.md` |
| 5. 规划证据 | `openspec instructions sources --change <change-name>`，再配合 `skills/sources-evidence/` | 人工核对来源分级、对象边界、evidence gap | `brief.md`、初始资料线索、已有下层资产 | `sources.md`，必要时补 `dependencies.md`、`evidence-matrix.md`、`decision-criteria.md` |
| 6. 写分析 | `openspec instructions analysis --change <change-name>`，再配合 `skills/analysis-writing/` | 人工检查是否先机制后价值，是否混写原生 / 生态 / 第三方能力 | `sources.md`、`glossary.md`、下层依赖 | `analysis.md` |
| 7. 写结论 | `openspec instructions verdict --change <change-name>`，再配合 `skills/decision-verdict/` 或 `support/prompts/build-verdict.md` | 人工检查结论是否有前提、是否保留不确定性 | `analysis.md`、`evidence-matrix.md`、`dependencies.md` | `verdict.md` |
| 8. 提炼长期资产 | 使用 `skills/promote-canonical/`，把稳定结果回写 `knowledge/analysis/` 或 `knowledge/decisions/` | 人工检查是否把过程文件误带入长期目录 | 已完成的研究改动包 | `knowledge/analysis/...` 或 `knowledge/decisions/...` 的长期结果 |
| 9. 沉淀长期规则 | 新开一个 `change`，再更新 `openspec/specs/` | 人工判断这是不是跨 case 的长期规则，而不是单 case 经验 | 多轮研究中反复出现的通用约束 | `openspec/specs/.../spec.md` 与相关 `support/docs/` / config 同步更新 |

## 对应关系：在我们的场景里，什么像 `changes`，什么像 `specs`

| spec-driven SDD | 本仓库中的对应物 | 说明 |
| --- | --- | --- |
| `changes/` | `openspec/changes/` | 直接对应当前改动包 |
| `specs/` | `openspec/specs/` + `knowledge/analysis/` | 前者是研究系统 specs，后者是长期技术分析资产 |
| `code/` | 无严格 1:1 对应；最接近的是 `knowledge/decisions/` | 决策资产是在使用知识，但不是代码 |
| `config / schema / workflow` | `openspec/config.yaml` + `openspec/schemas/...` | 直接对应工作流定义层 |

## 为什么过程文件和长期结果要分开

这是仓库级硬约束：

- `request.md`、`brief.md`、`sources.md`、`evidence-matrix.md` 属于 change packet
- `reference.md`、`glossary.md`、`dependencies.md`、`criteria.md`、`verdict.md` 才可能成为长期结果
- `primitive / synthesis / domain` 的稳定结论默认并回 `reference.md`
- `decision` 的 `verdict.md` 可以长期保留

## 如何新增一个 `primitive / synthesis / decision`

### 新增 `primitive`

1. `openspec new change <change-name> --schema blockchain-research`
2. 在 `openspec/changes/<change-name>/` 中完成 `request.md`、`brief.md`、`sources.md`、`glossary.md`、`analysis.md`、`verdict.md`
3. 本轮稳定后，将长期结果提炼进 `knowledge/analysis/primitives/<slug>/`，默认只保留 `reference.md` 与 `glossary.md`

### 新增 `synthesis`

1. `openspec new change <change-name> --schema blockchain-research`
2. 除核心六件套外，再补 `dependencies.md`、`evidence-matrix.md`
3. 本轮稳定后，将长期结果提炼进 `knowledge/analysis/synthesis/<slug>/`，默认保留 `reference.md`、`glossary.md`、`dependencies.md`

### 新增 `decision`

1. `openspec new change <change-name> --schema blockchain-research`
2. 除核心六件套外，再补 `dependencies.md`、`decision-criteria.md`、`evidence-matrix.md`
3. 本轮稳定后，将长期结果提炼进 `knowledge/decisions/<scenario>/<slug>/`，默认保留 `reference.md`、`criteria.md`、`dependencies.md`、`glossary.md`、`verdict.md`

## 一个真实的使用示例

围绕 `account-abstraction`：

1. 在 [knowledge/analysis/primitives/eip-4337/reference.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/knowledge/analysis/primitives/eip-4337/reference.md) 长期维护 4337 的事实参考稿。
2. 当“AA 相关对象之间的关系”足够复杂时，再在 [knowledge/analysis/synthesis/aa-eip-evolution/reference.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/knowledge/analysis/synthesis/aa-eip-evolution/reference.md) 单独维护一个 synthesis 参考稿。
3. 在 [knowledge/analysis/domains/account-abstraction/reference.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/knowledge/analysis/domains/account-abstraction/reference.md) 长期维护主题地图。
4. 在 [knowledge/decisions/agentic-payment/chain-comparison/reference.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/knowledge/decisions/agentic-payment/chain-comparison/reference.md) 结合场景维护决策参考稿，并在 [knowledge/decisions/agentic-payment/chain-comparison/verdict.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/knowledge/decisions/agentic-payment/chain-comparison/verdict.md) 给出条件性结论。

## 先看哪里

- 对象模型：[support/docs/research-model.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/support/docs/research-model.md)
- 工作流：[support/docs/workflow.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/support/docs/workflow.md)
- 命令模型：[support/docs/command-model.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/support/docs/command-model.md)
- 证据政策：[support/docs/evidence-policy.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/support/docs/evidence-policy.md)
- 语言风格：[support/docs/language-style.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/support/docs/language-style.md)
- 仓库级 AI 约束：[AGENTS.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/AGENTS.md)
