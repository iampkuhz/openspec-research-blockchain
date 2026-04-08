# OpenSpec 与 Harness 职责边界

**版本**：1.1
**最后更新**：2026-04-05

---

## 重要阅读提示

**任务语义优先，路径辅助**：不要因为文件位于某个路径下就自动加载本文件，只有当任务语义明确涉及**规约、治理、分层、仓库架构调整**时才读取本文件。

### 必须读取本文件的场景

* 调整 OpenSpec / Harness 的职责边界
* 修改 schema / specs / templates / governance / repository architecture
* 修改用于**定义或评审规约分层**的 workflow / rules / skills
* 修改 `.claude/commands/` 或 `.claude/agents/` 中与仓库路由、角色合同、阶段编排相关的内容
* 修改 `AGENTS.md` 中与仓库路由、治理、分层相关的段落
* 评审上述类型的变更

### 不要默认读取本文件的场景

* 普通技术调研、知识条目更新
* 来源收集与验证、图表生成
* 一般性的 research workflow 微调
* 与仓库分层无关的 skills 优化

**说明**：触发条件看的是**任务语义**，不是文件路径本身。

---

## 仓库定位

本仓库是 **区块链技术调研 / knowledge production repo**，主产物是 **research knowledge artifacts**，不是代码实现。

---

## 一句话边界

* **OpenSpec 是正式规则层**：定义这套研究流程里什么算合法、有哪些正式产物、这些产物如何流转、哪些约束不能违反、什么条件下可以 apply、哪些内容可以沉淀为长期资产。
* **Harness 是执行手册层**：定义 AI 实际如何干活、如何检查、如何评审、如何修复；这些检查应优先基于 OpenSpec 派生，但 Harness 也可以补充执行层自身需要的操作检查。

---

## OpenSpec 负责什么

OpenSpec 负责定义**正式规则**，也就是即使没有任何 agent，这些规则仍然成立的那一层。

### OpenSpec 负责的内容

1. **正式产物及其关系**

    * 有哪些 artifact
    * 这些 artifact 的依赖链是什么
    * 哪些前置条件满足后才能进入下一阶段
    * 哪些条件满足后才允许 apply

2. **正式产物的标准结构**

    * 每个 artifact 的 canonical template
    * 每个 artifact 必须包含哪些内容
    * 哪些 section 是必需的，哪些是可选的

3. **正式语义约束**

    * 证据等级政策
    * 图表政策
    * 语言风格政策
    * 仓库资产模型
    * 研究对象模型
    * 分析质量标准

4. **正式准入与沉淀规则**

    * 什么算合法的 change
    * 什么条件下可以 apply
    * 长期资产放在哪里
    * 哪些约束不能被 execution layer 重新定义

### OpenSpec 的核心特点

* 它不是给 agent 的临时提示词集合，而是 **canonical source of truth**
* 它定义的是**规则本体**
* 它决定什么是“正式规则”、什么是“正式产物”、什么能进入长期资产

### OpenSpec 对应文件

| 职责               | 文件位置                                                  |
| ---------------- | ----------------------------------------------------- |
| 正式产物定义、依赖关系、阶段流转 | `openspec/schemas/blockchain-research/schema.yaml`    |
| 正式产物的标准模板        | `openspec/schemas/blockchain-research/templates/*.md` |
| 正式语义约束           | `openspec/specs/*/spec.md`                            |
| 项目级配置入口          | `openspec/config.yaml`                                |

### 必须放在 OpenSpec 的内容

* artifact 依赖链定义
* artifact template 结构
* 什么条件下允许 apply
* 长期资产落位规则
* 证据等级政策
* 图表政策
* 语言风格约束
* 仓库资产模型
* 研究对象模型
* 正式质量标准

---

## Harness 负责什么

Harness 负责定义**执行手册**，也就是 AI 如何把 OpenSpec 的正式规则落实成可执行操作。

### Harness 负责的内容

1. **AI 的操作流程**

    * 先读什么
    * 后做什么
    * 哪一步生成什么
    * 哪一步触发 review / repair / apply

2. **执行层检查**

    * 如何把 OpenSpec 的正式规则转成可执行检查
    * 哪一步对照 evidence / diagram / language / template 规则检查
    * review 不通过时如何回修

3. **执行层治理与配套机制**

    * source collection / validation 的操作步骤
    * traceability 的执行流程
    * changelog / update 的执行流程
    * 图表选择、简化、评审 checklist
    * 术语治理的操作流程

4. **执行入口与路由**

    * workflows
    * rules
    * skills
    * governance review 的条件触发机制

### Harness 的核心特点

* 它不是正式规则本体
* 它是**把正式规则变成 AI 可执行操作体系**
* 它可以定义执行层自己的检查，但**不能反过来重新定义正式规则**

### Harness 对应文件

| 职责      | 文件位置                                                        |
| ------- | ----------------------------------------------------------- |
| 研究执行手册  | `harness/workflows/*.md`                                    |
| 执行面治理   | `harness/rules/general/repo-governance.md`                  |
| 执行面追溯流程 | `harness/rules/general/traceability-policy.md`              |
| 执行面更新流程 | `harness/rules/general/update-policy.md`                    |
| 执行面术语治理 | `harness/rules/general/terminology-policy.md`               |
| 图表执行指南  | `harness/rules/diagrams/*.md`                               |
| 研究写作指南  | `harness/rules/research/*.md`, `harness/rules/writing/*.md` |

### 可以合理保留在 Harness 的内容

* 来源收集、评审、修复、apply 的操作配方
* 追溯文件格式模板（Source Pack / Excerpt / Change Packet）
* 术语治理流程（创建 / 复用 / 冲突解决）
* 更新流程（changelog 格式、版本号规范）
* 图表类型选择指南、简化策略、评审清单
* review / repair / validation 的执行清单

---

## 两层的关系

### OpenSpec 像什么

OpenSpec 像 **制度 / 标准 / 准入规则**：

* 要交什么
* 什么算合格
* 什么时候可以进入下一步
* 什么能沉淀为正式资产

### Harness 像什么

Harness 像 **执行手册 / 检查手册**：

* AI 怎么一步步把这些东西做出来
* 哪些检查怎么落地
* 发现问题以后怎么修

### 两者之间的正确关系

* OpenSpec 先定义正式规则
* Harness 再把这些规则变成可执行动作和检查
* Harness 可以补充执行层自己的操作检查
* 但 Harness 不能反过来重写 OpenSpec 的正式规则

---

## 核心约束

| 约束                     | 归属       | 说明                                                |
| ---------------------- | -------- | ------------------------------------------------- |
| 变更准入与长期资产沉淀规则          | OpenSpec | 定义什么算合法 change、何时可 apply、长期资产如何落位                 |
| 工件模板结构                 | OpenSpec | 定义 artifact 的必需结构                                 |
| 证据等级政策                 | OpenSpec | L1/L2/L3/L4 定义及使用规则                               |
| 图表政策                   | OpenSpec | 图表生成 / 验证 / 交付标准                                  |
| 语言风格                   | OpenSpec | 中文优先、英文术语保留                                       |
| 研究对象模型                 | OpenSpec | 定义研究对象分类与分析视角                                     |
| 仓库资产模型                 | OpenSpec | 定义长期资产目录与命名方式                                     |
| 研究执行流程                 | Harness  | intake → source → analysis → review → apply 的执行步骤 |
| 追溯操作指引                 | Harness  | claim → source 的执行流程与落盘方式                         |
| 术语治理流程                 | Harness  | 术语创建 / 复用 / 冲突解决                                  |
| 更新流程                   | Harness  | changelog 格式、版本号规范、更新动作                           |
| 执行层 review / repair 机制 | Harness  | 评审、修复、复检的操作手册                                     |

---

## 判断标准

### 必须放在 OpenSpec 的内容

满足任一项，优先归 OpenSpec：

* 这是正式规则本体
* 这是 artifact 的 canonical 结构
* 这是 apply / archive / asset placement 的准入条件
* 这是即使没有 agent 也仍然成立的规则

### 可以放在 Harness 的内容

满足任一项，可以归 Harness：

* 这是 AI 的执行步骤
* 这是基于 OpenSpec 派生出的执行检查
* 这是 review / repair / validation / routing 的操作机制
* 这是 execution layer 自身需要的格式、清单或配套流程

### Harness 不应做的事

* 不重新定义 artifact contract
* 不重新定义 canonical evidence / diagram / language policy
* 不绕过 OpenSpec 直接把 execution guidance 升格为正式规则
* 不把执行层 convenience rule 伪装成 canonical policy

---

## 何时需要读取本文件

### 必须读取

* 调整 OpenSpec / Harness 职责边界
* 修改 schema / specs / templates / governance / repository architecture
* 修改用于定义或评审规约分层的 workflow / rules / skills
* 修改 `.claude/commands/` 或 `.claude/agents/` 中与仓库路由、角色合同、阶段编排相关的内容
* 修改 `AGENTS.md` 中与仓库路由、治理、分层相关的段落
* 评审上述类型的变更

### 不要默认读取

* 普通技术调研任务
* 概念定义 / 比较分析写作
* 证据收集 / 图表生成
* 一般性的 research workflow 微调
* 与仓库分层无关的 skills 优化

---

## 违规示例

### 错误

* 在普通 research 任务中默认加载本文件
* 把 Harness rules 当作 canonical policy 来源
* 绕过 OpenSpec 直接修改 `knowledge/`
* 在 Harness 中再写一份 artifact contract
* 在 Harness 中重新定义 evidence / diagram / language 的正式规则

### 正确

* 普通 research 任务只加载对应 workflow 和 rules
* Canonical policy 引用 `openspec/specs/`
* 所有知识更新走 `openspec/changes/` 流程
* Harness 只把 OpenSpec 规则落实成执行手册和检查机制

---

## 相关文件

* `AGENTS.md` - 导航入口（包含本文件的条件加载路由）
* `openspec/config.yaml` - OpenSpec 项目配置入口
* `openspec/schemas/blockchain-research/schema.yaml` - artifact contract 主定义
* `openspec/schemas/blockchain-research/templates/` - canonical artifact templates
* `openspec/specs/` - canonical semantic constraints
* `harness/workflows/` - research execution playbooks
* `harness/rules/` - execution-facing guidance
