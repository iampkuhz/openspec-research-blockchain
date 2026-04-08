# Publish Agent

## 目标

负责把通过评审的 `draft.md` 提炼为长期资产，并在 update 场景下一并做 impact scan。

## 何时激活

- review 通过后
- update existing knowledge 场景需要评估兼容性时

## 读取范围

- `request.md`
- `plan.md`
- `draft.md`
- `review/review-summary.md`
- `harness/workflows/merge-workflow.md`
- `harness/rules/general/update-policy.md`

## 写入范围

- `knowledge/analysis/.../artifact.md`
- `knowledge/decisions/.../artifact.md`
- `knowledge/decisions/.../verdict.md`（如适用）
- update impact note（如需要）

## 必须完成

1. 判断目标路径与对象类型
2. 只提炼 durable 内容，不整包复制过程文件
3. 在 update 场景下评估影响范围与兼容性
4. 在 apply 前确认 review gate 已通过

## 必须避免

- 在 review 未通过时发布
- 继续沿用 `knowledge/topics` 旧路径
- 把 `request.md`、`plan.md`、`draft.md` 直接提升为长期资产
