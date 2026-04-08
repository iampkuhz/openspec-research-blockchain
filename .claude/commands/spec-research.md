# spec-research

端到端完成一个 research change 的完整流程：request → plan → draft → review → artifact。

**用法：**
- `/spec-research`
- `/spec-research openspec/changes/<change-name>/`
- `/spec-research /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令是 **orchestrator 入口**。执行前必须优先读取：

- `harness/workflows/research-pipeline.md`
- `harness/agents/_index.yaml`
- active agents 对应 contract
- 各阶段 OpenSpec spec 与 template

本命令不重新定义 artifact contract，也不复制整份 workflow 正文。

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 如果用户提供了路径，使用该路径
   - 否则尝试从当前工作目录推断
   - 如果仍无法确定，再简短询问用户

2. **判断任务语义**
   - 如果是普通 research / update，继续本命令
   - 如果是 OpenSpec / Harness / AGENTS / governance 改造，切到 `governance-review-workflow.md`

3. **选择 active agents**
   - 默认：
     - `orchestrator`
     - `research-author-agent`
     - `source-evidence-agent`
     - `review-critic-agent`
     - `publish-agent`
   - 条件启用：
     - `diagram-agent`
     - `governance-review-agent`

4. **编排执行**
   - `request`：按 `research-author-agent` contract 生成或修订 `request.md`
   - `plan`：由 `research-author-agent` 负责，必要时并行拉起 `source-evidence-agent`
   - `draft`：由 `research-author-agent` 负责，primitive / mechanism-heavy 时启用 `diagram-agent`
   - `review`：由 `review-critic-agent` 独立完成，不与 author 合并
   - `artifact`：仅在 review 通过后，交给 `publish-agent`

5. **fallback**
   - 如果运行环境不支持真实 subagent，就按相同 contract 串行执行
   - 但必须在总结中说明哪些角色被折叠执行

6. **完成总结**
   - active agents 列表
   - 哪些角色并行、哪些串行
   - 各阶段状态
   - 使用的 change 路径
   - 是否生成 `sources/`、`review/`、`diagrams/`
   - 是否完成 artifact / apply
