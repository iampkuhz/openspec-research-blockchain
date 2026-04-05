# OpenSpec 与 Harness 职责边界

**版本**：1.0
**最后更新**：2026-04-05

---

## 重要阅读提示

**任务语义优先，路径辅助**：不要因为文件位于某个路径下就自动加载本文件，只有当任务语义涉及规约/架构调整时才加载。

**必须读取本文件的场景**：
- 调整 OpenSpec / Harness 职责边界
- 修改 schema / specs / templates / governance / repository architecture
- 修改用于定义或评审规约分层的 workflow / rules / skills
- 修改 AGENTS.md 中与仓库路由、治理、分层相关的段落
- 评审上述类型的变更

**不要默认读取本文件的场景**：
- 普通技术调研、知识条目更新
- 来源收集与验证、图表生成
- 一般性的 research workflow 微调
- 与仓库分层无关的 skills 优化

**说明**：触发条件是**任务语义是否涉及规约/治理/分层/架构调整**，而不是文件路径是否位于 `harness/` 或 `openspec/` 下。

---

## 仓库定位

本仓库是 **区块链技术调研 / knowledge production repo**，主产物是 **research knowledge artifacts**，不是代码实现。

---

## 职责边界

### OpenSpec 层负责

| 职责 | 文件位置 |
|------|----------|
| **工件契约主定义** | `openspec/schemas/blockchain-research/schema.yaml` |
| **标准模板** | `openspec/schemas/blockchain-research/templates/*.md` |
| **模式级工作流语义** | `openspec/schemas/blockchain-research/schema.yaml` (artifacts 段 dependencies) |
| **标准语义约束** | `openspec/specs/*/spec.md` |
| **项目级配置** | `openspec/config.yaml` (默认模式选择、上下文注入、单工件规则注入) |

**必须在 OpenSpec 的内容**：
- artifact 依赖链定义
- artifact template 结构
- 证据等级政策
- 图表政策（生成/验证/交付标准）
- 语言风格约束
- 仓库资产模型
- 研究对象模型

### Harness 层负责

| 职责 | 文件位置 |
|------|----------|
| **研究执行手册** | `harness/workflows/*.md` |
| **执行面治理** | `harness/rules/general/repo-governance.md` |
| **执行面追溯流程** | `harness/rules/general/traceability-policy.md` |
| **执行面更新流程** | `harness/rules/general/update-policy.md` |
| **执行面术语治理** | `harness/rules/general/terminology-policy.md` |
| **图表执行指南** | `harness/rules/diagrams/*.md` |
| **研究写作指南** | `harness/rules/research/*.md`, `harness/rules/writing/*.md` |

**可以合理保留在 Harness 的内容**：
- 来源收集、评审、修复、应用操作配方
- 追溯文件格式模板（Source Pack / Excerpt / Change Packet）
- 术语治理流程（创建/复用/冲突解决）
- 更新流程（changelog 格式、版本号规范）
- 图表类型选择指南、简化策略、评审清单

---

## 核心约束

| 约束 | 归属 | 说明 |
|------|------|------|
| 变更必须走 OpenSpec | OpenSpec | 禁止直接修改 `knowledge/` |
| 工件模板结构 | OpenSpec | 定义 artifact 的必需结构 |
| 证据等级政策 | OpenSpec | L1/L2/L3/L4 定义及使用规则 |
| 图表政策 | OpenSpec | 图表生成/验证/交付标准 |
| 语言风格 | OpenSpec | 中文优先、英文术语保留 |
| 研究执行流程 | Harness | intake → source → analysis → review → apply |
| 追溯操作指引 | Harness | claim-source 追溯执行流程 |
| 术语治理流程 | Harness | 术语创建/复用/冲突解决 |
| 更新流程 | Harness | changelog 格式、版本号规范 |

---

## 何时需要读取本文件

**必须读取**：
1. 修改 `openspec/` 下任何文件
2. 修改 `harness/` 下任何文件
3. 修改 `AGENTS.md` 或本文件
4. 修改 repo architecture / governance / workflow / schema / rules / skills
5. 评审上述类型的变更

**不要读取**：
1. 普通技术调研任务
2. 概念定义/比较分析写作
3. 证据收集/图表生成
4. 知识条目写作

---

## 违规示例

**错误**：
- 在普通 research 任务中默认加载本文件
- 把 harness rules 当作 canonical policy 来源
- 绕过 OpenSpec 直接修改 `knowledge/`

**正确**：
- 普通 research 任务只加载对应 workflow 和 rules
- Canonical policy 引用 `openspec/specs/`
- 所有知识更新走 `openspec/changes/` 流程

---

## 相关文件

- `AGENTS.md` - 导航入口（包含本文件的条件加载路由）
- `openspec/config.yaml` - OpenSpec 项目配置
- `openspec/schemas/blockchain-research/schema.yaml` - artifact contract 主定义
- `openspec/specs/` - canonical semantic constraints
- `harness/workflows/` - research execution playbooks
- `harness/rules/` - execution-facing guidance
