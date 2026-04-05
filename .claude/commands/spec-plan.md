# spec-plan

为当前仓库中的一个 research change 生成或改写 plan.md。

**用法：**
- `/spec-plan`
- `/spec-plan openspec/changes/<change-name>/`
- `/spec-plan /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 plan 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `openspec/schemas/blockchain-research/templates/plan.md` —— plan 模板
- `openspec/specs/plan-generation/spec.md` —— plan 阶段规范（入口）
- 相关上位规范（见 `plan-generation/spec.md` 中"与上位规范的关系"）

本命令不复制上位规范正文，仅负责 Claude Code 的触发、输入读取与结果写回。

若 `plan-generation/spec.md` 与其引用的上位规范存在差异，以相关上位规范为准。

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 如果用户在命令后提供了路径，就使用该路径
   - 如果用户没有提供路径：
     - 先尝试从当前工作目录推断是否位于某个 `openspec/changes/<change-name>/` 下
     - 否则优先使用仓库中最近正在编辑、且同时包含 `request.md` 的 change 目录
     - 如果仍无法唯一判断，再简短询问用户

2. **读取前置文件**
   - `request.md`

3. **增量改写**（如存在已有 `plan.md`）
   - 基于它增量改写，而不是整份重写

4. **生成或更新 `plan.md`**
   - 严格遵守上述规范中的所有约束

5. **完成总结**
   - 使用了哪个 change 路径
   - 更新了哪些 section
   - 建议用户重点 review 哪些部分
