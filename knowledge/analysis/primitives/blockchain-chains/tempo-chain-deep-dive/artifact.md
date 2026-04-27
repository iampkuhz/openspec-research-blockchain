# Tempo 链特性增强与链层优化深度分析

> **对象类型**：primitive
> **研究路径**：deep-dive
> **相关 domains**：blockchain-chains, payments, stablecoins

---

## 摘要

Tempo 是由 Stripe 和 Paradigm 联合孵化（2025 年 9 月公布）的 Layer 1 区块链，定位为"支付优化的通用链"（general-purpose blockchain optimized for payments）。与以太坊等通用平台链不同，Tempo 在共识、执行层、Token 标准、交易类型、DEX、隐私扩展等七个维度进行了系统性协议级增强，形成了完整的"稳定链（Stablechain）"技术体系。

核心设计哲学：**不引入原生代币**，交易费用直接以稳定币（TIP-20）支付；通过协议级创新实现亚秒确定性终局、支付车道隔离、原生智能账户和链上 DEX，而非依赖应用层合约或二层方案。

---

## 1. 共识与亚秒出块层

### 1.1 Simplex BFT 共识

Tempo 使用 **Simplex BFT** 共识协议（由 Commonware 实现），这是面向快速终局优化的拜占庭容错协议。

**核心指标**：

| 指标 | 值 | 说明 |
|------|-----|------|
| 正常出块间隔 | ~600ms | 500ms builder loop + 网络延迟与验证 |
| 终局类型 | 确定性终局 | 非概率性，无 reorg 风险 |
| 容错阈值 | \< 1/3 验证者拜占庭 | 安全性与以太坊 BFT 一致 |
| 存活性要求 | ≥ 2/3 验证者在线 | 低于阈值时网络暂停而非产出冲突块 |

### 1.2 出块机制

```
[Builder Loop 500ms] → [VRF Leader Selection] → [Block Validation] → [Finalization ~600ms total]
```

- **Builder Loop**：固定 500ms 周期的出块循环，确保确定的出块节奏
- **VRF 随机领导者选举**：使用 Verifiable Random Function 随机选择 Proposer，提供 DoS 保护和 MEV 抗性
- **分布式验证者集**：非单 Sequencer 模式，多个验证者共享出块责任，防止单点审查

### 1.3 确定性终局

与以太坊的"概率终局 + reorg 风险"不同，Tempo 一旦标记块为 finalized，交易即不可逆：

- 无需等待多个确认
- 无 reorg 风险（canonical chain 不会改变）
- 为支付场景提供与传统金融系统一致的结算确定性
- 通过 `eth_getBlockByNumber` 的 `finalized` tag 查询

### 1.4 降级行为

Simplex 共识在网络恶化时优先保障安全性（Safety over Liveness）：

| 条件 | 行为 |
|------|------|
| 网络分区 | 出块时间增加，但终局保证不变 |
| 验证者离线（阈值内） | 网络继续运行 |
| >1/3 验证者离线 | 网络暂停，阈值恢复后自动恢复 |

### 1.5 验证者集状态

- 当前测试网：4 个验证者（许可制）
- 主网：机构级验证者（初始许可制）
- 路线图：包含向无许可验证的演进路径

---

## 2. 执行层与 Blockspace 优化

### 2.1 基于 Reth SDK 的执行层

Tempo 的执行层构建在 **Reth SDK** 之上（Paradigm 开发的高性能 EVM 客户端），并在以下方面进行了定制：

- 扩展区块 Header 格式
- 引入支付专用车道机制
- 增加子秒级时间戳支持
- 添加多个系统预编译合约

### 2.2 Blockspace Header 扩展

Tempo 在以太坊 Header 基础上扩展了三个标量字段：

```rust
pub struct Header {
    pub general_gas_limit: u64,       // 非支付交易的 gas 上限
    pub shared_gas_limit: u64,        // 共享 gas 预算
    pub timestamp_millis_part: u64,   // 子秒级时间戳（毫秒部分）
    pub inner: Header,                // 标准以太坊 Header
}
```

**关键字段说明**：

- `general_gas_limit`：非支付交易的区块空间上限，确保 DeFi/复杂合约不会挤占支付容量
- `shared_gas_limit`：共享 gas 预算，管理支付与非支付交易的总容量分配
- `timestamp_millis_part`：子秒级时间戳（完整时间戳 = `inner.timestamp * 1000 + timestamp_millis_part`），支撑精确支付调度与定时交易

### 2.3 支付车道（Payment Lanes）

支付车道是 Tempo 核心的区块空间隔离机制：

**交易分类规则**（仅基于交易数据，不查询链上状态）：

```
is_payment(tx) = true 当且仅当:
  1. tx.to 地址以 TIP-20 前缀 0x20c0000000000000000000000000 开头，或
  2. TempoTransaction 中所有 calls 的目标地址都以该前缀开头
```

**双重 gas 约束**：

```
约束 1: general_gas_limit >= Σ gas_consumed(tx[i])  // 非支付交易在 proposer lane 的总 gas
约束 2: gas_limit >= Σ gas_consumed(all txs)         // 标准以太坊总 gas 约束
```

**核心价值**：即使链上有热门 DeFi 应用消耗大量区块空间，工资发放、客户付款等支付交易始终有专用通道，保证可预测的费用和执行时间。

### 2.4 系统交易排序

Tempo 区块体内的交易按以下顺序排列：

```
1. Start-of-block 系统交易（必须是 Rewards Registry 调用）
2. Proposer lane 交易（受 general_gas_limit 约束）
3. 共享 gas 预算内的剩余交易
4. Protocol 定义的 end-of-block 系统交易（按需）
```

---

## 3. 无原生代币与 TIP-20 Token 标准

### 3.1 无原生代币设计

Tempo **没有原生代币**（如 ETH）。交易费用（gas fee + priority fee）直接以 USD 计价的 TIP-20 稳定币支付。

- **固定 base fee**（非 EIP-1559 动态 base fee），确保 TIP-20 转账费用 \< $0.001
- 所有费用归打包该区块的验证者所有

### 3.2 Fee AMM 机制

Fee AMM 自动处理用户选择的费用 token 与验证者偏好 token 之间的转换：

```
用户选择 USDG 支付费用 → Fee AMM 自动转换为验证者偏好 token → 验证者收到其偏好 token
```

用户无需持有特定 gas token，消除"先买 ETH 再使用链"的引导成本。

### 3.3 TIP-20 Token 标准

TIP-20 是 Tempo 原生的 Token 标准，相比 ERC-20 增加了以下能力：

| 特性 | 说明 |
|------|------|
| **多 Token 费用支付** | 任何 USD 计价的 TIP-20 均可支付手续费 |
| **角色访问控制 (RBAC)** | ISSUER_ROLE（铸造/销毁）、PAUSE_ROLE/UNPAUSE_ROLE（暂停/恢复）、BURN_BLOCKED_ROLE（合规销毁） |
| **TIP-403 合规策略** | 白名单/黑名单政策，支持跨 token 共享策略 |
| **奖励分发** | 可选的 Token 持有者奖励分配系统 |
| **货币声明** | 声明 ISO 4217 货币代码（USD、EUR 等），用于 DEX 路由 |
| **32-byte Transfer Memo** | 转账附言（发票 ID、交易备注） |
| **供应上限** | 可设置最大供应量 |
| **Dedicated Blockspace** | 支付型 TIP-20 交易享有专用区块空间 |

### 3.4 Token 创建

所有 TIP-20 Token 通过与 **TIP-20 Factory 合约**交互（`createToken` 函数）创建，而非自行部署合约。这确保了所有 token 遵循统一标准，支持协议级功能（费用支付、支付车道、DEX 路由）。

---

## 4. 预置 Stablecoin DEX

### 4.1 设计概述

Tempo 内置 **链上 DEX**，位于预编译合约地址 `0xdec0000000000000000000000000000000000000`，专为同币种稳定币兑换设计（如 USDC ↔ USDT）。

### 4.2 订单簿模型

与 Uniswap 的 AMM（常量乘积公式）不同，Tempo DEX 使用 **订单簿 + 价格-时间优先匹配**：

- 订单按价格层级（price tick）分列队列
- 匹配引擎按价格优先、时间优先原则执行
- 支持限价单、市价单和 Flip Orders

### 4.3 订单类型

| 订单类型 | 行为 |
|----------|------|
| **Limit Order** | 在指定价格层级挂单，等待匹配或取消 |
| **Flip Order** | 完全成交后自动反向创建新订单，充当永续流动性池 |
| **Swap Order** | 立即对最优价格执行（市价单） |

### 4.4 pathUSD 路由

pathUSD 是 Tempo DEX 中的特殊稳定币，作为跨币种路由的中继：

- 所有 TIP-20 Token 声明 quote token（报价货币）
- USD 计价的 Token 通过 pathUSD 路由实现最优流动性路径
- 仅 USD 计价的 TIP-20 可用作 DEX 的 quote token

### 4.5 与协议其他组件的关系

- **Fee AMM** 可能使用 DEX 的流动性池进行费用 token 转换
- **支付车道** 中支付交易可通过 DEX 路由实现最优跨稳定币结算
- **TIP-20 货币声明** 决定了 Token 在 DEX 中的交易对

---

## 5. Tempo Transactions（协议层智能账户）

### 5.1 概述

Tempo Transactions 是 **EIP-2718** 新交易类型（类型字节 `0x76`），仅在 Tempo 链上可用。与 EIP-4337 的合约层 Account Abstraction 不同，这些能力是**协议原生**的。

### 5.2 交易结构

```rust
pub struct TempoTransaction {
    // 标准 EIP-1559 字段
    chain_id, max_priority_fee_per_gas, max_fee_per_gas, gas_limit,
    calls: Vec<Call>,        // 批量调用
    access_list,

    // 2D Nonce 字段
    nonce_key: U256,         // 0 = 协议 nonce, >0 = 用户 nonce
    nonce: u64,

    // 可选功能
    fee_token: Option<Address>,              // 费用 token
    fee_payer_signature: Option<Signature>,  // 费用赞助
    valid_before: Option<u64>,               // 交易过期时间
    valid_after: Option<u64>,                // 最早执行时间
    key_authorization: Option<SignedKeyAuthorization>, // Access Key
    aa_authorization_list: Vec<TempoSignedAuthorization>, // EIP-7702 AA 授权
}
```

### 5.3 核心能力矩阵

#### 5.3.1 Passkeys / P256 / WebAuthn 原生签名

Tempo 协议原生支持四种签名类型：

| 签名类型 | 长度 | 说明 |
|----------|------|------|
| **secp256k1** | 65 bytes | 标准 EOA 签名，向后兼容 |
| **P256** | 130 bytes | 椭圆曲线签名，支持 Passkeys |
| **WebAuthn** | 可变（最大 2KB） | WebAuthn 认证器签名 |
| **Keychain** | 可变 | Access Key 代理签名 |

**地址派生**：P256/WebAuthn 地址使用 `address(keccak256(pubKeyX || pubKeyY)[:20])`，与 secp256k1 不同。

**WebAuthn 验证**：协议实现 authenticatorData + clientDataJSON 解析，验证 UP 标志、challenge 匹配和 P256 签名。跳过 origin/RP ID 验证（区块链无中心 RP）。

#### 5.3.2 批量调用（Batch Calls）

- `calls: Vec<Call>` 字段支持在单交易中批量执行多个调用
- 原子性：要么全部成功，要么全部回滚
- 减少多交易场景下的 overhead

#### 5.3.3 费用赞助（Fee Sponsorship）

- 第三方（fee payer）可为交易发送者支付手续费
- **双签名域分离**：发送者用 `0x76` 域签名，费用赞助者用 `0x78` 魔术字节签名
- 防止签名重用攻击
- 费用赞助者只能使用 secp256k1 签名（当前）

#### 5.3.4 2D Nonces（并发交易）

Tempo 的 2D 非ce 系统允许同一账户并行提交多笔交易：

| Nonce Key | 说明 | Gas 额外成本 |
|-----------|------|-------------|
| **0（协议 nonce）** | 顺序 nonce，标准行为 | 0 |
| **1-N（用户 nonce）** | 独立 nonce 序列，支持并行 | 已有 key：5,000 gas；新 key：22,100 gas |

**实现细节**：用户 nonce 存储在预编译合约 `0x4E4F4E4345...`（ASCII "NONCE"）中，因为 Reth 账户状态无法直接扩展。

#### 5.3.5 过期 Nonces（TIP-1009）

- 设置 `nonceKey = maxUint256` + `validBefore` 实现交易自动过期
- 使用循环缓冲区实现自动重放保护
- 无未使用 nonce 的永久状态膨胀

#### 5.3.6 定时交易（Scheduled Transactions）

- 通过 `validAfter` 和 `validBefore` 定义交易可被打包的时间窗口
- 支持提前签名、延迟执行
- 适用于自动化付款、定时结算场景

#### 5.3.7 Access Keys（委托签名）

Access Keys 允许主账户（Root Key）授权子密钥（Access Key）代理签名：

**核心特性**：
- Root Key 通过 `key_authorization` 字段授权 Access Key
- 支持过期时间、TIP-20 消费限额、调用范围限制（T3 新增）
- Access Key 不能调用可变预编译函数（授权、撤销、改限额）
- Access Key 签名的交易不能创建合约

**Gas 成本**：

| 配置 | Gas 成本 |
|------|----------|
| secp256k1，无限额 | 30,000 |
| secp256k1，1 个限额 | 52,000 |
| P256，无限额 | 35,000 |

**关键预编译地址**：Account Keychain 位于 `0xAAAAAAAA00000000000000000000000000000000`

#### 5.3.8 EIP-7702 AA 授权

`aa_authorization_list` 支持 EIP-7702 风格的账户委托，但扩展了签名类型（不仅 secp256k1，还支持 P256 和 WebAuthn）。

### 5.4 与 EIP-4337 的差异

| 维度 | EIP-4337 | Tempo Transactions |
|------|----------|-------------------|
| 实现层 | 合约层（UserOperation mempool + Bundler） | 协议层（EIP-2718 新交易类型） |
| 验证者支持 | 需要 Bundler 基础设施 | 验证者原生支持 |
| 签名类型 | 仅 EOA 签名（合约逻辑抽象） | 原生 secp256k1 + P256 + WebAuthn |
| Gas 赞助 | Paymaster 合约 | 协议级双签名 |
| 并发 | 依赖 mempool 排序 | 协议级 2D Nonces |
| 定时 | 需要外部 Automation | 协议级 validBefore/validAfter |

---

## 6. Tempo Zones（隐私扩展环境）

### 6.1 概述

Tempo Zones 是挂靠在 Tempo 主网上的 **私有执行环境**，提供：

- **隐私性**：余额、转账、交易历史对外部不可见（区块浏览器、索引器无法查询）
- **安全性**：有效性证明（Validity Proofs）保证状态转换正确性
- **互操作性**：通过主网共享流动性，支持跨 Zone 转账

### 6.2 信任模型

```
Zone 用户 → [存款到 Zone Portal 合约] → 资金锁定在主网 → Sequencer 处理 Zone 内交易 → 有效性证明提交主网验证
```

- Zone Sequencer 可以看到所有活动（隐私依赖于 Sequencer 诚信）
- Sequencer 不能盗取资金：有效性证明保证状态转换的正确性
- 与 Optimistic Rollup 不同，Zone 使用 **Validity Proofs**（无需等待挑战期）

### 6.3 隐私能力

| 隐私维度 | 实现方式 |
|----------|----------|
| 余额隐私 | 合约级访问控制，仅账户所有者可查询 |
| 授权隐私 |  allowance 对外部不可见 |
| 交易历史 | 区块浏览器和索引器不可见 |
| 对手方关系 | 外部无法查询地址间的交易关系 |
| RPC 隔离 | JSON-RPC 按账户作用域限制 |

### 6.4 跨 Zone 桥接

- 存款通过主网 Zone Portal 合约锁定
- 提取通过有效性证明确认
- **组合式提取回调**：一个 Zone 提取 → DEX 兑换 → 存入另一个 Zone，单次操作完成
- 支持加密存款（私有 on-ramp）

### 6.5 合规策略镜像

TIP-403 合规策略（白名单/黑名单）在 Zone 内被**可证明地镜像执行**，有效性证明承诺每笔交易都遵循发行者的合规规则。

---

## 7. 机器支付协议（MPP）

### 7.1 概述

MPP（Machine Payments Protocol）将支付嵌入到 HTTP 请求/响应流程中，使 AI Agent、API 服务和应用能够实现无人工干预的按需支付。

### 7.2 协议流程

```
Client                          Server
  |--- GET /resource ------------->|
  |<-- 402 + Challenge -------------|  (WWW-Authenticate: Payment)
  |    [Client 完成链上支付]          |
  |--- GET /resource + Credential -->|  (Authorization: Payment)
  |<-- 200 + Receipt ----------------|  (Payment-Receipt header)
```

### 7.3 支付模式

| 模式 | 延迟 | 适用场景 |
|------|------|----------|
| **Charge（一次性）** | ~500ms（链上确认） | 单次 API 调用、内容访问 |
| **Session（会话）** | 近零（链下凭证） | LLM API、按量计费服务 |

### 7.4 与 Tempo 特性的协同

- **~500ms 终局**：支持同步请求/响应流
- **Sub-cent 费用**：支持微支付和按次计费
- **费用赞助**：服务端可代付 gas，客户端只需稳定币
- **2D/过期 Nonces**：支付交易不阻塞其他账户活动
- **高吞吐**：支持支付通道的大规模链上结算

---

## 8. 技术架构总览

### 8.1 协议层栈

```
┌──────────────────────────────────────────────┐
│           应用层                              │
│  MPP Agent Payments │ Machine Payment Protocol│
├──────────────────────────────────────────────┤
│           扩展层                              │
│  Tempo Zones (Validity Proofs, Privacy)      │
├──────────────────────────────────────────────┤
│           交易/账户层                          │
│  Tempo Transactions (0x76)                   │
│  - Passkeys/P256/WebAuthn                    │
│  - Batch Calls │ Fee Sponsorship             │
│  - 2D Nonces │ Scheduled Txs                 │
│  - Access Keys │ EIP-7702 AA                 │
├──────────────────────────────────────────────┤
│           资产层                               │
│  TIP-20 Tokens │ TIP-403 Policy Registry     │
│  Pre-compiled Stablecoin DEX (0xdec...)      │
│  Fee AMM (多 token 费用转换)                   │
├──────────────────────────────────────────────┤
│           Blockspace 层                       │
│  Payment Lanes (隔离区块空间)                  │
│  Sub-second Timestamps (timestamp_millis)    │
│  System Transactions (Rewards Registry)       │
├──────────────────────────────────────────────┤
│           执行层                               │
│  Reth SDK (定制扩展)                          │
│  Nonce Precompile │ Account Keychain         │
│  TIP Fee Manager                             │
├──────────────────────────────────────────────┤
│           共识层                               │
│  Simplex BFT (Commonware)                    │
│  ~600ms 出块 │ 确定性终局 │ VRF Leader       │
└──────────────────────────────────────────────┘
```

### 8.2 关键预编译合约索引

| 地址 | 名称 | 用途 |
|------|------|------|
| `0xAAAAAAAA...0000` | Account Keychain | Access Key 管理（授权、撤销、限额） |
| `0x4E4F4E4345...` | Nonce Precompile | 2D Nonces 状态管理 |
| `0xdec000000000...` | Stablecoin DEX | 预置稳定币订单簿 |
| TIP-20 前缀 `0x20c000...` | Token 识别前缀 | 支付车道交易分类 |

---

## 9. 关键差异对比：Tempo vs 以太坊 L1

| 维度 | 以太坊 L1 | Tempo |
|------|-----------|-------|
| **原生代币** | ETH | 无（稳定币直接支付费用） |
| **终局时间** | ~12-15 秒（概率性，12 分钟 BFT） | ~600ms（确定性） |
| **共识** | Gasper（PoS + Casper FFG） | Simplex BFT（Commonware） |
| **费用支付** | 必须用 ETH | 任意 USD TIP-20（Fee AMM 转换） |
| **区块空间** | 单一 gas limit | Payment Lanes 隔离 |
| **DEX** | 应用层（Uniswap 等） | 协议级预编译合约 |
| **签名** | secp256k1（+ EIP-7212 P256 precompile） | 原生 secp256k1 + P256 + WebAuthn |
| **Account Abstraction** | EIP-4337（合约层 + Bundler） | 协议级（EIP-2718 0x76） |
| **Nonce** | 顺序 nonce | 2D Nonces（并行） |
| **隐私** | 无原生支持 | Zones（Validity Proofs） |
| **机器支付** | 无原生支持 | MPP（HTTP 402 集成） |

---

## 10. 不确定性标注

| 领域 | 不确定性 | 置信度 |
|------|----------|--------|
| 主网验证者规模与去中心化程度 | 当前是 testnet 还是 mainnet，验证者数量和未来无许可验证时间表未在官方文档中明确 | medium |
| 100K TPS 数据来源 | 官方和第三方均引用此数字，但未找到第三方实测基准数据 | medium |
| Zones 具体证明系统 | 文档提到 Validity Proofs，但未明确使用 SNARK / STARK / 其他系统 | medium |
| T2 → T3 升级时间线 | T3 规范已定义（TIP-1011），但主网升级时间未明确 | medium |
| 与 Stripe 的技术集成深度 | Stripe 是投资者和技术共建方，但具体 USDC 集成细节未完全披露 | medium |

---

## 术语表

| 术语 | 定义 |
|------|------|
| **Stablechain** | 专为稳定币优化的 Layer 1 区块链 |
| **Simplex BFT** | Commonware 实现的拜占庭容错共识协议，面向快速终局优化 |
| **TIP-20** | Tempo 原生 Token 标准，类似 ERC-20 但增加费用支付、RBAC、合规等能力 |
| **TIP-403** | Tempo 策略注册表标准，实现合规白名单/黑名单 |
| **TIP-1009** | 过期 Nonces 提案 |
| **TIP-1011** | T3 升级提案，扩展 Access Keys 的调用范围和周期性限额 |
| **Payment Lanes** | 区块空间隔离机制，确保支付交易始终有专用容量 |
| **Fee AMM** | 自动处理费用 token 转换的协议级 AMM |
| **Flip Order** | DEX 中自动反向的永续订单类型 |
| **pathUSD** | DEX 中用于跨稳定币路由的中间稳定币 |
| **Tempo Transaction (0x76)** | EIP-2718 新交易类型，支持 Passkeys、2D Nonces、费用赞助等 |
| **Access Keys** | 协议级委托签名机制，支持限额和过期 |
| **Tempo Zones** | 基于有效性证明的隐私执行环境 |
| **MPP** | Machine Payments Protocol，HTTP 402 支付协议 |
| **VRF** | Verifiable Random Function，用于随机领导者选举 |
