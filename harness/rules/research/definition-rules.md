# 定义原子写作规则

## 目的

规范 definition atom 的写作结构和内容要求。

## Definition Atom 结构

```markdown
# 定义

[1-2 句简洁定义，包含核心本质]

## 形式化描述

[可选：伪代码、类型签名、接口定义]

## 关键术语

[列出 3-7 个核心术语，每个术语包含]
- 术语名
- 简洁定义
- 来源引用

## 边界条件

### 包含的内容
- ...

### 不包含的内容
- ...

## 前提条件

[理解此定义需要的前置知识]

## 相关概念

[与哪些概念相关，如何区分]
```

## 写作要求

### 定义必须

1. **简洁**：1-2 句表达核心
2. **准确**：使用 L1/L2 证据
3. **有边界**：明确 excludes
4. **可引用**：其他 `atom` 可引用此定义

### 术语区必须

1. **使用列表**：不是卡片式结构
2. **标注来源**：每个术语绑定 `source`
3. **区分层级**：protocol vs implementation

### 边界必须

1. **写清楚不是什么**：排除常见误解
2. **说明适用范围**：何时使用此定义

## 示例

```markdown
# EIP-4337 定义

EIP-4337 是一个实现账户抽象的 ERC 标准，通过伪交易对象 UserOperation 和
EntryPoint 合约，允许用户在不修改协议层的情况下实现智能合约账户。

## 形式化描述

```
UserOperation {
  sender: Address
  nonce: uint256
  initCode: bytes
  callData: bytes
  callGasLimit: uint256
  verificationGasLimit: uint256
  preVerificationGas: uint256
  maxFeePerGas: uint256
  maxPriorityFeePerGas: uint256
  paymasterAndData: bytes
  signature: bytes
}
```

## 关键术语

**UserOperation**
: EIP-4337 定义的用户操作原子，包含执行用户意图所需的全部信息。
  来源：[EIP-4337](https://eips.ethereum.org/EIPS/eip-4337#core-components)

**EntryPoint**
: 单例合约，处理 UserOperation 的验证和执行。
  来源：[EIP-4337](https://eips.ethereum.org/EIPS/eip-4337#entry-point-stake)

**Bundler**
: 链下角色，负责打包 UserOperations 并提交到 EntryPoint。
  来源：[EIP-4337](https://eips.ethereum.org/EIPS/eip-4337#first-time-account-creation)

## 边界条件

### 包含的内容
- UserOperation 数据结构定义
- Bundler/EntryPoint/Paymaster 角色定义
- 验证和执行流程
- Gas 计算模型

### 不包含的内容
- 具体钱包实现细节
- Bundler 服务的具体部署方式
- 与 EIP-7702 的对比（见 synthesis/bft-comparison）

## 前提条件
- 理解以太坊交易模型
- 理解智能合约账户概念
- 理解 Gas 机制

## 相关概念

**账户抽象（Account Abstraction）**
: 更广泛的概念，EIP-4337 是其一种实现方式。

**EIP-7702**
: 另一种账户抽象方案，通过在交易中设置代码实现。
  区分：EIP-4337 使用伪交易，EIP-7702 修改交易类型。
```

## 质量检查清单

- [ ] 定义是否简洁准确
- [ ] 是否覆盖所有关键术语
- [ ] 边界是否清晰
- [ ] 前提条件是否列出
- [ ] 相关概念是否区分
- [ ] 所有术语是否有来源
