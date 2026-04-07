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
   - 现有 `draft.md`（如有，用于增量改写）
   - 现有 `diagrams/` 目录（如有）

3. **图表决策树（强制，primitive/mechanism-heavy 类型必须先执行）**

   **步骤 3.1：实体分类**
   - 基于 request.md/plan.md 中的关键实体，完成实体分类表
   - 将每个实体归类为 `role / component / data object / state / external system`
   - 标明控制方和是否跨信任边界

   **步骤 3.2：回答四个判定问题**
   - Q1：是否存在两个及以上独立控制方？
   - Q2：是否有核心角色内部结构 materially 不同？
   - Q3：是否依赖跨角色消息/调用/证明流转？
   - Q4：是否依赖命名状态/轮次/epoch/timeout 转换？
   - 记录每个问题的是/否答案

   **步骤 3.3：生成图表清单表**
   - 基于步骤 3.2 的答案，声明必须/可省略的图表
   - 每张图注明：要回答的问题、采用格式、为什么需要/可省略

   **步骤 3.4：检查覆盖缺口**
   - 对比图表清单表与现有 `diagrams/` 目录
   - 如清单中某图标记为"必须"但不存在 → **阻塞**，告知用户需要补充哪些图（或询问是否现在生成）
   - 如清单中某图标记为"可省略"但已存在 → 建议删除或说明额外价值
   - 只有所有"必须"图表都存在或通过 skill 生成后，才能继续

4. **生成或更新 `draft.md`**
   - 首先写入实体分类表和图表清单表（位于"分析正文"章节开头）
   - 按图表清单表逐章编写
   - 严格遵守规范中的所有约束
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
   - 图表决策树执行情况（四个判定问题的答案）
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
