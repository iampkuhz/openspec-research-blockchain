# 架构组件图质量规约

## 目的

定义 PlantUML 架构组件图的质量标准，确保组件图能够清晰区分**组件**、**数据**、**角色**和**边界**，避免所有元素使用相同格式。

## 核心问题

**当前问题**：所有元素使用相同的矩形框和颜色，无法区分：
- 组件（Component）vs 数据（Data Artifact）
- 内部元素（Internal）vs 外部角色（External Actor）
- 存储（Storage）vs 处理（Processing）
- 协议层（Protocol）vs 应用层（Application）

## 质量要求

### 1. 元素类型区分（必须）

架构组件图必须使用不同的形状/颜色区分以下元素类型：

| 元素类型 | 形状 | 颜色 | PlantUML 语法 | 示例 |
|----------|------|------|---------------|------|
| **组件 (Component)** | 矩形 | 蓝色系 | `component [名称]` | 共识引擎、验证器模块 |
| **外部角色 (Actor)** | 人形 | 灰色系 | `actor [名称]` | 用户、管理员、验证者 |
| **数据存储 (Storage)** | 圆柱体 | 绿色系 | `database [名称]` | 区块存储、状态数据库 |
| **数据对象 (Data)** | 矩形（note） | 黄色系 | `note "名称" as 别名` | Proposal、Vote、Certificate |
| **接口/边界 (Interface)** | 圆形 | 橙色系 | `[名称] as 名称 <<接口>>` | API、RPC 端点 |
| **队列/通道 (Queue)** | 队列形状 | 紫色系 | `queue [名称]` | 消息队列、交易池 |

**注意**：PlantUML 不支持通过 stereotype 改变组件颜色，数据对象需使用 `note` 元素表示。

### 2. 分层着色（必须）

组件图必须通过背景色或 package 边界区分层次：

```plantuml
@startuml
skinparam componentStyle rectangle

' 定义配色方案
skinparam package {
    BackgroundColor LightBlue
    BorderColor Blue
}

skinparam component {
    BackgroundColor White
    BorderColor DarkBlue
    ArrowColor DarkGray
}

skinparam database {
    BackgroundColor LightGreen
    BorderColor Green
}

skinparam actor {
    BackgroundColor LightGray
    BorderColor Gray
}

package "共识层 <<Protocol>>" <<boundary>> {
    component [共识引擎]
    database [(区块存储)]
}

actor [验证者] as V

@enduml
```

### 3. 箭头语义（必须）

箭头必须标注语义，区分不同类型的关系：

| 关系类型 | 箭头样式 | 标注 | 说明 |
|----------|----------|------|------|
| **调用/请求** | 实线箭头 | `: 请求内容` | 组件间调用 |
| **数据流** | 虚线箭头 | `: 数据名称` | 数据传递 |
| **依赖** | 虚线无箭头 | `..` | 编译时依赖 |
| **创建** | 虚线箭头 + create | `create` | 创建新对象 |
| **生命周期** | 实线 + 销毁标记 | `destroy` | 销毁对象 |

### 4. 组件内聚（推荐）

每个组件应满足：
- **单一职责**：一个组件只做一件事
- **明确边界**：输入输出清晰
- **可解释性**：组件名称能说明其作用

### 5. 视觉层次（推荐）

- **核心组件**：放在图中央，使用更醒目的颜色
- **辅助组件**：放在边缘，使用较淡的颜色
- **外部依赖**：放在边界外，使用灰色

## 检查清单

在提交组件图前，必须完成以下检查：

### 基础检查（必须）

- [ ] 组件和数据使用了不同的形状/颜色
- [ ] 外部角色使用了 actor 语法
- [ ] 数据存储使用了 database 语法
- [ ] 所有箭头都有标注说明
- [ ] 有明确的分层边界（package）

### 进阶检查（推荐）

- [ ] 配色方案一致
- [ ] 核心组件在视觉中心
- [ ] 图例说明完整
- [ ] 组件数量适中（5-9 个）

## 示例：好的 vs 坏的

### 坏的示例

```plantuml
@startuml
' 所有元素都是相同的矩形框，无法区分
[Proposer]
[Validator Set]
[Block Production]
[Consensus Core]
[Finality Module]

[Proposer] --> [Block Production]
[Block Production] --> [Consensus Core]
[Consensus Core] --> [Validator Set]
[Validator Set] --> [Finality Module]
@enduml
```

**问题**：
1. 所有元素形状相同，无法区分组件和数据
2. 没有分层边界
3. 箭头无标注
4. 无法识别外部角色

### 好的示例

```plantuml
@startuml
skinparam componentStyle rectangle
skinparam package {
    BackgroundColor#F5F8FA
    BorderColor#4A90D9
}

skinparam component {
    BackgroundColor White
    BorderColor#2E5C8A
    ArrowColor#666666
}

skinparam database {
    BackgroundColor#E8F5E9
    BorderColor#4CAF50
}

skinparam actor {
    BackgroundColor#F5F5F5
    BorderColor#757575
}

package "Malachite 共识层 <<Protocol>>" {
    component [区块生产] as BP
    component [共识核心] as CC <<core>>
    component [最终性模块] as FM
}

package "数据对象 <<Data>>" <<boundary>> {
    [Proposal] as P <<数据>>
    [Vote] as V <<数据>>
    [Certificate] as C <<数据>>
}

actor [验证者] as Validator

Validator --> P : 提议
P --> BP : 接收
BP --> CC : Proposal
CC --> V : 收集
V --> FM : 投票
FM --> C : 生成证书
@enduml
```

**优点**：
1. 组件使用矩形，数据使用平行四边形，角色使用 actor
2. 通过 package 明确分层
3. 箭头有清晰标注
4. 配色一致，视觉层次清晰

## 配色方案参考

### 蓝色系（组件）

```plantuml
skinparam component {
    BackgroundColor#E3F2FD    ' 浅蓝背景
    BorderColor#1976D2        ' 深蓝边框
}
```

### 绿色系（数据/存储）

```plantuml
skinparam database {
    BackgroundColor#E8F5E9    ' 浅绿背景
    BorderColor#388E3C        ' 深绿边框
}
```

### 灰色系（外部角色）

```plantuml
skinparam actor {
    BackgroundColor#F5F5F5    ' 浅灰背景
    BorderColor#757575        ' 深灰边框
}
```

## 本仓库的默认配色方案

```plantuml
@startuml
skinparam componentStyle rectangle

' 配色方案
skinparam package {
    BackgroundColor#F8F9FA
    BorderColor#DEE2E6
}

skinparam component {
    BackgroundColor#FFFFFF
    BorderColor#0D6EFD
    ArrowColor#495057
}

skinparam database {
    BackgroundColor#D1E7DD
    BorderColor#0A58CA
}

skinparam actor {
    BackgroundColor#E9ECEF
    BorderColor#495057
}

skinparam legend {
    BackgroundColor#FFFFFF
    BorderColor#DEE2E6
}

legend right
  |= 元素 |= 说明 |
  | 矩形蓝色 | 组件 |
  | 平行四边形黄色 | 数据对象 |
  | 圆柱体绿色 | 数据存储 |
  | 人形灰色 | 外部角色 |
endlegend

@enduml
```

## 相关文件

- `openspec/specs/diagram-policy/spec.md`：图表总政策
- `skills/feipi-gen-plantuml-code/`：PlantUML 生成 skill
