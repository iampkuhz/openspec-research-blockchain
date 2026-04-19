# Draft 阶段规范

## 目的

定义本仓库 blockchain research change 中 `draft.md` artifact 的正式规则，包括：
- draft 在 research change 中的定位
- 进入 draft 阶段的前置条件
- draft 必须满足的形式要求
- draft 完成标准

## 适用范围

本规范适用于本仓库所有 research change 的 draft 阶段。

## draft.md 的定位

`draft.md` 是 research change 的第二轮集中 review artifact，负责：
- 合并关键术语、分析正文、有限结论为单一交付物
- 承载该 change 的核心图表（边界、架构、流程、状态、对比）
- 作为从 plan 阶段迈向 synthesis 阶段的过渡交付物

## 进入 draft 阶段的前置条件

必须满足以下条件方可进入 draft 阶段：

1. **plan.md 已完成 review**
   - `plan.md` 已存在且通过 review

2. **来源规划足以支撑正文**
   - `evidence-matrix.md`（如有）已足以支撑第一轮分析

## draft 阶段的正式要求

### 结构要求

`draft.md` 必须包含以下章节（顺序固定）：

1. 概述
2. 术语表
3. 组件架构
4. 核心流程（如必要）
5. 设计取舍
6. 能力边界
7. 相关协议对比
8. 结论
9. 待确认问题
10. 参考资料

### 术语表要求

- 必须使用**表格形式**（三列：术语、定义、作用）
- 不得采用按词分标题的卡片式写法

### 图表要求

draft 阶段必须遵守：

- `harness/rules/diagrams/diagram-policy.md`
- `harness/rules/diagrams/architecture-quality-rules.md`
- `harness/rules/diagrams/component-abstraction-rules.md`

**draft 阶段落点**：
- 图表必须承载主干信息（边界、架构关系、流程步骤、状态变化、对比结论）
- 作者必须先完成实体分类，再决定图表集合；不得直接进入"想到什么就画什么"
- **所有 PlantUML 图必须通过 skill 验证**：不得手写 PlantUML 代码后直接交付

#### 图表决策树（必须先回答，再生成图表）

**步骤 1：实体分类（强制）**

在正文开头必须先完成实体分类表，将关键实体归类为：
- `role`（角色）
- `component`（组件）
- `data object`（数据对象）
- `state`（状态）
- `external system`（外部系统）

**判定原则**：
- `role`：控制方不同，跨边界通信依赖 trust assumption
- `component`：控制方相同，内部默认无条件信任
- `state`：同一角色/组件的运行阶段，不是组件
- `data object`：消息、区块、证明、证书等载荷
- `external system`：系统边界之外的集成对象

**步骤 2：回答四个判定问题（强制）**

基于实体分类表，依次回答以下问题并记录答案：

| 判定问题 | 判定依据 | 是 → 必须产出 | 否 → 可省略 |
|----------|----------|---------------|-------------|
| Q1：是否存在两个及以上独立控制方？ | 实体分类表中 `role` 数量 ≥ 2，或存在跨信任边界通信 | 角色与信任边界总览图 | 可省略 |
| Q2：是否有核心角色内部结构 materially 不同？ | 是否存在多个内部结构不同的角色/组件族 | 角色内部组件图（canonical 图 + 差异表） | 可省略 |
| Q3：是否依赖跨角色消息/调用/证明流转？ | 协议是否依赖跨角色/跨节点的消息传递 | 跨角色核心流程图（happy path + 异常路径） | 可省略 |
| Q4：是否依赖命名状态/轮次/epoch/timeout 转换？ | 是否有显式的状态机、阶段转换、超时机制 | 状态转换图/表 | 可省略 |

**步骤 3：生成图表清单表（强制）**

基于步骤 2 的答案，生成图表清单表，明确说明：
- 计划交付哪些图
- 每张图要回答的问题
- 采用格式（PlantUML / Mermaid / Markdown 表格 / ASCII）
- 为什么需要（引用步骤 2 的判定结果）或可省略

**步骤 4：检查覆盖缺口（强制）**

对比图表清单表与现有 `diagrams/` 目录：
- 如清单中某图标记为"必须"但不存在 → **阻塞 draft 完成**，告知用户需要补充
- 如清单中某图标记为"可省略"但已存在 → 建议删除或说明额外价值

**步骤 5：术语依赖检查（新增，强制）**

在生成图表前，必须检查：
- 图表中出现的**所有依赖 primitive 的核心术语**是否已在【关键术语】章节定义
- 如未定义，必须先在【关键术语】章节补充，或在图下方用文字说明（不得用图内 note）

---

#### primitive draft 的必要覆盖（必须）

primitive 类型的 `draft.md` 至少必须覆盖以下内容：

1. **实体分类表**
   - 将关键实体归类为 `role / component / data object / state / external system`
   - 标明控制方与是否跨信任边界

2. **图表清单表**
   - 说明本文计划交付哪些图
   - 说明每张图解决什么问题、为什么必需或可省略

3. **角色与信任边界总览图**（按条件必须）
   - 当存在两个及以上独立控制方，或正文需要解释 trust assumption 时，必须提供

4. **角色内部组件图**（必须）
   - 对每个内部结构 materially 不同的核心角色族，至少提供一张
   - 若多个角色内部结构相同，可复用一张 canonical 图，并补差异表

5. **跨角色核心流程图**（按条件必须）
   - 当机制依赖跨角色交互时必须提供
   - 至少有 1 张 happy path
   - 若异常/超时/挑战/回滚路径影响安全性、活性或资金安全，必须补异常路径图或表

6. **状态转换图或状态表**（按条件必须）
   - 当机制依赖命名状态、phase、round、epoch、timeout、challenge window、lock/unlock 等转换时必须提供

7. **能力归属表**（必须）
   - 区分协议原生能力、角色职责、外部依赖和非目标

#### synthesis / decision draft

其他类型按各自上位规范要求交付图表；本规范重点收紧 primitive 的必要图表集合。

### 内容要求

- 必须区分 live / planned / promotional
- 必须写边界、失败条件、前提条件
- 证据不足时必须明确写不确定性
- 结论只能是 bounded conclusions，不得写绝对化判断
- 先写机制，再写价值
- 必须回答"为什么这样设计，而不是那样设计"
- 对 primitive，必须明确区分哪些实体是角色、哪些是组件、哪些只是状态或数据对象
- 若复用 canonical 角色内部组件图，必须写清复用理由与差异点

### 风格要求

draft 阶段必须遵守：

- `harness/rules/writing/language-rules.md`
- `openspec/specs/evidence-policy/spec.md`

**draft 阶段落点**：
- 不确定性必须显式声明，不得脑补
- 不得把 promotional 能力写成 live

### 流程图步骤说明要求

- 必须使用**无序列表**，禁止使用有序列表（避免与图中序号错位）
- 必须使用 `【S1→S3】` 格式与图中序号关联
- 每个要点聚焦一个关键机制，而非罗列步骤

### PlantUML 要求

- PlantUML 仅限用于 **Architecture Diagram** 和 **Sequence Diagram**
- 这两类 PlantUML 必须通过对应的全局 skill 完整生成与验证
- 每个 PlantUML block 必须有可追溯的 diagram package 与验证合同
- 不支持的图表类型（如状态机图、活动图、部署图、比较总览图）不得手写 PlantUML 交付，必须使用 Mermaid / Markdown 表格 / ASCII fallback

## draft 阶段完成标准

draft 阶段视为完成，当且仅当：

1. **结构完整**
   - 包含所有必须章节
   - 包含目录

2. **图表完备**
   - primitive draft 包含本规范要求的必要覆盖项
   - 所有 PlantUML 满足 diagram policy 的支持矩阵与验证合同要求

3. **内容合规**
   - 遵守所有上位规范要求
   - 满足本规范"正式要求"所有条款

4. **参考资料验证**
   - 【参考资料】章节中每条来源均附可点击链接
   - 所有链接已尝试验证（通过自动工具或手动）
   - 无法验证的链接已标注 `[未验证]` 并说明原因（如"网络限制"、"URL 失效"、"需认证"）

5. **角色/组件抽象正确**
   - 没有把跨信任边界角色误画成内部组件
   - 没有把状态或临时职责误画成平级组件

## 与上位规范的关系

本规范是以下规范的 draft 阶段特化：

| 上位规范 | 约束范围 |
|----------|----------|
| `openspec/schemas/blockchain-research/schema.yaml` | change 整体结构 |
| `harness/rules/diagrams/diagram-policy.md` | 图表政策 |
| `harness/rules/diagrams/architecture-quality-rules.md` | 架构图质量 |
| `harness/rules/diagrams/component-abstraction-rules.md` | 组件抽象层级 |
| `harness/rules/writing/language-rules.md` | 语言风格 |
| `openspec/specs/evidence-policy/spec.md` | 证据政策 |
| `openspec/specs/canonical-output-model/spec.md` | 输出模型 |

本规范不重复上位规范的正文，仅定义：
- draft 阶段的入口条件
- draft 阶段的形式要求
- draft 阶段的完成标准

## PlantUML 在 draft 阶段的落点

对 draft 阶段，PlantUML 的正式要求进一步收紧为：

1. **支持范围**
   - 仅 `Architecture Diagram` 和 `Sequence Diagram` 可以使用 PlantUML

2. **生成方式**
   - 必须通过对应的全局 skill 生成
   - 不得手写或手改后冒充 skill 产物

3. **交付证明**
   - 每个 PlantUML block 必须能追溯到 diagram package
   - diagram package 必须包含验证合同，且显示成功

4. **不支持类型**
   - 状态机图、活动图、部署图、比较总览图等无 dedicated skill 支持的类型
   - 必须使用 Mermaid、Markdown 表格或 ASCII/Unicode 图交付

## primitive 在 draft 阶段的必要图表矩阵

| 问题 | 最低交付物 | 是否必须 | 推荐格式 |
|------|------------|----------|----------|
| 系统里有哪些角色、边界在哪里？ | 角色与信任边界总览图 | 有多角色或 trust assumption 时必须 | PlantUML Architecture |
| 单个核心角色内部如何分层？ | 角色内部组件图 | 必须 | PlantUML Architecture |
| 关键步骤如何跨角色流转？ | 跨角色核心流程图 | 有跨角色交互时必须 | PlantUML Sequence |
| 关键状态如何迁移？ | 状态机图 / 状态转换表 | 有显式状态转换时必须 | Mermaid / Markdown 表格 / ASCII |
| 能力归属和非目标是什么？ | 能力归属表 | 必须 | Markdown 表格 |
| 多个角色是否复用同一内部结构？ | 角色差异表 | 复用 canonical 图时必须 | Markdown 表格 |

## 相关规范

- `openspec/schemas/blockchain-research/templates/draft.md` —— draft 模板
- `harness/rules/diagrams/diagram-policy.md` —— 图表政策
- `harness/rules/diagrams/architecture-quality-rules.md` —— 架构图质量
- `harness/rules/diagrams/component-abstraction-rules.md` —— 组件抽象层级
- `harness/rules/writing/language-rules.md` —— 语言风格
- `openspec/specs/evidence-policy/spec.md` —— 证据政策
- `openspec/specs/canonical-output-model/spec.md` —— 输出模型
