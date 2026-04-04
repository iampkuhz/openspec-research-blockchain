# 可追溯性政策

## 目的

确保所有知识主张（`claim`）都可追溯到来源，所有修改都可追溯到变更。

**术语统一说明**：本政策统一使用英文 `` `claim` `` 作为术语，YAML 字段使用 `` `statement` `` 表示 `claim` 的具体表述内容。详情见 `harness/GLOBAL-GLOSSARY.md`。

## 可追溯性层级

### L1: `claim` → `source`

每个 `claim` 必须可追溯到具体 `source`：

```yaml
# 在 claims/facts.yaml 中
- claim_id: claim-001
  statement: "EIP-4337 定义 UserOperation 为基本单位"
  sources:
    - source_id: eip-4337
      excerpt: "The UserOperation is the basic unit..."
      location: "Abstract"
  evidence_level: L1
  confidence: high
```

### L2: `atom` → `claim`

每个知识原子必须绑定 `claim`：

```markdown
<!-- 在 atoms/core-mechanism.md 中 -->
## UserOperation 处理流程

UserOperation 是 ERC-4337 的基本单位 [← claim-001]。

处理流程包括：
1. validateUserOp [← claim-015]
2. executeUserOp [← claim-016]
```

### L3: `topic` → `atom`

每个 `topic` 必须有 `atom` 索引：

```yaml
# 在 topic overview.md 中
atoms:
  definition: atoms/definition.md
  prerequisites: atoms/prerequisites.md
  core-mechanism: atoms/core-mechanism.md
  module-evolution: atoms/module-evolution.md
  limits-and-assumptions: atoms/limits-and-assumptions.md
```

### L4: `change` → `topic`

每次更新必须有 `change` packet：

```yaml
# 在 topic changelog.md 中
- date: 2024-01-15
  change_id: primitive-eip-4337-deep-dive-pass-1
  updated_atoms:
    - core-mechanism
    - module-evolution
  summary: "补充 gas 计算细节"
```

## 来源文件格式

### Source Pack YAML

```yaml
# sources/source-pack.yaml
version: "1.0"
topic: eip-4337
sources:
  - source_id: eip-4337
    title: "ERC-4337: Account Abstraction"
    url: https://eips.ethereum.org/EIPS/eip-4337
    source_type: standard
    source_tier: L1
    accessed_at: 2024-01-15
    relevant_atoms:
      - definition
      - core-mechanism
    supported_claims:
      - claim-001
      - claim-002
      - claim-015
    confidence: high
    notes: ""
```

### Excerpt 格式

```markdown
# sources/excerpts/eip-4337-abstract.md

Source: eip-4337
Location: Abstract
Captured_at: 2024-01-15

> ERC-4337: Account Abstraction Using Alt Mempool
>
> A proposal for account abstraction using a pseudo-transaction object called UserOperation.
> Users can send UserObjects that specify what they want to do, and "bundlers" will package these into transactions.

Relevance:
- Defines the core concept of UserOperation
- Establishes the bundler role

Related claims:
- claim-001 (UserOperation definition)
- claim-010 (Bundler role)
```

## 变更追溯

### Change Packet 内容

每个 `openspec/changes/<change-id>/` 必须包含：

```
<change-id>/
├── request.md           # 问题定义
├── plan.md              # 研究计划 + 来源规划
├── draft.md             # 术语 + 分析 + 结论
├── evidence-matrix.md   # `claim`-`source` 映射
├── sources/
│   ├── inbox.yaml       # 原始来源入口
│   ├── fetched/         # 抓取的来源
│   └── excerpts/        # 来源摘录
└── .openspec.yaml       # OpenSpec 元数据
```

### 从 Change 到 Knowledge 的追溯

```yaml
# 在 topic changelog.md 中
- date: 2024-01-15
  change_id: primitive-eip-4337-deep-dive-pass-1
  change_path: openspec/changes/primitive-eip-4337-deep-dive-pass-1/
  merged_at: 2024-01-15T10:30:00Z
  merge_commit: abc123
  updated_atoms:
    - file: atoms/core-mechanism.md
      changes:
        - section: "Gas Calculation"
          change_type: addition
          source_claims:
            - claim-020
            - claim-021
```

## 追溯性验证

### 验证脚本

```bash
# 验证 Claim-Source 追溯
scripts/research/validate_sources.py --topic eip-4337

# 验证 Atom-Claim 追溯
scripts/research/check_traceability.py --topic eip-4337

# 验证术语使用一致性
scripts/research/find_term_drift.py --topic eip-4337
```

### 验证规则

**必须通过**：
- 所有 `claim` 都有 `source` 绑定
- 所有 `atom` 都有 `claim` 支撑
- 所有术语都有定义来源
- 所有修改都有 `change` 记录

**禁止**：
- 无来源的主张
- 无 `claim` 的 `atom`
- 无 `change` 的主线修改

## 证据链示例

完整的证据链：

```
Topic: eip-4337
  ↓
Atom: core-mechanism.md
  ↓
  `claim`: claim-001 ("UserOperation 包含 sender, nonce, callData")
    ↓
    Source: eip-4337 (L1)
      ↓
      Excerpt: excerpts/eip-4337-section-core.md
        ↓
        URL: https://eips.ethereum.org/EIPS/eip-4337#core-components
```
