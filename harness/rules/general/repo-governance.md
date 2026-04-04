# 仓库治理规则

## 目的

定义本仓库的核心治理约束。

## 核心约束

### 约束 1：变更必须走 OpenSpec

**禁止**直接修改 `knowledge/` 下的主线知识资产。

**必须**通过以下流程：
1. 在 `openspec/changes/` 创建 change
2. 完成研究并产出 draft
3. 通过 review 后 apply 到 knowledge

**例外**：仅当修复明显的拼写错误、格式问题时，可直接修改（参见 [update-policy.md](./update-policy.md)）。

### 约束 2：证据可追溯

**禁止**无来源的主张。

所有技术主张必须有对应的证据等级（L1/L2/L3/L4），参见 [evidence-policy.md](./evidence-policy.md)。

### 约束 3：术语一致性

**禁止**在同一研究中混用不同术语指代同一概念。

必须复用 `knowledge/glossary/` 或 topic 下已定义的术语，参见 [terminology-policy.md](./terminology-policy.md)。
