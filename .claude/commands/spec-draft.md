# Deprecated: use /spec-research-step

本命令为兼容入口，不再作为主入口维护。

## 兼容行为

当前用户如果调用 `/spec-draft`，请转按 `/spec-research-step` 执行，并只生成或修正当前 change 的唯一主候选产物 `draft.md`。

不得生成：

- `work-products/*.md`
- `knowledge/**`

## 迁移指引

- 新需求请直接调用 `/spec-research-step`
- `/spec-research-step` 会自动检测当前 change 缺少的产物并推进下一步
