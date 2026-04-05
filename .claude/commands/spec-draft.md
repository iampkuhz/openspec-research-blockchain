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

5. **完成总结**
   - 使用了哪个 change 路径
   - 更新了哪些 section
   - 建议用户重点 review 哪些部分
