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

   按以下顺序提问，确保用户明确：

   a. **研究对象类型**（单选）：
      - `primitive` - 底层机制/协议
      - `synthesis` - 演进/综合分析
      - `domain` - 主题域
      - `decision` - 场景决策

   b. **研究路径**（单选）：
      - `deep-dive` - 深度机制分析
      - `evolution` - 演进脉络梳理
      - `scenario` - 场景化分析
      - `domain overview` - 领域概览

   c. **核心问题**（3-5 个）：
      - 基于对象类型引导用户明确要回答的关键问题

   d. **触发原因**：为什么现在要研究这个？

   e. **范围边界**：
      - 覆盖哪些对象/协议/链
      - 时间窗口
      - 明确不覆盖什么（非目标）

   f. **已知输入**：手上已有的资料、已有研究成果

3. **生成 `request.md`**
   - 基于收集的信息，按模板生成完整的 `request.md`
   - 确保结构完整、表述清晰

4. **完成总结**
   - 使用了哪个 change 路径
   - 研究对象类型和路径
   - 定义了哪些核心问题
   - 建议用户下一步执行 `/spec-plan`
