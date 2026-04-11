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

### 3.1 图例（legend）使用规范

**默认规则**：PlantUML 架构图和时序图**默认不包含图例**（legend）。

**原因**：
- 图例占用额外的排版空间，影响核心内容的视觉呈现
- 现代 PlantUML 渲染器的组件样式已足够清晰（Actor/Component/Database 等形状已有明显区分）
- 符号说明应在图外文字或正文中描述，而非依赖图例

**例外情况**：
- 仅当图中使用了非常规符号或自定义图标时，才可在 brief 中显式设置 `include_legend: true`
- 需要在 brief.yaml 的 `layout` 字段中明确声明

**brief.yaml 示例**：
```yaml
layout:
  direction: top_to_bottom
  include_legend: false  # 默认值，可省略
```

### 3.2 布局优化规范（黄金比例导向）

**目标**：架构图应避免极端化的扁宽或瘦高，追求接近黄金比例（约 1.6:1）的视觉平衡。

**组件排序规则**：

1. **同层组件数量平衡**
   - 当某层组件数量 ≥ 3 时，应考虑拆分子组或调整布局方向
   - 三层架构的组件数量比例建议为 `3:3:2` 或 `2:3:2`，避免 `5:1:1` 等极端比例

2. **Package ID 命名规范**
   - **必须使用简短单词**（如 `user_as`、`protocol`、`ext_sys`）
   - **禁止使用连字符长名**（如 `user-agent`、`ap2-protocol`）
   - 原因：PlantUML 对连字符 ID 的解析可能导致布局异常

3. **Package 描述格式**
   - **推荐格式**：使用 `\n\n` 分隔标题和描述，形成多行结构
   - **示例**：
     ```
     package "用户/Agent 控制域\n\n用户和 Agent 控制的组件\n授权决策的最终主体" as user_as
     ```
   - **禁止格式**：单行 `\n` 连接导致标题与描述混在一起

4. **同域组件对齐控制**
   - 当同 package 内有 ≥ 2 个组件时，**必须使用 `[hidden]` 虚线**强制对齐
   - **垂直对齐示例**：
     ```plantuml
     package "外部系统域" as ext_sys {
       cloud "Chain Verifier" as chain_verifier
       cloud "External Signer" as external_signer
       chain_verifier -down[hidden]- external_signer  ' 强制垂直排列
     }
     ```
   - **水平对齐示例**：
     ```plantuml
     package "内部组件" as internal {
       component "A" as a
       component "B" as b
       a -right[hidden]- b  ' 强制水平排列
     }
     ```

5. **布局方向选择**
   - **top_to_bottom**：适用于层间调用关系明确的架构图
   - **left_to_right**：适用于流程导向或组件数量较多的架构图
   - 选择原则：哪种方向更能平衡宽高比，就选哪种

**实现方式**：

上述布局优化规则已由 `feipi-plantuml-generate-architecture-diagram` skill 中的 `optimize_brief.py` 脚本自动实现。

在调用 skill 后，脚本会自动执行：
1. Layer ID 简短化
2. Package 描述格式化
3. 同域组件排序
4. hidden_lines 生成
5. include_legend 默认 false

**校验规则**：
- `lint_layout.sh` 会验证 package ID 是否为简短单词（无连字符）
- `lint_layout.sh` 会检查同域组件是否有 `[hidden]` 对齐线（当组件数 ≥ 2 时，作为 soft check 提示）

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

每张正式架构图都应在**图下方**（不得在图内）配套一小段文字说明，至少写清：
- 该图的视角：角色边界视角，还是角色内部组件视角
- 图中核心实体的控制方
- 图中是否存在被省略但与本视角无关的细节

**图内 note 与图外文字的职责边界**：

| 内容类型 | 应放在 | 原因 |
|----------|--------|------|
| 信任假设说明 | **图外文字** | 图内 note 会破坏视觉层次 |
| 组件职责说明 | **图外文字** | 图内 note 会使图过于拥挤 |
| 设计取舍说明 | **图外文字** | 需要较长文字描述 |
| 临时状态/阶段标记 | **图内 note（允许）** | 帮助理解流程中的临时状态 |
| 跨边界消息标签 | **图内 note（允许）** | 消息名称简短，直接在箭头上标注 |
| 简化/省略说明 | **图外文字** | 需要说明省略的原因和影响 |

**约束**：
- 单张图内 note 数量**不得超过 3 个**（仅用于跨边界消息标签或临时状态标记）
- 图内 note 的文字**不得超过 20 个单词**（或 30 个汉字）
- 超出限制的内容必须移到图下方文字说明

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
