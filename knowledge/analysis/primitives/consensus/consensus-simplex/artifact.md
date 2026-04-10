# Simplex 共识算法

## 概述

Simplex 是一种面向无许可区块链环境设计的拜占庭容错（BFT）共识协议，旨在在传统 BFT 协议难以适用的去中心化场景中实现亚秒级快速最终性（fast finality）[L2-002]。

与传统 BFT 协议（如 PBFT、Tendermint）不同，Simplex 能够在不依赖许可验证者集合的前提下，提供确定性的交易最终性，同时保持较高的吞吐量 [L2-002]。

**核心特征**：
- **Leader-based、vote-driven** 的 BFT 共识协议，在 Views 中运行 [L2-002]
- **两阶段投票**：验证者先进行 Notarize 投票，再进行 Finalize 投票 [L2-002]
- **确定性 Leader 选举**：每 View 的 Leader 通过 `ViewNumber % CommitteeSize` 确定性选出 [L2-002]
- **Dummy Block 机制**：超时后投票给特殊 Dummy Block（Hash Zero）实现 View 前进，无需复杂选举 [L2-002]
- **BLS 签名聚合**：采用 blst 库实现签名聚合，减少 QC 大小和验证开销 [L2-001]

**性能特性** [L2-001]：
- 最优乐观确认时间：3δ（三次网络延迟）
- 最优区块时间：2δ

**研究深度**：deep

## 关键术语

| 术语 | 定义 | 在本题中的作用 |
|------|------|---------------|
| Simplex | 面向无许可环境设计的 BFT 共识协议 | 研究对象 |
| Fast Finality | 快速最终性，指交易在较短时间内获得确定性确认 | Simplex 声称的核心特性 |
| View | 协议执行的基本单位，每个 View 有唯一编号 (ViewNumber) [L2-002] | Simplex 的执行上下文 |
| Leader | 当前 View 的确定性提议者，通过 `ViewNumber % CommitteeSize` 选出 [L2-002] | 区块提议方 |
| Validators | 验证者委员会，固定节点集合，负责验证和投票 [L2-002] | 共识参与方 |
| Learners | 非验证节点，同步链但不参与投票 [L2-002] | 被动观察者 |
| Notarize Vote | 验证者对区块有效性的第一阶段投票 [L2-002] | 共识第一阶段 |
| Finalize Vote | 验证者对区块最终化的第二阶段投票 [L2-002] | 共识第二阶段 |
| QuorumCertificate (QC) | 2f+1 聚合签名，证明区块获得法定多数认可 [L2-002] | 共识证明 |
| Dummy Block | 特殊区块（Hash Zero），用于超时场景的 View 前进 [L2-002] | 异常处理机制 |
| LastVotedView | 验证者上次投票的 View 编号，用于防止双重投票 [L2-002] | 安全约束 |

## 分析正文

### 实体分类

| 实体 | 类型 | 控制方 | 是否跨信任边界 | 主要职责 |
|------|------|--------|----------------|----------|
| Leader（领导者） | role | 当前 View 确定性选出 (`ViewNumber % CommitteeSize`) | 是 | 构造并广播区块、立即投票给自己的区块 |
| Validators（验证者委员会） | role | 固定节点集合，签名投票 | 是 | 验证区块、广播 Notarize/Finalize 投票、超时投票给 Dummy Block |
| Learners（学习者） | role | 非验证节点 | 是 | 同步链、不参与投票 |
| Block（区块） | data object | - | 是 | 包含 ParentHash、Justify QC、Payload、StateRoot |
| Vote（投票） | data object | - | 是 | Notarize 或 Finalize 类型，签名 BlockHash |
| QuorumCertificate（QC） | data object | - | 是 | 2f+1 聚合签名，证明区块获得法定多数 |

### 核心机制

#### 正常路径（5 阶段）

正常路径包含 5 个阶段 [L2-002]：

**Phase 1: Proposal**
- Leader 构造 Block，包含：ParentHash、Justify QC、Payload、StateRoot [L2-002]
- Leader 通过 Gossipsub 广播 Block 给所有验证者 [L2-002]
- Leader 立即投票给自己的区块（无需等待他人广播）[L2-002]

**Phase 2: Validation**
验证者收到 Block 后执行以下检查 [L2-002]：
- **View 检查**：验证 Block 的 ViewNumber 与当前 View 匹配
- **Parent 验证**：验证 ParentHash 指向已确认的父区块
- **执行验证**：执行 Block 中交易，验证 StateRoot 是否正确
- **QC 验证**：验证 Justify QC 的签名有效性
- **Equivocation 检查**：检查 Leader 是否在同一 View 中提议了多个 Block

**Phase 3: Voting (Notarize)**
- 验证者更新 `LastVotedView` 为当前 View [L2-002]
- 构造 Notarize 投票，签名 BlockHash [L2-002]
- 广播 Notarize 投票给网络 [L2-002]

**Phase 4: QC Formation**
- 收集 2f+1 个 Notarize 投票 [L2-002]
- 验证投票签名的有效性 [L2-002]
- 形成 Notarize QC 并保存 [L2-002]
- View 前进到 V+1 [L2-002]
- 广播 Finalize 投票 [L2-002]

**Phase 5: Finalization**
- 收集 2f+1 个 Finalize 投票 [L2-002]
- 形成 Finalize QC [L2-002]
- View 标记为 `Finalized` [L2-002]
- 区块不可变，状态提交 [L2-002]

#### 异常路径处理

**超时场景**：Leader 离线或网络延迟导致超时 [L2-002]

**Dummy Block 机制** [L2-002]：
1. 超时触发后，验证者投票给特殊 Dummy Block（Hash Zero）
2. Dummy Block 不包含实际交易，仅用于 View 前进
3. 收集 2f+1 票形成 QC
4. View 前进到 V+1
5. 在新 View 的 Dummy Block 上继续，直到恢复正常 Leader

**设计要点**：
- Dummy Block 允许 View 在无有效 Leader 时仍能前进 [L2-002]
- 避免复杂的 View Change 选举流程 [L2-002]
- 保证活性：即使 Leader 失败，协议仍能通过 Dummy Block 跳过该 View

### 角色与职责

#### Leader（领导者）

**选举方式**：每 View 确定性选出，公式为 `ViewNumber % CommitteeSize` [L2-002]

**职责** [L2-002]：
- 构造 Block：包含 ParentHash、Justify QC、Payload、StateRoot
- 广播 Block：通过 Gossipsub 将区块发送给所有验证者
- 立即投票：Leader 无需等待，立即对自己的区块投出 Notarize 票

**特性**：
- 确定性选举：无需 VRF 或轮询表，仅依赖 View 编号计算 [L2-002]
- 可预测性：所有节点可预先知道下一 View 的 Leader 是谁 [L2-002]

#### Validators（验证者委员会）

**组成**：固定节点集合 [L2-002]

**职责** [L2-002]：
- **验证 Block**：
  - View 检查：验证 Block 的 ViewNumber 与当前 View 匹配
  - Parent 验证：验证 ParentHash 指向已确认的父区块
  - 执行验证：执行交易并验证 StateRoot
  - QC 验证：验证 Justify QC 的签名有效性
  - Equivocation 检查：检查 Leader 是否在同一 View 提议了多个 Block
- **广播投票**：
  - Notarize 投票：验证通过后更新 LastVotedView，签名 BlockHash 并广播
  - Finalize 投票：QC 形成后广播 Finalize 投票
- **超时处理**：超时后投票给 Dummy Block（Hash Zero）[L2-002]

**信任假设**：
- 系统容忍最多 f 个恶意节点（总节点数 n ≥ 3f+1）[L2-002]
- 需要 2f+1 票形成 QC [L2-002]

#### Learners（学习者）

**定义**：非验证节点 [L2-002]

**职责** [L2-002]：
- 同步链：从验证者同步区块和状态
- 不参与投票：仅被动接收共识结果

**适用场景**：
- 轻客户端
- 区块浏览器
- 历史归档节点

### 安全与活性

#### 安全性（Safety）

**保证**：Finalized 后的区块不可变 [L2-002]

**条件** [L2-002]：
- **2f+1 超级多数要求**：需要 2f+1 个签名才能形成 QC
- **投票约束**：验证者更新 LastVotedView 后，在同一 View 中不能投给其他 Block
- **状态提交**：View 标记为 Finalized 后，状态正式提交

**证明逻辑** [L2-002]：
1. 要形成 Finalize QC，需要 2f+1 个 Finalize 投票
2. 要形成 Notarize QC，需要 2f+1 个 Notarize 投票
3. 两阶段投票确保没有两个冲突的 Block 能同时获得 QC
4. Finalized View 的区块获得密码学确定性

#### 活性（Liveness）

**保证**：在网络同步假设下，协议最终会达成新区块确认 [L2-002]

**Dummy Block 机制** [L2-002]：
- 当 Leader 离线或网络延迟时，验证者超时
- 超时后投票给 Dummy Block（Hash Zero）
- 收集 2f+1 票形成 QC，View 前进到 V+1
- 在新 View 中继续，直到恢复正常 Leader

**网络假设** [L2-002]：
- 同步网络假设：消息在已知超时阈值内送达
- 超时阈值需大于正常网络 RTT

### 数据结构

#### Block（区块）

```
Block {
    ParentHash: Hash,       // 父区块哈希
    JustifyQC: QC,          // 证明合法性的 QC
    ViewNumber: u64,        // 当前 View 编号
    Payload: Transactions,  // 交易负载
    StateRoot: Hash         // 状态根哈希
}
```

#### Vote（投票）

```
Vote {
    ViewNumber: u64,        // 投票所属 View
    BlockHash: Hash,        // 被投票区块的哈希
    VoteType: Notarize|Finalize,  // 投票类型
    Signature: Signature    // 验证者签名
}
```

#### QuorumCertificate（QC）

```
QuorumCertificate {
    BlockHash: Hash,        // 被证明的区块哈希
    ViewNumber: u64,        // QC 所属 View
    AggregateSignature,     // 2f+1 聚合签名
    Bitmap                  // 签名者位图
}
```

## 设计取舍

### 核心设计选择

| 设计维度 | Simplex 的选择 | 替代方案 | 来源 | 理由 |
|----------|---------------|---------|------|------|
| Leader 选举 | 确定性 (ViewNumber % CommitteeSize) | 轮询 / VRF 随机选择 | [L2-002] | 简单、可预测、无需额外通信开销 |
| 投票聚合 | BLS 聚合签名 (blst 库) | 直接收集各节点签名 | [L2-001] | QC 大小恒定，验证开销低 |
| 最终性证明 | 显式 QC（两阶段：Notarize + Finalize） | 隐式确认（如最长链） | [L2-002] | 明确区分"区块有效"和"区块最终化" |
| 异常处理 | Dummy Block 跳过 View | View Change 重新选举 Leader | [L2-002] | 无需复杂选举，View 可直接跳过 |
| 网络层 | Gossipsub 广播 | 直接 P2P 单播 | [L2-002] | 高效广播，适合共识消息传播 |

### 与相关 BFT 协议的对比

| 特性 | Simplex | Tendermint | HotStuff | PBFT |
|------|---------|------------|----------|------|
| 目标环境 | 无许可 [L2-002] | 通常许可 | 通常许可 | 许可 |
| 最终性类型 | 快速确定性 (两阶段 QC) [L2-002] | 快速确定性 (Prevote+Precommit) | 快速确定性 (三阶段) | 快速确定性 (三阶段) |
| Leader 机制 | View-based 确定性选举 [L2-002] | 轮询 | View-based | View-based |
| 异常处理 | Dummy Block 跳过 View [L2-002] | Timeout+View Change | View Change | View Change |
| 签名方案 | BLS 聚合 [L2-001] | Ed25519 | BLS 可选 | 可选 |
| 消息复杂度 | O(n) 投票广播 [L2-002] | O(n²) | O(n) | O(n²) |

**与 HotStuff 的关系**：Simplex 在设计上与 HotStuff 有相似之处（View-based、QC 机制），但通过 Dummy Block 简化了异常处理流程 [L2-002]。

## 边界与前提

### 协议原生能力

- **快速最终性保证**：两阶段投票（Notarize + Finalize）提供确定性最终性 [L2-002]
- **确定性 Leader 选举**：ViewNumber % CommitteeSize [L2-002]
- **拜占庭容错**：容忍最多 f 个恶意节点（n ≥ 3f+1）[L2-002]
- **BLS 签名聚合**：减少 QC 大小和验证开销 [L2-001]

### 外部依赖

- **底层 P2P 网络层**：使用 Gossipsub 进行消息广播 [L2-002]
- **交易池（mempool）机制**：Leader 从交易池选择交易打包 [L2-002]
- **密码学原语**：BLS 签名（blst 库）、哈希函数 [L2-001]

### 能力边界

- **同步网络假设**：需要消息在超时阈值内送达 [L2-002]
- **固定验证者集合**：验证者是预先确定的固定集合 [L2-002]
- **不提供分片或跨链互操作性**：非协议目标

### 故障假设

| 假设 | 说明 | 违反后果 |
|------|------|----------|
| 拜占庭节点 < 1/3 | 持有超过 1/3 投票权的节点不会合谋作恶 | 安全性被破坏 |
| 网络最终同步 | 消息最终会被送达 | 活性受阻，但安全性不受影响 |
| 密码学原语安全 | 签名、哈希等密码学假设成立 | 整个系统安全性被破坏 |

## 相关对象关系

### 与相邻协议的关系

| 对象 | 关系类型 | 说明 |
|------|----------|------|
| PBFT | 理论基础 | Simplex 基于 PBFT 简化设计，省略 Pre-prepare 阶段 |
| Tendermint | 替代方案 | Go 实现的 PoS+BFT，三阶段 (Prevote+Precommit)，通常用于许可环境 |
| HotStuff | 平行方案 | Libra/Diem 采用的 BFT 变体，三阶段，View-based |
| QBFT | 替代方案 | 企业级 BFT，联盟链场景，基于 QBFT 规范 |
| Malachite | 新兴替代 | Rust 实现的高性能 BFT |

### 协议家族演进

Simplex 可视为 PBFT 家族在无许可环境下的演进尝试：
- **核心差异**：领导者选举机制、参与许可模型
- **演进方向**：减少通信轮次、简化异常处理

## 结论

### 已确认（L2 证据）

基于 L2-002 (consensus_flow.md) 已确认：

**核心机制**：
- Simplex 是 leader-based、vote-driven 的共识协议，在 Views 中运行
- 每 View 有确定性 Leader (ViewNumber % CommitteeSize)
- 正常路径 5 阶段：Proposal → Validation → Notarize Vote → QC Formation → Finalization
- 超时处理：投票给 Dummy Block (Hash Zero) → 形成 QC → View 前进

**角色与职责**：
- Validators 是固定节点集合，负责验证和签名投票
- Learners 是非验证节点，同步链但不参与投票
- Leader 职责：构造 Block、Gossipsub 广播、立即投票给自己的区块

**数据结构**：
- Block 包含 ParentHash、Justify QC、Payload、StateRoot
- Vote 有 Notarize 和 Finalize 两种类型
- QuorumCertificate (QC) 需要 2f+1 聚合签名

**安全与活性**：
- 2f+1 超级多数要求保证安全性
- Finalized 后的区块不可变
- Dummy Block 机制保证活性
- 网络同步假设：消息在超时阈值内送达

**性能特性** [L2-001]：
- 最优乐观确认时间：3δ
- 最优区块时间：2δ
- 使用 BLS 签名聚合（blst 库）

### 尚需验证

- Simplex 原始论文作者和形式化定义（G1 证据缺口）
- 采用 Simplex 的具体区块链项目（Chainlink CCIP 采用情况需进一步验证）

## 参考资料

| 来源 | 说明 | 验证状态 |
|------|------|----------|
| [hadv/ockham](https://github.com/hadv/ockham) | Simplex Consensus Rust 实现 | [L2-001 已验证] |
| [consensus_flow.md](https://raw.githubusercontent.com/hadv/ockham/main/docs/consensus_flow.md) | Simplex 协议详细文档 | [L2-002 已验证] |
