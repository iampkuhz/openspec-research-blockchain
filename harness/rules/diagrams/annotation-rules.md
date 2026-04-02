# 注释规则

## 目的

规范图中注释的使用方式，提高图的可读性。

## 注释类型

### 类型 1: 术语注释

**用途**：解释图中专业术语

**格式**：
```plantuml
component "UserOperation" as UO
note right of UO
  <b>术语说明</b>
  EIP-4337 定义的用户操作原子
  包含 sender, nonce, callData 等字段
end note
```

### 类型 2: 边界注释

**用途**：说明组件/流程的边界

**格式**：
```plantuml
rectangle "EntryPoint Contract" {
  component "validateUserOp" as V
  component "executeUserOp" as E
}

note bottom of EntryPoint Contract
  <b>边界说明</b>
  仅展示核心验证和执行流程
  Gas 计算逻辑已省略
end note
```

### 类型 3: 流程注释

**用途**：说明流程的目的和结果

**格式**：
```plantuml
A -> B : validate
note on link
  <b>验证流程</b>
  1. 验证签名
  2. 验证 paymaster
  3. 检查 gas 限制
end note
```

### 类型 4: 假设注释

**用途**：说明分析所基于的假设

**格式**：
```plantuml
note top of diagram
  <b>假设条件</b>
  - Bundler 是可信的
  - Gas 价格稳定
  - 网络延迟 < 100ms
end note
```

## 注释位置规范

### 组件注释

| 位置 | 含义 | 使用场景 |
|------|------|----------|
| `note right of` | 组件说明 | 最常用，不遮挡关系 |
| `note left of` | 组件说明 | 右侧空间不足时 |
| `note top of` | 角色/职责 | 高层概念说明 |
| `note bottom of` | 实现细节 | 底层说明 |

### 关系注释

| 位置 | 含义 | 使用场景 |
|------|------|----------|
| `note on link` | 关系说明 | 解释交互内容 |
| `note left of link` | 条件说明 | 不影响关系可见性 |
| `note right of link` | 结果说明 | 补充信息 |

### 全局注释

| 位置 | 含义 | 使用场景 |
|------|------|----------|
| `note top of diagram` | 全局说明 | 前提条件、范围 |
| `note bottom of diagram` | 补充说明 | 参考信息、待办 |
| `note floating` | 独立说明 | 图例、key |

## 注释内容规范

### 必须包含的内容

**技术术语首次出现**：
- 简洁定义
- 来源引用（如 EIP 编号）

**非标准符号**：
- 符号含义说明
- 使用场景

**简化内容**：
- 省略了什么
- 为什么省略

### 禁止的内容

**禁止**：
- 过长文本（>100 字）
- 与图无关的信息
- 重复图中已明确的内容
- 模糊表述（"可能"、"大概"）

## 注释格式规范

### Markdown 语法

```plantuml
note right of Component
  <b>标题</b>

  正文内容，支持：
  - 列表项
  - 1. 编号列表
  - `code` 内联代码

  <i>斜体强调</i>
  <u>下划线</u>
end note
```

### 颜色使用

```plantuml
note right of Component #LightYellow
  一般注释
end note

note right of Component #LightCoral
  <b>重要警告</b>
  必须注意的内容
end note

note right of Component #LightGreen
  <b>最佳实践</b>
  推荐做法
end note
```

**颜色语义**：
- 黄色：一般信息
- 红色：警告/风险
- 绿色：推荐/最佳实践
- 蓝色：参考/链接

## 注释密度控制

### 最大密度原则

**规则**：注释面积不应超过图面积的 30%

**超限处理**：
1. 移到正文说明
2. 创建单独的注释图
3. 使用外部文档引用

### 分层注释

```plantuml
' 主图 - 最小注释
component "A" as A
component "B" as B
A --> B

' 详细注释图 - 单独展示
note "A 的详细说明..." as N1
note "B 的详细说明..." as N2
note "关系的详细说明..." as N3
```

## 示例：完整注释使用

```plantuml
@startuml
title ERC-4337 UserOp 处理流程 - 主流程

skinparam noteFontColor "black"
skinparam noteBackgroundColor "lightYellow"

participant "User" as U
participant "Wallet" as W
participant "Bundler" as B
participant "EntryPoint" as EP

note top of diagram
  <b>范围说明</b>
  仅展示成功路径
  错误处理详见错误流程图
end note

U -> W : 提交意图
note right of link
  <b>用户意图</b>
  如：Swap tokens
end note

W -> B : 构建 UserOp
note right of link
  <b>Wallet 职责</b>
  1. 构建 callData
  2. 估算 gas
  3. 签名
end note

B -> EP : handleOps([UserOp])
note on link
  <b>Bundler 行为</b>
  - 打包多个 UserOp
  - 提交到 EntryPoint
  - 承担 gas 成本
end note

EP -> EP : validateUserOp()
note right
  <b>验证内容</b>
  1. 验证签名
  2. 验证 paymaster
  3. 检查 nonce
end note

EP -> EP : executeUserOp()
note right
  <b>执行内容</b>
  执行用户 callData
end note

note bottom of diagram
  <b>图例</b>
  → : 消息流
  -->> : 返回
  note : 注释说明
end note

@enduml
```

## 检查清单

- [ ] 注释是否必要
- [ ] 注释位置是否合适
- [ ] 注释内容是否准确
- [ ] 注释密度是否过高
- [ ] 格式是否一致
