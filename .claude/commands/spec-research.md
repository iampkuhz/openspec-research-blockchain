# spec-research

端到端完成一个 research change 的完整流程：request → plan → draft → review → artifact。

**用法：**
- `/spec-research 研究 simplex 共识算法` - 创建新 change 并执行完整流程
- `/spec-research openspec/changes/<change-name>/` - 对现有 change 执行流程
- `/spec-research /absolute/path/to/openspec/changes/<change-name>/` - 绝对路径方式

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令是 **命令层入口**。执行前必须优先读取：

- `harness/workflows/research-pipeline.md`
- 各阶段 OpenSpec spec 与 template
- @agent contract（如 `@research-author-agent`、`@source-evidence-agent` 等）

本命令不重新定义 artifact contract，也不复制整份 workflow 正文。

## 变更初始化

如用户传入研究主题（如"研究 simplex 共识算法"）而非现有 change 路径：

1. **创建 change 目录**
   - 命名格式：`primitive-<topic>-deep-dive-pass-1`
   - 使用脚本：`./scripts/openspec/new_change.sh primitive <change-name>`
   - 或手动创建：`mkdir -p openspec/changes/<change-name>`

2. **初始化 request.md**
   - 对象类型：根据主题推断（默认 primitive）
   - 研究路径：deep-dive
   - 核心问题：基于主题生成 3-5 个问题
   - 范围与非目标：明确边界

3. **进入流程执行**

## 流程执行

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
     - **网络受限 fallback**：如 WebSearch/WebFetch 受限，在 plan.md 中记录证据缺口并继续
   - **窗口 C：draft-diagram parallel**
     - @research-author-agent 写概述、术语表、设计取舍、能力边界
     - @diagram-agent 并行准备实体分类、图表清单、diagram package
     - `draft.md` 只有在 diagram contract 通过后才可声称完成
     - **diagram agent 不可用 fallback**：图表标注为"待生成"，draft 仍可交付为工作草稿
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
     - L1 来源被网络限制拦住 → 记录到 plan.md 证据缺口，继续推进
     - diagram package 未通过 contract 校验 → 记录到 draft.md 待确认问题，继续推进
     - review 存在 high severity，publish 必须冻结 → 记录到 review/issues.md
   - 冰箱项应回写到最近的正式位置：
     - `plan.md` 的”证据缺口”/”待确认问题”
     - `draft.md` 的”待确认问题”/不确定性说明
     - `review/issues.md`

7. **fallback**
   - 如果运行环境不支持真实 subagent，就按相同 contract 串行执行
   - 但必须在总结中说明哪些角色被折叠执行
   - **网络受限 fallback**：WebSearch/WebFetch 受限时，使用已知知识并标注证据等级为 L3/L4
   - **diagram agent fallback**：无法生成 PlantUML 时，用 Markdown 表格和 ASCII 草图代替

8. **完成总结**
   - active agents 列表
   - 哪些角色并行、哪些串行
   - 各阶段状态（request/plan/draft/review/artifact）
   - 使用的 change 路径
   - 是否生成 `sources/`、`review/`、`diagrams/`
   - 是否完成 artifact / apply
   - 冰箱清单及其解冻条件
   - 证据缺口说明（L1/L2 缺失情况）
