# 术语治理政策

## 目的

定义术语的创建、复用、引用和冲突解决规则，确保跨 topic 的术语一致性。

**注意**：本文件是治理规则，不是术语表本身。术语表位于 `knowledge/glossary/` 和各 topic 下。

## 术语条目最小字段

每个术语条目必须包含：

```yaml
term: <canonical term>
aliases:
  - <alias 1>
  - <alias 2>
definition: <简洁定义，1-2 句>
boundaries:
  includes:
    - <明确包含的内容>
  excludes:
    - <明确不包含的内容>
forbidden_confusions:
  - <不可与哪些术语混淆>
usage_constraints:
  - <使用约束>
related_terms:
  - term: <相关术语>
    relation: <关系类型>
sources:
  - <source id>
```

### 字段说明

| 字段 | 说明 | 是否必填 |
|------|------|----------|
| `term` | 规范术语（canonical form） | 必填 |
| `aliases` | 同义词、缩写、变体 | 可选 |
| `definition` | 简洁定义，1-2 句 | 必填 |
| `boundaries` | 边界声明（includes/excludes） | 可选，新术语建议填写 |
| `forbidden_confusions` | 易混淆术语列表 | 可选，有已知陷阱时必填 |
| `usage_constraints` | 使用约束 | 可选 |
| `related_terms` | 相关术语及关系 | 可选 |
| `sources` | 来源 ID 列表 | 必填 |

## 何时新建术语

**必须**新建术语当：

1. 当前 topic 引入新概念，且：
   - 与已有术语有不同边界或约束
   - 需要在 `boundaries` 中明确声明范围

2. 下层 topic 定义了新的实体或机制

**禁止**新建术语当：

1. 仅是已有术语的 synonym（应使用 `aliases`）
2. 术语边界与已有术语重叠超过 80%
3. 未在 L1/L2 来源中出现

### 新建流程

```
1. 检查 knowledge/glossary/ 中是否已有该术语
2. 检查依赖的 topic 中是否已有定义
3. 在 topic 的 terms/ 下创建术语条目
4. 如为跨 topic 通用术语，提交到 knowledge/glossary/
```

## 何时复用术语

**必须**复用术语当：

1. 同一概念在同一 context 中已有定义
2. 依赖的 topic 中已定义该术语
3. 官方规范中使用相同术语

**复用方式**：

```yaml
# 在 topic 的 terms/ 下
term: UserOperation
refers_to: knowledge/glossary/terms/user-operation.md
context_note: 本 topic 中特指 EIP-4337 定义的 UserOperation
```

## Forbidden Confusions

### 已知的术语混淆陷阱

| 易混淆对 | 区分要点 |
|----------|----------|
| UserOperation vs Transaction | UserOperation 是 ERC-4337 概念，Transaction 是 L1 概念 |
| Bundler vs Block Builder | Bundler 打包 UserOp，Builder 打包交易 |
| Paymaster vs Gas Station | Paymaster 是协议原生，Gas Station 是第三方服务 |
| Account Abstraction vs Meta Transaction | AA 是协议层，Meta Tx 是应用层 |
| EntryPoint vs Executor | EntryPoint 是 AA 合约，Executor 是通用概念 |

### 在写作中的处理

**禁止**：
- "Bundler 类似于矿工"（混淆了不同 context 的角色）
- "UserOperation 就是交易"（忽略关键差异）

**必须**：
- 首次使用时明确"不同于 X，本术语 Y 指..."
- 在 `boundaries.excludes` 中明确排除项

## 在 Principle / Comparison / Diagram 中引用术语

### Principle 中

```markdown
## 关键术语

**UserOperation**
: ERC-4337 定义的用户操作原子，包含 sender, nonce, initCode, callData 等字段。
  不同于 Transaction，UserOperation 不直接存在于 L1 状态。

引用：`knowledge/glossary/terms/user-operation.md`
```

### Comparison 中

```yaml
terms_used:
  - term: UserOperation
    definition_source: knowledge/glossary/terms/user-operation.md
    comparison_context: 比较不同 AA 方案的 operation 格式
```

### Diagram 中

```plantuml
' 术语映射
rectangle "UserOperation" as UO
note "包含 sender, nonce, callData" as UO_NOTE
UO .. UO_NOTE
```

## 冲突术语处理

### 发现冲突时

当同一术语在不同 topic 中有不同定义：

1. **检查 context 是否不同**
   - 如 context 不同，明确标注各自 context
   - 如 context 相同，进入 reconciliate 流程

2. **Reconciliate 流程**：
   ```
   a. 列出所有定义及其来源
   b. 识别差异点（边界、约束、使用场景）
   c. 判断是否为同一概念
   d. 如为同一概念，选择 canonical 定义，其他列为 aliases
   e. 更新 knowledge/glossary/terms/<term>.md
   ```

3. **记录决策**：
   ```yaml
   term: <术语>
   conflict_id: CONF-<number>
   resolution:
     canonical_definition: <来源>
     rationale: <选择原因>
     deprecated_definitions:
       - source: <来源>
         reason: <废弃原因>
   ```

### 术语漂移检测

**必须**定期运行脚本检测术语漂移：

```bash
scripts/research/find_term_drift.py --term <term>
```

**检测内容**：
- 定义与原始来源是否一致
- 是否有 topic 使用了不同边界
- aliases 是否被错误地当作独立术语

## 术语表位置

| 范围 | 位置 |
|------|------|
| 跨 topic 通用 | `knowledge/glossary/terms/<term>.md` |
| topic 特有 | `knowledge/topics/<topic>/terms/<term>.md` |
| domain 特有 | `knowledge/domains/<domain>/terms/<term>.md` |

## 示例：完整术语条目

```yaml
# knowledge/glossary/terms/user-operation.md
---
name: user-operation
term: UserOperation
aliases:
  - UserOp
  - user operation (小写)
definition: |
  ERC-4337 定义的用户操作原子，包含执行用户意图所需的全部信息。
  UserOperation 不直接存在于 L1 状态，而是通过 EntryPoint 合约处理。
boundaries:
  includes:
    - sender 账户地址
    - nonce 防重放
    - initCode (可选) 合约部署代码
    - callData 调用数据
    - gas 限制和价格参数
    - paymaster 相关字段 (可选)
    - signature 用户签名
  excludes:
    - L1 Transaction 的 blockNumber
    - L1 Transaction 的 transactionIndex
    - 传统交易的 v/r/s 签名格式
forbidden_confusions:
  - 不可与 Transaction 混用
  - 不可与 CallRequest 混用
usage_constraints:
  - 仅在 ERC-4337 上下文中使用
  - 必须区分 UserOperation 和包装后的 Transaction
related_terms:
  - term: Transaction
    relation: mapped-to
  - term: EntryPoint
    relation: processed-by
sources:
  - eip-4337
  - account-abstraction-repo
---

## 正文

[术语定义正文，可用于引用]
```
