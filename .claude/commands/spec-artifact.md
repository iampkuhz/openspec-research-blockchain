# Deprecated: use /spec-research-publish

本命令为兼容入口，不再作为主入口维护。

## 兼容行为

当前用户如果调用 `/spec-artifact`，请转按 `/spec-research-publish` 执行。

当前语义不是"再生成一个中间 artifact"，而是：

- 检查 `publish.md`
- 根据 `publish_targets`
- 将 `draft.md` 发布为 `knowledge/**/artifact.md`
- decision 类型可发布 `knowledge/decisions/**/verdict.md`

不得跳过 `publish.md` 直接写 `knowledge/**`。

## 迁移指引

- 新需求请直接调用 `/spec-research-publish`
- `/spec-research-publish` 是唯一允许从 change 进入 `knowledge/**` 的 command
