---
name: maintenance-refresh-topic
description: 当既有知识主题因规范更新、事实错误或生态变化需要刷新时，创建 change 执行增量更新并生成 content-comparison.md 时使用。
---

# maintenance-refresh-topic

## 何时使用

- 用户请求"更新 <topic>"、"刷新这个主题"。
- 发现规范变更导致现有 artifact 需要调整。
- 发现事实错误或生态变化导致内容过期。

## 输入

- 目标长期资产路径（`knowledge/analysis/**/artifact.md` 或 `knowledge/decisions/**/artifact.md`）。
- 更新原因（`spec-update` / `error-fix` / `ecosystem-change`）。

## 输出

- 新 change：`openspec/changes/update-<topic>-<reason>-pass-1/`
- `content-comparison.md` 或 `plan.md` 中的影响评估

## 必读文件

- `harness/workflows/research-intake-routing.md`
- `harness/rules/general/update-policy.md`
- `harness/workflows/research-publish-flow.md`（发布阶段）

## 执行步骤

1. 读取现有长期资产，确认更新原因。
2. 评估 update 类型与影响范围（minor / major / refactor）。
3. 创建 change，标记 `change_operation: update`。
4. 生成 request.md 说明更新原因与影响范围。
5. 完成 request / plan / draft 流程。
6. 如为 update 类型，记录 impact scan 结果。
7. 通过评审后 publish。

## 禁止事项

- 不直接修改 `knowledge/`，必须通过 change。
- 不跳过影响范围评估。
- 不假定所有 update 都只是局部修补。
- 如有上层依赖，必须记录 follow-up 计划。

## 自检

```bash
python scripts/hooks/dispatch.py --change openspec/changes/<change-id> --gate post_draft --json
```
