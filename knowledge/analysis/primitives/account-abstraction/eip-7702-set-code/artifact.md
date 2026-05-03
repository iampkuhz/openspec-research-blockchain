# EIP-7702: Set Code Transaction

> **研究对象**: EIP-7702 (Set Code for EOAs)
> **对象类型**: primitive
> **深度**: comprehensive
> **相关 domains**: account-abstraction, ethereum-protocol

## Metadata

- **Author**: Vitalik Buterin, Sam Wilson, Ansgar Dietrichs, lightclient
- **Created**: 2024-05-07
- **Status**: Activated in Pectra upgrade (2025-05-07)
- **Transaction Type**: 0x04 (EIP-2718)
- **Requires**: EIP-2, EIP-161, EIP-1052, EIP-2718, EIP-2929, EIP-2930, EIP-3541, EIP-3607, EIP-4844

## Summary

EIP-7702 引入了一种新的 EIP-2718 交易类型（类型 `0x04`），允许外部所有账户（EOA）通过签署授权列表临时设置自己账户的 code，从而获得智能合约账户的能力——批量操作、Gas 赞助和权限降级。与 ERC-4337 不同，它是**协议层**方案，不依赖额外的 Bundler/EntryPoint 基础设施。最关键机制是**委托标记**（`0xef0100 || address`），它使 EVM 将所有代码执行操作重定向到目标合约。最大安全风险在于：签署授权即赋予代码对账户的完全控制权，且委托**持久化**不回滚。对钱包而言不能再假设 `tx.origin` 是 EOA；对 dApp 应通过 ERC-5792/6900 标准接口集成；用户获得智能合约钱包体验但需审慎审查委托目标。

---

## Body

> 以下章节为 EIP-7702 的完整技术正文。

---

## 1. 定义与定位

### 1.1 是什么

EIP-7702（Set Code for EOAs）是以太坊 Pectra 升级的核心提案。它引入类型 `0x04` 的 Set Code Transaction，允许 EOA 通过附加**授权列表（authorization_list）** 来设置自己账户的 code。设置后，该 EOA 在执行层面表现为委托的目标合约。[S1]

### 1.2 解决什么问题

- **批量操作（Batching）**：同一用户的多个操作在单笔原子交易中完成（如 ERC-20 授权 + 消费）[S1]
- **Gas 赞助（Sponsorship）**：第三方账户代为支付交易费用 [S1]
- **权限降级（Privilege De-escalation）**：用户可签署子密钥并赋予特定受限权限 [S1]

### 1.3 核心定位

EIP-7702 是**协议层**账户抽象方案，与 ERC-4337（应用层/alt mempool）形成互补关系。它不改变 EOA 的基本模型，而是让 EOA 能够"伪装"成智能合约账户。[S1][S3]

### 1.4 不在范围内

- ERC-4337 的完整机制（仅做定位对比）
- EIP-3074 的完整技术细节（仅做对比）
- 具体钱包实现的产品层面细节

---

## 2. 核心机制

### 2.1 授权模型

核心是**授权列表（authorization_list）**。每个授权元组包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `chain_id` | uint256 | 链 ID，0 表示所有链 |
| `address` | 20 bytes | 委托目标合约地址 |
| `nonce` | uint64 | 账户 nonce，防重放 |
| `y_parity` | uint8 | 签名 y 奇偶性 |
| `r` | uint256 | 签名 r 值 |
| `s` | uint256 | 签名 s 值 |

签名消息：`keccak256(MAGIC || rlp([chain_id, address, nonce]))`，其中 `MAGIC = 0x05`。[S1]

### 2.2 执行流程

Set Code Transaction 分两阶段执行：

**阶段一：授权处理**（在交易执行前，发送者 nonce 递增后）

对每个授权元组依次处理：
1. 验证 chain_id 为 0 或当前链
2. 验证 nonce < 2^64
3. 通过 `ecrecover` 恢复 authority 地址
4. 验证 authority 的 code 为空或已被委托
5. 验证 authority 的 nonce 匹配
6. 设置 authority 的 code 为 `0xef0100 || address`
7. authority 的 nonce +1

**如果任何步骤失败**，停止处理该元组并继续下一个。**交易执行失败不会回滚已处理的委托**。同一 authority 多个元组时，以最后一个有效的为准。[S1]

**阶段二：交易执行**

- 如果交易 destination 有委托标记，加载目标合约代码并在 EOA 上下文中执行
- `address(this)` 在委托上下文中等于 **EOA 地址**，不是被委托的合约地址

### 2.3 执行流程图

```plantuml
@startuml
see diagrams/eip-7702-execution-flow/diagram.puml
@enduml
```

> 完整时序图见：`diagrams/eip-7702-execution-flow/diagram.puml`
> 该图展示从用户签署授权 → 构建 Set Code Transaction → EVM 处理授权 → 设置委托标记 → 委托执行的完整五阶段流程。

### 2.4 机制总览表

| 机制点 | 作用 | 关键字段/行为 | 风险 |
|--------|------|-------------|------|
| Set Code Transaction 0x04 | 携带授权列表的新交易类型 | `authorization_list` 不能为空 | 不同类型交易的 mempool 传播行为差异 |
| authorization_list | 一组授权元组，每个定义委托目标 | `[chain_id, address, nonce, y_parity, r, s]` | 空列表导致交易无效 |
| 签名消息 | 验证授权确实来自 authority | `keccak(0x05 \|\| rlp(...))` | 与 EIP-712/EIP-191 不兼容 [S5] |
| delegation indicator | 标记账户已被委托 | `0xef0100 \|\| address`（23 字节） | 0xef 是 EIP-3541 禁止的 opcode |
| 持久化委托 | 交易结束后 code 保持 | 需新的 Set Code Tx 才能清除 | 用户可能忘记自己已被委托 |
| 清除委托 | 恢复为纯 EOA | address 设为 `0x0`，重置 code hash | 特殊处理增加 EVM 复杂度 |
| 委托不跟随 | EXT* 操作不跟随指针 | EXTCODESIZE 返回 23 | 保护依赖 codehash 的合约逻辑 |

---

## 3. 交易格式

### 3.1 数据结构

交易类型为 `0x04`，payload 为以下字段的 RLP 序列化：

```
rlp([
  chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas,
  gas_limit, destination, value, data, access_list,
  authorization_list,
  signature_y_parity, signature_r, signature_s
])
```

签名 over `keccak256(0x04 || TransactionPayload)`。[S1]

### 3.2 Gas 成本

| 项目 | 成本 |
|------|------|
| 基础费用 | 21000 gas（继承 EIP-2930） |
| Calldata | 16 gas/非零字节 + 4 gas/零字节 |
| 每授权 | PER_EMPTY_ACCOUNT_COST = 25000 gas |
| 冷账户首次读取 | 2600 gas |
| 暖账户读取 | 100 gas |

发送者支付所有授权费用，无论是否有效或重复。[S1]

### 3.3 有效性约束

- `authorization_list` 不能为空
- `destination` 不能为空
- 每个元组的字段必须在指定范围内 [S1]

---

## 4. 安全模型

安全风险按以下四层分层说明：

### 4.1 Protocol-Level 风险

| 风险 | 为什么出现 | 如何缓解 | 证据 |
|------|-----------|---------|------|
| 余额不变量破坏：任何调用都可能导致余额减少 | 委托后合约代码可在 EOA 上下文中执行 | 合约需重新审视依赖此不变量的逻辑 | [S1] |
| Nonce 单调性破坏：执行中 nonce 可增加 | 委托后可调用 create 操作 | 客户端需调整 pending 交易处理 | [S1] |
| tx.origin 不变量破坏：`msg.sender == tx.origin` 可在非顶层帧为 true | 委托后可在单笔交易中发起多次调用 | 破坏依赖此检查的重入保护 | [S1][S2] |

### 4.2 Wallet-Level 风险

| 风险 | 为什么出现 | 如何缓解 | 证据 |
|------|-----------|---------|------|
| 钓鱼：用户不知情的情况下签署恶意委托 | 授权签名不兼容 EIP-712/EIP-191，需要钱包专门支持 | 钱包显著展示目标合约地址，白名单已知合约 | [S2][S5] |
| 初始化抢先：攻击者截取委托签名后抢先初始化 | 委托时不运行 initcode | 用 `initWithSig` 或通过 4337 EntryPoint 调用 | [S2] |
| 存储碰撞：切换委托后旧 storage 残留 | 委托代码不清除现有 storage | 使用 ERC-7201 存储布局隔离 | [S1][S2] |

### 4.3 DApp-Integration 风险

| 风险 | 为什么出现 | 如何缓解 | 证据 |
|------|-----------|---------|------|
| 直接请求 7702 授权签名 | 没有标准化的 dApp → 授权直接请求方法 | dApp 应通过 ERC-5792/6900 标准接口 | [S2] |
| 重入保护失效 | `tx.origin == msg.sender` 不再可靠 | 使用 OpenZeppelin ReentrancyGuard 或 transient storage | [S2] |
| 供应商锁定 | 依赖特定 relayer/bundler 服务 | 使用 4337 公共 mempool 方案 | [S2] |

### 4.4 User-Level 风险

| 风险 | 为什么出现 | 如何缓解 | 证据 |
|------|-----------|---------|------|
| 完全控制权授予：恶意合约可清空账户 | 签署授权即赋予代码完全控制 | 只签名已知、审计过的合约 | [S4] |
| 跨链风险：chain_id=0 应用于所有链 | 同一委托在所有 EVM 链生效 | 优先使用特定 chain_id；只委托到 CREATE2 部署的合约 | [S2] |
| 签名盲签风险 | 用户不理解授权含义 | 钱包应显著展示目标合约地址 | [S4][S5] |

### 4.5 交易传播挑战

委托后，其他账户可在交易中调用该 EOA，导致无法静态判断余额是否被清空。**建议**：客户端不接受超过一笔 pending 交易来自同一委托 EOA。[S1]

---

## 5. 与现有方案对比

### 5.1 EIP-7702 vs EIP-4337 vs 普通 EOA vs 智能合约账户

| 维度 | 普通 EOA | EIP-7702 | ERC-4337 (智能合约账户) | 原生智能合约账户 |
|------|---------|----------|----------------------|----------------|
| 账户形态 | 私钥控制，无 code | EOA + 委托 code（0xef0100 \|\| address） | 独立合约账户，有自己的 code | 独立合约账户 |
| 是否改变 EOA 行为 | — | 是，临时伪装为合约 | 否，EOA 仍为 EOA | — |
| 是否需要 EntryPoint | 否 | 否 | 是 | — |
| 是否支持 sponsored tx | 否 | 是（通过委托合约） | 是（通过 Paymaster） | 是（合约逻辑） |
| 是否支持 batch | 否 | 是（通过委托合约） | 是（通过 Bundler） | 是（合约逻辑） |
| 主要风险 | 私钥泄露 | 委托到恶意合约 | EntryPoint 依赖、Bundler 审查 | 合约漏洞 |
| 适用场景 | 简单转账 | 快速 AA 能力，无需额外基础设施 | 完整 AA 生态，大规模采用 | 复杂钱包逻辑 |
| 已有采用 | 基础 | Pectra 后激活（2025-05-07） | 2600万+ 账户，1.7亿+ UserOps | 有限 |

### 5.2 方案选择矩阵

| 用户需求 | 推荐方案 |
|----------|---------|
| 不改变现有 EOA，立即使用 | ERC-4337 |
| 协议层原生支持，简单批量操作 | EIP-7702 |
| 完整智能合约钱包功能 | EIP-7702 委托到 4337 兼容合约 |
| 不依赖额外基础设施 | EIP-7702 |

---

## 6. 典型使用模式

### 6.1 批量操作（Batching）

用户在一个交易中完成 ERC-20 授权 + 消费：

```
sendTransaction({
  to: user.address,            // 目标是自己
  authorizationList: [auth],   // 附加授权
  data: encodeBatch(calls),    // 批量调用数据
})
```

关键点：`to` 是用户自己的 EOA 地址。执行时 `address(this)` 在委托上下文中等于 EOA 地址。[S4]

### 6.2 Gas 赞助（Sponsorship）

1. 用户离线签署批量调用（含 nonce 的 digest）
2. 赞助者包装签名，发送交易到用户地址
3. 合约验证用户签名后执行

**Nonce 设置的微妙细节**：
- 中继者广播：`authorization.nonce = 当前账户 nonce`
- 账户自身广播：`authorization.nonce = 交易 nonce + 1`（因 Ethereum 在执行授权前递增 nonce）[S4]

### 6.3 Session Key（权限降级）

委托到实现权限控制的合约，赋予子密钥受限权限（每日上限、特定代币、特定 dApp、时间窗口）。[S1]

### 6.4 开发者最佳实践

- dApp **不应**直接请求 7702 授权签名，应通过 ERC-5792 `wallet_sendCalls` 和 ERC-6900 接口 [S2]
- 推荐使用**代理模式**：委托到代理合约而非直接实现，便于升级 [S2]
- 与 4337 兼容：委托合约应支持 EntryPoint 0.8+ [S2]

---

## 7. 生态状态

### 7.1 激活

EIP-7702 于 **2025 年 5 月 7 日**作为 Pectra 升级的一部分在以太坊主网激活。[S3]

### 7.2 已知实现（已审计）

| 实现 | 提供方 | 特点 |
|------|--------|------|
| calibur | Uniswap | DEX 集成 |
| modular-account | Alchemy | ERC-6900 模块化 |
| ambire-common | AmbireTech | 轻量级（~200 行） |
| delegation-framework | MetaMask | 钱包原生支持 |
| Simple7702Account | EF AA team | 参考实现 |

### 7.3 工具链

Viem.js（自动处理 nonce 调整）、MetaMask Delegation Toolkit、SafeEIP7702Proxy。硬件钱包行业共识是白名单已知委托合约。[S4][S5]

---

## 8. 不确定性

| 不确定点 | 说明 |
|----------|------|
| 钱包采用进度 | 不同钱包对 7702 授权签名的 UI 支持程度不一 |
| 与 4337 长期关系 | 互补还是替代，取决于 4337 协议层集成进展 |
| 硬件钱包实现 | 各厂商对 7702 的安全策略尚未统一 |

---

## Evidence

本研究的核心结论基于以下来源：

| 来源 | 标题 | 类型 | 可信度 |
|------|------|------|--------|
| [S1] | EIP-7702: Set Code for EOAs | L1 spec | 最高（正式规范） |
| [S2] | Pectra 7702 Guidelines | L1 spec | 最高（官方文档） |
| [S3] | Account Abstraction (ethereum.org) | L1 spec | 最高（官方文档） |
| [S4] | EIP-7702: Delegated Execution and Sponsored Transactions | L2 article | 高（技术分析+代码） |
| [S5] | Safe EIP-7702 Overview | L2 implementation | 高（钱包实现文档） |
| [S6] | ERC-4337: Account Abstraction Using Alt Mempool | L1 spec | 最高（正式规范） |

来源元信息见：`sources/source-pack.md`。
精读笔记见：`notes/eip-7702-spec.md`、`notes/pectra-7702-practices.md`、`notes/usage-patterns.md`。
可验证主张见：`claims/transaction-type-0x04.md`、`claims/delegation-marker.md`、`claims/broken-invariants.md`。

## Traceability

### 支撑链

```
request.md → plan.md → sources/source-pack.md → sources/evidence-map.md
  → notes/*.md → claims/*.md → draft.md → review.md → publish.md
  → knowledge/analysis/primitives/account-abstraction/eip-7702-set-code/artifact.md
```

### Draft 章节 → 来源映射

| Draft 章节 | 主要来源 | 支撑 Notes/Claims |
|-----------|---------|------------------|
| 1. 定义与定位 | S1, S3 | — |
| 2. 核心机制 | S1, S2 | notes/eip-7702-spec.md |
| 3. 交易格式 | S1 | claims/transaction-type-0x04.md |
| 4. 安全模型 | S1, S2, S4, S5 | claims/broken-invariants.md |
| 5. 对比分析 | S1, S2, S3, S6 | — |
| 6. 使用模式 | S4, S2 | notes/usage-patterns.md |
| 7. 生态状态 | S2, S3, S5 | notes/pectra-7702-practices.md |

完整证据映射见：`sources/evidence-map.md`。
