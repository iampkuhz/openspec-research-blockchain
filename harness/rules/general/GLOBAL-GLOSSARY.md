# 全局术语表 (Global Glossary)

本文件定义本仓库的**核心元术语**（meta-terminology）。

**注意**：本术语表不同于 `knowledge/glossary/` 中的技术术语。本表定义的是**研究工作本身**使用的术语，而非研究对象（如区块链协议）的术语。

---

## 术语使用规范

### 格式要求

**必须**使用行内代码格式（`` `term` ``）强调以下术语：

```markdown
每个 `claim` 必须有对应的 `source` 支撑。
```

**目的**：
1. 区分术语与普通英文单词（如 `claim` vs "the leader claim company's policy"）
2. 强化术语边界，避免混淆

---

## 核心元术语

### `claim`

**定义**：一个可验证的技术主张/断言。

**特征**：
- 能用一句话清晰表述
- 有明确的真伪判断
- 能追溯到具体 `source`

**示例**：
- ✅ `"UserOperation 包含 sender 字段"` — 可验证
- ❌ `"ERC-4337 很好"` — 主观评价，不可验证

**相关字段**：
- `statement`：`claim` 的具体表述内容（YAML 字段名）
- `evidence_level`：证据等级（L1/L2/L3/L4）
- `confidence`：置信度（high/medium/low）

**来源**：`openspec/specs/evidence-policy/spec.md`

---

### `evidence`

**定义**：支撑 `claim` 的来源材料。

**证据等级**：

| 等级 | 来源类型 | 示例 |
|------|----------|------|
| `L1` | 官方规范 | EIP、白皮书、RFC |
| `L2` | 参考实现/深度技术分析 | 官方代码仓库、Vitalik 技术分析博客 |
| `L3` | 官方生态材料 | 官方博客、Roadmap |
| `L4` | 第三方分析 | 社区博客、媒体文章 |

**来源**：`openspec/specs/evidence-policy/spec.md`

---

### `source`

**定义**：`evidence` 的载体，`claim` 的追溯目标。

**必填字段**：
- `source_id`：唯一标识符
- `url`：链接或本地引用
- `source_type`：类型（standard/implementation/technical-analysis/blog/discussion）
- `source_tier`：等级（L1/L2/L3/L4）
- `accessed_at`：访问日期

**来源**：`harness/rules/general/traceability-policy.md`

---

### `confidence`

**定义**：对 `claim` 为真的确信程度。

**枚举值**：

| 值 | 说明 | 证据组合示例 |
|------|------|-------------|
| `high` | 高置信度 | 多个独立 L1 或单一 L1 + 多 L2 |
| `medium` | 中置信度 | 仅 L3 |
| `low` | 低置信度 | 有 L4 支持但无 L1/L2 |

**来源**：`openspec/specs/evidence-policy/spec.md`

---

### `atom`

**定义**：知识的最小组织单元。

**类型**：
- `primitive`：底层机制（如 `eip-4337` 的 `core-mechanism`）
- `synthesis`：演进/综合分析（如 `aa-eip-evolution`）
- `decision`：场景判断（如 `agentic-payment`）

**位置**：
- `knowledge/analysis/primitives/`
- `knowledge/analysis/synthesis/`
- `knowledge/decisions/`

**来源**：`AGENTS.md` (资产层定义)

---

### `topic`

**定义**：一个完整的研究对象，由多个 `atom` 组成。

**示例**：
- `eip-4337`：包含 `definition`、`core-mechanism`、`limits-and-assumptions` 等 `atom`
- `consensus-malachite`：包含 `definition`、`core-mechanism` 等 `atom`

**来源**：`openspec/schemas/blockchain-research/schema.yaml`

---

### `change`

**定义**：一次研究变更包，包含从问题定义到评审的完整过程产物。

**路径**：`openspec/changes/<change-id>/`

**核心产物**：
- `request.md`：问题定义
- `plan.md`：研究计划与来源规划
- `draft.md`：集中 review 稿
- `sources/`：来源抓取、摘录与 source review

**来源**：`harness/rules/general/traceability-policy.md`

---

### `traceability`

**定义**：知识可追溯性，包含四个层级：

| 层级 | 追溯关系 | 说明 |
|------|----------|------|
| L1 | `claim` → `source` | 每个 `claim` 必须可追溯到具体 `source` |
| L2 | `atom` → `claim` | 每个 `atom` 必须绑定 `claim` |
| L3 | `topic` → `atom` | 每个 `topic` 必须有 `atom` 索引 |
| L4 | `change` → `topic` | 每次更新必须有 `change` 记录 |

**来源**：`harness/rules/general/traceability-policy.md`

---

### `evidence-gap`

**定义**：证据缺口，指无法用 L1/L2 证据支撑的 `claim` 或机制细节。

**必须记录的场景**：
1. 机制细节在 L1 中未明确
2. 实现与规范有差异
3. 不同来源有冲突
4. 依赖未来规划

**记录格式**：
```yaml
gap_id: GAP-001
description: EIP-7702 的具体 gas 成本计算方式未在规范中明确
impact: 影响成本估算准确性
related_claims:
  - claim-tx-gas
status: unresolved
```

**来源**：`openspec/specs/evidence-policy/spec.md`

---

## 术语关系图

```
┌─────────────┐    supports    ┌─────────────┐
│   source    │ ─────────────► │    claim    │
└─────────────┘                └─────────────┘
       │                              │
       │ tier (L1/L2/L3/L4)           │ statement
       │                              │
       ▼                              ▼
┌─────────────┐               ┌─────────────┐
│  evidence   │               │ confidence  │
│   level     │               │ (high/med)  │
└─────────────┘               └─────────────┘
                                      │
                                      │ bounds
                                      ▼
                               ┌─────────────┐
                               │    atom     │
                               └─────────────┘
                                      │
                                      │ part-of
                                      ▼
                               ┌─────────────┐
                               │    topic    │
                               └─────────────┘
                                      ▲
                                      │
                               ┌─────────────┐
                               │   change    │ ──► updates
                               └─────────────┘
```

---

## 更新术语表

**流程**：
1. 创建 `openspec/changes/` 记录变更
2. 评审变更
3. 更新本文件

**原则**：
- 术语必须有明确边界
- 避免与日常英文单词混淆（使用行内代码格式）
- 优先使用英文，避免中英文混用
