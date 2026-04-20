# 仓库治理规则（引用页）

**本文件是薄引用页，不再重复定义正式约束。**

## 核心约束

| 约束 | 主定义位置 | 说明 |
|------|-----------|------|
| 变更必须走 OpenSpec | `openspec/specs/repository-asset-model/spec.md` | 禁止直接修改 `knowledge/` 主线；必须通过 `openspec/changes/` → review → apply 流程 |
| 证据可追溯 | `openspec/specs/evidence-policy/spec.md` | 所有技术主张必须有 L1/L2/L3/L4 证据等级 |
| 术语一致性 | `harness/rules/general/terminology-policy.md` | 禁止在同一研究中混用不同术语指代同一概念 |

## 例外

仅当修复明显的拼写错误、格式问题时，可直接修改（参见 `./update-policy.md`）。
