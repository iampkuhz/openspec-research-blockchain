# 共识算法流程描述规约

## 目的

定义 consensus primitive 分析中**流程描述**和**对比分析**的深度要求，确保：
1. 流程描述精确到算法步骤，而非高层概述
2. 对比分析解释"为什么"，而非仅罗列差异

## 问题 1：流程描述不够深入

### 当前问题

现有分析停留在高层概述：
```markdown
【S1】Proposer 选择：基于 PoS 权重和 round-robin 选择当前高度的提议者
【S2】Prevote 阶段：验证者对 proposal 进行 prevote 投票，收集 2/3 多数
【S3】Precommit 阶段：prevote 通过后进行 precommit 投票
```

**缺失的信息**：
- 具体是什么消息？字段是什么？
- 什么时候超时？超时后做什么？
- 2/3 是指什么？如何计算？
- Prevote 通过后发生什么？不通过呢？
- 为什么可以省略 PBFT 的 Prepare 阶段？

### 要求的流程描述深度

#### 必须覆盖的要素

对于每个共识阶段，必须描述：

| 要素 | 说明 | 示例问题 |
|------|------|----------|
| **触发条件** | 什么事件启动这个阶段？ | 收到 Proposal 消息？超时？ |
| **输入消息** | 接收什么消息？字段？ | `MsgProposal{Block, Round, Signature}` |
| **本地验证** | 节点验证什么？ | 签名有效？Quorum 证书有效？ |
| **状态转换** | 节点状态如何变化？ | `State.Round = Round + 1` |
| **输出消息** | 发送什么消息？给谁？ | 广播 `MsgPrevote{BlockHash, Round}` |
| **超时处理** | 超时后做什么？ | 进入下一轮，发送 `Nil` 投票 |
| **终止条件** | 阶段何时结束？ | 收到 2f+1 条 Precommit |

#### 消息格式定义

必须定义关键消息的结构：

```markdown
### 消息格式

**Proposal 消息**：
```go
type MsgProposal struct {
    Block     Block  // 提议的区块
    Round     int64  // 当前轮次
    Signature []byte // Proposer 签名
}
```

**Prevote 消息**：
```go
type MsgPrevote struct {
    BlockHash []byte // 投票的区块哈希（nil 表示跳过）
    Round     int64  // 轮次
    Signature []byte // 验证者签名
}
```
```

#### 状态机定义

必须定义节点状态转换：

```markdown
### Tendermint 状态机

```
状态：
- RoundStepNewHeight: 新区块高度开始
- RoundStepNewRound: 新轮次开始
- RoundStepPropose: 等待 Proposal
- RoundStepPrevote: 等待 Prevote
- RoundStepPrecommit: 等待 Precommit
- RoundStepCommit: 提交区块

转换：
NewHeight → NewRound → Propose → Prevote → Precommit → Commit → NewHeight...
```
```

## 问题 2：对比分析不深入

### 当前问题

现有对比停留在表格罗列：

| 维度 | PBFT | Tendermint |
|------|------|------------|
| 投票阶段 | 三阶段 | 两阶段 |

**缺失的信息**：
- 为什么 PBFT 需要三阶段？
- 为什么 Tendermint 可以省略一阶段？
- 省略的代价是什么？
- 两者的安全性证明有什么差异？

### 要求的对比分析深度

#### 必须回答的"为什么"问题

对于每个差异点，必须回答：

1. **设计原因**：为什么这样设计？
2. **前提条件**：依赖什么假设才能成立？
3. **代价/权衡**：获得了什么，失去了什么？
4. **边界情况**：在什么情况下这个设计不工作？

#### 对比框架

使用以下框架进行对比：

```markdown
### 差异分析：两阶段 vs 三阶段

**PBFT 为什么需要三阶段？**

PBFT 的三阶段（Pre-prepare → Prepare → Commit）设计原因：

1. **Pre-prepare**：Leader 提议，绑定视图 V 和序列号 N
   - 目的：在异步网络中，确保 Leader 不会为同一序列号发送两个不同请求
   - 必要性：没有这步，无法防止 Leader 作恶

2. **Prepare**：验证者确认收到 Pre-prepare
   - 目的：形成"准备证书"（2f+1 个 Prepare），证明大多数节点同意处理这个请求
   - 必要性：没有这步，无法进入 Commit 阶段

3. **Commit**：验证者确认准备完成
   - 目的：形成"提交证书"，确保最终性

**Tendermint 为什么可以两阶段？**

Tendermint 的两阶段（Prevote → Precommit）设计原因：

1. **依赖同步假设**：Tendermint 假设部分同步网络，有超时机制
   - 关键差异：PBFT 假设异步网络，Tendermint 假设部分同步
   - 代价：在完全异步网络中可能无法进展

2. **轮次概念**：Tendermint 有 Round 概念，PBFT 有 View 概念
   - Round 超时后自动进入下一轮
   - 不需要显式的 View Change 协议

3. **PoS 集成**：验证者集固定，通过 PoS 选择 Proposer
   - 简化：不需要 PBFT 的复杂 Leader 选举

**代价分析**：

| 特性 | PBFT 优势 | Tendermint 优势 |
|------|----------|-----------------|
| 网络假设 | 异步网络也能工作 | 部分同步网络更高效 |
| 延迟 | 3 轮通信 | 2 轮通信 |
| View Change | 复杂但安全 | 简单但依赖超时 |
| 适用场景 | 联盟链、广域网 | PoS 公链 |
```

## 质量要求

### 1. 流程深度（必须）

对于共识算法的核心流程，必须覆盖：

- [ ] 每个阶段的触发条件
- [ ] 每个阶段的输入消息格式
- [ ] 每个阶段的本地验证逻辑
- [ ] 每个阶段的状态转换
- [ ] 每个阶段的输出消息
- [ ] 每个阶段的超时处理
- [ ] 每个阶段的终止条件

### 2. 对比深度（必须）

对于与 PBFT 的对比，必须回答：

- [ ] 为什么 PBFT 需要这个阶段？
- [ ] 为什么 Tendermint 可以省略？
- [ ] 省略的代价是什么？
- [ ] 两者的安全性假设有何不同？

### 3. 代码/伪代码（推荐）

对于核心逻辑，推荐使用伪代码：

```go
// Tendermint Prevote 阶段伪代码
func (cs *ConsensusState) handlePrevote(msg *MsgPrevote) {
    // 1. 验证签名
    if !verifySignature(msg.Signature, msg.Sender) {
        return
    }

    // 2. 验证轮次匹配
    if msg.Round != cs.Round {
        return
    }

    // 3. 累加投票
    cs.votes.AddPrevote(msg)

    // 4. 检查是否达到 2/3
    if cs.votes.HasTwoThirdsPrevote() {
        cs.enterPrecommit()
    }
}
```

## 示例：好的 vs 坏的

### 坏的示例（流程描述）

```markdown
【S1】Proposer 选择：基于 PoS 权重和 round-robin 选择当前高度的提议者
【S2】Prevote 阶段：验证者对 proposal 进行 prevote 投票
【S3】Precommit 阶段：prevote 通过后进行 precommit 投票
```

**问题**：
- 没有消息格式
- 没有状态转换
- 没有超时处理
- 没有解释"为什么是两阶段"

### 好的示例（流程描述）

```markdown
### Tendermint 共识流程详解

#### Round 0：Proposer 选择

**触发条件**：新区块高度开始，或上一轮超时

**Proposer 选择算法**：
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

**触发条件**：被选为 Proposer

**Proposer 行为**：
1. 从 Mempool 获取交易
2. 构造区块 `Block{Transactions, Height, Round}`
3. 签名并广播 `MsgProposal{Block, Signature}`

**验证者行为**：
1. 等待 `MsgProposal`
2. 验证：
   - Proposer 签名有效
   - 区块格式正确
   - 交易有效性
3. 如果有效，进入 Prevote；否则发送 `Nil` 投票

#### Round 0：Prevote 阶段

**超时时间**：`timeout_prevote = 1000ms * (Round + 1)`

**验证者行为**：
1. 广播 `MsgPrevote{BlockHash, Round, Signature}`
   - 如果收到有效 Proposal，`BlockHash = hash(Block)`
   - 如果没收到或无效，`BlockHash = nil`
2. 收集来自其他验证者的 Prevote
3. 当收到 **2/3 多数**（2f+1 条）Prevote 时：
   - 如果 2/3 投给同一区块：进入 Precommit
   - 如果 2/3 投给 nil 或分散：超时，进入下一轮

**2/3 计算**：
```go
func HasTwoThirdsMajority(votes *VoteSet) bool {
    totalPower := votes.TotalVotingPower()
    for hash, count := votes.VoteTally() {
        if count > (2 * totalPower / 3) {
            return true
        }
    }
    return false
}
```

#### Round 0：Precommit 阶段

**触发条件**：观察到 2/3 Prevote 多数

**验证者行为**：
1. 广播 `MsgPrecommit{BlockHash, Round, Signature}`
2. 收集 Precommit
3. 当收到 **2/3 多数** Precommit 时：
   - 区块被提交
   - 进入 Commit 阶段

**为什么两阶段就够了？**

Tendermint 的两阶段（Prevote + Precommit）相当于 PBFT 的 Prepare + Commit，省略了 Pre-prepare，原因是：

1. **同步假设**：Tendermint 假设部分同步网络，Proposer 在超时内必须发送 Proposal
2. **轮次隔离**：每个 Round 是独立的，Round N 的投票不影响 Round N+1
3. **PoS 经济安全**：验证者质押了代币，作恶会被罚没

**代价**：
- 在完全异步网络中可能无法进展（依赖超时）
- 需要更强的同步假设
```

## 相关文件

- `openspec/specs/analysis-principles/spec.md`：分析原则总政策
- `openspec/specs/evidence-policy/spec.md`：证据等级政策
