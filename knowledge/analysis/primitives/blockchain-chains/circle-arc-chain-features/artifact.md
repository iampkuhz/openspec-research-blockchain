---
title: "Circle ARC 链特性增强与链层优化"
type: knowledge_primitive
source_change: circle-arc-chain-features
published_at: "2026-04-27"
---

# Circle ARC 链特性增强与链层优化

## 概述

Circle ARC 是由 Circle 从头构建的开放 Layer-1 区块链，专为稳定币金融设计 [S1]。与以太坊、Solana 等通用链不同，ARC 定位于金融基础设施，将支付、外汇、结算和通证化资产等金融原语直接内建到协议层 [S1, S5]。ARC 是 EVM 兼容的，支持现有以太坊工具和 Solidity 智能合约开箱即用 [S1, S5]。

ARC 的设计哲学可以概括为一句话：**让链上资金的行为与企业期望的确定性和成本可控性匹配** [S5]。围绕这一目标，ARC 在链层面做了以下核心特性增强：

---

## 一、共识算法优化：Malachite 与确定性亚秒最终性

### 1.1 Malachite 共识引擎

ARC 采用名为 **Malachite** 的高性能共识引擎，基于 Tendermint 类 BFT（拜占庭容错）协议 [S2, S5]。Malachite 由 Informal Systems 团队开发，该团队已正式加入 Circle [S1, S2]。

核心设计：
- **确定性最终性**（Deterministic Finality）：当超过 2/3 的验证者提交区块后，交易立即且不可变地最终确定 [S2]
- **无分叉重组风险**：与以太坊的概率最终性（~14 分钟经济最终性）和比特币的概率最终性（~1 小时）不同，ARC 上的交易要么未确认，要么最终确定，没有中间状态 [S2]
- **Proof-of-Authority（PoA）验证者集**：由已知机构组成的许可验证者集，满足运营和合规要求 [S2, S5]

### 1.2 性能指标

| 配置 | TPS | 最终性时间 | 来源 |
|------|-----|-----------|------|
| 20 验证者（10 地理区域，商用硬件） | ~3,000 | < 350ms | [S2, S6, S11] |
| 4 验证者 | ~10,000 | < 100ms | [S2] |

20 验证者配置下，ARC 每日可处理的交易量是 Fedwire 资金服务的约 **280 倍** [S2]。

### 1.3 共识路线图

- **多提议者支持**（Multi-proposer）：利用并行化将吞吐提升约 **10 倍** [S2, S5]
- **降低容错配置**：延迟降低约 **30%** [S2]
- **从 PoA 向许可 PoS 演进**：在合格验证者集中引入质押、削减和轮换规则 [S5]

### 1.4 与传统链对比

| 网络 | 最终性时间 | 最终性类型 | 分叉重组风险 |
|------|-----------|-----------|-------------|
| ARC | ~1s | 确定性 | 无 |
| Ethereum PoS + L2s | ~14m | 经济最终性 | 低但非零 |
| Bitcoin | ~1h | 概率最终性 | 非零 |

---

## 二、出块性能优化

ARC 的亚秒出块优化直接源于 Malachite 共识的设计选择：

- **平滑出块节奏**：不像以太坊那样依赖 slot/epoch 层级结构调整，ARC 的区块提交由 BFT 共识直接驱动，出块节奏由共识消息复杂度而非定时器决定 [S2, S5]
- **端到端延迟优化**：确定性最终性将"确认管理"从复杂的应用层关注点简化为二元事件（确认/未确认） [S5]
- **执行与共识分离**：EVM 执行层与共识核心解耦，EVM 执行、mempool 传输和客户端签名/广播的开销不影响共识层的最终性保证 [S5]

---

## 三、Gas 模型与费用优化

### 3.1 USDC 作为原生 Gas 代币

ARC 最大的创新之一是使用 **USDC 作为原生 Gas 代币**，而非传统的波动性原生代币（如 ETH、SOL） [S1, S3, S5]。

解决的问题：
- 企业无需持有波动性加密资产来支付 Gas [S1]
- 费用和账单使用同一计价单位（美元稳定币），简化会计和税务处理 [S5]
- 基础设施预算可以以美元为单位保持稳定 [S3, S5]

### 3.2 EIP-1559 改进

ARC 的费用模型基于以太坊的 EIP-1559 架构，但做了关键改进 [S19]：

- **平滑基础费更新**：不使用逐块跳跃的基础费，协议基于近期利用率使用**加权移动平均**平滑函数更新 [S3, S19]
  - 结果：更低抖动，短期需求峰值时费用更少意外波动
- **边界与策略杠杆**：协议可设置上下限和显式策略（如优先通道、量级定价） [S3, S5]
- **Treasury sink**：费用收集到链上金库，用于生态增长或治理重定向 [S5]

### 3.3 Paymaster 抽象

虽然 USDC 是原生 Gas 资产，ARC 实现了基于 **ERC-4337** 的 Paymaster 抽象 [S5, S8]：
- 允许费用以其他法币挂钩代币（如 EURC）赞助或支付 [S5]
- 在 ARC 上，由于 USDC 本身就是默认费用代币，Paymaster 使得**非 USDC 代币**也能支付 Gas [S8]

---

## 四、预置服务：FX Engine、DEX 与 Token 标准

### 4.1 内置 StableFX 引擎（链上外汇引擎）

ARC 内置了一个**机构级 RFQ（Request-for-Quote，报价请求）外汇引擎** [S1, S10]：

- 支持稳定币对之间的价格发现和 24/7 PvP（Payment-versus-Payment）链上结算 [S1, S5]
- 做市商可通过链下 RFQ 层高效报价 [S5]
- 早期阶段为许可模式以维护市场完整性；长期目标是变为无许可协议，同时保持强结算保证 [S5]
- 支持配置结算窗口、交易注册、抵押品管理 [S5]

**注意**：ARC 并非内置传统意义上的 AMM DEX（如 Uniswap），而是内置了**机构级 RFQ/订单簿外汇引擎**，专注于支付和外汇场景。普通 DEX 功能由生态 dApp 在 EVM 兼容层上构建。

### 4.2 预置 Token 标准

ARC 在协议层原生支持以下资产：
- **USDC**：原生 Gas 代币和主要结算资产 [S1]
- **EURC**：欧元稳定币，通过 Paymaster 可作为 Gas [S1, S5]
- **USYC**：Day-1 原生资产，通证化短期国债（Hashnote International Short Duration Fund） [S1]

这些资产直接内建在协议层，而非通过第三方合约部署 [S5]。ARC 支持通证化证券、大宗商品和结构化产品等金融工具 [S1]。

### 4.3 协议级金融原语

ARC 将以下金融原语作为一等协议特性：
- **结构化元数据**：转账可附加发票号、采购订单 ID、备忘录，用于自动对账 [S5]
- **退款和争议流**：与主流商业消费者保护对齐 [S5]
- **策略驱动的金库代理**：自动现金管理、跨币种再平衡、维持缓冲区、扫入收益工具 [S5]
- **DvP（Delivery-versus-Payment）**：USDC + USYC 作为 Day-1 原生资产，支持通证化金融工具的即时 DvP 结算和抵押品管理 [S1]

---

## 五、账户模型：AA 账户与智能账户

### 5.1 ERC-4337 Account Abstraction

ARC 原生支持 **ERC-4337 标准**的账户抽象 [S5, S8]：

- **Circle Paymaster**：原本是基于 ERC-4337 的功能，允许在其他 EVM 链上用 USDC 代替原生代币支付 Gas [S8]
- 在 ARC 上，由于 USDC 本身就是默认费用代币，Paymaster 使得**非 USDC 代币**也能支付交易费用 [S8]
- ERC-4337 添加了 EntryPoint、Bundler 和 Paymaster 功能，无需改变以太坊协议 [S8]

### 5.2 智能账户能力

- Paymaster 抽象支持费用赞助场景：企业或应用可为用户代付 Gas [S5]
- 与 ARC 的确定性最终性结合，智能账户可以可靠地依赖确定的结算状态执行逻辑 [S2, S5]
- 支持 Agentic commerce（AI 代理商务）：可预测的 USDC Gas 费用 + 亚秒最终性 + 隐私控制 → AI 代理可直接嵌入链上支付工作流 [S1]

**注意**：目前公开信息主要覆盖 Paymaster 层面的 AA，是否包含完整的 Smart Account（合约钱包、Session Key、Batch 等）栈需要更多官方文档确认。

---

## 六、隐私与合规

### 6.1 可选隐私（Opt-in Privacy）

ARC 的隐私系统是**模块化且实用主义**的 [S5]：

- **机密转账**：交易金额被遮蔽，地址保持公开 [S5]
- **选择性屏蔽**：用户和企业可选择性地屏蔽余额和交易，同时满足合规义务 [S1, S14]
- **选择性披露**：机构可通过密钥向审计员、监管者或特定对手方授予查看权限 [S5]

### 6.2 可插拔加密后端

隐私功能通过 **EVM precompile** 暴露，路由到可插拔的加密后端 [S5]：
- **初始后端**：TEE（可信执行环境），对加密数据进行低延迟计算 [S5]
- **未来扩展**：随着 MPC（安全多方计算）、FHE（全同态加密）或 ZK（零知识）系统成熟，ARC 可接入这些后端用于私有状态和机密计算 [S5]

### 6.3 PFMI 对齐

ARC 的设计符合《金融市场基础设施原则》（PFMI）第 8 原则：提供清晰、确定的最终结算，最好为日内或实时结算 [S2, S10]。

---

## 七、安全性增强：量子抗性路线图

### 7.1 四阶段量子抗性计划

Circle 为 ARC 发布了全栈、分阶段的后量子安全路线图，覆盖钱包、签名、验证者和链下基础设施，时间线至 **2030 年** [S9, S20]：

- **阶段 1（Mainnet 启动时）**：引入后量子签名方案，用户可选择创建量子抗性钱包 [S9, S20]
- **阶段 2**：扩展到私有状态和验证者层
- **阶段 3**：覆盖链下基础设施
- **阶段 4**：全面过渡

### 7.2 防御场景

- 防御"先窃取后解密"（Harvest-now-decrypt-later）攻击 [S15]
- 到 2030 年，强大的量子计算机可能破解当前加密算法 [S20]

### 7.3 实施特点

- 采用**选择性加入**（opt-in）模式，保持灵活性 [S9, S20]
- 基于 NIST 后量子密码标准 [S4, S20]
- 路线图可能随标准演进而变化 [S4]

---

## 八、跨链与互操作性

### 8.1 CCTP（Cross-Chain Transfer Protocol）

- ARC 原生集成 Circle 的 CCTP，支持 USDC 在 ARC 与其他链之间的**无信任桥接** [S12, S13, S16]
- 基于 burn-and-mint 机制：在源链销毁 USDC，在目标链铸造 [S5, S13]
- 确定性最终性使得目标链可在单个区块确认后快速铸造，无需等待长安全窗口 [S5]

### 8.2 Gateway

- Circle 的 Gateway 产品结合 CCTP，实现**多链 USDC 流动性统一整合**到 ARC 上的单一钱包余额 [S16]
- 目前处于 testnet 阶段 [S16]

### 8.3 第三方桥接

- Across、Stargate、Wormhole 等跨链协议已连接 ARC [S7]
- ARC 定位为**稳定币流动性枢纽**，连接多链生态 [S5]

---

## 九、MEV 策略

ARC 对 MEV（最大可提取价值）采取**区分对待**策略 [S5]：

| 类型 | 处理方式 | 示例 |
|------|---------|------|
| 建设性 MEV | 允许 | 收窄价差的套利，改善稳定币可替代性和 FX 定价 |
| 有害 MEV | 抑制 | 夹击攻击，损害用户信任并注入隐性成本 |

缓解措施：
- **加密 Mempool**：防止对挂起交易的投机性窥探 [S5]
- **批处理**：减少微秒级时序操作的优势 [S5]
- **多提议者排序**：减少单提议者对排序流的主观裁量 [S5]

---

## 十、与其他 L1 的差异化对比

| 维度 | ARC | Ethereum | Solana |
|------|-----|----------|--------|
| 定位 | 稳定币金融专用基础设施 | 通用智能合约平台 | 高性能通用链 |
| Gas 代币 | USDC（稳定币） | ETH（波动性） | SOL（波动性） |
| 最终性 | 确定性，~350ms | 经济最终性，~14m | 概率最终性，~400ms |
| 共识 | Malachite（BFT, PoA→PoS） | Gasper（PoS） | Proof-of-History + PoS |
| 内置 FX | 是（StableFX RFQ 引擎） | 否（由 DEX 实现） | 否（由 DEX 实现） |
| 隐私 | 可选，TEE/MPC/FHE/ZK 可插拔 | 否（由 Layer2/应用实现） | 否（由应用实现） |
| 量子抗性 | 有路线图（至 2030） | 无官方路线图 | 无官方路线图 |
| 验证者 | 许可机构（PoA→PoS） | 无许可（PoS） | 无许可（PoS） |
| EVM 兼容 | 是 | 原生 | 否 |

---

## 待决问题与不确定性

1. **原生 Token 是否存在**：有报道称 Circle 正在"探索原生 Arc Token 的可能性" [S7]，但官方尚未确认。本研究中 ARC 被描述为无独立原生代币、以 USDC 为唯一 Gas 的链。

2. **共识算法开源细节**：Malachite 的完整源码和协议规范尚未完全公开，仅发布了性能数据和架构描述 [S1, S2]。

3. **预置 DEX 的具体机制**：ARC 内置的是 RFQ 外汇引擎而非传统 AMM DEX。链上是否有预置的 swap 合约或 DEX 标准尚需更多文档确认。

4. **AA 账户的完整栈**：目前公开信息主要覆盖 Paymaster 层面的 AA。是否包含完整的 Smart Account（合约钱包、Session Key、Batch 等）需要更多官方文档确认。

5. **性能数据独立性**：所有性能数据均来自官方/内部测试 [S2]，独立第三方验证数据有限。

6. **主网上线时间**：官方目标为 2026 年 mainnet beta [S1]，实际时间线需持续关注官方更新。

---

## 来源

| 编号 | 来源 | URL |
|------|------|-----|
| S1 | Circle 官方博客 — Introducing Arc | https://www.circle.com/blog/introducing-arc-an-open-layer-1-blockchain-purpose-built-for-stablecoin-finance |
| S2 | Arc 官方博客 — Deterministic Finality | https://www.arc.network/blog/deterministic-finality-on-arc |
| S3 | Arc 官方博客 — How Gas Works on Arc | https://www.arc.network/blog/how-gas-works-on-arc |
| S4 | Arc 官方博客 — Quantum-Resistant Roadmap | https://www.arc.network/blog/arcs-quantum-resistant-design-and-roadmap-why-it-matters |
| S5 | Medium 技术解析 — Some Technical Notes About Circle's New Blockchain | https://medium.com/sentora/some-technical-notes-about-circles-new-blockchain-d09b8d26e0a4 |
| S6 | Eco 支持文档 — What Is Arc Blockchain | https://eco.com/support/en/articles/12160003 |
| S7 | CoinGecko 百科 — What Is Arc | https://www.coingecko.com/learn/what-is-arc-stablechain |
| S8 | Coin Bureau — What Is Circle Arc Blockchain | https://coinbureau.com/education/what-is-arc-circle-stablechain |
| S9 | CryptoNews — Quantum-Resistant Roadmap | https://cryptonews.com/news/circle-quantum-resistant-roadmap-arc-blockchain/ |
| S10 | Token Vitals — Circle Arc Chain Deep Dive | https://tokenvitals.com/blog/circle-arc-chain-deep-dive |
| S11 | Gate 百科 — Arc Layer-1 Financial Infrastructure | https://www.gate.com/crypto-wiki/article/arc-layer-1-financial-infrastructure-technology-analysis |
| S12 | GitHub — circle-cctp-crosschain-transfer | https://github.com/circlefin/circle-cctp-crosschain-transfer |
| S13 | Arc 官方文档 — Bridge USDC to Arc | https://docs.arc.network/arc/tutorials/bridge-usdc-to-arc |
| S14 | Circle 新闻稿 — Arc Public Testnet | https://www.circle.com/pressroom/circle-launches-arc-public-testnet |
| S15 | Circle 官方博客 — Preparing Blockchains for Q-Day | https://www.circle.com/blog/preparing-blockchains-for-q-day |
| S16 | Circle 官方博客 — CCTP and Gateway | https://www.circle.com/blog/consolidate-crosschain-usdc-fast-low-cost-transfers-with-cctp-and-gateway |
| S17 | Arc 官方网站 | https://www.arc.network/ |
| S18 | 23stud.io — Circle Arc Blockchain Analysis | https://23stud.io/blog/circle-arc-blockchain-walled-garden-for-wall-street |
| S19 | Yahoo Finance — What Is Arc | https://finance.yahoo.com/news/arc-stablecoin-blockchain-usdc-issuer-150103906.html |
| S20 | Bitget 新闻 — Quantum-Resistant Roadmap | https://www.bitgetapp.com/news/detail/12560605362018 |
