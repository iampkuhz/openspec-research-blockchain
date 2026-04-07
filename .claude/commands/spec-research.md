# spec-research

端到端完成一个 research change 的完整流程：request → plan → draft → artifact。

**用法：**
- `/spec-research` - 在当前 change 目录下执行完整流程
- `/spec-research openspec/changes/<change-name>/` - 指定 change 目录
- `/spec-research /absolute/path/to/openspec/changes/<change-name>/` - 绝对路径

**默认模式：带检查点的全自动连续执行**（阶段 3→4 之间暂停 review）

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行端到端 research pipeline 规则，正式流程来自：

- `harness/workflows/research-pipeline.md` —— 端到端流程真源
- 各阶段 OpenSpec spec 与模板（见 research-pipeline.md 中"阶段定义"）

本命令不复制阶段正式规则正文，仅负责 Claude Code 的触发、目标目录解析与结果汇报。

若 pipeline 引用的规范存在差异，以相关上位规范为准。

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 如果用户提供了路径，使用该路径
   - 否则尝试从当前工作目录推断是否位于 `openspec/changes/<change-name>/` 下
   - 如无法确定，询问用户要使用的 change 名称
   - 检查目录是否存在，不存在则创建

2. **委托给分步命令执行**（核心机制）

   **不要自己重新定义各阶段的执行逻辑**，而是委托给已有的分步命令：

   - 执行 `/spec-request <change-dir>` → 生成 `request.md`
   - 执行 `/spec-plan <change-dir>` → 生成 `plan.md`
   - 执行 `/spec-draft <change-dir>` → 生成 `draft.md`（含图表决策树和 PlantUML 校验）
   - **暂停点**：告知用户 draft 已完成，需要 review 图表质量，询问是否继续进入 artifact 阶段
   - 用户确认后，执行 `/spec-artifact <change-dir>` → 生成 `artifact.md`

   **优势**：
   - 复用分步命令已验证的规范和质量控制
   - 避免重新定义流程导致的规范稀释
   - 图表决策树和 PlantUML 校验由 `/spec-draft` 强制执行

3. **完成总结**
   - 执行模式（全自动/分阶段 review）
   - 各阶段状态（执行/跳过）
   - 使用的 change 路径
   - 研究对象类型和路径
   - 提炼的长期资产路径
   - 图表闸门执行情况（如有 PlantUML 图）
   - 建议用户下一步操作（如 review artifact）

## 相关命令

- `/spec-request` - 单独执行 request 阶段
- `/spec-plan` - 单独执行 plan 阶段
- `/spec-draft` - 单独执行 draft 阶段（含图表决策树和 PlantUML 校验）
- `/spec-artifact` - 单独执行 artifact 阶段
