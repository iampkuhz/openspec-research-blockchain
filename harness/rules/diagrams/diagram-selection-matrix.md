# 图表选择矩阵

## 目的

根据要表达的内容选择合适的图表类型。

## 图表类型矩阵

| 要表达的内容 | 推荐类型 | 备选类型 |
|-------------|----------|----------|
| 组件关系 | Component Diagram | Deployment Diagram |
| 时序流程 | Sequence Diagram | Activity Diagram |
| 状态变化 | State Diagram | - |
| 部署架构 | Deployment Diagram | Component Diagram |
| 数据流 | Activity Diagram | Sequence Diagram |
| 层级关系 | Component Diagram | - |
| 接口定义 | - | 文本描述 |

## Component Diagram

### 适用场景

- 展示系统组件及其关系
- 说明组件职责边界
- 表达依赖关系

### 元素语义

```plantuml
rectangle "Component" as C <<component>>
interface "Interface" as I
database "Storage" as D

C --> I : uses
C ..> I : implements
C --* D : contains
C o-- D : aggregates
```

### 关系类型

| 关系 | 符号 | 含义 |
|------|------|------|
| 依赖 | `-->` | 使用关系 |
| 实现 | `..>` | 实现接口 |
| 包含 | `--*` | 强所有 |
| 聚合 | `o--` | 弱所有 |

### 何时不使用

- 需要展示时间顺序 → 用 Sequence Diagram
- 需要展示状态变化 → 用 State Diagram
- 需要展示物理部署 → 用 Deployment Diagram

## Sequence Diagram

### 适用场景

- 展示时间顺序
- 多参与方交互
- 消息传递流程

### 元素语义

```plantuml
participant "User" as U
database "Contract" as C

U -> C: message(args)
C --> U: return(value)
C -> C: self_call()
note over C: processing
```

### 何时不使用

- 只需要展示组件关系 → 用 Component Diagram
- 流程过于复杂（>10 步）→ 分解为多个图
- 不需要时间维度 → 用 Component Diagram

## State Diagram

### 适用场景

- 展示状态变化
- 状态机逻辑
- 条件转移

### 元素语义

```plantuml
[*] --> Initial
Initial --> Processing : event
Processing --> Complete : success
Processing --> Failed : error
Complete --> [*]
Failed --> [*]
```

### 何时不使用

- 没有明确状态 → 用 Activity Diagram
- 状态过多（>10）→ 分解
- 只需要流程 → 用 Activity Diagram

## Deployment Diagram

### 适用场景

- 展示物理部署
- 节点分布
- 网络拓扑

### 元素语义

```plantuml
node "Server" as S {
  artifact "App" as A
}

cloud "Internet" as I

S -- I : HTTP
```

### 何时不使用

- 只需要逻辑关系 → 用 Component Diagram
- 不涉及物理节点 → 用 Component Diagram

## 图复杂度控制

### 单一职责原则

**禁止**在一张图中表达过多内容。

**推荐**：
- Component 图：5-10 个组件
- Sequence 图：3-6 个参与方，5-15 步
- State 图：3-8 个状态

### 分层策略

当内容过多时：
1. 创建 Overview 图（高层）
2. 创建 Detail 图（子组件）
3. 使用引用链接

```plantuml
' Overview
package "System" {
  component "SubSystem" <<subsystem>>
}

note "详见 SubSystem Detail 图" as NOTE
SubSystem .. NOTE
```

## 图的选择决策树

```
要表达什么？
├── 组件关系 → Component Diagram
│   ├── 需要展示物理部署？ → Deployment Diagram
│   └── 需要展示层级？ → 分层 Component Diagram
│
├── 时间流程 → Sequence Diagram
│   ├── 参与方>6？ → 分解为多个序列
│   └── 步骤>15？ → 创建摘要图 + 详细图
│
├── 状态变化 → State Diagram
│   ├── 状态>8？ → 分层状态机
│   └── 多对象状态？ → 并行列出或分离
│
└── 数据/控制流 → Activity Diagram
    ├── 分支过多？ → 简化或分解
    └── 并发流程？ → 使用泳道
```

## 示例：选择过程

### 场景 1: 解释 ERC-4337 架构

**需求**：展示 Bundler、EntryPoint、Paymaster、Wallet 的关系

**选择**：Component Diagram

**原因**：
- 需要展示组件关系
- 不需要时间顺序
- 组件数量适中（4 个）

### 场景 2: 解释 UserOp 处理流程

**需求**：展示 UserOp 从提交到执行的完整流程

**选择**：Sequence Diagram

**原因**：
- 有时间顺序
- 多参与方交互
- 消息传递清晰

### 场景 3: 解释 EntryPoint 状态

**需求**：展示 UserOp 验证和执行的状态变化

**选择**：State Diagram

**原因**：
- 明确的状态
- 条件转移
- 状态数量有限
