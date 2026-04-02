# 机制分析写作规则

## 目的

规范 mechanism atom 的写作结构和内容要求。

## Mechanism Atom 结构

```markdown
# 概述

[机制的核心作用和目标]

## 设计动机

[为什么需要这个机制，解决了什么问题]

## 核心流程

### 流程概述

[高层流程描述]

### 详细步骤

[逐步详解，每步包含]
- 触发条件
- 参与方
- 状态变化
- 关键计算

## 关键设计决策

[为什么这样设计，而不是其他方案]

## 边界情况

[特殊情况的处理]

## 复杂度分析

[时间/空间复杂度，Gas 成本等]
```

## 写作要求

### 必须解释为什么

**禁止**只描述"是什么"。

**必须**解释：
- 为什么这样设计
- 替代方案是什么
- 为什么排除替代方案

### 必须区分层级

| 层级 | 内容 |
|------|------|
| Protocol | 规范定义的行为 |
| Implementation | 参考实现细节 |
| Ecosystem | 生态扩展 |

### 必须有边界

**禁止**无限扩展机制范围。

**必须**：
- 明确机制的适用范围
- 说明不适用的场景
- 列出假设条件

## 示例：Gas 计算机制

```markdown
# Gas 计算机制

## 概述

EIP-4337 的 Gas 计算机制决定了 UserOperation 的费用计算方式，
确保 Bundler 能够获得合理补偿，同时防止滥用。

## 设计动机

**问题**：UserOperation 不是 L1 交易，如何定价？

**约束**：
- 必须覆盖 Bundler 成本
- 必须防止 DoS 攻击
- 必须支持 Paymaster 代付

**设计目标**：
- 费用可预测
- 验证和执行分离计费
- 支持批量打包

## 核心公式

```
totalGasUsed = preVerificationGas + verificationGasUsed + callGasUsed
totalFee = totalGasUsed * effectiveGasPrice + priorityFee
```

## 详细步骤

### 1. Pre-Verification Gas

**用途**：补偿 Bundler 的链下成本

**计算**：
```
preVerificationGas = fixed_cost + calldata_cost
calldata_cost = calldata_size * gas_per_byte
```

**为什么**：Bundler 需要将 UserOp 打包成交易，这部分成本与
UserOp 大小成正比，与执行无关。

### 2. Verification Gas

**用途**：验证 UserOp 和 Paymaster

**触发**：每次调用 validateUserOp

**限制**：verificationGasLimit 防止无限循环

**为什么**：验证逻辑是用户定义的，必须限制 Gas 防止 DoS。

### 3. Call Gas

**用途**：执行用户操作

**限制**：callGasLimit

## 关键设计决策

### 为什么分离验证和执行 Gas？

**替代方案**：统一 Gas 池

**选择分离的原因**：
1. 验证失败不应影响执行 Gas
2. Paymaster 只验证，不参与执行
3. 更精确的费用计算

### 为什么需要 preVerificationGas？

**问题**：链下成本无法在链上精确计算

**解决方案**：预估 + 多退少补

## 边界情况

### Paymaster 超时

如果 validatePaymaster 超时：
- 消耗 verificationGas
- UserOp 被拒绝
- Bundler 仍然获得补偿

### 嵌套调用

UserOp 执行中调用其他合约：
- 计入 callGas
- 受 callGasLimit 限制

## 复杂度分析

| 阶段 | 时间复杂度 | Gas 范围 |
|------|------------|----------|
| preVerification | O(1) | ~21000 |
| verification | O(n) | 验证逻辑复杂度 |
| execution | O(m) | 执行逻辑复杂度 |
```

## 质量检查清单

- [ ] 是否解释设计动机
- [ ] 是否列出替代方案
- [ ] 是否区分层级
- [ ] 是否有边界说明
- [ ] 是否覆盖边界情况
- [ ] 是否有复杂度分析
