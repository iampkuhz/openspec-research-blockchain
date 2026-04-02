# Tendermint 共识算法

## 概述

Tendermint 是 Cosmos 生态的核心共识算法，是第一个将 PoS（权益证明）与 BFT（拜占庭容错）原生集成的共识协议。采用简化的两阶段投票（Prevote/Precommit）和超时驱动的视图转换机制，提供即时最终性保证。

**研究范围**：本协议为成熟 BFT 实现，属于 PoS+BFT 的代表性方案。
**研究深度**：deep
**对象类型**：primitive

## 关键术语

| 术语 | 定义 | 在本题中的作用 |
|------|------|---------------|
| Tendermint | Cosmos 的 BFT 共识协议 | 研究对象 |
| Prevote/Precommit | 两阶段投票 | Tendermint 的核心机制 |
| Round | 轮次，超时后递增 | View Change 的简化替代 |
| Proposer | 当前轮次的 Leader | 临时角色，非固定组件 |
| Validator | 验证者，参与投票 | 节点类型，需质押 |
| Voting Power | 验证者质押权重 | 决定 Proposer 选择和共识阈值 |

## 分析正文

### 组件架构

**架构图说明**：
- 本图聚焦于**单个 Tendermint Validator 节点内部**（抽象层级 Level 3）
- **蓝色矩形**：节点内部组件（共识引擎、Mempool、状态机）
- **黄色 note**：数据对象（Proposal、Prevote、Precommit）
- **灰色人形**：外部角色（其他验证者、全节点）
- **绿色圆柱体**：数据存储（区块存储）

**注意**：Proposer 不是独立组件，是 Validator 在当前轮次的**角色**。

```plantuml
@startuml
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"
skinparam defaultFontSize 14
skinparam backgroundColor #FFFFFF

' 纵向布局
top to bottom direction
skinparam nodesep 25
skinparam ranksep 35

' 配色方案
skinparam package {
    BackgroundColor #F0F4F8
    BorderColor #5A6C7D
}

skinparam component {
    BackgroundColor #E3F2FD
    BorderColor #1565C0
}

skinparam database {
    BackgroundColor #C8E6C9
    BorderColor #2E7D32
}

skinparam actor {
    BackgroundColor #E0E0E0
    BorderColor #424242
}

skinparam note {
    BackgroundColor #FFF9C4
    BorderColor #F9A825
}

title Tendermint Validator Node Internal Architecture

package "Tendermint Validator Node" {
    component [Consensus Engine] as CE
    component [Mempool] as MP
    component [State Machine] as SM
    database [(Blockchain Store)] as BS

    note right "Current Role:\nProposer or Voter" as Role
}

package "Data Objects" {
    note "Proposal" as N_P
    note "Prevote" as N_PV
    note "Precommit" as N_PC
}

actor "Other Validators" as OtherVals
actor "Full Nodes" as FullNodes

' 数据流
OtherVals --> N_PV : Prevote/Precommit
N_PV --> CE : Collect Votes
CE --> MP : Get Txs
CE --> SM : Execute Block
SM --> BS : Write State
CE --> N_PC : Broadcast
N_PC --> FullNodes : Block

legend right
  |= Element |= Shape |= Color |= Description |
  | Component | Rectangle | Blue | Internal module |
  | Data | Note | Yellow | Message object |
  | Actor | Human | Gray | External node |
  | Storage | Cylinder | Green | Persistent data |
  | Role | Note | Yellow | Node's current state |
endlegend

@enduml
```

### 节点角色说明

| 角色/类型 | 说明 | 是否投票 | 选择方式 |
|-----------|------|----------|----------|
| **Proposer** | 当前轮次的 Leader，负责提议区块 | 是（同时作为 Validator） | Round-robin + PoS 权重 |
| **Validator** | 验证者节点，参与共识投票 | 是 | PoS 质押选择 |
| **Full Node** | 全节点，同步状态但不投票 | 否 | 无需质押 |
| **Light Client** | 轻节点，只验证头部 | 否 | 无需质押 |

**重要**：Proposer 是**临时角色**，不是独立组件。每个 Validator 在某些轮次可以是 Proposer。

### 核心机制（与 PBFT 对比）

**PBFT 三阶段基线**：

| 阶段 | 作用 | 为什么需要？ |
|------|------|-------------|
| Pre-prepare | Leader 绑定视图 V 和序列号 N | 防止 Leader 为同一序列号发送两个不同请求 |
| Prepare | 验证者确认收到 Pre-prepare | 形成"准备证书"（2f+1 Prepare） |
| Commit | 验证者确认准备完成 | 形成"提交证书"，确保最终性 |

**Tendermint 两阶段**：

| 阶段 | 作用 | 为什么可以省略 Pre-prepare？ |
|------|------|---------------------------|
| Prevote | 验证者投票给 Proposal 或 nil | Tendermint 有 Round 概念，每个 Round 独立 |
| Precommit | 确认提交 | 2/3 Precommit 形成提交证书 |

**为什么 Tendermint 可以省略 Pre-prepare？**

1. **同步假设差异**：
   - PBFT 假设**异步网络**：不能依赖超时，必须有 Pre-prepare 防止 Leader 作恶
   - Tendermint 假设**部分同步网络**：可以依赖超时，Proposer 在超时内必须发送 Proposal

2. **轮次隔离**：
   - Tendermint 每个 Round 是独立的
   - Round N 的投票不影响 Round N+1
   - 不需要 Pre-prepare 来绑定视图和序列号

3. **PoS 经济安全**：
   - 验证者质押了代币
   - 作恶会被罚没（slashing）
   - 比 PBFT 的纯密码学假设有额外经济层安全

**代价**：
- 在完全异步网络中可能无法进展（依赖超时）
- 需要更强的同步假设

### Tendermint 共识流程详解

#### Round 0：Proposer 选择

**触发条件**：新区块高度开始，或上一轮超时

**选择算法**：
```go
// 基于质押权重的轮转选择
func ChooseProposer(validators []Validator, height int64, round int64) Validator {
    // 按质押权重排序
    sort.Slice(validators, func(i, j int) bool {
        return validators[i].VotingPower > validators[j].VotingPower
    })

    // 计算总权重
    totalPower := sum(validators)

    // 基于 (height, round) 计算索引
    index := (height + round) % totalPower

    return validators[index]
}
```

#### Round 0：Propose 阶段

**Proposer 行为**（触发：被选为 Proposer）：

| 步骤 | 动作 | 说明 |
|------|------|------|
| 1 | 从 Mempool 获取交易 | `txs := mempool.ReapMaxBytes(maxBytes)` |
| 2 | 构造区块 | `block = NewBlock(txs, height, round)` |
| 3 | 签名并广播 | `broadcast MsgProposal{block, signature}` |

**验证者行为**（触发：收到 MsgProposal）：

| 步骤 | 验证内容 | 失败处理 |
|------|----------|----------|
| 1 | Proposer 签名有效 | 丢弃消息 |
| 2 | 区块格式正确 | 发送 nil Prevote |
| 3 | 交易有效性 | 发送 nil Prevote |
| 4 | 通过 | 进入 Prevote |

**超时**：`timeout_propose = 3000ms * (round + 1)`

#### Round 0：Prevote 阶段

**触发条件**：收到有效 Proposal 或超时

**Prevote 消息格式**：
```go
type MsgPrevote struct {
    BlockHash []byte // 投票的区块哈希（nil 表示跳过）
    Round     int64  // 轮次
    Signature []byte // 验证者签名
    Sender    Address // 发送者地址
}
```

**验证者行为**：

```go
// 伪代码
func (cs *ConsensusState) enterPrevote() {
    // 1. 如果有有效 Proposal，投给 BlockHash
    if cs.Proposal != nil && cs.validateBlock(cs.Proposal) {
        cs.signAndBroadcast(&MsgPrevote{
            BlockHash: hash(cs.Proposal.Block),
            Round: cs.Round,
        })
    } else {
        // 2. 否则投给 nil
        cs.signAndBroadcast(&MsgPrevote{
            BlockHash: nil,
            Round: cs.Round,
        })
    }

    // 3. 等待 Prevote
    cs.waitForPrevotes()
}
```

**2/3 多数计算**：
```go
func HasTwoThirdsMajority(votes *VoteSet) bool {
    totalPower := votes.TotalVotingPower()
    for hash, power := votes.VotePowerTally() {
        if power > (2 * totalPower / 3) {
            return true, hash  // 返回多数哈希
        }
    }
    return false, nil
}
```

**超时处理**：
- 超时时间：`timeout_prevote = 1000ms * (round + 1)`
- 超时后：进入下一轮（Round + 1）

#### Round 0：Precommit 阶段

**触发条件**：观察到 2/3 Prevote 多数

**Precommit 消息格式**：
```go
type MsgPrecommit struct {
    BlockHash []byte // 提交的区块哈希
    Round     int64  // 轮次
    Signature []byte // 验证者签名
}
```

**验证者行为**：

```go
func (cs *ConsensusState) enterPrecommit(blockHash []byte) {
    // 1. 广播 Precommit
    cs.signAndBroadcast(&MsgPrecommit{
        BlockHash: blockHash,
        Round: cs.Round,
    })

    // 2. 等待 Precommit
    cs.waitForPrecommits()

    // 3. 收到 2/3 Precommit 后提交
    if cs.votes.HasTwoThirdsPrecommit() {
        cs.enterCommit()
    }
}
```

#### Commit 阶段

**触发条件**：收到 2/3 Precommit

**提交行为**：
```go
func (cs *ConsensusState) enterCommit() {
    // 1. 执行区块
    cs.stateMachine.ExecuteBlock(cs.CommittedBlock)

    // 2. 写入存储
    cs.blockStore.SaveBlock(cs.CommittedBlock)

    // 3. 进入下一高度
    cs.enterNewHeight(cs.Height + 1)
}
```

### Tendermint 状态机

```
状态转换：

NewHeight
    ↓
NewRound (选择 Proposer)
    ↓
Propose (等待 Proposal)
    ↓
Prevote (收集 Prevote)
    ↓
Precommit (收集 Precommit) ──[2/3 Precommit]──> Commit
    │                                              │
    └──[超时/无多数]───────────────────────────────┘
                                                   ↓
                                            NewRound (Round++)
```

### 设计取舍

| 设计选择 | 优势 | 劣势 | 取舍原因 |
|----------|------|------|----------|
| 两阶段投票 | 减少一轮通信，延迟更低 | 需要更严格的同步假设 | 优化区块确认时间 |
| Round-robin Proposer | 去中心化，抗审查 | 频繁 Leader 切换 | 避免单点故障 |
| 超时驱动 | 简化视图转换，自恢复 | 网络不稳定时可能多轮 | 简化协议复杂度 |
| PoS 原生集成 | 无需额外共识层 | 验证者集相对固定 | 与 Cosmos 经济模型对齐 |

## 边界与前提

### 角色归属表

| 角色 | 作用说明 | Protocol-native | Official | Third-party | 状态 |
|------|----------|-----------------|----------|-------------|------|
| Proposer | 区块提议（轮转） | ✓ | - | - | live |
| Validator | 投票验证（需质押） | ✓ | - | - | live |
| Full Node | 同步和验证，不质押 | - | ✓ | ✓ | live |
| Light Client | 轻节点，验证头部 | - | ✓ | ✓ | live |

### 能力边界

**能解决**：
- 拜占庭容错共识（≤1/3 故障节点）
- PoS 验证者管理
- 即时最终性保证
- 自恢复（超时驱动）

**不能解决**：
- 网络完全异步场景
- 长程攻击（需要检查点）
- 应用层逻辑

**故障假设**：部分同步网络
**容错比例**：≤1/3 拜占庭节点
**状态**：live（成熟）

## 相关对象关系

### 与相邻协议的关系

| 对象 | 关系类型 | 说明 |
|------|----------|------|
| PBFT | 前身 | Tendermint 简化了 PBFT 的三阶段 |
| QBFT | 替代方案 | 企业级 BFT，联盟链场景 |
| HotStuff | 演进方案 | Facebook Libra 的 BFT 协议，进一步优化 |
| Malachite | 新兴替代 | Rust 实现的高性能 BFT |
| Simplex | 新兴替代 | Commonware 的高吞吐 BFT |

## 结论

**已确认**：
- 【L1 证据】Tendermint 是第一个 PoS+BFT 原生集成的共识协议
- 【L1 证据】采用两阶段投票（Prevote/Precommit）
- 【L1 证据】超时驱动的 Round 转换机制
- 【L1 证据】Cosmos Hub 及多个 Cosmos SDK 链在使用

**尚需验证**：
- 与 IBC 跨链协议的深度集成细节
- Cosmos Hub 升级后的变化

## 待确认问题

| 问题 | 状态 | 下一步 |
|------|------|--------|
| IBC 集成细节 | 部分解决 | 阅读 IBC 规范 |
| Cosmos Hub 升级后变化 | 未解决 | 追踪 Cosmos Hub 升级 |

## 参考资料

| 来源 | 说明 |
|------|------|
| Tendermint 官方文档 | L1 来源 |
| Cosmos Hub 文档 | L1 来源 |
| https://github.com/tendermint/tendermint | L2 来源，参考实现 |
