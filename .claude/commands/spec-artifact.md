# spec-artifact

把一个 research change 的稳定 draft.md 提炼为长期 artifact。

**用法：**
- `/spec-artifact`
- `/spec-artifact openspec/changes/<change-name>/`
- `/spec-artifact /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 artifact 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `openspec/specs/artifact-generation/spec.md` —— artifact 阶段规范（入口）
- `openspec/specs/canonical-output-model/spec.md` —— 长期资产结构
- 相关上位规范（见 `artifact-generation/spec.md` 中"与上位规范的关系"）

本命令不复制上位规范正文，仅负责 Claude Code 的触发、输入读取与结果写回。

若 `artifact-generation/spec.md` 与其引用的上位规范存在差异，以相关上位规范为准。

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 路径解析规则与 `/spec-plan` 相同
   - 支持相对路径和绝对路径

2. **读取前置文件**
   - `request.md`
   - `plan.md`
   - `draft.md`
   - 可选：`dependencies.md`、`decision-criteria.md`

3. **判断对象类型与目标路径**
   - `primitive` / `synthesis` / `domain` → `knowledge/analysis/.../artifact.md`
   - `decision` → `knowledge/decisions/.../artifact.md` + `verdict.md`（可选）

4. **提炼并写入长期资产**
   - 只保留 durable 内容，移除过程性痕迹
   - 严格遵守上述规范中的所有约束

5. **完成总结**
   - 使用了哪个 change 路径
   - 写入了哪些长期文件
   - 建议用户重点 review 哪些部分
