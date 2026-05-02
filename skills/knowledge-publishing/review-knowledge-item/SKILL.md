---
name: publish-review-knowledge
description: 当 change 产物需要独立评审，校验 artifact contract 与质量门，生成 review.md 及按需 supporting review 文件时使用。
---

# publish-review-knowledge

## 何时使用

- `draft.md` 已完成，需要进入 review 阶段。
- 需要对 draft 的 claim traceability、术语一致性、结论边界进行独立评审。
- 用户请求"评审这个研究"或"检查 <topic> 的质量"。

## 输入

- `openspec/changes/<change-id>/draft.md`
- `openspec/changes/<change-id>/sources/` 证据材料
- `openspec/changes/<change-id>/change.yaml`

## 输出

- `openspec/changes/<change-id>/review.md`
- `openspec/changes/<change-id>/review/checklist.yaml`
- `openspec/changes/<change-id>/review/issues.md`

## 必读文件

- `harness/workflows/research-step-execution.md`
- `harness/rules/artifacts/review-rules.md`
- `openspec/specs/evidence-policy/spec.md`

## 执行步骤

1. 读取 draft.md 与来源证据，加载评审流程。
2. 逐项完成 checklist：准确性、完整性、可读性、术语一致性。
3. 记录发现的问题，按 severity（high/medium/low）分级。
4. 生成评审结论：approved / approved-with-minor-fixes / needs-revision。
5. 区分可自动修复项与需人工确认项。

## 禁止事项

- 不跳过 checklist 直接给结论。
- 不修改 `knowledge/**` 正文。
- 不在评审未完成时允许 merge。
- 不在没有依据的情况下要求修改。

## 自检

```bash
python scripts/hooks/dispatch.py --change openspec/changes/<change-id> --gate pre_publish --json
```
