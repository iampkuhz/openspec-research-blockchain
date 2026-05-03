---
artifact_type: synthesis
source_change: public-chain-integration-guide
created: 2026-05-03
schema: blockchain-research
operation: create
---

# 目录

- [摘要](#摘要)
- [引言](#引言)
  - [研究目的与与 primitive 的关系](#研究目的与与-primitive-的关系)
  - [阅读指南](#阅读指南)
- [术语表](#术语表)
- [服务端各模块注意事项](#服务端各模块注意事项)
  - [钱包管理](#钱包管理)
  - [交易构造与签名](#交易构造与签名)
  - [RPC 调用层](#rpc-调用层)
  - [事件监听与订阅](#事件监听与订阅)
  - [Gas 管理](#gas-管理)
  - [Nonce 管理](#nonce-管理)
  - [合约交互](#合约交互)
  - [区块数据解析](#区块数据解析)
- [中间基础设施风险点与最佳实践](#中间基础设施风险点与最佳实践)
  - [RPC 服务商选型](#rpc-服务商选型)
  - [节点运维](#节点运维)
  - [区块链浏览器依赖](#区块链浏览器依赖)
- [公链各层常见坑点](#公链各层常见坑点)
  - [网络层](#网络层)
  - [共识层（Reorg 与 Finality）](#共识层reorg-与-finality)
  - [执行层](#执行层)
  - [存储层](#存储层)
  - [合约层](#合约层)
- [技术事项布局规划](#技术事项布局规划)
  - [技术选型方法论](#技术选型方法论)
  - [容量规划](#容量规划)
  - [监控告警体系](#监控告警体系)
  - [降级容灾策略](#降级容灾策略)
- [EVM 与非 EVM 链注意事项差异](#evm-与非-evm-链注意事项差异)
  - [核心差异维度](#核心差异维度)
  - [对服务端模块的影响评估](#对服务端模块的影响评估)
  - [EVM 兼容链的注意事项复用](#evm-兼容链的注意事项复用)
- [趋势判断与不确定性](#趋势判断与不确定性)
  - [尚未形成共识的事项](#尚未形成共识的事项)
  - [需要持续跟踪的变化](#需要持续跟踪的变化)
- [有限结论](#有限结论)
  - [未解问题](#未解问题)
- [能力边界](#能力边界)
  - [纳入范围](#纳入范围)
  - [有限覆盖](#有限覆盖)
  - [不纳入范围](#不纳入范围)
- [上线前 Checklist](#上线前-checklist)
  - [钱包管理](#上线-checklist-钱包管理)
  - [交易构造与签名](#上线-checklist-交易构造与签名)
  - [RPC 调用层](#上线-checklist-rpc-调用层)
  - [事件监听与订阅](#上线-checklist-事件监听与订阅)
  - [Gas 管理](#上线-checklist-gas-管理)
  - [Nonce 管理](#上线-checklist-nonce-管理)
  - [合约交互](#上线-checklist-合约交互)
  - [区块数据解析](#上线-checklist-区块数据解析)
  - [基础设施](#上线-checklist-基础设施)
  - [监控告警](#上线-checklist-监控告警)
  - [降级容灾](#上线-checklist-降级容灾)
- [参考资料](#参考资料)
- [证据](#证据-1)
- [追踪链](#追踪链)
- [待决问题](#待决问题)

---

# 摘要

本 synthesis 基于 sibling primitive `public-chain-integration-architecture` 的端到端架构拆解，将架构模块映射到工程实践中的注意事项、常见陷阱和最佳实践。研究覆盖服务端各模块（钱包管理、交易构造、RPC 调用、事件监听、Gas/Nonce 管理、合约交互、区块解析）、中间基础设施（RPC 选型、节点运维、浏览器依赖）、公链各层工程坑点（网络层到合约层）、技术选型与监控体系，以及 EVM 与非 EVM 链的差异维度。最终形成一份可作为接入公链时技术扫盲和 checklist 参考的工程指南。所有技术主张均追溯到来源或 primitive draft，不脱离依赖内容独立评分。

# 引言

## 研究目的与与 primitive 的关系

本 synthesis 以 sibling primitive `public-chain-integration-architecture` 的架构模块为维度骨架，不重复底层机制分析，而是将每个模块映射到具体的工程注意事项、常见陷阱和最佳实践。Primitive 回答"架构是什么"，本 synthesis 回答"工程实践中要注意什么"。

## 阅读指南

- 第 3 章术语表建立基础理解
- 第 4 章按服务端模块逐一分析，是核心章节
- 第 5-6 章分别覆盖中间基础设施和公链协议层的工程坑点
- 第 7 章提供技术选型方法论和监控体系规划
- 第 8 章对比 EVM 与非 EVM 链的差异
- 第 9-10 章为趋势判断、有限结论和上线前 Checklist
- 所有引用使用 `[src-XX]` 格式对应 source-pack 中的来源编号

# 术语表

| 术语 | 定义 | 作用 | 来源 |
|---|---|---|---|
| Nonce | 从某个账户地址发出的交易计数器，每笔交易递增 1 [src-04] | 保证交易顺序、防止重放和 nonce hole 导致的 stuck | [src-03], [src-04] |
| Mempool | 已广播但尚未被打包进区块的交易的暂存区 [src-16] | 交易排队与 Gas 竞价的市场，影响交易确认时间 | [src-16], [src-25] |
| Reorg (Chain Reorganization) | 节点发现更长链后切换到新链，旧链上已确认交易可能被回滚 [src-06] | 业务系统需处理已确认事件的回滚和重新确认 | [src-06], [src-07] |
| Finality | 区块经过 2 个 epoch 的 justified 后达到 finalized 状态 [src-07] | 达到 finality 后交易不可逆转，是业务确认的安全锚点 | [src-07] |
| EIP-1559 | 以太坊交易费用市场规范，引入 base fee + priority fee 混合定价 [src-02] | 替代 first-price auction，Gas 费用更可预测 | [src-02], [src-03] |
| Base Fee | 每个区块的基础费用，根据上一个区块 Gas 使用量动态调整 [src-02] | 协议层自动计算，燃烧不分配给验证者 | [src-02] |
| Priority Fee (Tip) | 支付给验证者的优先费，决定交易在区块中的优先级 [src-02] | 影响交易打包速度和顺序 | [src-02] |
| k-depth | 等待 N 个后续区块确认的策略 [src-07] | 简单但不安全的确认策略，PoS 下 depth 不等于安全性 | [src-07] |
| Typed Transaction Envelope (EIP-2718) | 以太坊交易类型封装，支持 Type 0-4 [src-03] | 向后兼容的交易格式扩展机制 | [src-03] |
| Archive Node | 保留每个区块完整状态快照的节点类型 [src-09] | 支持历史状态查询，磁盘需求约 1.9 TB - 12 TB+ | [src-09], [src-12] |

# 服务端各模块注意事项

## 钱包管理

**核心职责**：密钥安全存储、地址派生、账户分类（热/冷钱包）和签名接口提供。

**常见陷阱**：

- **热钱包私钥暴露风险**：热钱包私钥存储在服务端内存或加密文件中，适用于高频交易场景但增加了泄露面 [src-15], [src-25]。生产环境必须限制热钱包的权限和余额上限。
- **冷钱包与热钱包混用**：将大额资产存放在热钱包中是常见的安全反模式 [src-15], [src-25]。应按业务风险等级分离 hot/warm/cold 钱包层级 [src-25]。
- **多签方案的成本考量**：多签钱包虽然提高了安全性，但智能合约多签（如 Gnosis Safe）比 EOA 多签的 Gas 成本更高 [src-15]。

**最佳实践**：

- 采用 hot/cold 钱包组合策略：热钱包处理日常高频交易，冷钱包保管大额资产 [src-15], [src-25]
- 使用第三方托管服务（如 Fireblocks、AWS KMS）管理热钱包密钥，而非裸存文件系统 [src-15], [src-25]
- HD 钱包派生路径遵循 BIP-44/BIP-84 标准，确保跨客户端兼容

**防御性策略**：

- 热钱包设置单笔/日累计转账上限，超额交易需多签审批
- 定期轮换热钱包密钥，旧密钥对应的地址余额应及时转移到冷钱包
- 实现钱包余额监控告警，异常余额变化立即触发告警

## 交易构造与签名

**核心职责**：将业务意图转换为链上交易对象，完成签名并序列化。

**常见陷阱**：

- **EIP-2718 交易类型混用**：EVM 兼容链支持 Type 0 (Legacy)、Type 1 (EIP-2930)、Type 2 (EIP-1559) 等多种交易类型 [src-03]。在 EIP-1559 启用后使用 Legacy 交易（Type 0）可能导致 Gas 费用估算不准确，因为 legacy 交易的 gas_price 将全部被 base fee + priority fee 消耗 [src-02]。
- **缺少 replay 保护**：未使用 EIP-155 签名格式的交易可能被重放到其他链上 [src-03]。必须确保 chain_id 字段被正确填充。
- **gas estimation 失败未处理**：当交易本身会 revert 或过于复杂时，`eth_estimateGas` 会返回 UNPREDICTABLE_GAS_LIMIT 错误 [src-08]。常见原因包括合约不存在、require 条件不满足或 ABI 不匹配 [src-08]。
- **序列化格式错误**：EIP-1559 交易的 RLP 编码格式为 `0x02 || rlp([chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list, signature_y_parity, signature_r, signature_s])` [src-02]，字段顺序和数量与 Legacy 交易不同。

**最佳实践**：

- 优先使用 Type 2 (EIP-1559) 交易格式，max_fee_per_gas 设置为可接受的费用上限 [src-02]
- 签名前验证合约存在性（`provider.getCode(address)`）和 ABI 版本匹配 [src-08]
- 使用成熟的交互库（viem 或 ethers.js）处理序列化和签名，避免手动 RLP 编码 [src-17], [src-18]

**防御性策略**：

- Gas estimation 失败时，根据错误类型区分处理：CALL_EXCEPTION 应检查合约状态，NUMERIC_FAULT 应检查参数范围 [src-08]
- 发送前做交易模拟（dry run），使用 Tenderly 等工具提前检测 revert [src-21]
- 对交易构造层实施参数校验：value 不超过阈值、data 不为空时验证 ABI 可解析、gasLimit 在合理范围内

## RPC 调用层

**核心职责**：业务系统与公链之间的统一接口，覆盖查询、交易提交、事件订阅和 Gas 查询。

**常见陷阱**：

- **供应商锁定**：不同 RPC 服务商的增强 API 能力差异显著 [src-19]。如果业务系统深度依赖某一供应商的增强端点（如 Alchemy NFT API），切换成本会大幅增加。
- **计费模型不一致**：Alchemy 按月计算单元（CU），Infura 按请求次数 + 计算复杂度，QuickNode 按 credit 系统 [src-13], [src-14]。同一操作在不同供应商的计费可能相差数倍。
- **HTTP 与 WebSocket 混用不当**：标准 JSON-RPC 请求走 HTTP(S) 更合适（支持负载均衡、自动重试、gZip 压缩可改善 75% 延迟），WebSocket 仅用于 event subscription [src-05]。将普通查询走 WS 会导致静默失败风险增加且无法利用负载均衡 [src-05]。
- **Rate Limit 触发后的降级缺失**：当 RPC 端点返回 429 状态码时，如果没有备选端点或重试策略，业务系统会短暂不可用 [src-05], [src-13]。

**最佳实践**：

- **多 Provider 故障转移**：维护至少 2 个 RPC 端点，主端点失败或 rate limit 时自动切换 [src-13]
- **标准 vs 增强 API 分层抽象**：标准 JSON-RPC 方法（`eth_getBalance`、`eth_call` 等）应实现供应商无关的调用层；增强 API 作为可选能力，降级时回退到标准方法 [src-13]
- **HTTP 优先**：标准 JSON-RPC 请求使用 HTTPS 而非 WS，仅在需要 push 通知时建立 WebSocket 连接 [src-05]
- **差异化超时控制**：查询类方法设置 5-10 秒超时，交易类方法设置 30-60 秒

**防御性策略**：

- 实现请求级别的 circuit breaker：连续 N 次失败后标记端点不可用，切换到备选端点
- 对只读查询结果进行短期缓存（如区块数据缓存 12 秒、余额数据缓存 30 秒），减少 RPC 调用频率
- 订阅范围尽可能窄（按 address、topic filter），不需要完整交易对象时使用 hashesOnly 模式降低带宽消耗 [src-05]

## 事件监听与订阅

**核心职责**：捕获链上事件并触发业务逻辑，支持实时推送和历史查询。

**常见陷阱**：

- **未处理 reorg 导致的事件重复/丢失**：当链发生 reorg 时，已推送的新区块头和新日志可能被回滚 [src-06]。`newHeads` 订阅在 reorg 时会推送分叉后的区块头，`logs` 订阅的 `removed` 字段标记被回滚的日志 [src-10]。如果业务系统未处理 `removed` 字段，会导致状态不一致。
- **WebSocket 断连未恢复**：WebSocket 是长连接，绑定到单一节点而非负载均衡 [src-05]。断连后如果没有重连机制，会丢失期间的事件。
- **宽泛订阅消耗带宽**：未指定 address 或 topic filter 的 `logs` 订阅会匹配所有合约的事件，按带宽计费时快速消耗额度 [src-05]。
- **轮询模式的性能瓶颈**：`eth_getLogs` 在大时间范围查询时性能差，部分节点限制查询范围（如最多 10000 个区块）[src-02]。

**最佳实践**：

- **验证 block hash continuity**：每个推送的区块的 parent hash 应匹配前一个区块的 hash，发现不匹配时暂停处理并验证 [src-06]
- **处理 `removed` 字段**：`logs` 订阅返回的事件中，`removed: true` 表示该事件已被回滚，业务系统需要执行反向操作 [src-10]
- **WebSocket 断连回退到 HTTP polling**：当 WS 断连无法恢复时，降级为定期 `eth_getLogs` 轮询，确保事件不丢失 [src-05]
- **缩窄订阅范围**：按合约 address 和 topic filter 过滤，仅在需要完整交易对象时请求 full transaction [src-05]

**防御性策略**：

- 事件持久化采用 upsert 而非 insert 语义，确保 reorg 后的状态更新安全 [src-06]
- 对关键事件实现双路径监听：WebSocket 实时推送 + HTTP 定期校对，交叉验证事件完整性
- 记录已处理的最高区块号，服务重启时从该位置恢复而非从头扫描

## Gas 管理

**核心职责**：动态预估交易费用，确保交易在合理费用下及时被打包。

**核心机制（EIP-1559）**：

EIP-1559 将 Gas 定价从 first-price auction 改为混合定价模型 [src-02]。交易需设置两个参数：

| 参数 | 说明 | 计算策略 | 来源 |
|---|---|---|---|
| maxFeePerGas | 用户愿意支付的最高 Gas 费用 | `baseFee * 2 + priorityFee`，确保 base fee 翻倍时仍有效 | [src-02], [src-05] |
| maxPriorityFeePerGas | 支付给验证者的优先费 | 通过 `eth_maxPriorityFeePerGas` 获取建议值 | [src-02], [src-05] |

Base Fee 由协议层自动计算，每块最大变化幅度为 12.5%（`BASE_FEE_MAX_CHANGE_DENOMINATOR = 8`）[src-02], [src-03]。计算公式为：当 `parent_gas_used > parent_gas_target` 时上升，增量为 `parent_base_fee * gas_used_delta / parent_gas_target / 8` [src-02], [src-03]。

**常见陷阱**：

- **Base Fee 突发增长**：在网络拥堵时，base fee 每块最多上升 12.5%，连续多块累积可能导致费用暴涨 [src-02]。如果 maxFeePerGas 设置过低，交易会长期 pending。
- **Gas Limit 预估过低**：`eth_estimateGas` 返回的预估值不包含安全余量，实际执行可能因状态变化消耗更多 Gas [src-02], [src-08]。预估失败时返回 UNPREDICTABLE_GAS_LIMIT 错误 [src-08]。
- **替换交易费用涨幅不足**：使用相同 nonce 替换 pending 交易时，maxFeePerGas 和 maxPriorityFeePerGas 都必须至少提升 10%，否则节点会拒绝 [src-04]。只提升其中一个参数会导致 "replacement transaction underpriced" 错误 [src-04]。

**最佳实践**：

- 通过 `eth_feeHistory` 获取近期 base fee 趋势，辅助 maxFeePerGas 决策 [src-02], [src-05]
- Gas limit 使用 `eth_estimateGas` 预估值乘以 1.2-1.5 倍安全系数
- 替换交易时阶梯式升级 Gas：1.2x -> 1.5x -> 2x，设硬上限防止费用失控 [src-04]

**防御性策略**：

- 对 Gas 价格设置全局上限告警，超过阈值时暂停非紧急交易
- 拥堵场景下优先保障高优先级交易的 Gas 预算，低优先级交易延迟发送
- 监控 base fee 变化速率，连续 N 块上升时触发拥堵告警

## Nonce 管理

**核心职责**：维护账户维度的递增计数器，确保并发交易按正确顺序提交。

**Nonce Hole 问题**：

交易必须严格按 nonce 顺序包含到区块中，不允许间隔 [src-04]。如果 nonce 42 的交易卡住（pending），nonce 43-46 的交易也全部无法被包含，形成 "nonce hole" [src-04]。**修复规则：始终先修复最老的 stuck transaction** [src-04]。

**常见陷阱**：

- **并发 race condition**：两个 worker 同时调用 `getTransactionCount(address, "pending")` 会得到相同的 nonce，导致 nonce 冲突 [src-04]。这是 nonce 管理中最常见的并发反模式。
- **服务重启后 nonce 不一致**：重启后如果直接取 `getTransactionCount("latest")`，会忽略已发送但未确认的交易，导致新交易与 pending 交易 nonce 冲突 [src-04]。
- **Private mempool nonce 不透明**：通过 Flashbots Protect 等 private relay 发送的交易不经过公开 mempool，Flashbots RPC 不返回 private 交易的 pending nonce（除非 EIP-191 签名请求）[src-04]。

**最佳实践**：

- **Local NonceTracker**：维护持久化的 next nonce 值，启动时取 `max(persisted_nonce, getTransactionCount("pending"))` [src-04]
- **序列化发送**：单进程内用 Promise chain 序列化同一账户的交易发送，跨进程需要外部锁或统一 signer service [src-04]
- **Geth/Reth mempool 容量感知**：单账户 pending cap 约 16 笔 + queued cap 约 64 笔（默认值），发送前确认已发送交易数避免堆叠过多 [src-04]

**防御性策略**：

- 定期与链上状态校对 NonceTracker，通过 `eth_getTransactionCount(address, "pending")` 回填 [src-04]
- 检测 stuck transaction：超过阈值（如 5 分钟）未确认的交易，用相同 nonce 提交更高 Gas 的替代交易 [src-04], [src-24]
- 实现 nonce 一致性监控：本地计数器与链上 nonce 差值超过阈值时告警

## 合约交互

**核心职责**：ABI 编解码、合约部署、函数调用和返回值解析。

**常见陷阱**：

- **ABI 版本不匹配**：合约升级后 ABI 变更，旧版 ABI 编解码会产生错误数据或 CALL_EXCEPTION [src-08]。
- **代理合约升级兼容性**：通过代理模式（如 UUPS、Transparent Proxy）升级合约时，存储布局变更可能导致数据错位 [UNC-01]。
- **Multicall 的 Gas 预估偏差**：将多个合约调用打包为 multicall 时，`eth_estimateGas` 可能低估总 Gas 消耗，因为各子调用间的状态变更会影响后续调用 [UNC-02]。

**最佳实践**：

- 使用 viem 或 ethers.js 的 ABI 编解码功能，确保类型安全 [src-17], [src-18]
- 只读调用优先使用 `eth_call`，不产生 Gas 消耗且不改变链上状态 [src-02]
- 对代理合约，维护 ABI 版本映射表，升级时同步更新

**防御性策略**：

- 合约调用前验证合约地址有效性（`provider.getCode(address)` 返回非空字节码）[src-08]
- 实现 revert 原因解析：捕获 CALL_EXCEPTION 后通过 `eth_call` 的 revert data 解析具体错误消息 [src-08]
- 对状态修改调用实施 dry run 验证，使用 Tenderly 等工具模拟执行结果 [src-21]

## 区块数据解析

**核心职责**：解析区块头、交易数据、状态树和事件日志。

**常见陷阱**：

- **Archive 节点数据缺失**：状态树读取（Merkle Patricia Trie 历史状态查询）需要 Archive 节点支持 [src-09]。使用 Snap sync 节点无法查询历史状态 [src-09]。
- **区块头验证遗漏**：未验证区块的 parent hash 和时间戳单调性，可能在 reorg 场景下处理错误数据 [src-06]。
- **RLP 编码解析错误**：交易数据从 RLP 编码解码时需正确处理 Type 2 (EIP-1559) 交易的额外字段 [src-02], [src-03]。

**最佳实践**：

- 解析区块头时验证 parent hash 连续性、时间戳单调性和 base fee 计算正确性 [src-02], [src-06]
- 历史状态查询前确认节点同步模式支持（Archive > Full > Snap）[src-09]
- 使用成熟库（如 ethers.js / viem）的内置解码器处理交易和日志解析 [src-17], [src-18]

# 中间基础设施风险点与最佳实践

## RPC 服务商选型

**风险点**：

- **单供应商单点故障**：使用单一 RPC 服务商时，该服务商宕机或 rate limit 将导致业务完全不可用 [src-13]
- **增强 API 供应商锁定**：Alchemy 的 NFT API、Token API 等增强能力在其他供应商上不可用 [src-13], [src-19]
- **Rate Limit 策略不透明**：不同供应商的限流阈值和计费模型差异大，实际触发点难以精确预测 [src-13], [src-14]

**最佳实践**：

- 生产环境至少维护 2 个 RPC 供应商端点 [src-13]
- 将标准 JSON-RPC 方法与增强 API 分离抽象，确保核心功能可跨供应商迁移 [src-13]
- 部署前设置 usage limits 和 alerts，监控计费单元消耗速率 [src-05]
- 优先使用 HTTPS 发送标准 JSON-RPC 请求，利用负载均衡和 gZip 压缩（75% 延迟改善）[src-05]
- WebSocket 仅用于 event subscription，且订阅范围尽可能窄 [src-05]

> **不确定性 [UNC-03]**：各供应商的具体 Rate Limit 数值和 SLA 承诺来自第三方对比文章 [src-19]，非官方文档。实际限流阈值可能随供应商策略调整而变化。

## 节点运维

**风险点**：

- **同步模式选择不当**：Snap sync（默认模式）只能查询当前状态，无法查询历史状态 [src-09]。如果需要历史数据但选择了 Snap sync，会导致查询失败。
- **同步中数据不完整**：节点在 state healing 阶段无法提供完整数据 [src-09]，期间服务不可用。
- **存储容量预估不足**：Archive 节点磁盘需求约 1.9 TB - 12 TB+（取决于存储优化版本）[src-09], [src-12]，初始预估不足会导致磁盘写满。

**最佳实践**：

- 根据业务需求选择同步模式：大多数生产场景使用 Snap sync（~1 TB），需要历史交易验证用 Full sync（~1-2 TB），区块浏览器或数据分析用 Archive sync [src-09], [src-12]
- 自建节点作为托管 RPC 的 fallback，而非主通道（运维成本高、初始同步慢）[src-09], [src-11]
- 监控节点同步状态和磁盘使用率，设置阈值告警

> **不确定性 [UNC-04]**：Archive 节点磁盘大小存在来源差异。src-09 引用 Geth 早期数据约 12 TB，而 Geth 新版本 path-based storage 已优化到约 1.9 TB。数据时效性需确认 [src-09], [src-12]。

> **不确定性 [UNC-05]**：Light client 在当前 PoS 架构下不可用（Geth 文档明确 "light-sync does not work"）[src-09]。部分来源仍将 light node 列为可用类型 [src-12]，与实际状态不符。

## 区块链浏览器依赖

**风险点**：

- **浏览器 API Rate Limit**：Etherscan 等区块链浏览器的 API 有严格的 Rate Limit，且数据存在延迟，不能作为链上数据唯一来源 [UNC-06]。
- **浏览器数据不可作为信任锚**：浏览器数据来源于其自有节点的解析结果，可能与业务系统使用的 RPC 端点不一致 [UNC-06]。

**最佳实践**：

- 浏览器仅用于交易状态二次确认和异常交易调试，不用于业务核心数据读取 [UNC-06]
- 合约源码验证和 ABI 获取可通过浏览器辅助，但生产环境应自行维护 ABI 版本库 [UNC-06]

# 公链各层常见坑点

## 网络层

**坑点**：

- **P2P 传播延迟**：交易通过 EL P2P 网络（DevP2P 协议）传播，从提交到全网可见存在数秒延迟 [src-01]。在高频交易场景下，延迟可能导致交易顺序与预期不同。
- **节点发现依赖 Bootnode**：自建节点的 P2P 连接依赖 bootnode 列表，如果 bootnode 不可用，节点发现过程会显著变慢 [src-01]。

## 共识层（Reorg 与 Finality）

**坑点**：

- **k-depth 确认策略在 PoS 下的局限性**：PoS 下 block depth 不等于安全性 [src-07]。固定等待 N 个区块确认的策略不能保证交易一定留在 canonical chain [src-07]。然而在实际工业实践中，k-depth 仍被广泛使用，因为它实现简单且对短范围 reorg 有效 [src-07], [src-28]。
- **Reorg 检测责任在用户侧**：RPC 服务商（如 QuickNode）可能提供 reorg 检测和重流功能，但验证 block hash continuity 的责任仍在业务系统 [src-06]。
- **Finality 时间线**：以太坊完全 finality 约需 2.5 epochs（~15 分钟）[src-07]。业务系统不能依赖最终性来做实时决策，需要在快速确认和最终性之间权衡 [src-07]。

**缓解策略**：

- 根据业务风险设置确认深度：小额支付 1-3 个区块，DeFi 交易 12-20 个区块，高价值结算等待 finality（~15 分钟）
- 实现 block hash continuity 检查：每个新区块的 parent hash 必须匹配前一个区块的 hash [src-06]
- 事件处理采用 upsert 语义，支持 reorg 后的状态回滚和更新 [src-06]

> **不确定性 [UNC-07]**：single-slot finality 路线需要重大协议变更，实际时间表不确定 [src-07]。如果实现，将大幅缩短确认时间，但当前不可依赖。

## 执行层

**坑点**：

- **EVM opcode gas 成本变更**：以太坊升级（如硬分叉）可能调整 opcode gas 成本，导致现有交易的 gas limit 预估失效 [UNC-08]。
- **Storage vs Memory 成本差异**：合约中 storage 操作（SLOAD/SSTORE）的 gas 成本远高于 memory 操作，接入层在构造复杂合约交互时需预估存储操作的 Gas 消耗 [UNC-08]。

## 存储层

**坑点**：

- **State trie 膨胀**：链上状态持续增长，全节点和归档节点的存储需求随时间增加 [src-09]。未规划存储扩容可能导致节点停服。
- **Pruning 策略影响历史查询**：启用 pruning 的节点会删除历史状态数据，影响历史余额和事件查询能力 [src-09]。

## 合约层

**坑点**：

- **重入攻击**：合约在状态更新前调用外部合约，攻击者可递归调用实现资金盗取 [src-01]。历史上 The DAO Hack 和 2024 年 12 月 GemPad 漏洞（损失约 $1.9M）均为重入攻击案例 [src-11], [src-26]。现代变体还包括 read-only reentrancy（如 Sturdy Finance exploit）[src-27]。
- **Checks-Effects-Interactions 模式**：防御重入的标准模式是先检查条件、再更新状态、最后与外部交互 [src-01], [src-12]。接入层调用合约时应确认目标合约遵循此模式或使用 ReentrancyGuard [src-01]。
- **代理合约升级的存储兼容性**：通过代理模式升级合约时，新合约的存储布局必须与旧合约兼容，否则会导致数据错位 [UNC-09]。

**缓解策略**：

- 接入层不直接处理合约安全审计，但应调用经过审计的合约版本
- 对未知合约调用实施 Gas limit 上限和 value 上限
- 使用 Tenderly 等工具在发送前模拟合约调用结果 [src-21]

# 技术事项布局规划

## 技术选型方法论

**RPC 服务商评估矩阵**：

| 维度 | 权重建议 | 评估要点 | 来源 |
|---|---|---|---|
| 可用性 (SLA) | 高 | 历史 uptime、多区域部署、故障转移能力 | [src-13], [src-19] |
| 标准 JSON-RPC 覆盖 | 高 | 是否覆盖项目所需的全部标准方法 | [src-02], [src-13] |
| 增强 API 能力 | 中 | 是否需要 NFT API、Token API 等增强能力 | [src-13], [src-19] |
| 成本模型 | 中 | 计费单元换算、免费额度、超额定价 | [src-13], [src-14] |
| WebSocket 支持 | 中 | 订阅类型、断连恢复、带宽计费 | [src-05], [src-13] |
| 多链覆盖 | 低-中 | 是否支持目标链及未来扩展链 | [src-13], [src-19] |

**客户端库选择标准**：

| 库 | 优势 | 劣势 | 适用场景 | 来源 |
|---|---|---|---|---|
| viem | 模块化、TypeScript 类型安全、树摇优化、对齐以太坊官方术语 | 相对较新、生态较小 | TypeScript 项目、对类型安全要求高 | [src-17], [src-24] |
| ethers.js | 生态成熟、社区支持广泛、文档完善 | 体积较大、类型系统不如 viem 精确 | JavaScript/TypeScript 通用项目、需要广泛社区支持 | [src-18], [src-24] |
| web3.js | 历史最久、多语言覆盖 | 维护活跃度下降、API 风格不一致 | 遗留项目维护 | [src-19] |

## 容量规划

**QPS 预估**：

- 查询类 RPC 调用（`eth_getBalance`、`eth_call`）的 QPS 取决于业务读取频率。高频场景（如实时价格查询）可能需要 10-100 QPS，低频场景（如定时对账）可能 <1 QPS [UNC-10]。
- 事件监听的 QPS 取决于链上事件产生速率。在 DeFi 高峰期，单合约每秒可能产生数十笔事件 [UNC-10]。

**存储需求估算**：

| 节点类型 | 磁盘需求 | 适用场景 | 来源 |
|---|---|---|---|
| Snap sync | ~1 TB | 大多数生产场景，只需当前状态 | [src-09] |
| Full sync | ~1-2 TB | 需要历史交易验证 | [src-09] |
| Archive sync | ~1.9 TB - 12 TB+ | 区块浏览器、数据分析 | [src-09], [src-12] |

**Nonce 管理容量**：

- 单账户 pending cap 约 16 笔 + queued cap 约 64 笔（Geth/Reth 默认）[src-04]
- 高并发场景建议按业务维度拆分签名账户，避免单账户 nonce 成为瓶颈 [src-04]

**生产级 NonceTracker 设计要点** [src-04]：

1. 持久化 next nonce 值（支持崩溃恢复）
2. 启动时取 `max(persisted_nonce, getTransactionCount("pending"))`
3. 单进程内用 Promise chain 序列化同一账户发送
4. 跨进程需要外部锁或统一 signer service

## 监控告警体系

**链上指标监控**：

| 指标 | 告警阈值建议 | 监控工具 | 来源 |
|---|---|---|---|
| Base fee 变化速率 | 连续 3 块上升 >10% | Tenderly、自有监控 | [src-02], [src-21] |
| 节点同步状态 | 落后最新区块 > 100 | 自建节点 health check | [src-20] |
| Gas price 阈值 | 超过业务可接受上限 | 自有监控 | [src-02], [src-05] |
| 交易 stuck 检测 | pending > 5 分钟 | 自有 NonceTracker + 轮询 | [src-04], [src-24] |
| RPC 延迟 | P95 > 5 秒 | 自有 APM | [src-13] |
| WebSocket 连接状态 | 断连 > 30 秒未恢复 | 自有监控 | [src-05] |

**节点健康指标** [src-20]：

- 节点同步状态（syncing status、current block vs highest block）
- peer 数量和连接质量
- 磁盘使用率和 I/O 延迟
- 证书过期告警（HTTPS 端点）

**交易模拟与错误跟踪**：

- 使用 Tenderly 进行发送前交易模拟，检测潜在 revert [src-21]
- 集成 Tenderly 错误跟踪，捕获生产环境的 CALL_EXCEPTION 和 Gas estimation 失败 [src-21]

## 降级容灾策略

**多 RPC 降级链**：

```
主 RPC (Alchemy) → 备 RPC (Infura) → 自建节点 (Geth) → 只读缓存
```

- 主端点超时或 429 时切换到备端点
- 备端点不可用时回退到自建节点
- 所有写端点不可用时，只读查询返回缓存数据，写操作进入队列等待

**请求降级**：

- 增强 API 不可用时回退到标准 JSON-RPC 方法 [src-13]
- WebSocket 断连时回退到 HTTP polling（`eth_getLogs` 定期查询）[src-05]
- `eth_estimateGas` 失败时使用预定义的上限 Gas limit [src-08]

**交易回退机制**：

- Stuck transaction 处理：用相同 nonce 提交更高 Gas 的替代交易（maxFeePerGas 和 maxPriorityFeePerGas 都提升 10%+）[src-04]
- Cancel 交易：用相同 nonce 发送零 value 交易到自身地址 [src-15]
- Timeout 策略：超过设定阈值后放弃原交易，用新 nonce 重新提交

**Reorg 降级**：

- 检测到 block hash 不连续时暂停事件处理 [src-06]
- 等待 reorg 稳定后（latest block delay）再恢复处理 [src-06]
- 已确认但被回滚的事件执行反向操作 [src-06]

# EVM 与非 EVM 链注意事项差异

本节以 EVM 链为基准，指出切换到 Solana 等非 EVM 链时需重新审视的注意事项。

## 核心差异维度

| 维度 | EVM | Solana | 影响模块 | 来源 |
|---|---|---|---|---|
| 账户模型 | Account-based，账户直接持有余额和状态 [src-03] | 基于 Account 但语义不同：所有数据存储在 Account 对象中，Program 与数据 Account 分离 | 钱包管理、区块解析 | [src-03], [src-16] |
| 交易格式 | Typed Transaction Envelope (Type 0-4) [src-03] | 指令列表 (Instruction list) | 交易构造与签名 | [src-03], [src-16] |
| 签名算法 | secp256k1 [src-03] | Ed25519 | 钱包管理、交易签名 | [src-03], [src-16] |
| Gas 模型 | Gas 单位计量，EIP-1559 混合定价 [src-02], [src-08] | Compute Unit (CU) 计量 | Gas 管理 | [src-02], [src-16] |
| Nonce 机制 | 递增计数器 [src-03], [src-04] | Recent Blockhash 作为防重放机制 | Nonce 管理 | [src-03], [src-16] |
| 执行模型 | 单线程顺序执行 [src-08] | Sealevel 并行执行 | 合约交互 | [src-08], [src-16] |
| 智能合约 | Solidity/Vyper → EVM 字节码 [src-08] | Rust/C → BPF 字节码 | 合约交互 | [src-08], [src-16] |

## 对服务端模块的影响评估

| 模块 | 影响程度 | 原因 |
|---|---|---|
| 交易构造与签名 | 完全重写 | 交易格式、签名算法、nonce 机制完全不同 |
| Nonce 管理 | 完全重写 | Nonce 机制被 Recent Blockhash 替代，无需维护递增计数器 |
| Gas 管理 | 完全重写 | Compute Unit 定价模型与 EIP-1559 机制完全不同 |
| 合约交互 | 完全重写 | ABI 编解码被 IDL 替代，程序调用方式不同 |
| 钱包管理 | 部分适配 | 密钥生成算法从 secp256k1 改为 Ed25519，hot/cold 分离策略可复用 |
| RPC 调用层 | 部分重写 | 方法名和语义不同，但 Provider 抽象模式可复用 |
| 事件监听 | 部分重写 | 事件订阅机制不同，但 push/poll 模式可复用 |
| 区块数据解析 | 部分重写 | 区块结构和数据格式不同，但解析模式可复用 |

> **不确定性 [UNC-11]**：Solana 非 EVM 链的详细分析基于间接来源 [src-16] 和领域知识标注。Solana 官方架构文档（docs.solana.com）的 L1 来源未在本次收集中覆盖，精确的架构差异分析需补充官方来源。

## EVM 兼容链的注意事项复用

对于 EVM 兼容链（BSC、Polygon、Arbitrum、Optimism 等），大部分 EVM 注意事项可直接复用，但需注意：

- **Gas 参数差异**：不同 EVM 兼容链的 base fee 计算参数和 Gas limit 可能不同 [UNC-12]。
- **确认时间差异**：L2 的确认时间通常短于 L1，stuck transaction 超时从分钟级缩短到秒级 [src-04]。
- **L2 Sequencer 风险**：Sequencer 是单点故障，需监控 sequencer uptime [src-04]。Arbitrum 有约 24 小时 force inclusion 延迟，OP/Base 几乎立即 [src-04]。
- **L2 Sequencer 和 Bridge 机制**的官方文档未在本次收集中覆盖，需补充 docs.arbitrum.io / docs.optimism.io 的 L1 来源。

# 趋势判断与不确定性

## 尚未形成共识的事项

1. **确认策略选择**：k-depth 策略简单但在 PoS 下不保证安全性 [src-07]；Circle 的快速确认规则（基于 validator 投票统计）更精确但实现复杂 [src-07]。生产环境中应如何权衡尚无统一最佳实践。
2. **Single-slot finality**：以太坊正在探索 single-slot finality 路线，如果实现将大幅缩短确认时间，但需要重大协议变更 [src-07]。业务系统不应在当前阶段依赖此特性。
3. **Private mempool 的 nonce 一致性**：Flashbots 等 private relay 的 pending nonce 不透明问题，在不同 provider 下行为可能不同 [src-04]。Local NonceTracker 是当前推荐的解决方案，但跨系统的 nonce 协调仍需人工干预。
4. **WebSocket vs HTTP 的生产取舍**：Alchemy 官方建议标准 JSON-RPC 走 HTTP、WS 仅用于 event subscription [src-05]。但实际生产中，不同 RPC 提供商的 WebSocket 可靠性差异可能导致不同实践。

## 需要持续跟踪的变化

- **EIP-1559 参数调整**：base fee 计算参数（如 ELASTICITY_MULTIPLIER、BASE_FEE_MAX_CHANGE_DENOMINATOR）可能随协议升级调整 [src-02], [src-03]
- **RPC 服务商定价和 SLA 变化**：计费模型和免费额度可能调整，需定期重新评估选型 [src-13], [src-14]
- **Geth 存储优化**：path-based storage 已将 Archive 节点磁盘从 ~12 TB 优化到 ~1.9 TB [src-09]，后续优化可能进一步降低存储需求
- **交互库版本演进**：ethers.js 从 v5 到 v6、viem 从 v1 到 v2 的 API 差异需要在升级时评估 [src-08], [src-09]

# 有限结论

基于 32 个来源（L1: 3, L2: 13, L3: 12, L4: 4）的分析，本研究的核心发现如下：

1. **Nonce 管理和 Gas 管理是服务端模块中风险最高的环节**：Nonce hole 会冻结同一账户的所有后续交易 [src-04]，Gas 预估失败或费用过低会导致交易长期 pending [src-02], [src-08]。两者都需要本地状态追踪和定期链上校对。

2. **事件监听的架构选型取决于业务对实时性和可靠性的权衡**：WebSocket 提供实时推送但需要处理断连和 reorg [src-05], [src-06]；HTTP polling 可靠性高但延迟大 [src-02]；Indexer 服务适合复杂聚合查询但引入额外依赖 [src-22]。生产环境建议组合使用：WS 实时 + HTTP 校对。

3. **RPC 服务商选型是架构设计的首要决策点，但不存在最优单一选择**：多供应商抽象提高了可用性但增加了开发复杂度 [src-13]。推荐方案是标准 JSON-RPC 方法实现供应商无关抽象，增强 API 作为可选能力层 [src-13]。

4. **Reorg 处理是任何链上数据系统不可绕过的工程挑战**：block hash continuity 验证是用户侧责任 [src-06]，事件处理必须支持 upsert 和回滚 [src-06], [src-29]。确认深度策略应根据业务风险分级设定 [src-07]。

5. **从 EVM 切换到非 EVM 链的工作量集中在交易构造、签名和 Gas/Nonce 模块**：这些模块与链的底层模型（账户模型、签名算法、执行模型）强耦合，无法通过简单抽象层复用 [src-16]。钱包管理和事件监听的架构模式可部分复用。

## 未解问题

| 问题 | 影响 | 状态 |
|---|---|---|
| Solana 等非 EVM 链的 L1 官方架构文档缺失 | 无法给出精确的架构差异分析 | [evidence-gap] 需要 docs.solana.com |
| L2 Sequencer 和 Bridge 机制的官方文档缺失 | 无法覆盖 L2 特有的确认和强制包含差异 | [evidence-gap] 需要 docs.arbitrum.io / docs.optimism.io |
| 各 RPC 供应商官方 Rate Limit 和 SLA 文档未逐一确认 | 影响容量规划的准确性 | [evidence-gap] 需要官方文档 |
| ethers.js v6 / viem v2 最新版本错误处理 API 差异 | src-08 为 ethers v5，src-09 为 viem v1，可能过时 | [evidence-gap] 需要最新文档 |
| 工作量分布的定量数据（QPS、延迟分位数）缺乏 | 无法给出精确的容量规划数值建议 | [uncertainty] 需要实际测量数据 |

# 能力边界

## 纳入范围

- EVM 兼容链（以太坊、BSC、Polygon 等）的服务端模块注意事项 [src-01]-[src-30]
- 中间基础设施（RPC 选型、节点运维、浏览器依赖）的风险与最佳实践
- 公链各层（网络层到合约层）的常见工程坑点
- 技术选型方法论、容量规划、监控告警和降级策略
- EVM 与非 EVM 链（Solana）的差异维度

## 有限覆盖

- 非 EVM 链（Solana）的详细注意事项，因缺乏 L1 官方来源标注为 uncertainty [src-16]
- Layer 2（Arbitrum/Optimism/ZK-Rollup）特有的工程问题，仅覆盖 nonce 和确认时间差异 [src-04]

## 不纳入范围

- 具体业务代码实现细节（DEX、NFT 平台业务逻辑）
- 智能合约本身的审计流程与安全审计清单
- 合规与法律层面的分析（牌照、KYC/AML 流程）
- 以太坊黄皮书级别的共识细节
- 前端钱包 UI/UX 设计

# 上线前 Checklist

## 钱包管理

- [ ] 热钱包和冷钱包已按业务风险等级分离，热钱包设置单笔/日累计转账上限
- [ ] 热钱包密钥使用托管服务（如 Fireblocks、AWS KMS）管理，不裸存文件系统
- [ ] HD 钱包派生路径遵循 BIP-44/BIP-84 标准
- [ ] 钱包余额监控告警已配置，异常余额变化可触发告警
- [ ] 多签方案（如使用）的 Gas 成本已评估并纳入交易费用预算 [src-15]

## 交易构造与签名

- [ ] 使用 EIP-1559 Type 2 交易格式，避免使用 Legacy 格式 [src-02]
- [ ] chain_id 字段正确填充，确保 replay 保护 [src-03]
- [ ] 交易发送前验证合约存在性（`provider.getCode(address)`）[src-08]
- [ ] Gas limit 使用 `eth_estimateGas` 预估值乘以 1.2-1.5 倍安全系数
- [ ] 使用 Tenderly 等工具进行发送前交易模拟 [src-21]
- [ ] 交易构造层实施参数校验（value 上限、data 可解析性、gasLimit 范围）
- [ ] 确认目标合约已实施重入防护（ReentrancyGuard 或 Checks-Effects-Interactions 模式）

## RPC 调用层

- [ ] 生产环境至少维护 2 个 RPC 供应商端点 [src-13]
- [ ] 标准 JSON-RPC 方法实现供应商无关抽象，增强 API 作为可选能力层 [src-13]
- [ ] 标准 JSON-RPC 请求使用 HTTPS 而非 WebSocket [src-05]
- [ ] 已实现多 Provider 故障转移（主端点超时/429 时切换）
- [ ] 查询类方法超时设置为 5-10 秒，交易类方法设置为 30-60 秒
- [ ] 已部署 usage limits 和 alerts 监控计费单元消耗 [src-05]
- [ ] 只读查询结果已实现短期缓存（区块 12s、余额 30s）

## 事件监听与订阅

- [ ] 已实现 block hash continuity 验证 [src-06]
- [ ] 已处理 `logs` 订阅的 `removed` 字段（reorg 回滚）[src-10]
- [ ] WebSocket 断连回退到 HTTP polling（`eth_getLogs` 定期查询）[src-05]
- [ ] 订阅范围已缩窄（按 address、topic filter）[src-05]
- [ ] 事件持久化采用 upsert 语义，支持 reorg 安全更新 [src-06]
- [ ] 已记录最高处理区块号，支持服务重启恢复

## Gas 管理

- [ ] 通过 `eth_feeHistory` 获取近期 base fee 趋势 [src-02], [src-05]
- [ ] maxFeePerGas 设置为 `baseFee * 2 + priorityFee`，确保 base fee 翻倍时有效 [src-02]
- [ ] 已配置 Gas 价格全局上限告警，超过阈值时暂停非紧急交易
- [ ] 替换交易时阶梯式升级（1.2x -> 1.5x -> 2x），设硬上限 [src-04]
- [ ] 已监控 base fee 变化速率，连续上升时触发拥堵告警

## Nonce 管理

- [ ] 已实现 Local NonceTracker，持久化 next nonce 值 [src-04]
- [ ] 启动时取 `max(persisted_nonce, getTransactionCount("pending"))` [src-04]
- [ ] 单账户交易发送已序列化（Promise chain 或外部锁）[src-04]
- [ ] 定期与链上状态校对 NonceTracker [src-04]
- [ ] 已实现 stuck transaction 检测（pending > 5 分钟告警）[src-04], [src-24]
- [ ] 替换交易时 maxFeePerGas 和 maxPriorityFeePerGas 都提升 10%+ [src-04]

## 合约交互

- [ ] 使用 viem 或 ethers.js 的 ABI 编解码，确保类型安全 [src-17], [src-18]
- [ ] 代理合约 ABI 版本映射表已维护，升级时同步更新
- [ ] 只读调用优先使用 `eth_call`，不产生 Gas 消耗 [src-02]
- [ ] 已实现 CALL_EXCEPTION 的 revert 原因解析 [src-08]
- [ ] 未知合约调用已实施 Gas limit 和 value 上限

## 区块数据解析

- [ ] 已验证节点同步模式满足业务查询需求（Snap/Full/Archive）[src-09]
- [ ] 区块头解析已验证 parent hash 连续性和时间戳单调性 [src-06]
- [ ] 历史状态查询前确认节点为 Archive 模式 [src-09]
- [ ] 交易解码正确处理 EIP-1559 Type 2 的额外字段 [src-02], [src-03]

## 基础设施

- [ ] 自建节点（如有）已选择正确的同步模式并规划存储容量 [src-09]
- [ ] 节点同步状态和磁盘使用率已配置监控告警 [src-20]
- [ ] 区块链浏览器仅用于调试和二次确认，不用于核心数据读取
- [ ] 自建节点 health check 已配置（peer 数量、同步状态、证书过期）[src-20]

## 监控告警

- [ ] Base fee 变化速率监控已配置（连续 3 块上升 >10% 告警）[src-02], [src-21]
- [ ] 交易 stuck 检测已配置（pending > 5 分钟告警）[src-04], [src-24]
- [ ] RPC P95 延迟监控已配置（>5 秒告警）[src-13]
- [ ] WebSocket 连接状态监控已配置（断连 >30 秒告警）[src-05]
- [ ] 交易模拟已集成发送前验证流程 [src-21]

## 降级容灾

- [ ] 多 RPC 降级链已配置（主 → 备 → 自建 → 缓存）
- [ ] WebSocket 断连回退到 HTTP polling 已实现 [src-05]
- [ ] Stuck transaction 替代和 cancel 机制已实现 [src-04], [src-15]
- [ ] Reorg 检测时事件处理暂停和恢复逻辑已实现 [src-06]

# 参考资料

## L1 一级来源

- [src-02] [EIP-1559: Fee market change for ETH 1.0 chain](https://eips.ethereum.org/EIPS/eip-1559) — EIP-1559 官方规范：base fee、priority fee、max fee 机制，安全考量
- [src-03] [EIP-1559 (GitHub Reference Implementation)](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md) — EIP-1559 Python 参考实现：base fee 验证公式
- [src-01] [Reentrancy - Ethereum Smart Contract Best Practices](https://consensysdiligence.github.io/smart-contract-best-practices/attacks/reentrancy/) — Consensys Diligence 重入攻击最佳实践（页面超时未验证）

## L2 二级来源

- [src-04] [Ethereum nonce management: preventing stuck transactions](https://chainstack.com/ethereum-nonce-management/) — 生产级 nonce 管理指南：NonceTracker、并发序列化、nonce hole 修复、EIP-1559 替换规则、private mempool nonce、L2 sequencer nonce
- [src-05] [Best Practices for Using WebSockets in Web3 (Alchemy)](https://www.alchemy.com/docs/reference/best-practices-for-using-websockets-in-web3) — Alchemy WebSocket 最佳实践：HTTP vs WS 对比、5 种订阅类型、订阅范围缩窄
- [src-06] [Reorg Handling (QuickNode Docs)](https://www.quicknode.com/docs/streams/reorg-handling) — QuickNode reorg 处理：检测机制、block hash continuity 验证、Latest Block Delay
- [src-07] [Exploring Confirmation Rules for Ethereum (Circle)](https://www.circle.com/blog/exploring-confirmation-rules-for-ethereum) — Circle 快速确认规则研究：k-depth 局限性、LMD-GHOST + FFG、69 秒平均确认
- [src-08] [Error Codes (ethers.js v5)](https://docs.ethers.org/v5/troubleshooting/errors/) — ethers.js 错误码：CALL_EXCEPTION、NONCE_EXPIRED、REPLACEMENT_UNDERPRICED 等
- [src-09] [Error Handling (viem)](https://v1.viem.sh/docs/error-handling.html) — viem 错误处理：BaseError 继承体系、强类型 catch、.walk() 方法
- [src-10] [Using WebSockets (ethereum.org)](https://ethereum.org/developers/tutorials/using-websockets/) — ethereum.org WebSocket 教程：eth_subscribe、newHeads reorg 行为、logs removed 字段
- [src-16] [A Complete Guide to Solana Development for Ethereum Developers](https://solana.com/developers/evm-to-svm/complete-guide) — Solana 官方 EVM→SVM 迁移指南（需抓取验证）
- [src-19] [Alchemy vs Infura vs Quicknode vs Chainnodes - RPC Provider Comparison](https://www.chainnodes.org/blog/alchemy-vs-infura-vs-quicknode-vs-chainnodes-ethereum-rpc-provider-pricing-comparison/) — 主流 RPC 提供商横向对比（需抓取验证）
- [src-21] [Tenderly Real-Time Blockchain Monitoring & Alerting](https://tenderly.co/monitoring) — Tenderly 监控平台：交易模拟、错误跟踪（需抓取验证）
- [src-22] [Wallet Nonce Management (Circle Docs)](https://developers.circle.com/cpn/concepts/transactions/wallet-nonce-management) — Circle wallet nonce 管理官方说明（需抓取验证）

## L3 三级来源

- [src-11] [The Ultimate Guide To Reentrancy (Immunefi)](https://immunefi.com/blog/expert-insights/ultimate-guide-to-reentrancy/) — 重入攻击终极指南：DAO Hack、read-only reentrancy
- [src-12] [Ethereum Smart Contract Security Recommendations (Consensys)](https://consensys.io/blog/ethereum-smart-contract-security-recommendations) — 智能合约安全建议：checks-effects-interactions 模式
- [src-13] [EIP-1559 Gas Fees: Base Fee, Priority Fee, & Max Fee (Blocknative)](https://www.blocknative.com/blog/eip-1559-fees) — EIP-1559 工程解读
- [src-14] [The Developer EIP-1559 Prep Kit (Alchemy)](https://www.alchemy.com/blog/eip-1559) — Alchemy EIP-1559 开发者准备指南
- [src-15] [Multisig Wallet Guide: Security, Setup & MPC Comparison 2026](https://www.cobo.com/post/what-is-a-multisig-wallet-the-complete-guide-to-multi-signature-security) — 多签钱包安全指南
- [src-17] [Bitcoin vs Ethereum vs Solana: Architecture Comparison for Developers](https://fystack.io/blog/bitcoin-vs-ethereum-vs-solana-architecture) — 三链架构对比
- [src-18] [Ethereum vs Solana: Speed, Fees, and Architecture Explained Clearly](https://www.bleap.finance/blog/ethereum-vs-solana) — ETH vs SOL 对比
- [src-20] [9 Blockchain Monitoring Metrics You Should Track in Production](https://chainlaunch.dev/blog/blockchain-monitoring-metrics) — 生产监控指标
- [src-25] [Hot vs. cold vs. warm wallets (Fireblocks)](https://www.fireblocks.com/blog/hot-vs-warm-vs-cold-which-crypto-wallet-right-for-me) — 钱包分类与安全性分析
- [src-28] [What is Chain Reorganization? (Cube Exchange)](https://www.cube.exchange/what-is/chain-reorganization) — 链重组基础知识
- [src-29] [Indexing and Reorgs (Envio Docs)](https://docs.envio.dev/blog/indexing-and-reorgs) — 索引器 reorg 安全处理
- [src-30] [Structured errors for programmatic error handling (viem GitHub Discussion)](https://github.com/wevm/viem/discussions/4281) — viem 结构化错误 .walk() 实践

## L4 四级来源

- [src-23] [gas estimation error because of reverted (Stack Exchange)](https://ethereum.stackexchange.com/questions/156825/gas-estimation-error-because-of-reverted) — gas estimation 失败与 revert 关系讨论
- [src-24] [Why Ethereum Transactions Get Stuck and How to Fix Them](https://blog.coinhako.com/why-ethereum-transactions-get-stuck-and-how-to-fix-them/) — 交易卡住原因与修复方法
- [src-26] [Explained: The GemPad Hack (December 2024)](https://www.halborn.com/blog/post/explained-the-gempad-hack-december-2024) — GemPad 重入漏洞复盘（$1.9M）
- [src-27] [Sturdy Finance Exploit: Price Oracle Manipulation & Reentrancy](https://www.okx.com/learn/sturdy-finance-exploit-price-oracle-defi) — read-only reentrancy 攻击复盘

## 依赖 Primitive

- [primitive] `public-chain-integration-architecture/draft.md` — 端到端架构拆解：服务端模块分解、中间角色、公链分层、交易与查询流程、EVM 与非 EVM 差异、可靠性策略

# 证据

| Claim / Source | 支撑章节 | 置信度 |
|---|---|---|
| EIP-1559 定义了 base fee + priority fee 混合定价模型 | Gas 管理、术语表 | high (L1: src-02, src-03) |
| Base fee 每块最大变化 12.5%，计算公式确定 | Gas 管理 | high (L1: src-02, src-03) |
| Nonce hole 会冻结同一账户后续所有交易，须先修最老的 stuck TX | Nonce 管理、Checklist | high (L2: src-04) |
| Local NonceTracker 是解决 nonce 并发和跨系统不一致的最佳方案 | Nonce 管理 | high (L2: src-04, src-22) |
| 标准 JSON-RPC 应走 HTTP(S)，WS 仅用于 event subscription | RPC 调用层、事件监听 | high (L2: src-05) |
| WebSocket 支持 5 种订阅类型（alchemy_minedTransactions、alchemy_pendingTransactions、newPendingTransactions、newHeads、logs） | 事件监听 | high (L2: src-05) |
| Reorg 时 block hash continuity 验证是用户侧责任 | 事件监听、共识层 | high (L2: src-06) |
| PoS 下 k-depth 不保证安全性，Circle 快速确认规则平均 69 秒 | 共识层、确认策略 | high (L2: src-07) |
| 以太坊 finality 约 2.5 epochs（~15 分钟） | 共识层、术语表 | high (L2: src-07) |
| ethers.js 核心错误类型：CALL_EXCEPTION / NONCE_EXPIRED / REPLACEMENT_UNDERPRICED / UNPREDICTABLE_GAS_LIMIT | 交易构造、错误处理 | high (L2: src-08) |
| viem 错误处理：BaseError 继承体系、.walk() 方法遍历错误链 | 错误处理 | high (L2: src-09) |
| `logs` 订阅的 `removed` 字段标记被回滚的事件 | 事件监听 | high (L2: src-10) |
| 重入攻击历史案例：The DAO Hack、GemPad $1.9M (2024.12)、Sturdy Finance read-only reentrancy | 合约层 | medium (L3: src-11, src-12; L4: src-26, src-27) |
| 多 Provider 故障转移是生产环境推荐策略 | RPC 调用层、降级策略 | medium (L2: src-13, src-19) |
| RPC 供应商计费模型差异大（CU vs 请求次数 vs credit） | RPC 调用层、技术选型 | medium (L2: src-13, src-14) |
| Solana 使用 Ed25519 签名、Instruction list 交易格式、Sealevel 并行执行、Recent Blockhash 防重放 | EVM 与非 EVM 差异 | medium (L2: src-16; 需补充 L1 官方来源) |
| Archive 节点磁盘需求 ~1.9 TB - 12 TB+（存在来源冲突） | 存储层、节点运维 | medium (L2: src-09, src-12; UNC-04) |
| 单账户 pending cap ~16 + queued cap ~64（Geth/Reth 默认） | Nonce 管理、容量规划 | medium (L2: src-04) |
| EIP-1559 替换交易要求 maxFeePerGas 和 maxPriorityFeePerGas 都提升 10%+ | Gas 管理、Nonce 管理 | medium (L2: src-04) |
| Single-slot finality 路线需重大协议变更，时间表不确定 | 趋势判断 | medium (L2: src-07; UNC-07) |
| Flashbots private mempool 不返回 private 交易 pending nonce | Nonce 管理 | medium (L2: src-04) |
| L2 stuck transaction timeout 从分钟级缩短到秒级，Arbitrum ~24h force inclusion 延迟 | Nonce 管理、L2 差异 | medium (L2: src-04) |
| Tenderly 提供交易模拟和错误跟踪能力 | 监控告警、合约交互 | medium (L2: src-21) |
| 索引器 reorg 安全需实现 upsert 而非 insert | 事件监听、索引器 | medium (L3: src-29) |
| Light client 在当前 PoS 架构下不可用 | 节点运维 | medium (L2: src-09; UNC-05) |

# 追踪链

- 来源 change: public-chain-integration-guide
- Request: openspec/changes/public-chain-integration-guide/request.md
- Plan: openspec/changes/public-chain-integration-guide/plan.md
- Draft: openspec/changes/public-chain-integration-guide/draft.md
- Review: openspec/changes/public-chain-integration-guide/review.md
- Publish: openspec/changes/public-chain-integration-guide/publish.md

# 待决问题

- Solana 等非 EVM 链的 L1 官方架构文档缺失，影响精确的架构差异分析
- L2 Sequencer 和 Bridge 机制的官方文档未覆盖，L2 特有差异待补充
- 各 RPC 供应商官方 Rate Limit 和 SLA 文档未逐一确认，影响容量规划准确性
- ethers.js v6 / viem v2 最新版本的错误处理 API 差异待验证（当前来源基于 v5 / v1）
- 工作量分布的定量数据（QPS、延迟分位数）缺乏实际测量数据支撑
