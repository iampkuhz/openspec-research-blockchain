---
name: openspec-build-research-support
description: 当需要端到端执行一个 change 的完整 pipeline（request → plan → draft → review → artifact）时使用，按阶段自动跳过已完成的文件。
---

# openspec-build-research-support

## 何时使用

- 需要端到端完成一个 research change，从 request 开始逐阶段执行。
- 已有部分阶段文件，需要增量补全至 artifact。
- 用户请求一次性推进整个研究流程。

## 输入

- `openspec/changes/<change-id>/` 路径（如不存在则自动创建）。
- 用户提供的研究背景、触发原因（如 request 尚未存在）。

## 输出

- `openspec/changes/<change-id>/` 下按阶段补齐的 `request.md` → `plan.md` → `draft.md` → `review.md` → `knowledge/**`

## 必读文件

- `harness/workflows/research-pipeline.md` —— 端到端流程真源

## 执行步骤

1. 读取 change.yaml 确定 `task_type` 与 `change_operation`。
2. 检查各阶段文件是否存在且内容完整，按顺序跳过已完成的阶段。
3. 从第一个不完整的阶段开始执行：request → plan → sources → draft → review → artifact。
4. 每个阶段完成后验证 gate，失败则停止并报告。
5. 不跳过阶段直接执行后续步骤。

## 禁止事项

- 不直接写 `knowledge/**` 除非已通过完整 pipeline。
- 不生成 `work-products/*.md`。
- 不在阶段 gate 失败时继续执行后续阶段。
- 不绕过 change.yaml。

## 自检

```bash
python scripts/hooks/dispatch.py --change openspec/changes/<change-id> --gate post_draft --json
```
