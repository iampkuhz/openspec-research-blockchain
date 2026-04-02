# 不确定性处理规则

## 目的

规范如何识别、记录和传达研究中的不确定性。

## 不确定性类型

### Type 1: 证据不足

**特征**：
- 只有 L3/L4 来源
- 官方文档未明确说明
- 实现与规范不一致

**记录方式**：
```yaml
uncertainty_id: UNC-001
type: insufficient-evidence
claim: claim-xxx
description: "仅有博客提到，规范未明确"
impact: "影响成本估算"
status: unresolved
```

### Type 2: 来源冲突

**特征**：
- 多个来源给出不同信息
- 官方与实现不一致
- 版本之间存在差异

**记录方式**：
```yaml
uncertainty_id: UNC-002
type: conflicting-sources
claim: claim-yyy
sources:
  - source_a: "说法 A"
  - source_b: "说法 B"
discrepancy: "具体差异"
resolution: pending
```

### Type 3: 技术未定

**特征**：
- 提案尚未通过
- 规范正在讨论
- 实现尚未完成

**记录方式**：
```yaml
uncertainty_id: UNC-003
type: not-finalized
subject: "EIP-7702 gas 计算"
status: draft
tracking:
  - eip-7702
  - eth-magicians-thread-xxx
```

### Type 4: 假设条件

**特征**：
- 基于特定假设的分析
- 条件性结论
- 依赖外部因素

**记录方式**：
```yaml
uncertainty_id: UNC-004
type: assumption
assumption: "假设 L2 采用相同 AA 方案"
consequence: "如假设不成立，结论需调整"
validity_check: 定期检查 L2 实现
```

## 在写作中处理不确定性

### 禁止的做法

❌ "可能是这样"（模糊）
❌ "看起来"（主观）
❌ "应该是"（猜测）
❌ 完全忽略不确定性

### 推荐的做法

✅ "根据 [来源 L3]，但目前规范未明确 [evidence gap]"
✅ "存在两种说法：A [来源 1] 和 B [来源 2]，待确认"
✅ "这是基于 X 假设的分析，如假设变化结论需调整"
✅ "这是当前理解，可能随规范更新而变化"

### 写作模板

```markdown
## 待确认问题

### UNC-001: Gas 计算方式

**问题**：EIP-7702 的具体 gas 计算方式未在规范中明确

**当前理解**：根据 Vitalik 博客 [L3]，可能使用以下公式：
```
gas = base_cost + calldata_cost
```

**证据缺口**：
- 规范草案未包含详细计算
- 参考实现尚未完成

**影响**：如计算方式变化，成本估算需调整

**追踪**：
- EIP-7702 规范更新
- 参考实现发布

**最后更新**：2024-01-15
```

## 在 Claims 中标记不确定性

### Claim 格式

```yaml
- claim_id: claim-xxx
  statement: "UserOperation 包含 sender 字段"
  sources:
    - source_id: eip-4337
      evidence_level: L1
  confidence: high
  uncertainty: null

- claim_id: claim-yyy
  statement: "EIP-7702 将降低 50% Gas"
  sources:
    - source_id: vitalik-blog-7702
      evidence_level: L3
  confidence: low
  uncertainty:
    type: insufficient-evidence
    description: "仅基于博客估算，实际取决于实现"
    impact: "成本分析可能有重大偏差"
```

### Confidence 等级

| 等级 | 条件 |
|------|------|
| high | L1 证据，无冲突 |
| medium | L2 证据，或 L1 有 minor 冲突 |
| low | 仅 L3/L4，或有重大冲突 |

## 在 Diagram 中标记不确定性

```plantuml
note right: 待确认 [UNC-001]
  Gas 计算方式
  规范未明确
  仅基于博客估算
end note
```

## 不确定性审查

### 定期审查

```bash
# 审查所有未决不确定性
scripts/research/review_uncertainties.py --topic <topic>
```

### 审查要点

- [ ] 是否有新来源解决不确定性
- [ ] 假设是否仍然有效
- [ ] 冲突来源是否有新进展
- [ ] 是否需要更新影响评估

### 更新流程

1. 检查相关来源更新
2. 更新不确定性状态
3. 如已解决，更新相关 claims
4. 记录在 changelog

## 示例：完整不确定性记录

```yaml
# uncertainties.yaml
uncertainties:
  - uncertainty_id: UNC-001
    created_at: 2024-01-10
    type: insufficient-evidence
    subject: "EIP-7702 Gas 计算"

    description: |
      EIP-7702 的具体 gas 计算方式在规范中未明确。
      目前仅有 Vitalik 博客中的粗略估算。

    current_understanding: |
      可能使用 base_cost + calldata_cost 模式，
      但具体参数未知。

    evidence_gaps:
      - 规范草案无详细公式
      - 无参考实现
      - 无官方测试向量

    related_claims:
      - claim-gas-estimate

    impact: |
      如计算方式与当前理解有重大差异，
      成本分析部分需要重写。

    status: unresolved

    tracking:
      - EIP-7702 规范更新
      - 参考实现发布

    last_reviewed: 2024-01-15
    next_review: 2024-02-15
```
