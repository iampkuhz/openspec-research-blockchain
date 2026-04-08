# spec-research

端到端完成一个 research change 的完整流程：request → plan → draft → review → artifact。

**用法：**
- `/spec-research`
- `/spec-research openspec/changes/<change-name>/`
- `/spec-research /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令是 **命令层入口**。执行前必须优先读取：

- `harness/workflows/research-pipeline.md`
- `harness/agents/_index.yaml`
- @agent contract
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
   - 从 `harness/agents/_index.yaml` 加载：
     - @research-author-agent
     - @source-evidence-agent
     - @review-critic-agent
     - @publish-agent
   - 条件启用：
     - @diagram-agent
     - @governance-review-agent

4. **编排执行**
   - `request`：按 @research-author-agent contract 生成或修订 `request.md`
   - `plan`：由 @research-author-agent 负责，必要时并行拉起 @source-evidence-agent
   - `draft`：由 @research-author-agent 负责，primitive / mechanism-heavy 时启用 @diagram-agent
   - `review`：由 @review-critic-agent 独立完成，不与 author 合并
   - `artifact`：仅在 review 通过后，交给 @publish-agent

5. **更细的并行策略**
   - **窗口 A：request bootstrap**
     - @research-author-agent 先生成最小可用的 `request.md` 语义骨架
     - 同时可并行读取 schema、template、已有 change 文件
   - **窗口 B：plan-source parallel**
     - @research-author-agent 并行推进问题拆解、交付范围、完成标准
     - @source-evidence-agent 并行生成 `sources/` 和 `source-review.md`
     - `plan.md` 定稿前必须回收 `source-review.md`
   - **窗口 C：draft-diagram parallel**
     - @research-author-agent 写概述、术语表、设计取舍、能力边界
     - @diagram-agent 并行准备实体分类、图表清单、diagram package
     - `draft.md` 只有在 diagram contract 通过后才可声称完成
   - **窗口 D：review preheat**
     - @review-critic-agent 可基于 `plan.md`、`sources/` 预热 checklist
     - 但不能在 `draft.md` 冻结前给出正式 severity 和结论
   - **窗口 E：publish preflight**
     - @publish-agent 可提前计算目标路径、impact scope、目录落点
     - 但 review 通过前不得写长期资产

6. **冰箱策略**
   - 当某个子任务被阻塞时，不让整个命令停摆，而是把它放入冰箱清单
   - 冰箱项至少记录：
     - blocked item
     - blocked by
     - wake condition
     - downstream impact
   - 典型场景：
     - L1 来源被网络限制拦住
     - diagram package 未通过 contract 校验
     - review 存在 high severity，publish 必须冻结
   - 冰箱项应回写到最近的正式位置：
     - `plan.md` 的“证据缺口”/“待确认问题”
     - `draft.md` 的“待确认问题”/不确定性说明
     - `review/issues.md`

7. **fallback**
   - 如果运行环境不支持真实 subagent，就按相同 contract 串行执行
   - 但必须在总结中说明哪些角色被折叠执行

8. **完成总结**
   - active agents 列表
   - 哪些角色并行、哪些串行
   - 各阶段状态
   - 使用的 change 路径
   - 是否生成 `sources/`、`review/`、`diagrams/`
   - 是否完成 artifact / apply
   - 冰箱清单及其解冻条件
