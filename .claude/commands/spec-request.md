# spec-request

辅助生成或完善 research change 的 `request.md` 文件。

**用法：**
- `/spec-request` - 在当前 change 目录下生成 request.md
- `/spec-request openspec/changes/<change-name>/` - 指定 change 目录
- `/spec-request /absolute/path/to/openspec/changes/<change-name>/` - 绝对路径

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 request 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `openspec/schemas/blockchain-research/templates/request.md` —— request 模板
- `openspec/specs/request-generation/spec.md` —— request 阶段规范（入口）
- 相关上位规范（见 `request-generation/spec.md` 中"与上位规范的关系"）

本命令不复制上位规范正文，仅负责 Claude Code 的触发、问题收集与结果写回。

若 `request-generation/spec.md` 与其引用的上位规范存在差异，以相关上位规范为准。

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 如果用户提供了路径，使用该路径
   - 否则尝试从当前工作目录推断是否位于 `openspec/changes/<change-name>/` 下
   - 如无法确定，询问用户要创建的 change 名称

2. **交互式收集信息**（如用户未提供足够上下文）

   当用户未提供足够上下文时，按 `openspec/specs/request-generation/spec.md` 补齐 request 所需关键信息：

   - 研究对象类型
   - 研究路径
   - 核心问题
   - 触发原因
   - 范围边界（覆盖对象、协议、时间窗口、非目标）
   - 已知输入

   若信息不足以进入 plan 阶段，应先补齐 request 基本语义。

3. **生成 `request.md`**
   - 基于收集的信息，按模板生成完整的 `request.md`
   - 确保结构完整、表述清晰

4. **完成总结**
   - 使用了哪个 change 路径
   - 研究对象类型和路径
   - 定义了哪些核心问题
   - 建议用户下一步执行 `/spec-plan`
