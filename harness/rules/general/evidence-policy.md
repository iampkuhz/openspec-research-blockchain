# 证据政策规则

## 目的

定义本仓库研究工作的证据等级、使用要求和 Claim 映射规范。

## 证据等级

### L1 - 官方规范

**来源**：
- 协议规范文档
- EIP / ERC 标准
- 白皮书
- RFC

**可信度**：最高
**引用方式**：直接引用原文 + 链接

**示例**：
```yaml
source_id: eip-4337
type: standard
url: https://eips.ethereum.org/EIPS/eip-4337
accessed_at: 2024-01-15
```

### L2 - 实现与深度技术分析

**来源（两类）**：

| 类型 | 说明 | 示例 |
|------|------|------|
| 参考实现 | 官方代码仓库、SDK、API 文档 | account-abstraction 参考实现 |
| 高质量技术分析 | 对技术细节和实现流程进行深入分析的博客文章 | Vitalik 博客中关于 EIP 技术细节的分析 |

**高质量技术分析的标准**：
- 包含代码级别的技术细节
- 有清晰的流程/机制分析
- 作者具有领域专业知识（如核心开发者、协议研究者）

**非高质量技术分析（仍为 L4）**：
- 行业发展评价
- 市场前景分析
- 感性评论而非技术细节

**可信度**：高
**引用方式**：代码片段 + 链接 / 博客分析 + 链接

**示例**：
```yaml
# 参考实现
source_id: account-abstraction-repo
type: implementation
url: https://github.com/eth-infinitism/account-abstraction
commit: abc123

# 高质量技术分析
source_id: vitalik-blog-aa
type: technical-analysis
url: https://vitalik.eth.limo/general/2021/...
note: 对 ERC-4337 技术细节的深度分析
```

### L3 - 官方生态材料

**来源**：
- 官方博客（无技术细节）
- Release notes
- Roadmap 文档
- 生态系统材料

**可信度**：中
**使用约束**：不可作为技术实现的唯一证据
**示例**：
```yaml
source_id: eth-blog-announcement
type: official-blog
url: https://blog.ethereum.org/...
note: 用于说明规划来源，不作为实现证据
```

### L4 - 第三方分析

**来源**：
- 第三方技术博客（无深度分析）
- 媒体文章
- 社区讨论
- 第三方分析报告

**可信度**：低
**使用约束**：
- 仅用于补充背景
- 不可作为核心主张证据
- 必须标注为第三方观点

## 证据使用规则

### 规则 1：技术主张优先 L1/L2

**禁止**仅基于 L3/L4 做出技术实现主张。

**必须**：
- 核心机制主张有 L1 或 L2 支持
- 如只有 L3/L4，降低结论强度
- 明确标注证据缺口

**示例对比**：

❌ 错误：
> "EIP-7702 使用 SENTINUM 指令"（仅有博客提到）

✅ 正确：
> "根据 Vitalik 博客 [L3]，EIP-7702 计划引入新指令，但具体 opcode 尚未在规范中定义 [evidence gap]"

### 规则 2：区分状态

**必须**区分三种状态：

| 状态 | 描述 | 证据要求 |
|------|------|----------|
| shipped | 已上线 | L1 或 L2 证明已部署 |
| planned | 规划中 | L3 说明规划来源 |
| promotional | 宣传性 | L4 标注为市场材料 |

**示例**：

```yaml
# Shipped - 有 L1 证明
- claim: "EIP-4337 已在 Ethereum 主网激活"
  sources: [eip-4337]
  status: shipped

# Planned - 只有 L3
- claim: "EIP-7702 计划引入 ACCOUNT_DELEGATION 指令"
  sources: [vitalik-blog-7702]
  status: planned

# Promotional - L4 宣传材料
- claim: "某项目将革命化账户抽象"
  sources: [project-announcement]
  status: promotional
```

## Claim 定义与粒度

### 什么是 `claim`

**`claim`** = 一个可验证的技术主张/断言

**注意**：本文件统一使用英文 `claim` 作为术语，中文"主张"或"声明"仅在非技术性描述中出现。在技术文档写作中，必须使用 `` `claim` `` 格式（行内代码）以区别于日常英文。

详情见：`harness/GLOBAL-GLOSSARY.md`

**判断标准**：
- 能用一句话清晰表述
- 有明确的真伪判断
- 能追溯到具体来源

### `claim` 粒度示例

| ❌ 不是 Claim（太笼统） | ✅ 是 Claim（可验证） |
|--------------------------|------------------------|
| "ERC-4337 很好" | "UserOperation 包含 sender 字段" |
| "Bundler 负责提交" | "Bundler 调用 handleOps() 提交 UserOp" |
| "Gas 费用很低" | "verificationGasLimit 默认 100000" |
| "AA 生态很成熟" | "Stackup 是 ERC-4337 Bundler 实现方之一" |

### `claim` 拆分原则

**一个 `claim` 应该多细？**

| 场景 | 一个 Claim | 拆成多个 Claims |
|------|-----------|-----------------|
| 字段定义 | "UserOp 包含 sender/nonce/callData" | 拆成 3 个 Claim：每个字段一个 |
| 流程步骤 | "Bundler 提交 UserOp 到 EntryPoint" | 拆成多个 Claim：每个步骤一个 |
| 条件判断 | "签名验证通过后才执行" | 拆成 2 个 Claim：验证条件 + 执行结果 |

**示例**：

```yaml
# ❌ 一个 Claim 包含太多内容
claim-bad: "UserOperation 包含 sender, nonce, callData, initCode 等字段，Bundler 负责提交到 EntryPoint"

# ✅ 拆分成独立 Claims
claim-001: "UserOperation 包含 sender 字段（地址类型）"
claim-002: "UserOperation 包含 nonce 字段（uint256 类型）"
claim-003: "UserOperation 包含 callData 字段（bytes 类型）"
claim-004: "Bundler 通过 EntryPoint.handleOps() 提交 UserOp"
```

## 证据矩阵

### 结构要求

每个 change 必须包含 `evidence-matrix.md` 或 `sources/source-pack.yaml` 中的 `claim` 映射：

```markdown
## Claim 映射

| `claim` ID | `statement` 内容 | Source ID | Evidence Level | Confidence |
|----------|-----------|-----------|----------------|------------|
| `claim-001` | "UserOperation 包含 sender 字段" | eip-4337 | L1 | high |
| `claim-002` | "Bundler 调用 handleOps()" | eip-4337, aa-repo | L1 + L2 | high |
| `claim-003` | "Stackup 是主流 Bundler 提供商" | stackup-docs | L2 | medium |
```

### 置信度计算

| `evidence` 组合 | `confidence` |
|----------|------------|
| 多个独立 L1 | `high` |
| 单一 L1 或多 L2 | `high` |
| 仅 L3 | `medium` |
| 有 L4 支持但无 L1/L2 | `low` |

## `evidence-gap` 处理

### 必须记录的场景

1. 机制细节在 L1 中未明确
2. 实现与规范有差异
3. 不同来源有冲突
4. 依赖未来规划

### 记录格式

```yaml
gap_id: GAP-001
description: EIP-7702 的具体 gas 成本计算方式未在规范中明确
impact: 影响成本估算准确性
related_claims:
  - claim-tx-gas
sources_checked:
  - eip-7702-draft
  - vitalik-blog-7702
status: unresolved
```

## Source Pack 字段

每个 topic 的 `sources/source-pack.yaml` 必须包含：

```yaml
sources:
  - source_id: <unique-id>
    title: <标题>
    url: <链接或本地引用>
    source_type: standard|implementation|technical-analysis|official-blog|blog|discussion
    source_tier: L1|L2|L3|L4
    accessed_at: <日期>
    relevant_atoms:
      - definition
      - core-mechanism
    supported_claims:
      - claim-001
      - claim-002
    confidence: high|medium|low
    notes: <可选说明>
```

## 术语统一说明

本文件中的核心术语：

| 术语 | 格式 | 说明 |
|------|------|------|
| `claim` | 行内代码 | 可验证的技术主张 |
| `statement` | 行内代码 | `claim` 的具体表述内容（YAML 字段名） |
| `evidence` | 行内代码 | 支撑 `claim` 的来源材料 |
| `confidence` | 行内代码 | 置信度（high/medium/low） |
| `source` | 行内代码 | `evidence` 的载体 |

详情见：`harness/GLOBAL-GLOSSARY.md`
