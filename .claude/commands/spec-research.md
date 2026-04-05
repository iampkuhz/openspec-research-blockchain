# spec-research

端到端完成一个 research change 的完整流程：request → plan → draft → artifact。

**用法：**
- `/spec-research` - 在当前 change 目录下执行完整流程
- `/spec-research openspec/changes/<change-name>/` - 指定 change 目录
- `/spec-research /absolute/path/to/openspec/changes/<change-name>/` - 绝对路径

**默认模式：全自动连续执行**（4 个阶段不等待用户逐阶段确认）

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

2. **调用端到端 pipeline**
   - 按 `harness/workflows/research-pipeline.md` 定义的顺序执行 4 个阶段
   - 默认全自动连续执行，不等待用户逐阶段确认
   - 如某阶段文件已存在且内容完整，自动跳过该阶段

3. **完成总结**
   - 执行模式（全自动/分阶段 review）
   - 各阶段状态（执行/跳过）
   - 使用的 change 路径
   - 研究对象类型和路径
   - 提炼的长期资产路径
   - 建议用户下一步操作
