---
name: build-plan
description: 用于在 request.md 已经成型后，生成和修订 plan.md；适合把 brief 与 source planning 合并为一次集中 review。
---

# 生成研究计划

## 何时使用

- `request.md` 已经写好
- 需要把问题收紧为可执行计划
- 需要一次性生成预算、来源规划、evidence gap 与后续确认问题

## 输出要求

- `plan.md`
- 如确有必要，再补 `dependencies.md`、`decision-criteria.md`、`evidence-matrix.md`

## 强约束

- `plan.md` 是 review 文件，不是分析正文
- 把计划层与来源规划层的职责合并到 `plan.md`
- 对 `primitive`，必须在"待确认问题"中覆盖以下三类问题（具体措辞随研究对象调整，以下为 EIP 类的参考示例）：
  - **设计选择类**：为什么选择当前架构路径而不是更直接的协议层改动（示例：为什么不改传统 transaction 路径）
  - **角色分层类**：关键角色分别位于哪一层，是 protocol-native、official ecosystem 还是 third-party（示例：Bundler 属于哪一层）
  - **能力边界类**：哪些声称的能力不是 protocol-native，依赖了什么外部假设（示例：哪些能力不是 protocol-native）
- 结论优先依赖 `L1/L2`
- 明确区分协议原生、官方生态、第三方能力

### 来源链接约束

- 每条来源必须附可点击链接；如当下无法确认准确 URL，标注 `[待补链接: 原因]`，不允许只写纯文字描述
- **L3 / L4 层**所有链接，生成时如无法通过工具（`fetch_content`）实时验证存活，一律标注 `[未验证]`；**严禁写入未经核实的推测 URL**（模型记忆中的印象地址不算模型判断）
- **L1 / L2 层**链接应优先验证；如无法验证，同样标注 `[未验证]`
- 来源规划表结构为三列：`来源 | 类型 | 说明`，**不得加"状态"列**（plan 阶段全部是 pending，该列无信息量）

### 图表规划约束

`交付范围` section 中必须显式列出图表类 deliverable，并按以下优先级说明图的类型和渲染工具：

- **组件图（必须）**：PlantUML 组件图，由 `feipi-gen-plantuml-code` skill 渲染，展示角色 / 组件 / 层级关系
- **流程图（可选）**：时序图，由 `feipi-gen-plantuml-code` skill 渲染，展示核心执行路径；必须在 plan 中明确标注"可有可无"或"必须"
- **对比表 / 归属表（推荐）**：能力归属、链适配对比等结构化表格，信息不得与图重复
- 原则：多用图表辅助阅读，但每张图 / 表必须有独立的信息价值
- **强制规定：所有图，只要 PlantUML 支持该图类型，必须使用 PlantUML 生成，统一由 `feipi-gen-plantuml-code` skill 渲染；禁止手写图或使用其他工具生成**

### 完成标准必填项

每个 `plan.md` 的完成标准中，以下两项为固定必填项，不得省略：

- `[ ] draft.md 包含【参考资料】章节，每条来源均附可点击链接`
- `[ ] 所有链接已通过工具验证存活，或明确标注 [未验证] 并说明原因`
