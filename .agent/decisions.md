# Decision Log — V2 Spec System Overhaul

**Branch:** `2605-archv2`
**Started:** 2026-05-14

| Date | Task | Decision | Rationale |
|---|---|---|---|
| 2026-05-14 | 08 | `unarchived_changes.py` kept as standalone, not registered | Advisory-only (always exits 0), no gate references, useful for periodic archive hygiene. Not gate-driven. |
| 2026-05-14 | V2-fix | `reference_integrity` uses repo-root path resolution | Paths like `docs/governance/...` are repo-root relative, not file-relative. Fixed `resolve_ref()` to detect known top-level prefixes. |
| 2026-05-14 | V2-fix | `schema_package` uses `x_required_artifacts` / `x_optional_artifacts` | Profile files use prefixed keys, not bare `required`/`optional`. Fixed validator to match actual schema. |
| 2026-05-14 | V2-fix | `move_change_outputs.py` missing `ROOT` definition | Added `ROOT = Path(__file__).resolve().parent.parent.parent` to prevent NameError on `--archive`. |
| 2026-05-14 | V2-fix | New validators wired to `governance_check` gate | Added `governance_check` gate to `harness/gates/registry.yaml` with `reference_integrity`, `phase_index`, `schema_package`. Added 4 tests. |
| 2026-05-14 | 27 | `.gitignore` 保留通用 `lib/` 规则，通过 `!scripts/hooks/lib/` + `!scripts/hooks/lib/*.py` 精确反忽略 | 不删除通用规则（仍屏蔽 Python build artifact 中的 `lib/` 目录），但明确允许 hooks 核心 helper 入库。移除重复的 `/openspec/changes/` 规则，避免覆盖前面的 negate。 |
| 2026-05-14 | 27 | 将 `scripts/hooks/lib/` 下全部 7 个 `.py` 文件纳入版本控制 | 上一轮 gate 的运行依赖 `gate_result.py` 等被误伤未入库，clean checkout 无法复现治理 gate。 |
