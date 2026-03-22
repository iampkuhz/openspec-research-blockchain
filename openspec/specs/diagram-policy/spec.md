# 图表政策

## 目的

定义本仓库所有研究输出中图表（尤其是 PlantUML）的生成、验证与交付标准，确保所有图表可渲染、可维护。

## 要求

### 1. PlantUML 必须通过 skill 生成

- 所有 PlantUML 代码必须通过 `/feipi-gen-plantuml-code` skill 生成
- 禁止直接手写 PlantUML 代码后未经校验就提交
- skill 会自动执行语法校验（`syntax_result=ok`）和布局检查

### 2. 校验标准

- 必须通过 `scripts/check_plantuml.sh` 校验：`syntax_result=ok`
- 必须通过布局检查：`layout_check=ok`
- 必须生成可读的 `.svg` 输出，无文字重叠/遮挡

### 3. 交付物要求

- `draft.md` 中的 PlantUML 必须嵌入代码块（```plantuml）
- 代码块内容必须是 skill 生成的、通过校验的代码
- 不得使用 `participant ... optional` 等非标准语法

### 4. 流程集成

- `build-draft` skill 必须在生成包含 PlantUML 的 draft 时，调用 `feipi-gen-plantuml-code` skill
- `build-draft` skill 的 SKILL.md 必须显式声明此依赖关系

### 5. 问题追溯

- 若发现 PlantUML 编译失败，视为 `build-draft` skill 执行缺陷
- 修复方案：更新 `build-draft/SKILL.md` 的约束条款，而非仅修复单个 draft

## 相关文件

- `skills/openspec-research-build-draft/SKILL.md`：必须引用本政策
- `support/templates/draft.md`：必须提示使用 PlantUML skill
- `.qoder/skills/feipi-gen-plantuml-code/`：图表生成与校验工具
