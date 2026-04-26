# Deprecated: use /spec-governance-review

本命令为兼容入口，不再作为主入口维护。

## 兼容行为

当前用户如果调用 `/spec-system-audit`，请转按 `/spec-governance-review` 执行，并聚焦系统一致性审计。

## 迁移指引

- 新需求请直接调用 `/spec-governance-review`
- `/spec-governance-review` 覆盖规约治理与系统审计的全部能力
