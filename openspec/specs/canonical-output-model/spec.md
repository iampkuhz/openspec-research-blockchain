# 长期产出模型

## 目的

定义一次研究完成后，哪些内容应保留在长期 `knowledge/analysis/` 与 `knowledge/decisions/` 目录中。

## 要求

- 长期 `knowledge/analysis/primitives/<slug>/` 默认只保留 `reference.md` 与 `glossary.md`。
- 长期 `knowledge/analysis/synthesis/<slug>/` 默认只保留 `reference.md`、`glossary.md`、`dependencies.md`。
- 长期 `knowledge/analysis/domains/<slug>/` 默认只保留 `reference.md`、`glossary.md`、`dependencies.md`。
- 长期 `knowledge/decisions/<domain>/<slug>/` 默认只保留 `reference.md`、`criteria.md`、`dependencies.md`、`glossary.md`、`verdict.md`。
- `request.md`、`brief.md`、`sources.md`、`evidence-matrix.md` 不得进入长期目录。
- case 级 `README.md` 默认不作为长期知识文件保留；目录说明应放在上层 `README.md`、`openspec/specs/` 或 `support/docs/`。
- 对 `primitive / synthesis / domain`，结论应折叠进 `reference.md`，默认不单独长期保留 `verdict.md`。
- 过程性纠偏记录必须留在 `openspec/changes/`，不得进入长期目录。
- 从 change packet 提升到长期资产时，必须做提炼，而不是整包照搬。
