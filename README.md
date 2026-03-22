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

所以这里不沿用 `proposal / spec / design / tasks`，而是使用 research-driven 的最小主链：

`request.md -> plan.md -> draft.md -> promote`

其中：

- `request.md`：你定义问题，不要求提前懂完整机制
- `plan.md`：AI 先帮你合并“研究计划 + 来源规划”，你 review
- `draft.md`：AI 再帮你合并“术语 + 分析 + 有限结论”，你 review
- `promote`：把稳定内容提炼进 `knowledge/`

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
│   │   ├── domains/                                 # 【最终产物】主题域地图
│   │   ├── primitives/                              # 【最终产物】单对象参考稿
│   │   └── synthesis/                               # 【最终产物】关系与演进参考稿
│   └── decisions/                                   # 【最终产物】长期场景决策
│       ├── README.md
│       └── agentic-payment/                         # 【最终产物】场景族目录
├── openspec/                                        # 【流程配置】OpenSpec 工作流层
│   ├── changes/                                     # 【临时改动】当前研究工作区
│   ├── schemas/                                     # 【流程配置】research-driven schema
│   └── specs/                                       # 【长期规约】研究系统 specs
├── scripts/                                         # 【命令入口】本地脚本
├── skills/                                          # 【固定结构】可映射到客户端命令的 skills
│   ├── build-draft/                                 # 【AI 入口】生成 draft.md
│   ├── build-plan/                                  # 【AI 入口】生成 plan.md
│   └── promote-canonical/                           # 【AI 入口】提炼长期产物
└── support/                                         # 【支撑资产】手册、模板、提示词
    ├── docs/                                        # 【人工参考】操作说明与清单
    ├── prompts/                                     # 【AI 入口】提示词
    └── templates/                                   # 【人工参考】模板与表格骨架
```

## `knowledge/` 里保留什么

| 文件 | 放在 `openspec/changes/` | 放在 `knowledge/analysis/` | 放在 `knowledge/decisions/` | 说明 |
| --- | --- | --- | --- | --- |
| `request.md` | 是 | 否 | 否 | 问题定义文件，属于过程 |
| `plan.md` | 是 | 否 | 否 | 合并后的计划与来源规划文件，属于过程 |
| `draft.md` | 是 | 否 | 否 | 合并后的术语、分析、有限结论草稿，属于过程 |
| `dependencies.md` | 视需要保留 | 视需要保留 | 是 | 统一的依赖声明文件 |
| `decision-criteria.md` | 视需要保留 | 否 | 否 | decision 的过程性标准原件 |
| `evidence-matrix.md` | 视需要保留 | 否 | 否 | 过程性证据约束矩阵 |
| `reference.md` | 否 | 是 | 是 | 长期正式参考稿 |
| `criteria.md` | 否 | 否 | 是 | 提炼后的长期决策标准 |
| `verdict.md` | 否 | 否 | 是 | decision 的长期条件性结论 |

补充约束：

- glossary 层是核心内容，但默认并入 `draft.md` 与 `reference.md` 的“关键术语”区
- `primitive / synthesis / domain` 的稳定结论默认并入 `reference.md`
- `decision` 的条件性结论单独长期保留在 `verdict.md`

## 命令与 Skills

假设你已经安装好 `openspec`。这个仓库的命令层分三层：

1. OpenSpec 原生命令
2. 客户端 qoder slash command
3. 仓库本地 wrapper

推荐顺序也是这个顺序。

### OpenSpec 主入口

- `openspec update`
- `openspec new change <change-name> --schema blockchain-research`
- `openspec status --change <change-name>`
- `openspec instructions request --change <change-name>`
- `openspec instructions plan --change <change-name>`
- `openspec instructions draft --change <change-name>`
- `openspec instructions dependencies --change <change-name>`
- `openspec instructions decision-criteria --change <change-name>`
- `openspec instructions evidence-matrix --change <change-name>`
- `openspec schema validate blockchain-research`

### qoder command 应该怎么理解

qoder command 不是 `openspec update` 自动生成的仓库能力。更准确地说：

- `openspec update` 负责刷新 OpenSpec 指令层
- qoder 的 slash command 是客户端侧别名
- 仓库侧能提供的是稳定 skill 和清晰的输入输出约定

这个仓库已经提供了项目级 Qoder commands：

- `/build-plan`
- `/build-draft`
- `/promote-reference`

它们对应的配置文件在：

- `.qoder/commands/build-plan.md`
- `.qoder/commands/build-draft.md`
- `.qoder/commands/promote-reference.md`

职责分别是：

- `/build-plan`
  输入：`request.md`
  输出：`plan.md`
- `/build-draft`
  输入：`request.md`、`plan.md`、必要时 `dependencies.md` / `evidence-matrix.md`
  输出：`draft.md`
- `/promote-reference`
  输入：稳定版 `draft.md`
  输出：`knowledge/.../reference.md`，以及 decision 的 `verdict.md`

### 为什么不把 `/opsx:propose` 当主入口

`/opsx:propose` 仍然属于 OpenSpec 默认 spec-driven 语义，默认更接近：

- `proposal.md`
- `specs/`
- `design.md`
- `tasks.md`

这和本仓库的研究主链不一致。所以这里不要把 `/opsx:propose` 当主入口。

### 仓库 wrapper

仓库里仍保留一层便捷入口：

- `./scripts/new_change.sh <domain|primitive|synthesis|decision> <change-name>`
- `make change-domain NAME=<change-name>`
- `make change-primitive NAME=<change-name>`
- `make change-synthesis NAME=<change-name>`
- `make change-decision NAME=<change-name>`
- `make install-skills`
- `make scan-language`
- `make validate-schema`

## 使用步骤

| 步骤 | 执行 | 输入 / 依赖 | 人工检查 | 产物 | 参考 |
| --- | --- | --- | --- | --- | --- |
| 0. 刷新指令层 | `openspec update` | `openspec/config.yaml`、`openspec/schemas/...` | schema 名是否为 `blockchain-research` | 最新指令层 | `support/docs/command-model.md` |
| 1. 开 change | `openspec new change <change-name> --schema blockchain-research` | change 名、对象层级 | 名称是否稳定，层级是否判断正确 | `openspec/changes/<change-name>/` | `support/docs/workflow.md` |
| 2. 写 request | 直接编辑 `request.md` | 你的研究意图 | 是否只定义问题、范围、非目标；是否避免提前回答机制细节 | `request.md` | `support/docs/eip-4337-deep-dive-runbook.md` |
| 3. 生成 plan | `openspec instructions plan --change <change-name>` 或 `/build-plan <change-path>` | `request.md` | 是否把预算、来源规划、后续确认问题写全 | `plan.md` | `skills/build-plan/` |
| 4. 补可选文件 | `openspec instructions dependencies ...`、`decision-criteria ...`、`evidence-matrix ...` | `plan.md` | 是否真的需要这些文件，不要滥开 | 可选过程文件 | `support/docs/checklists/` |
| 5. 生成 draft | `openspec instructions draft --change <change-name>` 或 `/build-draft <change-path>` | `request.md`、`plan.md`、可选依赖文件 | 是否先机制后价值；术语区是否是列表；是否区分原生 / 生态 / 第三方 | `draft.md` | `skills/build-draft/` |
| 6. 提炼长期结果 | `/promote-reference <change-path>` 或按 `skills/promote-canonical/` 手工执行 | 稳定版 `draft.md` | 是否把过程痕迹误带入长期目录 | `reference.md`，decision 额外保留 `verdict.md` | `skills/promote-canonical/` |
| 7. 沉淀长期规则 | 新开 change，再更新 `openspec/specs/` | 多轮 case 的共同规律 | 是否真的是跨 case 规则，不是单次经验 | `openspec/specs/.../spec.md` | `openspec/specs/README.md` |

## 如何新增一个 `primitive / synthesis / decision`

### 新增 `primitive`

1. `openspec new change <change-name> --schema blockchain-research`
2. 手工完成 `request.md`
3. 用 `plan.md` 和 `draft.md` 跑完一轮 review
4. 稳定后提炼到 `knowledge/analysis/primitives/<slug>/reference.md`

### 新增 `synthesis`

1. `openspec new change <change-name> --schema blockchain-research`
2. 手工完成 `request.md`
3. 用 `plan.md` 跑第一轮 review，并补 `dependencies.md`
4. 必要时补 `evidence-matrix.md`
5. 用 `draft.md` 跑第二轮 review
6. 稳定后提炼到 `knowledge/analysis/synthesis/<slug>/reference.md` 与 `dependencies.md`

### 新增 `decision`

1. `openspec new change <change-name> --schema blockchain-research`
2. 手工完成 `request.md`
3. 用 `plan.md` 跑第一轮 review，并补 `dependencies.md`、`decision-criteria.md`
4. 必要时补 `evidence-matrix.md`
5. 用 `draft.md` 跑第二轮 review
6. 稳定后提炼到 `knowledge/decisions/<scenario>/<slug>/reference.md`、`criteria.md`、`dependencies.md`、`verdict.md`

## 一个真实的使用示例

以 `EIP-4337` 为例：

1. 在 `openspec/changes/primitive-eip-4337-deep-dive-pass-1/` 中先手工写 `request.md`
2. 再用 `/build-plan openspec/changes/primitive-eip-4337-deep-dive-pass-1/` 或 `openspec instructions plan --change primitive-eip-4337-deep-dive-pass-1` 生成 `plan.md`
3. 你 review `plan.md`，重点看后续确认问题、来源分层和证据缺口
4. 然后用 `/build-draft openspec/changes/primitive-eip-4337-deep-dive-pass-1/` 或 `openspec instructions draft --change primitive-eip-4337-deep-dive-pass-1` 生成 `draft.md`
5. 你 review `draft.md`，重点看术语区、机制、设计原因、边界和有限结论
6. 最后把稳定内容提炼到 `knowledge/analysis/primitives/eip-4337/reference.md`

## 先看哪里

- `EIP-4337` 实验手册：`support/docs/eip-4337-deep-dive-runbook.md`
- workflow 总览：`support/docs/workflow.md`
- 命令模型：`support/docs/command-model.md`
- 研究对象模型：`support/docs/research-model.md`
- 证据政策：`support/docs/evidence-policy.md`
