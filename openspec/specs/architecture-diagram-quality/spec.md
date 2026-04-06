# 架构组件图质量规约

## 目的

定义区块链技术分析中架构组件图的质量标准。

**注意**：本规约是领域特定要求，通用 PlantUML 规范参见用户级 skills (`feipi-plantuml-generate-architecture-diagram` 和 `feipi-plantuml-generate-sequence-diagram`)。

## 两段式架构

架构组件图生成采用两段式架构：

| 阶段 | 负责方 | 交付物 |
|------|--------|--------|
| 阶段 1 | 发起方 | brief 需求模板（YAML 格式） |
| 阶段 2 | 画图方 | `<diagram-id>.puml` + `.svg` |

发起方填写需求模板，画图方（用户级 skill）根据模板生成并校验。

两段式架构详细说明见 skill 文档：`feipi-plantuml-generate-architecture-diagram/SKILL.md`

## 领域特定要求

### 0. 架构图的两种正式视角（必须先选一种）

本仓库中的 Architecture Diagram 只有两种正式用法：

| 视角 | 要回答的问题 | 允许出现的主体 | 常见用途 |
|------|--------------|----------------|----------|
| **角色与信任边界总览图** | 系统里有哪些角色、谁和谁跨边界通信、边界在哪里 | 角色、外部系统、关键数据对象 | primitive 总览、角色职责划分、边界说明 |
| **角色内部组件图** | 单个核心角色内部如何分层协作 | 同一控制方下的组件、存储、关键数据对象 | Validator / Sequencer / Relayer 内部架构 |

**禁止**在同一张架构图里同时画：
- 多个独立控制方之间的信任边界
- 某个角色内部的详细组件分层

如果需要同时说明两者，必须拆成多图。

### 1. 分层规范（区块链特定）

架构组件图必须区分以下层次：

| 层次 | 说明 | 示例组件 |
|------|------|----------|
| Protocol Layer | 协议核心层 | 共识引擎、最终性模块、证明验证器 |
| Data Layer | 数据对象层 | Proposal、Vote、Certificate |
| Application Layer | 应用接口层 | RPC Endpoint、API Gateway |
| External Layer | 外部参与方 | 验证者、用户、管理员 |

**注意**：`Validator Set`、`Proposer` 这类角色或角色集合不应与 `Consensus Engine` 这类内部组件并列落在同一层级中。

### 2. 组件内聚要求

每个组件应满足：
- **单一职责**：一个组件只做一件事
- **明确边界**：输入输出清晰
- **可解释性**：组件名称能说明其作用

### 3. 视觉层次（推荐）

- **核心组件**：放在图中央，使用更醒目的颜色
- **辅助组件**：放在边缘，使用较淡的颜色
- **外部依赖**：放在边界外，使用灰色

### 4. primitive 的最低交付要求（架构视角）

对于 `primitive` deep-dive，单靠一张"大而全"架构图通常不够，至少应满足以下约束：

1. **角色与信任边界总览图**
   - 当存在两个及以上独立控制方，或正文需要解释 trust assumption 时，必须提供。

2. **角色内部组件图**
   - 对每个**内部结构 materially 不同**的核心角色族，至少提供一张。
   - 如果多个角色内部结构相同，可复用一张 canonical 图，并用表格或短说明写清差异。

3. **不要把临时职责画成组件**
   - `Proposer`、`Leader`、`Aggregator` 若只是某角色的临时职责，应通过 note、标签或正文说明表达，而不是新增一个平级组件。

### 5. 架构图随附说明（必须）

每张正式架构图都应在图前或图后配套一小段说明，至少写清：
- 该图的视角：角色边界视角，还是角色内部组件视角
- 图中核心实体的控制方
- 图中是否存在被省略但与本视角无关的细节

如果复用了 canonical 角色内部组件图，还必须补一张差异表：

| 角色/节点类型 | 是否复用 canonical 图 | 差异点 |
|--------------|----------------------|--------|
| Example Role A | 是 | 无差异 |
| Example Role B | 是 | 缺少组件 X，新增组件 Y |

## 与 Diagram Policy 的关系

本规约是 `openspec/specs/diagram-policy/spec.md` 在架构组件图领域的具体化。

## 相关文件

- `openspec/specs/diagram-policy/spec.md`：图表总政策
- `feipi-plantuml-generate-architecture-diagram/SKILL.md`：PlantUML 生成 skill（包含两段式架构说明、元素规范和样式库）
- `feipi-plantuml-generate-architecture-diagram/assets/templates/architecture-brief.yaml`：架构组件图需求模板
- `feipi-plantuml-generate-architecture-diagram/references/template-architecture-brief.md`：需求模板详细说明
