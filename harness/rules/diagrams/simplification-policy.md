# 简化政策

## 目的

在保证准确性的前提下，规范图表的简化策略。

## 简化原则

### 原则 1: 准确性优先

**禁止**为简化而牺牲准确性。

**必须**：
- 核心机制准确
- 关键关系正确
- 边界条件清晰

### 原则 2: 场景驱动

根据读者和目的选择简化程度：

| 读者 | 目的 | 简化程度 |
|------|------|----------|
| 技术决策者 | 高层理解 | 高简化 |
| 开发者 | 集成的需要 | 中等简化 |
| 研究者 | 深入分析 | 低简化 |

### 原则 3: 渐进披露

**推荐**：
1. Overview 图（简化）
2. Detail 图（详细）
3. 完整规范（引用）

## 简化维度

### 维度 1: 组件数量

| 简化级别 | 组件数 | 适用场景 |
|----------|--------|----------|
| L1 - High | 3-5 个 | 高层概述 |
| L2 - Medium | 5-8 个 | 一般说明 |
| L3 - Low | 8-15 个 | 详细分析 |

**简化策略**：
```
原始：15 个组件
→ L2: 按功能分组为 6 个 subsystem
→ L1: 展示 3 个核心组件
```

### 维度 2: 关系复杂度

| 简化级别 | 关系数/组件 | 处理 |
|----------|-------------|------|
| L1 - High | 1-2 | 仅核心依赖 |
| L2 - Medium | 2-4 | 主要关系 |
| L3 - Low | 4+ | 完整关系 |

**简化策略**：
```
原始：每个组件 5 个关系
→ L2: 保留 3 个主要关系
→ L1: 保留 1 个核心关系
```

### 维度 3: 流程步骤

| 简化级别 | 步骤数 | 适用 |
|----------|--------|------|
| L1 - High | 3-5 步 | 高层流程 |
| L2 - Medium | 5-10 步 | 一般流程 |
| L3 - Low | 10-20 步 | 详细流程 |

**简化策略**：
```
原始：20 步流程
→ L2: 合并为 8 个关键步骤
→ L1: 展示 4 个里程碑步骤
```

## 简化技术

### 技术 1: 分组

```plantuml
' 不分组
component "A1" as A1
component "A2" as A2
component "A3" as A3
component "B1" as B1
component "B2" as B2

' 分组后
package "Subsystem A" {
  component "A1" as A1
  component "A2" as A2
  component "A3" as A3
}

package "Subsystem B" {
  component "B1" as B1
  component "B2" as B2
}
```

### 技术 2: 抽象接口

```plantuml
' 详细实现
component "ConcreteImplA" as A
component "ConcreteImplB" as B
A --> B : uses specific method

' 抽象接口
interface "IService" as I
component "Client" as C
C --> I : uses
note "有多个实现" as N
I .. N
```

### 技术 3: 折叠子流程

```plantuml
' 简化流程
A -> B : Process
note on link
  <b>处理流程</b>
  1. validate
  2. transform
  3. execute
  详见详细流程图
end note

' 而非展开所有步骤
```

### 技术 4: 使用注释

```plantuml
note right of diagram
  <b>简化说明</b>
  本图省略：
  - 错误处理流程
  - 边界情况
  - 监控和日志
  详见完整文档
end note
```

## 何时允许简化

### 可以简化的内容

1. **内部实现细节**
   - 当关注接口而非实现时

2. **错误处理路径**
   - 当关注成功路径时

3. **边界情况**
   - 当关注主流程时

4. **监控和日志**
   - 当关注业务逻辑时

5. **配置和部署**
   - 当关注设计时

### 禁止简化的内容

1. **核心机制**
   - 影响理解的关键逻辑

2. **安全边界**
   - 信任边界、权限检查

3. **数据完整性**
   - 关键数据流

4. **关键依赖**
   - 缺少则无法理解的依赖

## 简化标注

### 必须标注简化

**格式**：
```plantuml
note top of diagram
  <b>简化说明</b>
  本图简化内容：
  - 省略错误处理
  - 合并相似组件
  完整版本见：xxx.md
end note
```

### 简化程度指示

```plantuml
' 在标题中标注
title ERC-4337 架构 (简化版 - L2)
title ERC-4337 UserOp 流程 (详细版 - L3)
```

## 简化版本管理

### 版本对应

| 简化版 | 详细版 | 用途 |
|--------|--------|------|
| Overview | Architecture | 快速理解 |
| Summary | Detailed Flow | 演示 |
| Concept | Implementation | 设计讨论 |

### 引用链

```
简化版图
  ↓ 引用
详细版图
  ↓ 引用
完整规范
```

## 示例：简化对比

### 完整版 (L3)

```plantuml
@startuml
title ERC-4337 完整架构 - L3

package "Protocol" {
  component "UserOperation" as UO
  component "EntryPoint" as EP
  component "Aggregator" as AGG
  component "Paymaster" as PM
}

package "Reference Implementation" {
  component "EntryPoint.sol" as EPS
  component "SenderCreator" as SC
  component "StakeManager" as SM
  component "Mempool" as MP
}

package "Ecosystem" {
  component "Bundler" as B
  component "Wallet" as W
  component "DApp" as D
}

' 完整关系（省略具体连线）
UO --> EP
EP --> AGG
EP --> PM
EPS ..> EP
B --> MP
W --> UO
D --> EP

note bottom: 完整版本，包含所有核心组件和关系
@enduml
```

### 简化版 (L1)

```plantuml
@startuml
title ERC-4337 核心架构 - L1

package "Protocol" {
  component "UserOperation" as UO
  component "EntryPoint" as EP
}

package "Ecosystem" {
  component "Bundler" as B
  component "Wallet" as W
}

B --> EP : submits
W --> UO : creates

note bottom
  <b>简化说明</b>
  仅展示核心组件：
  - 省略 Aggregator, Paymaster
  - 省略参考实现细节
  完整版见 architecture-full.md
end note

@enduml
```

## 检查清单

- [ ] 简化是否影响准确性
- [ ] 是否标注简化内容
- [ ] 是否引用完整版本
- [ ] 简化程度是否适合读者
- [ ] 核心机制是否保留
