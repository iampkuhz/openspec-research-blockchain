# .claude/skills — Claude Code 标准技能目录

本目录是 Claude Code 期望的技能注册位置。所有技能以符号链接指向 `skills/` 目录下的实际定义。

**维护原则**：
- `skills/` 目录是真源（source of truth）
- `.claude/skills/` 中的条目均为符号链接，不应直接编辑
- 新增技能时，先在 `skills/` 下创建，再在 `.claude/skills/` 下创建对应符号链接
- deprecated skill 不暴露在 `.claude/skills/` 下

**当前 active skill 数量**：23（6 分类）

| 分类 | 数量 |
|------|------|
| openspec-flow | 7 |
| research-authoring | 6 |
| knowledge-publishing | 5 |
| governance | 3 |
| diagrams | 1 |
| maintenance | 1 |

完整索引、合并历史与维护指南参见 [`skills/README.md`](../../skills/README.md)
