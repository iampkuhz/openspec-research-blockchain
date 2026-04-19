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

## 格式要求

### Frontmatter 强制

- `artifact.md` **必须**以 YAML frontmatter 开头（即文件第一行是 `---`）。
- Frontmatter **必须**包含 `object_type`、`title`、`research_depth`、`updated_at` 字段。
- Frontmatter 字段值**必须**符合 `check_frontmatter.py` 中定义的枚举约束。
- **禁止**使用已废弃字段：`status`、`source_change`、`topic_slug`、`primary_domain`、`decision_space`。

### 目录（TOC）强制

- `artifact.md` **必须**以目录（TOC）开头（frontmatter 之后），方便导航。
- TOC **必须**覆盖所有一级（`##`）和二级（`###`）标题。
- `verdict.md` 如超过 20 行，也**必须**以目录开头。
- TOC 使用标准 Markdown 列表格式，标题链接使用小写连字符形式。

### 增量更新约束

- 更新现有 artifact 时，新内容**必须**以旧 artifact 为基础进行扩充，**禁止**全量替换。
- 旧 artifact 中仍然有效的章节**必须**保留，可以重写表述、补充细节、调整结构，但不能以"不相关"为由直接删除。
- 如确实需要删除旧章节，**必须**在 draft 中明确说明删除理由和替代内容的位置。
