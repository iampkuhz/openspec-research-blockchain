# spec-draft

为当前仓库中的一个 research change 生成或改写 draft.md。

**用法：**
- `/spec-draft`
- `/spec-draft openspec/changes/<change-name>/`
- `/spec-draft /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 真理之源

**本命令的核心约束和规则统一由以下规范定义**：

- `openspec/specs/draft-generation/spec.md` —— Draft 生成规范（真理之源）

本 adapter 仅定义 Claude Code 平台特定的触发逻辑和执行步骤。

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
   - 严格遵守 `openspec/specs/draft-generation/spec.md` 中的所有约束

5. **完成总结**
   - 使用了哪个 change 路径
   - 更新了哪些 section
   - 建议用户重点 review 哪些部分

## 必须参考

- `openspec/specs/draft-generation/spec.md`（核心约束）
- `openspec/schemas/blockchain-research/templates/draft.md`（模板）
- `openspec/specs/diagram-policy/spec.md`（图表政策）
