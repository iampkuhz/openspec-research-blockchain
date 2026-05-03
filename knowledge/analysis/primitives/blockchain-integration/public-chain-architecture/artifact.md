---
title: 公链接入架构 Primitive
type: knowledge_primitive
domain: blockchain-integration
created: 2026-05-03
source_change: public-chain-integration-architecture
schema: blockchain-research
---

# 目录

- [摘要](#摘要)
- [术语表](#术语表)
- [端到端架构概览](#端到端架构概览)
  - [全链路分层](#全链路分层)
  - [数据流向](#数据流向)
- [服务端模块分解](#服务端模块分解)
  - [钱包管理](#钱包管理)
  - [交易构造与签名](#交易构造与签名)
  - [RPC 调用层](#rpc-调用层)
  - [事件监听与订阅](#事件监听与订阅)
  - [Gas 管理](#gas-管理)
  - [Nonce 管理](#nonce-管理)
  - [链上合约交互](#链上合约交互)
  - [区块数据解析](#区块数据解析)
- [中间角色与基础设施](#中间角色与基础设施)
  - [RPC 服务商](#rpc-服务商)
  - [节点运营商](#节点运营商)
  - [区块链浏览器](#区块链浏览器)
  - [预言机](#预言机)
  - [Indexer 服务](#indexer-服务)
- [公链分层结构](#公链分层结构)
  - [P2P 网络层](#p2p-网络层)
  - [共识层](#共识层)
  - [执行层](#执行层)
  - [存储层](#存储层)
  - [智能合约层](#智能合约层)
- [工作量分布分析](#工作量分布分析)
- [交易与查询的核心流程](#交易与查询的核心流程)
  - [写交易流程](#写交易流程)
  - [读查询流程](#读查询流程)
  - [交易状态转换](#交易状态转换)
- [EVM 与非 EVM 链的架构差异](#evm-与非-evm-链的架构差异)
- [可靠性与降级策略](#可靠性与降级策略)
- [设计取舍与能力边界](#设计取舍与能力边界)
- [有限结论](#有限结论)
- [证据](#证据)
- [追踪链](#追踪链)
- [待决问题](#待决问题)

# 摘要

本研究是一次 primitive（deep-dive）分析，目标是梳理"接入一条公链"的端到端技术架构。研究覆盖从业务服务端到目标公链的全链路，识别所有参与角色、职责边界与工作量分布，并对每个模块进行结构化拆解。以 EVM 兼容链为主要研究对象，同时指出非 EVM 链在架构层面的关键差异点。

核心发现：EVM 公链接入的架构复杂度主要来自三个维度——交易生命周期管理（mempool 不确定性、分叉回滚）、RPC 层抽象（多供应商适配、增强 API 差异）和 Gas/Nonce 的并发安全。RPC 服务商选型是架构设计的首要决策点，直接决定 rate limit 策略、成本模型和降级方案。非 EVM 链适配的工作量集中在交易构造、签名和 Gas/Nonce 模块，这些模块与链的底层模型强耦合。

# 术语表

| 术语 | 定义 | 作用 | 来源 |
|---|---|---|---|
| EVM (Ethereum Virtual Machine) | 以太坊虚拟机，以太坊网络的计算状态机，负责执行智能合约和交易 | EVM 兼容链的执行环境标准 | [S08] |
| JSON-RPC | 无状态、无连接的远程过程调用协议，以太坊执行客户端通过该接口暴露功能 | 业务系统与公链节点之间的标准通信接口 | [S02], [S04] |
| Gas | 以太坊网络中衡量计算工作量的单位，每笔交易消耗固定数量的 Gas | 防止无限循环和资源滥用的经济机制 | [S08] |
| Nonce | 从某个账户地址发出的交易计数器，每笔交易递增 1 | 保证交易顺序和防止重放攻击 | [S03] |
| Mempool | 已广播但尚未被打包进区块的交易的暂存区 | 交易排队与 Gas 竞价的市场 | [S16], [S25] |
| Execution Client (EL) | 处理交易执行、状态管理和 P2P gossip 的客户端（如 Geth、Nethermind） | 执行层核心组件，暴露 JSON-RPC 接口 | [S01], [S10] |
| Consensus Client (CL) | 处理区块提议、attestation、fork choice 和 P2P 共识的客户端（如 Prysm、Lighthouse） | 共识层核心组件，通过 Engine API 与 EL 通信 | [S01] |
| Validator | 质押 32 ETH 并参与区块提议和 attestation 的网络参与者 | PoS 共识的安全基础 | [S01] |
| Sequencer | Layer 2 网络中负责排序和打包交易的角色 | L2 交易排序与数据提交 | [`uncertainty`] |
| Engine API | 执行客户端与共识客户端之间的本地 RPC 接口 | PoS 架构下 EL 和 CL 的解耦通信通道 | [S01] |

# 端到端架构概览

## 全链路分层

公链接入的完整链路可划分为三个层次：

**业务服务端层**：包含钱包管理、交易构造、RPC 调用、事件监听、Gas 管理、Nonce 管理、合约交互和区块数据解析等模块。这一层由业务系统直接控制，负责将业务逻辑转换为链上操作。

**中间基础设施层**：包括 RPC 服务商（Alchemy、Infura、QuickNode 等）、区块链浏览器（Etherscan 等）、预言机（Chainlink 等）和 Indexer 服务（The Graph 等）。这些组件提供网络接入、数据索引和外部数据喂价能力。

**公链协议层**：包含 P2P 网络层、共识层、执行层、存储层和智能合约层。这是公链的核心协议栈，决定了交易的最终确认和状态变更。

## 数据流向

业务系统构造交易并通过 JSON-RPC 发送到 RPC 服务商；RPC 服务商转发到执行客户端的交易池（mempool）；执行客户端通过 P2P 网络传播交易；验证者通过共识客户端打包交易到区块；区块确认后状态变更持久化到存储层。

# 服务端模块分解

## 钱包管理

钱包管理模块负责账户体系的维护，包括私钥/助记词的存储与访问控制、地址生成和账户分类。在生产环境中，密钥管理策略可分为：

- **热钱包**：私钥存储在服务端内存或加密文件中，适用于高频交易场景
- **冷钱包**：私钥离线存储，适用于大额资产保管
- **托管方案**：通过第三方托管服务（如 Fireblocks、AWS KMS）管理密钥

该模块与交易构造模块通过签名接口对接，与 Nonce 管理模块共享账户维度数据。

## 交易构造与签名

交易构造模块将业务意图转换为链上交易对象。EVM 兼容链的交易包含以下字段：

| 字段 | 说明 | 来源 |
|---|---|---|
| from | 发送方地址 | [S03] |
| to | 接收方地址（合约调用时为合约地址） | [S03] |
| nonce | 账户交易计数器 | [S03] |
| gasLimit | 最大 Gas 消耗上限 | [S03] |
| maxFeePerGas | EIP-1559 最大费用（含 base fee + priority fee） | [S05] |
| maxPriorityFeePerGas | EIP-1559 优先费 | [S05] |
| value | 转账金额（wei） | [S03] |
| input / data | 合约调用时的 calldata | [S03] |

EIP-2718 定义了 Typed Transaction Envelope，当前支持 Type 0（Legacy）、Type 1（EIP-2930 Access List）、Type 2（EIP-1559）、Type 3（EIP-4844 Blob）和 Type 4（EIP-7702 Set Code）五种交易类型。

签名过程使用 secp256k1 椭圆曲线算法，生成 v、r、s 三个参数。序列化后的 RLP 编码交易通过 `eth_sendRawTransaction` RPC 方法广播。

## RPC 调用层

RPC 调用层是业务系统与公链之间的统一接口。核心方法分类如下：

| 方法类别 | 代表方法 | 用途 | 来源 |
|---|---|---|---|
| 查询类 | `eth_getBalance`, `eth_getBlockByNumber`, `eth_call` | 读取链上状态 | [S02], [S04] |
| 交易类 | `eth_sendRawTransaction`, `eth_getTransactionReceipt` | 提交和查询交易 | [S02], [S04] |
| 订阅类 | `eth_subscribe`, `eth_newFilter` | 事件监听 | [S02], [S04] |
| Gas 类 | `eth_gasPrice`, `eth_feeHistory`, `eth_maxPriorityFeePerGas` | Gas 价格预估 | [S02], [S05] |
| 日志类 | `eth_getLogs` | 历史事件查询 | [S02], [S04] |

RPC 调用层需要实现以下策略：

- **多 Provider 路由**：在多个 RPC 服务商之间动态切换，应对单点故障和 rate limit
- **重试与降级**：对 `eth_call` 等查询方法实现指数退避重试；对 `eth_sendRawTransaction` 实现 nonce 回填和替代交易机制
- **超时控制**：根据方法类型设置差异化的超时阈值

不同 RPC 服务商对相同操作的计费单位存在差异：Alchemy 按月计算单元（CU），Infura 按请求次数 + 计算复杂度，QuickNode 按 credit 系统计费。RPC 调用层应对此进行统一抽象，避免供应商锁定。

## 事件监听与订阅

事件监听模块负责捕获链上事件并触发业务逻辑。实现方式包括：

- **WebSocket 订阅**：通过 `eth_subscribe`（logs、newHeads、pendingTransactions 等事件类型）实现实时推送
- **轮询模式**：定期调用 `eth_getLogs` 获取历史事件，适用于不支持 WebSocket 的 RPC 端点
- **Webhook 回调**：部分 RPC 服务商（如 Alchemy）提供 Webhook 机制，将事件推送到业务服务器

分叉处理是事件监听模块的核心挑战。当链发生 reorg 时，已确认的事件可能被回滚。业务系统需要根据确认深度策略（如等待 N 个区块确认）来决定事件的业务生效时机。

## Gas 管理

Gas 管理模块负责交易费用的动态预估和调整。EIP-1559 引入了新的 Gas 定价机制：

- **Base Fee**：每个区块的基础费用，根据上一个区块的 Gas 使用量动态调整（目标使用率为 50%）。Base Fee 在协议层面被销毁（burned），不参与分配
- **Priority Fee（Tip）**：支付给验证者的优先费，用于激励打包
- **Max Fee**：用户愿意支付的最高 Gas 费用，计算公式为 `maxFee = baseFee * 2 + priorityFee` 以确保在 base fee 翻倍时交易仍有效

业务系统应通过 `eth_feeHistory` 和 `eth_maxPriorityFeePerGas` 获取实时参数。Gas limit 的动态调整策略：首次调用使用 `eth_estimateGas` 获取预估消耗，然后乘以安全系数（通常 1.2-1.5 倍）作为实际 limit。

## Nonce 管理

Nonce 管理确保同一账户的并发交易按正确顺序提交。核心挑战包括：

- **本地 Nonce 追踪**：维护账户维度的递增计数器，每次构造交易时读取并递增
- **并发处理**：当多个线程同时为同一账户构造交易时，需要原子操作获取下一个 nonce 值
- **回填策略**：交易确认或 dropped 后，通过 `eth_getTransactionCount(address, "pending")` 回填当前 nonce
- **替代交易**：当交易长时间 pending 时，可用相同 nonce 但更高 Gas 价格的交易进行替换（gas price bump 通常要求 10% 以上）

Nonce 不一致会导致交易被节点拒绝或永久 pending。生产环境建议维护独立 nonce 数据库，定期与链上状态校对。

## 链上合约交互

合约交互模块处理 ABI 编解码、合约部署和函数调用：

- **ABI 编解码**：将结构化参数编码为 calldata（bytes），以及将返回值解码为结构化类型
- **合约部署**：构造包含合约 bytecode 的交易（to 字段为空），通过 `eth_sendRawTransaction` 提交
- **只读调用**：通过 `eth_call` 执行合约函数，不产生 Gas 消耗且不改变链上状态
- **状态修改调用**：构造交易调用合约函数，需要签名并提交到链上

viem 和 ethers.js 是官方推荐的 JavaScript/TypeScript 交互库。viem 采用模块化设计、强类型对齐以太坊官方术语，ethers.js 提供更成熟的生态和更广泛的社区支持。

## 区块数据解析

区块数据解析模块负责处理区块头和交易数据：

- **区块头解析**：解析区块号、时间戳、Gas 使用量、base fee、parent hash 等字段
- **交易解码**：从 RLP 编码的交易数据中提取发送方、接收方、value、input 等字段
- **状态树读取**：Merkle Patricia Trie 结构的状态读取需要 Archive 节点支持
- **日志解析**：从 `eth_getLogs` 返回的事件中提取 contract address、topics、data

# 中间角色与基础设施

## RPC 服务商

RPC 服务商是业务系统接入公链的首要通道。主流供应商对比如下：

| 维度 | Alchemy | Infura | QuickNode | 来源 |
|---|---|---|---|---|
| 免费额度 | 月 3 亿 CU | 日 10 万次请求 | 月 1000 万 credit | [S13], [S14] |
| 增强 API | 提供（NFT API、Token API 等） | 基础 | 提供（增强端点） | [S13] |
| 支持网络 | 以太坊 + L2 多链 | 以太坊 + 多链 | 多链覆盖最广 | [S11], [S13] |

架构设计中，RPC 调用层应实现对多供应商的统一抽象。不同供应商的增强 API 能力差异较大，业务系统应区分标准 JSON-RPC 能力（可跨供应商迁移）和增强能力（供应商锁定）。

## 节点运营商

节点分为自建节点和托管节点两种模式：

- **自建节点**：自行部署 Geth/Erigon 等客户端，完全控制数据和控制面。优势是数据隐私和无 rate limit，劣势是运维成本高
- **托管节点**：通过 RPC 服务商间接访问节点。优势是开箱即用，劣势是受限于供应商的 rate limit 和定价策略

同步模式选择直接影响运维工作量：

| 模式 | 磁盘需求 | 同步时间 | 能力 | 来源 |
|---|---|---|---|---|
| Snap（默认） | ~1 TB | 数小时到数天 | 当前状态 + 近期历史 | [S09] |
| Full | ~1-2 TB | 数天 | 完整可验证历史 | [S09] |
| Archive | ~1.9 TB - 12 TB+ | 数天到数周 | 所有历史状态 | [S09], [S12] |

> **不确定性 [UNC-02]**：Archive 节点磁盘大小存在来源冲突。Geth 新版本 path-based storage 已优化到约 1.9 TB，早期数据约 12 TB。数据时效性需要确认。

> **不确定性 [UNC-03]**：Light client 在当前 PoS 架构下不可用（"light-sync does not work"）。部分来源仍将 light node 列为可用类型，这与实际状态不符。

## 区块链浏览器

区块链浏览器（如 Etherscan）提供交易查询、合约验证、地址余额查询等公开查询能力。在业务架构中，浏览器主要用于交易状态二次确认、合约源码验证和 ABI 获取、异常交易调试。

## 预言机

预言机（如 Chainlink）将链下数据喂入链上合约。在业务系统中，预言机的作用包括价格数据喂价（DEX、借贷协议）、随机数生成（VRF）和链下计算验证（Automation）。

## Indexer 服务

Indexer（如 The Graph）将链上事件索引为可查询的 GraphQL 接口。相比直接调用 `eth_getLogs`，Indexer 的优势在于跨合约事件聚合查询、历史数据的高效分页和过滤、预定义的子图（Subgraph）Schema。

> **Evidence Gap**：L2 Sequencer 架构（如 Arbitrum/Optimism 的 Sequencer 和 Bridge 机制）的 L1 来源未在本次收集中覆盖，需要补充 docs.arbitrum.io / docs.optimism.io 的相关文档。

# 公链分层结构

## P2P 网络层

P2P 网络层负责节点发现和交易/区块传播。以太坊 PoS 架构下，执行层和共识层各自维护独立的 P2P 网络：

- **EL P2P 网络**：执行客户端通过 DevP2P 协议传播交易和区块
- **CL P2P 网络**：共识客户端通过 libp2p 传播 attestation 和 beacon 块

两层 P2P 网络的分离使得执行层和共识层可以独立升级和替换。交易通过 mempool gossip 在 EL 网络中传播，区块通过 CL 网络中的 attestation 机制进行共识。

## 共识层

共识层处理区块提议、attestation 和 fork choice。以太坊 PoS 机制下：

- **验证者周期**：验证者被随机分配为 proposers 和 attesters
- **Epoch 和 Slot**：每个 epoch 包含 32 个 slot，每个 slot 12 秒，一个 proposer 负责提议区块
- **Fork Choice**：基于 attestation 权重的最长链规则
- **Finality**：交易需先达到 justified 状态，再经过约 2 个 epoch 后达到 finalized（通常约 12-15 分钟）

Engine API 是共识层和执行层之间的本地 RPC 通信通道。CL 通过 `engine_newPayload` 将区块传递给 EL，EL 通过 `engine_getPayload` 返回组装好的交易集合。

## 执行层

执行层是 EVM 运行环境，负责交易验证和状态变更。核心组件包括：

- **EVM**：基于栈的虚拟机，执行字节码指令
- **交易池（Mempool）**：暂存已广播但未打包的交易
- **状态管理**：账户余额、storage、nonce 的状态更新
- **RPC 服务**：通过 JSON-RPC 暴露查询和提交接口

Geth 作为最广泛使用的执行客户端，其架构包含 P2P 模块、交易池、状态数据库、RPC 服务等多个组件。

## 存储层

存储层负责持久化链上状态和历史数据：

- **状态 Trie**：Merkle Patricia Trie 结构，存储账户状态
- **历史数据**：区块头和交易数据按序存储
- **归档数据**：Archive 节点保留每个区块的完整状态快照，支持历史状态查询

Snap sync 模式在同步完成后会进行 state healing 阶段，修复缺失的 trie 节点。该阶段无法监控进度，且取决于磁盘和网络速度。

> **Evidence Gap**：智能合约层详细设计（状态树、Merkle Patricia Trie 内部结构）需要 ethereum.org/developers/docs/data-structures-and-encoding/ 的 L1 来源补充。

## 智能合约层

智能合约层是运行在 EVM 上的应用程序逻辑，包括协议合约（DEX、借贷、稳定币等 DeFi 核心合约）、治理合约（DAO 投票和参数调整）和业务合约（业务系统部署的自定义合约）。

# 工作量分布分析

### 业务服务端

| 模块 | 主要消耗 | 估算依据 |
|---|---|---|
| RPC 调用层 | 请求量（QPS）和供应商成本 | 不同 RPC 供应商对相同操作的计费差异显著 |
| Nonce 管理 | 并发控制和一致性维护 | 需要独立数据库 + 定期校对机制 |
| 事件监听 | 存储和索引 | 高频事件的持久化和查询需要独立索引服务 |
| Gas 管理 | 实时计算 | 需持续调用 `eth_feeHistory` 和 `eth_maxPriorityFeePerGas` |

> **不确定性 [UNC-04]**：工作量的定量数据（QPS、延迟分位数）缺乏官方测量来源。

### RPC 服务商层

| 环节 | 主要消耗 | 估算依据 |
|---|---|---|
| 查询处理 | 计算和带宽 | `eth_call` 等状态查询需要实时访问状态数据库 |
| Archive 查询 | 磁盘 I/O 和存储 | Archive 节点需维护完整历史状态快照 |
| Rate Limit 控制 | 计算 | 按不同计费模型追踪用户配额 |

### 节点层

| 环节 | 主要消耗 | 估算依据 |
|---|---|---|
| 节点同步 | 磁盘、网络带宽、时间 | Snap sync 需要 ~1 TB 磁盘和数小时到数天 |
| 交易池维护 | 内存和 CPU | 高频场景下 mempool 包含数千笔 pending 交易 |
| 共识参与 | CPU、网络 | 验证者需要持续参与 attestation 和区块提议 |

### 链上层

| 环节 | 主要消耗 | 估算依据 |
|---|---|---|
| 交易执行 | Gas（计算/存储/带宽） | 每笔交易消耗固定 Gas 量 |
| 状态存储 | 存储增长 | 每个状态变更持久化到 trie |
| 数据传播 | P2P 网络带宽 | 交易和区块通过两层 P2P 网络传播 |

# 交易与查询的核心流程

## 写交易流程

写交易的完整生命周期如下：

**阶段 1：构造与签名**

1. 业务系统获取账户当前 nonce（`eth_getTransactionCount`）
2. 构造交易对象：填充 to、value、data、gasLimit、maxFeePerGas、maxPriorityFeePerGas
3. 使用私钥对交易进行 secp256k1 签名
4. 序列化为 RLP 编码的 raw transaction

**阶段 2：广播与 Mempool**

5. 通过 `eth_sendRawTransaction` 将交易提交到 RPC 端点
6. 交易进入执行客户端的 mempool
7. 交易通过 EL P2P 网络在节点间传播
8. 节点验证交易：nonce 有效性、签名正确性、Gas 上限、余额充足性

**阶段 3：打包与确认**

9. 验证者从 mempool 选择交易（按 priority fee 排序）
10. 交易被打包进区块，状态为 "mined"
11. 区块通过 CL attestation 获得 justified 状态
12. 经过 2 个 epoch 后区块达到 finalized

**阶段 4：异常路径**

- **Pending**：交易在 mempool 中等待，可能因 Gas 价格过低而长时间不打包
- **Dropped**：交易被 mempool 驱逐（nonce 过期、Gas 不足、余额不足）
- **Replaced**：相同 nonce 的替代交易以更高 Gas 价格提交

## 读查询流程

读查询不涉及状态变更，路径更短：

1. 业务系统通过 `eth_call`、`eth_getBalance`、`eth_getBlockByNumber` 等方法发起查询
2. RPC 端点在执行客户端的状态数据库中查找
3. 返回查询结果（不涉及 mempool 或共识层）

对于事件订阅查询：

1. 业务系统通过 `eth_subscribe("logs", filter)` 注册事件过滤器
2. RPC 端点在新区块产生时匹配 filter 条件
3. 匹配到的事件通过 WebSocket 推送给业务系统

## 交易状态转换

交易在各状态之间转换：

- **Pending → Mined**：验证者选择交易打包
- **Pending → Dropped**：nonce 过期、Gas 不足、mempool 满时驱逐
- **Pending → Replaced**：相同 nonce 的替代交易被打包
- **Mined → Reorg**：链分叉导致区块回滚，交易回到 pending 状态

# EVM 与非 EVM 链的架构差异

本章节以 EVM 链为基准，对比 Solana 等非 EVM 链在架构层面的核心差异。

### 账户模型

| 维度 | EVM | Solana | 来源 |
|---|---|---|---|
| 模型 | Account-based：账户直接持有余额和状态 | 基于 Account 但语义不同：所有数据存储在 Account 对象中 | [S03] |
| 存储 | 合约 storage 映射结构 | Program 与数据 Account 分离 | |

> **Evidence Gap**：Solana 官方架构文档（docs.solana.com）的 Account 模型、Sealevel 执行模型、交易格式等 L1 来源未在本次收集中覆盖。

### 交易模型

| 维度 | EVM | Solana | 来源 |
|---|---|---|---|
| 类型系统 | Typed Transaction Envelope（Type 0-4） | 指令列表（Instruction list） | [S03] |
| 签名 | secp256k1 单签名者/多签 | Ed25519 签名方案 | [S03] |
| Gas | Gas 单位计量 | Compute Unit（CU）计量 | [S08] |
| Nonce | 递增计数器 | Recent Blockhash 作为防重放机制 | [S03] |

### 执行模型

| 维度 | EVM | Solana | 来源 |
|---|---|---|---|
| 执行方式 | 单线程顺序执行 | Sealevel 并行执行 | [S08] |
| 状态访问 | 全局状态 | Account 隔离 | |
| 智能合约 | Solidity/Vyper → 字节码 | Rust/C → BPF 字节码 | |

### 对服务端模块的影响

从 EVM 切换到 Solana 时，以下模块需要重写：

| 模块 | 影响程度 | 原因 |
|---|---|---|
| 交易构造与签名 | 完全重写 | 交易格式、签名算法、nonce 机制完全不同 |
| RPC 调用层 | 部分重写 | 方法名和语义不同，但抽象层次（Provider 模式）可复用 |
| Gas 管理 | 完全重写 | Gas 定价机制和预估逻辑不同 |
| Nonce 管理 | 完全重写 | Nonce 机制被 Recent Blockhash 替代 |
| 合约交互 | 完全重写 | ABI 编解码、IDL 格式、程序调用方式不同 |
| 钱包管理 | 部分适配 | 密钥生成算法从 secp256k1 改为 Ed25519 |
| 事件监听 | 部分重写 | 事件订阅机制不同，但模式可复用 |

# 可靠性与降级策略

### RPC 不可用处理

RPC 服务商可能发生宕机、超时或 rate limit 拒绝。降级策略包括：

- **多 Provider 故障转移**：维护至少 2 个 RPC 端点，主端点失败时自动切换
- **请求降级**：增强 API 不可用时回退到标准 JSON-RPC 方法
- **缓存策略**：对只读查询结果进行短期缓存，减少 RPC 调用频率

### 链分叉处理

链分叉（reorg）发生时：

- **事件监听模块**：回滚已确认但被分叉的事件，重新处理新链上的事件
- **交易确认模块**：已"确认"的交易可能被回滚到 pending 状态，需要重新广播
- **业务策略**：根据业务风险承受能力设置确认深度（如 DeFi 交易等待 12-20 个区块确认，小额支付等待 1-3 个区块）

### 交易 Pending 处理

交易长时间 pending 时的处理：

- **Gas Bump**：用相同 nonce 提交更高 Gas 价格的替代交易（通常要求 10%+ 的价格提升）
- **Cancel 交易**：用相同 nonce 发送零 value 交易到自身地址，取消原交易
- **Timeout 策略**：超过设定阈值后放弃原交易，用新 nonce 重新提交

### 同步模式选择对可用性的影响

不同同步模式影响节点的数据可用性：

- **Snap sync**：只能查询当前状态，无法查询历史状态
- **Archive sync**：支持所有历史状态查询，但存储成本高
- **同步中**：节点在 state healing 阶段无法提供完整数据

# 设计取舍与能力边界

### RPC 供应商选型

| 方案 | 优势 | 劣势 | 适用场景 | 来源 |
|---|---|---|---|---|
| 单供应商 | 简单、一致的开发体验 | 单点故障、供应商锁定 | 测试/小规模 | [S13] |
| 多供应商抽象 | 高可用、灵活切换 | 开发复杂度高、增强 API 差异难统一 | 生产环境 | [S13], [S22] |
| 自建节点 | 无 rate limit、数据隐私 | 运维成本高、初始同步慢 | 高频/大规模 | [S09], [S11] |

### 同步模式选择

| 模式 | 速度 | 存储 | 信任假设 | 适用场景 | 来源 |
|---|---|---|---|---|---|
| Snap | 快 | ~1 TB | 依赖共识验证 | 大多数生产场景 | [S09] |
| Full | 中 | ~1-2 TB | 完全验证历史 | 需要历史交易验证 | [S09] |
| Archive | 慢 | ~1.9 TB - 12 TB+ | 完全验证所有历史状态 | 区块浏览器、数据分析 | [S09], [S12] |

### 交互库选型

| 库 | 优势 | 劣势 | 来源 |
|---|---|---|---|
| viem | 模块化、TypeScript 类型安全、树摇优化、对齐以太坊官方术语 | 相对较新、生态较小 | [S17], [S24] |
| ethers.js | 生态成熟、社区支持广泛、文档完善 | 体积较大、类型系统不如 viem 精确 | [S18], [S24] |
| web3.js | 历史最久、多语言覆盖 | 维护活跃度下降、API 风格不一致 | [S19] |

### 事件监听架构

| 方案 | 优势 | 劣势 | 来源 |
|---|---|---|---|
| 直接 RPC 订阅 | 简单、实时 | 不支持 WebSocket 时退化为轮询、分叉处理复杂 | [S02] |
| Webhook 推送 | 无需维护 WebSocket 连接、供应商管理可靠性 | 供应商锁定、延迟不可控 | [S13] |
| Indexer 查询 | 高效聚合、预定义 Schema | 额外依赖、更新延迟、成本 | [S22] |

### 能力边界

本研究的能力边界如下：

- **纳入范围**：EVM 兼容链（以太坊、BSC、Polygon 等）的端到端接入架构
- **有限覆盖**：非 EVM 链（Solana 等）的架构差异点，因缺乏 L1 官方来源标注为 uncertainty
- **不纳入范围**：Layer 2（Arbitrum/Optimism/ZK-Rollup）与 Layer 1 的架构差异（需后续独立 change）、具体业务逻辑实现、以太坊黄皮书级别的共识细节、合规与法律层面的分析

# 有限结论

1. **EVM 公链接入的架构复杂度主要来自三个维度**：交易生命周期管理（mempool 不确定性、分叉回滚）、RPC 层抽象（多供应商适配、增强 API 差异）和 Gas/Nonce 的并发安全

2. **RPC 服务商选型是架构设计的首要决策点**：直接决定了 rate limit 策略、成本模型和降级方案。生产环境建议至少维护 2 个供应商端点

3. **事件监听的架构选型取决于业务需求**：简单场景使用 RPC 订阅，复杂聚合查询需要 Indexer，分叉处理需要在业务层实现

4. **非 EVM 链适配的工作量集中在交易构造、签名和 Gas/Nonce 模块**：这些模块与链的底层模型强耦合，无法通过抽象层复用

### 未解问题

| 问题 | 影响 | 状态 |
|---|---|---|
| Solana 等非 EVM 链的 L1 官方架构文档缺失 | 无法给出精确的架构差异分析 | [`evidence-gap`] 需要 docs.solana.com |
| L2 Sequencer 和 Bridge 机制的官方文档缺失 | 无法覆盖 L2 特有的架构差异 | [`evidence-gap`] 需要 docs.arbitrum.io / docs.optimism.io |
| 工作量分布的定量数据缺乏 | 无法给出精确的容量规划建议 | [`uncertainty`] 需要实际测量数据 |
| Archive 节点磁盘大小的时效性 | 影响存储成本估算 | [UNC-02] 需要 Geth 最新版本数据 |

# 证据

| Source | 支撑章节 | 置信度 |
|---|---|---|
| [S01] Node architecture | 术语表、P2P 网络层、共识层、执行层 | high (L1) |
| [S02] JSON-RPC API | 术语表、RPC 调用层、事件监听、交易流程 | high (L1) |
| [S03] Transactions | 术语表、交易构造、Nonce 管理、交易流程 | high (L1) |
| [S05] EIP-1559 | Gas 管理 | high (L1) |
| [S08] Ethereum development docs | 术语表、执行层、智能合约层 | high (L1) |
| [S09] Sync modes (Geth) | 节点运营商、存储层、工作量分布、设计取舍 | medium (L2) |
| [S13] RPC providers comparison 2026 | RPC 服务商、可靠性策略、设计取舍 | medium (L3) |
| [S14] Best Ethereum RPC Providers 2026 | RPC 服务商、工作量分布 | medium (L3) |
| [S15] Ethereum Transactions: Pending, Mined, Dropped | 交易流程、可靠性策略 | medium (L2) |
| [S16] Understanding the Mempool | 术语表、执行层、交易流程 | medium (L3) |
| [S17] Viem | 合约交互、设计取舍 | medium (L3) |
| [S18] Ethers.js | 钱包管理、合约交互、设计取舍 | medium (L3) |
| [S19] Ethereum for JavaScript developers | 交互库选型 | high (L1) |
| [S22] How to Design a Blockchain Integration Layer | 事件监听、Indexer 服务、工作量分布、设计取舍 | medium (L4) |
| [S24] Viem vs Ethers.js comparison | 交互库选型 | medium (L3) |

# 追踪链

- 来源 change: `public-chain-integration-architecture`
- Request: `openspec/changes/public-chain-integration-architecture/request.md`
- Plan: `openspec/changes/public-chain-integration-architecture/plan.md`
- Draft: `openspec/changes/public-chain-integration-architecture/draft.md`
- Review: `openspec/changes/public-chain-integration-architecture/review.md`
- Publish: `openspec/changes/public-chain-integration-architecture/publish.md`

# 待决问题

- Solana 等非 EVM 链的 L1 官方架构文档缺失，无法给出精确的架构差异分析
- L2 Sequencer 和 Bridge 机制的官方文档缺失，无法覆盖 L2 特有的架构差异
- 工作量分布的定量数据缺乏，无法给出精确的容量规划建议
- Archive 节点磁盘大小的时效性需要 Geth 最新版本数据确认
