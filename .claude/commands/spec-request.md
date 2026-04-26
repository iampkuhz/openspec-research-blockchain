# Deprecated: use /spec-research

本命令为兼容入口，不再作为主入口维护。

## 兼容行为

当前用户如果调用 `/spec-request`，请转按 `/spec-research` 执行，但只推进到初始化 `change.yaml` 与生成 `request.md` 为止。

不得生成：

- `plan.md`
- `draft.md`
- `knowledge/**`

## 迁移指引

- 新需求请直接调用 `/spec-research`
- `/spec-research` 会自动完成 change 初始化、类型路由、request.md 与 plan.md 生成
