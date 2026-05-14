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
| 2026-05-14 | 6.2 | `reference_integrity` is blocking for governance_check | Dead refs in spec-system files waste context and cause routing errors. Changed `blocking` from false to true. Aggregate now respects per-validator `blocking` — non-blocking validator failures downgrade to warn instead of failing the gate. |
| 2026-05-14 | 6.1 | Dispatcher `run_validator` parses pretty JSON | Changed from line-by-line parsing to: (1) full stdout json.loads, (2) brace-matching JSON extraction, (3) line-by-line fallback. Prevents legal pretty JSON from being dumped into warnings. |
