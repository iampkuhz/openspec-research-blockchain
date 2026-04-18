# 架构组件图抽象层级规约

## 目的

定义架构组件图中**组件抽象层级**的要求，确保图中组件处于同一抽象维度，避免将**整体与部分**、**角色与系统**混为一谈。

## 核心问题

### 问题 1：维度混用

**错误示例**：
```plantuml
package "Tendermint Consensus" {
  [Proposer] as P          ' 角色（节点的一种功能）
  [Validator Set] as V     ' 角色集合
  [Consensus Engine] as CE ' 模块
  [Application] as APP     ' 外部系统
  [Blockchain] as BC       ' 整体系统
}
```

**问题分析**：
- `Proposer` 是节点的角色，不是独立组件
- `Validator Set` 是角色集合，不是组件
- `Blockchain` 是整体系统，包含 Consensus Engine
- 这些元素**不是同一抽象层级**，不能并列

### 问题 2：重复表示

同一实体在图中多次出现，使用不同名称：
- `Validator` 和 `Validator Set` 实际是同一概念
- `Proposer` 和 `Leader` 实际是同一概念

### 问题 3：上下级关系缺失

没有表达"包含"关系：
- Blockchain **包含** Consensus Engine
- Validator **可以是** Proposer（轮转）

## 控制权与信任边界定义

在本仓库中，判断一个实体应落入"角色图"还是"组件图"，以**控制权**和**信任边界**为准。

| 实体类型 | 判断标准 | 信任关系 | 典型问题 | 推荐落图 |
|----------|----------|----------|----------|----------|
| **Role（角色）** | 控制方不同，或即使同属协议也需要跨边界通信 | 存在显式信任假设 | 谁和谁交互？边界在哪里？ | 角色与信任边界总览图、跨角色流程图 |
| **Component（组件）** | 控制方相同，属于同一操控者内部实现 | 默认无内部信任假设 | 该角色内部如何分层协作？ | 角色内部组件图 |
| **State（状态）** | 同一角色/组件在运行中的阶段 | 不单独形成信任边界 | 状态如何迁移？什么事件触发？ | 状态机图 / 状态转换表 |
| **Data Object（数据对象）** | 消息、证书、区块、证明等载荷 | 不是角色，也不是组件 | 传递了什么数据？ | 作为辅助元素出现在架构图或流程图中 |
| **External System（外部系统）** | 系统外部的集成对象或环境 | 与研究对象之间存在边界 | 系统与外部如何交互？ | 角色与信任边界总览图 |

### 关键判定规则

1. **同一控制方 + 无条件信任 = 组件**
   - 例如同一 Validator 进程中的 Consensus Engine、Mempool、State Machine。

2. **不同控制方 + 需要协议约束通信 = 角色**
   - 例如 Validator、User、Sequencer、Prover、Relayer。

3. **临时职责不是独立组件**
   - 例如 Proposer/Leader/Executor 若只是某个角色在特定轮次承担的职责，应视为角色的状态或子职责，而不是独立组件。

4. **状态不是组件**
   - 例如 `RoundStepPrevote`、`ChallengeWindowOpen`、`Locked` 应放入状态机表达，而不是放入组件图。

## 视图与问题映射

同一个 primitive 往往需要多张图，但每张图只能回答一类问题：

| 视图 | 回答的问题 | 允许元素 | 推荐图种 |
|------|------------|----------|----------|
| **角色与信任边界视图** | 系统里有哪些角色？谁和谁跨边界通信？ | 角色、外部系统、关键数据对象 | Architecture Diagram |
| **角色内部组件视图** | 单个核心角色内部如何分层和协作？ | 单一角色内部组件、存储、关键数据对象 | Architecture Diagram |
| **跨角色流程视图** | 关键步骤如何在角色之间流转？ | 角色、消息、关键数据对象 | Sequence Diagram |
| **角色局部状态视图** | 某个角色内部状态如何转换？ | 状态、事件、转换条件 | Mermaid stateDiagram / 状态表 |

## 抽象层级定义

组件图必须明确表达以下抽象层级：

### Level 1 - 系统边界（System Boundary）

描述系统与外部环境的关系。

**元素类型**：
- 系统本身（如：Tendermint Network）
- 外部系统（如：Application、Client）
- 外部角色（如：User、Operator）

**PlantUML 表示**：
```plantuml
package "Tendermint Network <<system>>" {
    ' 系统内部组件
}

actor "External Application" as App
```

### Level 2 - 节点类型（Node Type）

描述系统内不同类型的节点。

**元素类型**：
- Validator Node（验证者节点）
- Full Node（全节点）
- Light Client（轻节点）

**PlantUML 表示**：
```plantuml
package "Validator Nodes" {
    component [Validator A] as Va
    component [Validator B] as Vb
}
```

### Level 3 - 节点内部（Internal Components）

描述单个节点的内部组件。

**元素类型**：
- Consensus Engine（共识引擎）
- Mempool（内存池）
- Blockchain Store（区块存储）
- State Machine（状态机）

**PlantUML 表示**：
```plantuml
package "Validator Node Internal" {
    component [Consensus Engine] as CE
    component [Mempool] as MP
    component [State Machine] as SM
    database [(Blockchain Store)] as BS
}
```

### Level 4 - 角色/功能（Role/Function）

描述节点在特定时刻扮演的角色。

**元素类型**：
- Proposer（提议者）- 当前轮次的 Leader
- Voter（投票者）- 其他验证者

**重要**：角色**不是独立组件**，是节点的**临时状态**。

**PlantUML 表示**（使用 note 或 stereotype）：
```plantuml
component [Validator A] as Va
note right of Va: Current Proposer
```

## 质量要求

### 1. 单一抽象层级原则（必须）

**每个组件图应聚焦于一个抽象层级**，不要混用多个层级。

| 图类型 | 聚焦层级 | 允许出现的关系 |
|--------|----------|----------------|
| 角色与信任边界总览图 | Level 1 / Level 2 | 角色 ↔ 角色、系统 ↔ 外部实体 |
| 角色内部组件图 | Level 3 | 组件 ↔ 组件、组件 ↔ 数据存储 |
| 跨角色流程图 | Level 4 | 角色 ↔ 消息、角色 ↔ 角色 |
| 状态转换图 | 角色局部状态 | 状态 ↔ 状态、状态 ↔ 事件 |

### 1.1 角色图与组件图分离（必须）

**禁止**在同一张架构图里同时表达：
- 跨角色信任边界
- 某个角色内部的组件分层

如果既要表达"谁和谁通信"，又要表达"某个角色内部如何实现"，必须拆成至少两张图：
- 一张角色与信任边界总览图
- 一张角色内部组件图

### 2. 包含关系显式化（必须）

如果组件 A 包含组件 B，必须使用 package 或注释明确：

```plantuml
package "Tendermint Node" {
    component [Consensus Engine] as CE
    component [Mempool] as MP
}

' 或
[Consensus Engine] as CE <<inside: Tendermint Node>>
```

### 3. 角色与组件分离（必须）

角色（Proposer/Leader）不是固定组件，是**节点的状态**：

```plantuml
' 错误：Proposer 作为独立组件
component [Proposer] as P

' 正确：Proposer 是节点的角色
component [Validator A] as Va
note right of Va: <<Proposer>>
```

### 4. 节点类型明确定义（必须）

对于 BFT 共识，必须区分：

| 节点类型 | 作用 | 是否投票 |
|----------|------|----------|
| Validator | 验证者，参与共识 | 是 |
| Full Node | 全节点，同步状态 | 否 |
| Light Client | 轻节点，验证头部 | 否 |

## 检查清单

在提交组件图前，必须回答以下问题：

### 抽象层级检查（必须）

- [ ] 图中的每个组件属于哪个抽象层级？
- [ ] 是否有混用不同层级的组件？
- [ ] 如果有混用，是否用 package 明确区分？
- [ ] 每个实体是否已先判断为 role / component / state / data / external？
- [ ] 该图回答的是"边界问题"还是"内部实现问题"？

### 关系检查（必须）

- [ ] Proposer 是哪个 Validator 的角色？
- [ ] Validator Set 包含哪些具体节点？
- [ ] Blockchain 和 Consensus Engine 是什么关系？
- [ ] 哪些实体跨控制方通信？
- [ ] 哪些实体属于同一控制方、应视为内部组件？

### 重复检查（必须）

- [ ] 是否有同一实体的多个名称？
- [ ] Validator 和 Validator Set 是否同时出现？
- [ ] Proposer 和 Leader 是否同时出现？

## 示例：好的 vs 坏的

### 坏的示例（Tendermint）

```plantuml
@startuml
package "Tendermint Consensus" {
  [Proposer] as P          ' 问题：角色，不是组件
  [Validator Set] as V     ' 问题：集合，不是具体节点
  [Consensus Engine] as CE ' 问题：这是节点内部组件
  [Application] as APP     ' 问题：外部系统
  [Blockchain] as BC       ' 问题：整体系统
}

P --> CE : Proposal
V --> CE : Vote
@enduml
```

**问题分析**：
1. 5 个元素分属 4 个不同层级
2. Proposer 是 Validator 的角色，不是独立实体
3. Validator Set 包含 Validator，但 Validator 未出现
4. Blockchain 包含 Consensus Engine，但画成并列关系

### 好的示例（Tendermint - 节点内部视角）

```plantuml
@startuml
skinparam componentStyle rectangle

title Tendermint Validator Node Internal Architecture

package "Tendermint Validator Node" {
    component [Consensus Engine] as CE
    component [Mempool] as MP
    component [State Machine] as SM
    database [(Blockchain Store)] as BS

    note "Current Role: Proposer or Voter" as Role
}

' 外部实体
actor "Other Validators" as OtherVals
actor "Full Nodes" as FullNodes

' 数据流
OtherVals --> CE : Prevote/Precommit
CE --> MP : Get Transactions
CE --> SM : Execute Block
SM --> BS : Write State
CE --> FullNodes : Broadcast Block

@enduml
```

**优点**：
1. 聚焦于**单个 Validator 节点内部**
2. 明确 Proposer/Voter 是角色说明
3. 组件都在 Level 3（节点内部组件）
4. 外部交互清晰（Other Validators、Full Nodes）

### 好的示例（Tendermint - 系统视角）

```plantuml
@startuml
skinparam componentStyle rectangle

title Tendermint Network - Validator Interaction

package "Validator Network (3 Validators)" {
    package "Validator A" {
        component [Consensus A] as CA
        note right of CA: <<Proposer Round N>>
    }

    package "Validator B" {
        component [Consensus B] as CB
        note right of CB: <<Voter>>
    }

    package "Validator C" {
        component [Consensus C] as CC
        note right of CC: <<Voter>>
    }
}

CA --> CB : Proposal + Prevote
CA --> CC : Proposal + Prevote
CB --> CA : Precommit
CC --> CA : Precommit

@enduml
```

**优点**：
1. 展示多节点交互
2. 用 note 标注当前角色
3. 每个 Validator 是独立 package
4. 消息流清晰

## 相关文件

- `harness/rules/diagrams/architecture-quality-rules.md`：元素类型区分
- `harness/rules/diagrams/diagram-policy.md`：图表总政策
