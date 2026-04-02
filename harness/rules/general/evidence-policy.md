# 证据政策规则

## 目的

定义本仓库研究工作的证据要求和处理方式。

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

### L2 - 参考实现

**来源**：
- 官方代码仓库
- SDK / API 文档
- 参考实现代码
- 开发者文档

**可信度**：高
**引用方式**：代码片段 + 仓库链接
**示例**：
```yaml
source_id: account-abstraction-repo
type: implementation
url: https://github.com/eth-infinitism/account-abstraction
commit: abc123
```

### L3 - 官方生态材料

**来源**：
- 官方博客
- Release notes
- Roadmap 文档
- 生态系统材料

**可信度**：中
**使用约束**：不可作为技术实现的唯一证据
**示例**：
```yaml
source_id: vitalik-blog-aa
type: blog
url: https://vitalik.eth.limo/general/2021/...
note: 说明设计动机，但不作为实现证据
```

### L4 - 第三方分析

**来源**：
- 技术博客
- 媒体文章
- 社区讨论
- 第三方分析

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

### 规则 2：区分能力归属

**必须**区分三层能力：

| 层级 | 描述 | 示例 |
|------|------|------|
| protocol-native | 协议原生能力 | EIP-4337 的 UserOperation |
| official-ecosystem | 官方生态能力 | ERC-4337 参考实现 |
| third-party | 第三方能力 | Stackup Bundler |

**禁止**将第三方能力描述为协议能力。

### 规则 3：区分状态

**必须**区分三种状态：

| 状态 | 描述 | 证据要求 |
|------|------|----------|
| shipped | 已上线 | L1 或 L2 证明已部署 |
| planned | 规划中 | L3 说明规划来源 |
| promotional | 宣传性 | L4 标注为市场材料 |

## 证据矩阵

### 结构要求

每个 change 必须包含 `evidence-matrix.md`：

```markdown
## Claim 映射

| Claim | Source ID | Evidence Level | Confidence |
|-------|-----------|----------------|------------|
| ...   | ...       | L1/L2/L3/L4    | high/med/low |
```

### 置信度计算

- 多个独立 L1 → high
- 单一 L1 或多 L2 → high
- 仅 L3 → medium
- 有 L4 支持但无 L1/L2 → low

## Evidence Gap 处理

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
    source_type: standard|implementation|blog|discussion
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
