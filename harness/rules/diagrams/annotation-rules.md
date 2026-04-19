# 注释规则

## 目的

规范 PlantUML 图中注释的使用方式，提高图的可读性和可理解性。

## 核心原则

### 原则 1: 注释是补充，不是主体

**注释用于**：
- 解释专业术语
- 说明简化内容
- 标注假设条件
- 强调关键约束

**注释不用于**：
- 替代清晰的图结构
- 承载大量正文内容
- 重复图中已明确的信息

### 原则 2: 简洁优先

**单条注释约束**：
- 不超过 100 字
- 不超过 5 行
- 使用列表而非长段落

### 原则 3: 分层披露

| 层次 | 注释策略 |
|------|----------|
| Overview 图 | 最小注释，仅核心说明 |
| Detail 图 | 按需添加技术细节注释 |
| 完整规范 | 外部文档引用 |

## 注释类型

### 类型 1: 术语注释

**用途**：解释图中专业术语或缩写

**何时使用**：
- 术语首次出现
- 缩写可能有歧义
- 非目标读者熟悉的领域专有名词

**示例**：
```plantuml
component "UserOperation" as UO
note right of UO
  <b>术语</b>
  EIP-4337 定义的用户操作原子
  包含 sender, nonce, callData 等字段
end note
```

### 类型 2: 简化标注

**用途**：说明图中省略了什么内容

**何时使用**：
- 省略错误处理路径
- 省略边界情况
- 省略次要组件或关系

**示例**：
```plantuml
note top of diagram
  <b>简化说明</b>
  本图仅展示成功路径
  错误处理详见错误流程图
end note
```

### 类型 3: 边界注释

**用途**：说明组件或流程的边界范围

**何时使用**：
- 组件职责需要明确边界
- 流程有明确的起止条件

**示例**：
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

### 类型 4: 假设注释

**用途**：说明分析所基于的假设条件

**何时使用**：
- 分析依赖特定前提
- 结论有适用条件

**示例**：
```plantuml
note top of diagram
  <b>假设条件</b>
  - Bundler 是可信的
  - Gas 价格稳定
  - 网络延迟 < 100ms
end note
```

### 类型 5: 流程注释

**用途**：说明流程步骤的目的或结果

**何时使用**：
- 流程步骤需要额外说明
- 箭头标签不足以表达完整含义

**示例**：
```plantuml
A -> B : validate
note on link
  <b>验证流程</b>
  1. 验证签名
  2. 验证 paymaster
  3. 检查 gas 限制
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

### 颜色语义

| 颜色 | 语义 | 使用场景 |
|------|------|----------|
| `#LightYellow` | 一般信息 | 默认注释 |
| `#LightCoral` | 警告/风险 | 必须注意的内容 |
| `#LightGreen` | 推荐/最佳实践 | 推荐做法 |
| `#LightBlue` | 参考/链接 | 外部引用 |

### 密度控制

**规则**：注释面积不应超过图面积的 30%

**超限处理**：
1. 移到外部文档
2. 创建单独的注释图
3. 简化注释内容

## 何时无需注释

**禁止注释的情况**：
- 图中结构已清晰表达
- 添加注释会遮挡关键关系
- 注释内容重复图中已明确的信息

## 检查清单

- [ ] 注释是否必要
- [ ] 注释位置是否合适
- [ ] 注释内容是否准确
- [ ] 注释密度是否过高
- [ ] 格式是否一致

## 相关文件

- `harness/rules/diagrams/diagram-policy.md`：图表总政策
- `harness/rules/diagrams/relationship-rules.md`：关系语义规范
- `harness/rules/diagrams/simplification-policy.md`：简化政策
- `harness/rules/diagrams/architecture-quality-rules.md`：架构图质量规约
