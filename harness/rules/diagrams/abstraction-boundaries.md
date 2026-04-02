# 抽象边界规则

## 目的

防止在图中混用不同抽象层的概念。

## 抽象层定义

### Layer 0: Protocol

**描述**：协议层定义

**元素**：
- 协议规范定义的概念
- 标准接口
- 共识规则

**示例**：
- UserOperation (EIP-4337)
- Transaction (Ethereum Protocol)
- Block (Ethereum Protocol)

### Layer 1: Implementation

**描述**：参考实现层

**元素**：
- 参考实现中的类/结构
- 合约实现
- 具体算法

**示例**：
- UserOperation.sol 结构体
- EntryPoint 合约实现
- Bundler 参考实现

### Layer 2: Ecosystem

**描述**：生态扩展层

**元素**：
- 第三方服务
- 工具实现
- 应用扩展

**示例**：
- Stackup Bundler 服务
- Pimlico Paymaster
- 钱包 SDK

### Layer 3: Application

**描述**：应用层

**元素**：
- DApp 集成
- 用户界面概念
- 业务逻辑

**示例**：
- 钱包 UI 中的"发送"按钮
- DApp 中的支付流程
- 服务配置

## 禁止的混用

### 错误示例 1: 混用 Protocol 和 Implementation

❌ 错误：
```plantuml
component "UserOperation" as UO  ' Protocol 概念
component "UserOperation.sol" as UOS  ' Implementation 概念
UO --> UOS : ???  ' 错误关系
```

**问题**：UserOperation 是协议概念，UserOperation.sol 是实现，两者不是同一抽象层。

✅ 正确：
```plantuml
' Protocol 层
component "UserOperation" as UO <<protocol>>

note right of UO
  Protocol 层定义
  详见 EIP-4337
end note

' Implementation 层（单独图或分区）
package "Reference Implementation" {
  component "UserOperation.sol" as UOS <<struct>>
}

UOS ..> UO : implements
```

### 错误示例 2: 混用 Protocol 和 Ecosystem

❌ 错误：
```plantuml
component "EntryPoint" as EP  ' Protocol 概念
component "Stackup SDK" as SDK  ' Ecosystem 概念
EP --> SDK : uses  ' 错误：协议不会使用第三方 SDK
```

**问题**：EntryPoint 是协议层单例合约，不会"使用"第三方 SDK。

✅ 正确：
```plantuml
component "EntryPoint" as EP <<protocol>>
component "Wallet App" as Wallet <<application>>
component "Stackup SDK" as SDK <<ecosystem>>

Wallet --> SDK : uses
SDK --> EP : interacts with
```

### 错误示例 3: 混用不同 Protocol 层

❌ 错误：
```plantuml
component "UserOperation" as UO  ' ERC-4337
component "Transaction" as TX  ' L1 Protocol
component "Bundle" as B  ' MEV-Boost
UO --> TX : becomes
TX --> B : included in
```

**问题**：虽然这些概念有关联，但直接画在一起会模糊边界。

✅ 正确：
```plantuml
' ERC-4337 层
package "ERC-4337" {
  component "UserOperation" as UO
  component "EntryPoint" as EP
}

' L1 Protocol 层
package "L1 Protocol" {
  component "Transaction" as TX
  component "Block" as BLK
}

' MEV-Boost 层
package "MEV-Boost" {
  component "Bundle" as B
}

UO ..> TX : bundled into
TX ..> B : included in
```

## 正确的分层策略

### 策略 1: 分层展示

```plantuml
top to bottom direction

' Layer 0: Protocol
rectangle "Protocol Layer" {
  component "UserOperation" as UO
  component "EntryPoint" as EP
}

' Layer 1: Implementation
rectangle "Implementation Layer" {
  component "EntryPoint.sol" as EPS
  component "UserOperation.sol" as UOS
}

' Layer 2: Ecosystem
rectangle "Ecosystem Layer" {
  component "Bundler Service" as BS
  component "Paymaster Service" as PS
}

UO ..> UOS : defined by
EP ..> EPS : implemented by
EPS --> BS : used by
```

### 策略 2: 使用 Stereotype

```plantuml
component "UserOperation" as UO <<protocol>>
component "UserOperation.sol" as UOS <<implementation>>
component "Stackup SDK" as SDK <<ecosystem>>

UOS ..> UO : implements
SDK --> UO : uses definition
```

### 策略 3: 分区注释

```plantuml
note top of diagram
  本图包含多层概念：
  - Protocol: UserOperation, EntryPoint
  - Ecosystem: Bundler, Paymaster
  注意区分层次
end note
```

## 关系语义

### 跨层关系类型

| 关系 | 含义 | 示例 |
|------|------|------|
| `implements` | 实现/具现 | Implementation → Protocol |
| `uses` | 使用 | Application → Ecosystem |
| `interacts with` | 交互 | Ecosystem → Protocol |
| `defined by` | 定义 | Implementation → Protocol |
| `extends` | 扩展 | Ecosystem → Implementation |

### 禁止的关系

❌ Protocol `uses` Ecosystem
- 协议不会使用第三方服务

❌ Ecosystem `implements` Protocol
- 生态服务不是"实现"协议

❌ Application `is part of` Protocol
- 应用不是协议的一部分

## 图的标题规范

**必须**在标题或注释中说明抽象层：

```plantuml
title ERC-4337 架构 - Protocol 层

' 或

note top of diagram
  本图展示 Protocol 层概念
  Implementation 详见实现文档
end note
```

## 检查清单

在创建图时检查：

- [ ] 是否混用了不同抽象层
- [ ] 关系语义是否正确
- [ ] 是否需要分层展示
- [ ] stereotype 是否正确标注
- [ ] 标题是否说明抽象层
