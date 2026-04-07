# QBFT 共识算法

## 概述

QBFT（Quorum Byzantine Fault Tolerance）是基于 PBFT 的拜占庭容错共识算法，由 ConsenSys 为 Quorum（企业级 Ethereum 分发版）和 Hyperledger Besu 开发。QBFT 保留了 PBFT 经典的三阶段提交流程（Proposal → Prepare → Commit），通过 IST（Immutable State Tree）机制实现确定性的 Leader 选择，支持同步和异步两种视图切换模式。

**研究范围**：QBFT 共识协议核心机制，覆盖组件架构、共识流程、IST 机制、视图切换协议。
**研究深度**：deep
**对象类型**：primitive

## 关键术语

| 术语 | 定义 | 在本题中的作用 |
|------|------|---------------|
| QBFT | Quorum Byzantine Fault Tolerance，Quorum 的 BFT 共识实现 | 本研究的核心对象 |
| IST | Immutable State Tree，不可变状态树，用于确定性 Leader 选择 | QBFT 的核心创新机制 |
| View | 视图，PBFT 中 Leader 的任期概念 | 视图切换的核心变量 |
| Round | 轮次，QBFT 中尝试达成共识的一轮 | 与 View 配合使用 |
| Proposal | 提议阶段，Leader 广播区块提案 | 三阶段提交的第一阶段 |
| Prepare | 准备阶段，验证者确认收到提案 | 三阶段提交的第二阶段 |
| Commit | 提交阶段，验证者确认提交 | 三阶段提交的第三阶段 |
| View Change | 视图切换，当 Leader 失败时切换到新 Leader | QBFT 的 Leader 故障恢复机制 |
| 2f+1 | 2 倍容错数加 1，PBFT 系共识的投票阈值 | 安全性和活性的数学基础 |

## 分析正文

### 实体分类表

在展开分析前，先对 QBFT 系统中的关键实体进行分类：

| 实体 | 类型 | 控制方 | 是否跨信任边界 | 主要职责 | 应落入哪类图 |
|------|------|--------|----------------|----------|--------------|
| Leader (Proposer) | Role | 独立验证者 | 是 | 提出区块提案 | 角色边界图 |
| Validator (Replica) | Role | 独立验证者 | 是 | 验证并投票 | 角色边界图 |
| Proposal 消息 | Data Object | - | 是 | 承载区块提案 | 时序图 |
| Prepare 消息 | Data Object | - | 是 | 承载准备投票 | 时序图 |
| Commit 消息 | Data Object | - | 是 | 承载提交投票 | 时序图 |
| ViewChange 消息 | Data Object | - | 是 | 请求切换视图 | 时序图 |
| NewView 消息 | Data Object | - | 是 | 通知新视图建立 | 时序图 |
| IST | Component | 所有验证者 | 否 | 确定性 Leader 选择 | 组件图 |
| 共识状态机 | Component | 每个验证者 | 否 | 管理状态转换 | 组件图 |

### 组件架构

所有验证者节点内部结构相同，核心组件包括共识状态机、IST、消息验证器、P2P 网络层和存储层。

**节点内部组件职责**：

| 组件 | 职责 | 所属层 |
|------|------|--------|
| 共识状态机 | 管理状态转换（Propose/Prepare/Commit） | 共识核心 |
| IST | 确定性 Leader 选择（公式：`LeaderIndex = (View + Round) mod N`） | 共识核心 |
| 消息验证器 | 验证签名和消息格式 | 共识核心 |
| 消息广播 | P2P 消息传播 | 网络层 |
| 消息队列 | 接收和缓冲消息 | 网络层 |
| 消息日志 | 记录 Prepare/Commit 投票 | 存储层 |
| 区块存储 | 区块数据存储 | 存储层 |
| 状态数据库 | 状态持久化（LevelDB/BadgerDB） | 存储层 |

**重要说明**：
- Proposer 是 Validator 的**临时职责**，不是独立组件
- IST 是 QBFT 的核心创新，提供确定性 Leader 选择
- 状态（如 Propose、Prepare、Commit）是组件的运行阶段，不是组件

### 核心共识流程（Happy Path）

### 核心共识流程（Happy Path）

QBFT 的三阶段提交流程（Proposal → Prepare → Commit）：

**流程步骤说明**：

1. **Proposal 阶段**：IST 选定的 Leader 构造区块并签名，广播 Proposal 消息给所有验证者
2. **Prepare 阶段**：每个验证者验证区块有效性（签名、格式、交易），验证通过后广播 Prepare 消息
3. **Commit 阶段**：当验证者收集到 2f+1 个 Prepare 消息（形成 Prepare 证书），广播 Commit 消息
4. **提交区块**：当验证者收集到 2f+1 个 Commit 消息（形成 Commit 证书），提交区块到状态机

**消息格式定义**：

```java
// Proposal 消息
struct Proposal {
    bytes32 blockHash;      // 区块哈希
    uint256 view;           // 当前视图
    uint256 round;          // 当前轮次
    bytes signature;        // Leader 签名
    bytes[] transactions;   // 交易列表
}

// Prepare 消息
struct Prepare {
    bytes32 blockHash;      // 准备的区块哈希
    uint256 view;           // 视图
    uint256 round;          // 轮次
    bytes signature;        // 验证者签名
}

// Commit 消息
struct Commit {
    bytes32 blockHash;      // 提交的区块哈希
    uint256 view;           // 视图
    uint256 round;          // 轮次
    bytes signature;        // 验证者签名
}
```

### IST 机制（Leader 选择）

QBFT 的核心创新是 IST（Immutable State Tree），用于确定性 Leader 选择：

**Leader 选择公式**：
```
LeaderIndex = (View + Round) mod N

其中：
  - View: 当前视图（Leader 任期）
  - Round: 当前轮次（尝试次数）
  - N: 验证者数量
```

**IST 与 PBFT View 的差异**：

| 维度 | PBFT View | QBFT IST |
|------|-----------|----------|
| Leader 选择 | 固定 Primary (View 0), View Change 后重新协商 | 确定性公式计算 |
| View Change | 复杂协商协议 | 简单计数器递增 |
| 可预测性 | 低（依赖协商） | 高（确定性公式） |

### 状态转换

QBFT 节点状态机：

| 状态 | 触发进入 | 退出条件 |
|------|----------|----------|
| Idle | 初始化完成 / 提交完成 | 成为 Leader 或收到 Proposal |
| Propose | IST 选定为 Leader | 广播 Proposal 完成 / 超时 |
| Prepare | 收到有效 Proposal | 收集 2f+1 Prepare / 超时 |
| Commit | 收集 2f+1 Prepare | 收集 2f+1 Commit / 超时 |
| Committed | 收集 2f+1 Commit | 提交区块完成 |

**状态转换流程**：
```
NewHeight → NewRound → Propose → Prepare → Commit → Committed → NewHeight...
                             ↓
                        超时/ViewChange → NewRound
```

### View Change 机制（异常路径）

**触发条件**：
- Leader 在规定时间内未广播 Proposal
- 共识在 Round r 无法达成（2f+1 Prepare 或 Commit）

**View Change 流程**：
1. 超时后广播 ViewChange 消息（newView = v+1）
2. 新 Leader 收集 2f+1 ViewChange 消息
3. 新 Leader 广播 NewView 消息（包含 ViewChange 证明）
4. 验证者验证 NewView，重置状态，进入 Proposal 阶段

**ViewChange 消息格式**：
```java
struct ViewChange {
    uint256 newView;        // 新视图
    uint256 round;          // 最后轮次
    bytes32 preparedBlock;  // 已准备的区块哈希 (可选)
    bytes[] preparedProof;  // Prepare 证书
    bytes signature;        // 验证者签名
}
```

### 设计取舍

#### 为什么保留三阶段而非简化为两阶段？

**选择**：QBFT 保留 PBFT 的三阶段（Proposal → Prepare → Commit），而 Tendermint 简化为两阶段（Prevote → Precommit）。

**设计原因**：
1. **历史兼容性**：QBFT 设计时优先考虑与 PBFT 的兼容性，便于从传统 BFT 系统迁移
2. **安全性证明**：PBFT 的三阶段安全性证明成熟，工程风险低
3. **视图切换简单**：三阶段下 View Change 协议更直接

**Trade-off**：

| 特性 | 三阶段 (QBFT/PBFT) | 两阶段 (Tendermint) |
|------|-------------------|---------------------|
| 通信轮次 | 3 轮 | 2 轮 |
| 延迟 | 较高 | 较低 |
| 安全性证明 | 成熟 | 依赖同步假设 |
| 网络假设 | 部分同步 | 部分同步 |
| 工程复杂度 | 较低（兼容 PBFT） | 中等（需处理超时） |

#### 为什么 IST 选择确定性公式而非随机选举？

**选择**：QBFT 使用 `(View + Round) mod N` 确定性公式选择 Leader。

**设计原因**：
1. **可预测性**：所有验证者可以独立计算 Leader，无需额外通信
2. **简单性**：实现简单，无随机数生成复杂性
3. **公平性**：长期来看每个验证者轮流担任 Leader

#### 为什么支持同步和异步两种视图切换？

**选择**：QBFT 支持同步和异步两种视图切换模式。

- **同步模式**：所有验证者同时切换视图，需要额外的同步消息，适用于网络稳定的联盟链
- **异步模式**：每个验证者独立决定切换，依赖 ViewChange 消息传播，适用于网络不稳定的场景

## 边界与前提

### 协议原生能力 vs 外部依赖

| 能力 | 归属 | 说明 |
|------|------|------|
| 共识达成 | 协议原生 | QBFT 核心功能 |
| 最终性保证 | 协议原生 | 2f+1 Commit 后最终化 |
| Leader 选择 | 协议原生 | IST 机制 |
| 视图切换 | 协议原生 | View Change 协议 |
| 交易执行 | 外部依赖 | EVM 或执行引擎 |
| 验证者集管理 | 外部依赖 | Quorum 智能合约 |
| P2P 通信 | 外部依赖 | Ethereum devp2p / libp2p |

### 安全性假设

| 假设 | 说明 | 违反后果 |
|------|------|----------|
| f < n/3 拜占庭节点 | 恶意验证者不超过总数的 1/3 | 安全性被破坏，可能双签 |
| 网络最终同步 | 消息最终会被送达 | 活性受阻，安全性不受影响 |
| 密码学原语安全 | 签名、哈希安全 | 整个系统安全性被破坏 |
| 验证者私钥安全 | Leader 私钥不被泄露 | 恶意 Leader 可破坏活性 |

### 能力边界

**能解决**：
- 拜占庭容错共识（≤1/3 故障节点）
- 确定性 Leader 选择（IST 机制）
- 即时最终性保证
- 视图切换和 Leader 故障恢复

**不能解决**：
- 应用逻辑：交易执行由 EVM 或外部引擎负责
- 验证者管理：验证者加入/退出由外部机制管理
- 跨链通信：需要额外协议（如 IBC 桥接）
- 隐私保护：交易默认公开（Quorum 的隐私交易是额外层）
- 51% 攻击：持有 > 1/3 投票权的攻击者可破坏安全性

### 性能边界

| 指标 | 典型值 | 瓶颈 |
|------|--------|------|
| TPS | 100 - 1000 | 交易执行 + 网络传播 |
| 延迟 | 1-3 秒 | 三阶段通信 + 超时配置 |
| 节点规模 | < 50 | O(n²) 消息复杂度 |

> 注：以上数据基于 Quorum/Besu 公开文档，实际性能取决于配置和网络条件。

## 相关对象关系

### 与相邻协议定位

| 协议 | 关系 | 说明 |
|------|------|------|
| PBFT | 上游 | QBFT 基于 PBFT，保留三阶段核心 |
| IBFT 2.0 | 前身 | QBFT 是 IBFT 2.0 的改进版，修复了 IBFT 的活性问题 |
| Tendermint | 平行 | BFT 共识的另一代表，两阶段优化 |
| HotStuff | 平行 | 新一代 BFT，线性通信复杂度 |
| Raft | 平行 | CFT 共识，崩溃容错而非拜占庭容错 |

### QBFT 与 IBFT 2.0 的演进关系

IBFT 2.0 是 Quorum 早期的 BFT 共识，QBFT 在其基础上改进：

| 维度 | IBFT 2.0 | QBFT | 改进说明 |
|------|----------|------|----------|
| 视图切换 | 无明确限制 | 支持同步/异步 | 修复 IBFT 活性问题 |
| Leader 选择 | 轮转 | IST 确定性公式 | 更清晰的语义 |
| 消息验证 | 基础 | 增强验证 | 防止无效消息攻击 |

## 结论

**已确认**：
- QBFT 是基于 PBFT 的 BFT 共识，保留三阶段提交
- 使用 IST 机制实现确定性 Leader 选择（公式：`(View + Round) mod N`）
- 支持同步和异步两种视图切换模式
- 容错比例为 f < n/3（标准 BFT 假设）
- 2f+1 投票阈值保证安全性和最终性
- 被 Quorum 和 Hyperledger Besu 采用

**尚需验证**：
- QBFT 2.0 是否存在及其与 QBFT 的具体差异
- IST 的完整规范来源（当前基于实现推断）
- 同步 vs 异步视图切换的具体配置参数
- Quorum/Besu 实现中的具体优化细节

## 待确认问题

| 问题 | 状态 | 说明 |
|------|------|------|
| QBFT 与 IBFT 2.0 的完整差异列表 | 未解决 | 需要查阅 IBFT 2.0 规范对比 |
| IST 的完整规范 | 未解决 | 当前基于实现代码推断 |
| Quorum/Besu 实现差异 | 未解决 | 两个实现在细节上可能有差异 |
| 生产环境性能数据 | 未解决 | 需要实际部署数据 |
| 针对 QBFT 的攻击分析 | 未解决 | 安全事件和防护措施需补充 |

## 参考资料

| 来源 | 说明 |
|------|------|
| https://github.com/ConsenSys/qbft-core | QBFT 核心规范仓库 |
| https://besu.hyperledger.org/HowTo/Configure/Consensus-Protocols/QBFT | Hyperledger Besu QBFT 文档 |
| https://github.com/hyperledger/besu | Hyperledger Besu 实现 |
| https://github.com/ConsenSys/quorum | Quorum 实现 |
| https://eips.ethereum.org/EIPS/eip-2100 | IBFT 2.0 规范 |
