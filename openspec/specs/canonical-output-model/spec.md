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

## 写作质量硬约束

以下约束适用于所有 `artifact.md`：

### 总-分结构

每个分析章节必须采用总-分结构：先用一段话概括该阶段/模块的核心特征与技术思考，再展开具体条目。禁止直接进入条目罗列。

### 列表维度一致性

同一层级的列表条目必须处于同一维度。禁止混用：
- "新增某文件"（物理变更）与"某种设计模式"（抽象概念）
- "版本号"（元数据）与"架构变化"（实质变更）

### 禁止无意义精确数字

禁止罗列对项目理解无意义的精确数字，如文件数、代码行数、commit 数。仅在数字本身代表关键架构决策时才使用精确数字。

### 演进类 artifact 必须包含图表

演进类 artifact 必须包含至少一张演进路线图（ASCII 或 PlantUML timeline），不得仅用文字罗列版本。

## 格式要求

### Frontmatter 强制

- `artifact.md` **必须**以 YAML frontmatter 开头（即文件第一行是 `---`）。
- Frontmatter **必须**包含 `object_type`、`title`、`research_depth`、`updated_at` 字段。
- Frontmatter 字段值**必须**符合 `check_frontmatter.py` 中定义的枚举约束。

### 目录（TOC）强制

- `artifact.md` **必须**以目录（TOC）开头（frontmatter 之后），方便导航。
- TOC **必须**覆盖所有一级（`##`）和二级（`###`）标题。
- `verdict.md` 如超过 20 行，也**必须**以目录开头。
- TOC 使用标准 Markdown 列表格式，标题链接使用小写连字符形式。

### 增量更新约束

- 更新现有 artifact 时，新内容**必须**以旧 artifact 为基础进行扩充，**禁止**全量替换。
- 旧 artifact 中仍然有效的章节**必须**保留，可以重写表述、补充细节、调整结构，但不能以"不相关"为由直接删除。
- 如确实需要删除旧章节，**必须**在 draft 中明确说明删除理由和替代内容的位置。
