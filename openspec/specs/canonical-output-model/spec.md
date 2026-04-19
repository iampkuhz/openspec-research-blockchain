# 长期产出模型

## 目的

定义一次研究完成后，哪些内容应保留在长期 `knowledge/analysis/` 与 `knowledge/decisions/` 目录中。

## 要求

- 长期 `knowledge/analysis/primitives/<domain_id>/<topic_slug>/` 默认只保留 `artifact.md`。
- 长期 `knowledge/analysis/synthesis/<topic_slug>/` 默认只保留 `artifact.md`。
- 长期 `knowledge/decisions/<domain_id>/<topic_slug>/` 默认只保留 `artifact.md`、`verdict.md`。
- `decision-criteria.md` 是 `openspec/changes/<change-id>/` 下的过程文件，不进入长期目录。
- `request.md`、`plan.md`、`evidence-matrix.md`、`dependencies.md` 不得进入长期目录。依赖声明已合并入 `plan.md`，过程文件保留在 `openspec/changes/`。
- case 级 `README.md` 默认不作为长期知识文件保留；目录说明应放在上层 `README.md` 或 `openspec/specs/`。
- 对 `primitive / synthesis`，结论应折叠进 `artifact.md`，默认不单独长期保留 `verdict.md`。
- `domain` 是目录分组概念，不是独立 `object_type`，不生成独立长期 `artifact.md`。
- glossary 层默认折叠进 `artifact.md` 的“关键术语”区，不单独长期保留 `glossary.md`。
- 过程性纠偏记录必须留在 `openspec/changes/`，不得进入长期目录。
- 从 change packet 提升到长期资产时，必须做提炼，而不是整包照搬。
