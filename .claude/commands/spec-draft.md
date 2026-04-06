# spec-draft

为当前仓库中的一个 research change 生成或改写 draft.md。

**用法：**
- `/spec-draft`
- `/spec-draft openspec/changes/<change-name>/`
- `/spec-draft /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 draft 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `openspec/schemas/blockchain-research/templates/draft.md` —— draft 模板
- `openspec/specs/draft-generation/spec.md` —— draft 阶段规范（入口）
- `openspec/specs/diagram-policy/spec.md` —— 图表政策
- 相关上位规范（见 `draft-generation/spec.md` 中"与上位规范的关系"）

本命令不复制上位规范正文，仅负责 Claude Code 的触发、输入读取与结果写回。

若 `draft-generation/spec.md` 与其引用的上位规范存在差异，以相关上位规范为准。

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 路径解析规则与 `/spec-plan` 相同
   - 支持相对路径和绝对路径

2. **读取前置文件**
   - `request.md`
   - `plan.md`
   - `dependencies.md`（如有）
   - `evidence-matrix.md`（如有）

3. **增量改写**（如存在已有 `draft.md`）

4. **生成或更新 `draft.md`**
   - 严格遵守上述规范中的所有约束
   - 对 primitive 或 mechanism-heavy 内容，先补实体分类表和图表清单表
   - 再按"角色与信任边界 / 角色内部组件 / 跨角色流程 / 状态转换"四类问题决定是否需要对应图表
   - 不得把角色、组件、状态混在一张图里

5. **PlantUML diagram 合同校验（强制）**
   - 所有 PlantUML 图必须通过用户级 skills 生成：
     - 架构图：`feipi-plantuml-generate-architecture-diagram`
     - 时序图：`feipi-plantuml-generate-sequence-diagram`
   - **禁止**直接手写或手改 PlantUML 代码后未经 skill 完整执行合同就写入 draft.md
   - 每个 PlantUML block 前必须有紧邻的 contract comment：
     ```
     <!-- verified-diagram: package=./diagrams/<diagram-id>/validation.json puml=./diagrams/<diagram-id>/diagram.puml sha256=<sha256> -->
     ```
   - diagram package 必须位于标准位置：`openspec/changes/<change-id>/diagrams/<diagram-id>/`
   - 必须包含 `validation.json` 且 `final_status=success` 和 `render_result=ok`
   - 写完 `draft.md` 后，必须执行：
     ```bash
     python3 scripts/research/validate_draft_diagram_contract.py <change-dir>/draft.md
     ```
   - 只有脚本返回 0，才能声称 draft 完成

6. **完成总结**
   - 使用了哪个 change 路径
   - 更新了哪些 section
   - 建议用户重点 review 哪些部分
   - diagram contract 校验结果（如有 PlantUML blocks）

## PlantUML diagram 完整执行合同

**所有 PlantUML 图必须遵守以下合同，否则不得写入 draft.md：**

1. **必须使用全局 skill 生成**
   - 架构图：`feipi-plantuml-generate-architecture-diagram`
   - 时序图：`feipi-plantuml-generate-sequence-diagram`
   - 禁止手写或手改 PlantUML 代码

2. **必须产出 diagram package**
   - 标准位置：`openspec/changes/<change-id>/diagrams/<diagram-id>/`
   - 包含：`brief.normalized.yaml`、`diagram.puml`、`diagram.svg`、`validation.json`

3. **必须通过 validation.json 验证**
   - `final_status=success`
   - `render_result=ok`
   - `puml_sha256` 与 diagram.puml 一致

4. **必须在 draft.md 中添加 contract comment**
   - 每个 PlantUML block 前必须有紧邻的单行 HTML 注释
   - 格式固定：`<!-- verified-diagram: package=... puml=... sha256=... -->`
   - sha256 必须与 diagram.puml 和 validation.json 一致

5. **必须通过合同校验脚本**
   - 写完 draft.md 后必须执行 `validate_draft_diagram_contract.py`
   - 校验通过（返回 0）后才能声称 draft 完成

**违反以上任一约束的 draft.md 视为未完成。**
