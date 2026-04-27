---
name: publish-merge-knowledge
description: 当 change 产物已通过 publish gate 校验，需要合并到 `knowledge/` 主线并记录发布元数据时使用。
---

# publish-merge-knowledge

## 何时使用

- `publish.md` 已定义合法的 `publish_targets`。
- 渲染完成（`artifact.md` / `verdict.md` 已写入）。
- 用户请求"合并这个 change"或"完成 merge"。

## 输入

- `openspec/changes/<change-id>/change.yaml`
- `openspec/changes/<change-id>/review/review-summary.md`
- 已渲染的 `knowledge/` 文件

## 输出

- 更新后的 `knowledge/analysis/**/artifact.md` 或 `knowledge/decisions/**/artifact.md` + `verdict.md`
- Git commit 记录

## 必读文件

- `harness/workflows/merge-workflow.md`
- `harness/rules/general/update-policy.md`

## 执行步骤

1. 确认 review gate 通过，评审结论允许继续 publish。
2. 校验 `publish_targets` 与已渲染文件一致。
3. 按 `change_operation` 类型处理：`create` 新增、`update` 执行 impact scan、`supersede` 标记旧版。
4. 提交 git 变更。
5. 记录发布元数据（change-id、来源路径、时间）。

## 禁止事项

- 不绕过 pre_publish gate 直接 merge。
- 不从 request.md / plan.md 直接发布。
- 不沿用 `knowledge/topics` 旧路径。
- 不把过程文件整包复制到长期目录。

## 自检

```bash
python scripts/hooks/dispatch.py --change openspec/changes/<change-id> --gate pre_publish --json
```
