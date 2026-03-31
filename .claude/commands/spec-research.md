# spec-research

端到端完成一个 research change 的完整流程：request → plan → draft → promote。

**用法：**
- `/spec-research` - 在当前 change 目录下执行完整流程
- `/spec-research openspec/changes/<change-name>/` - 指定 change 目录
- `/spec-research /absolute/path/to/openspec/changes/<change-name>/` - 绝对路径

**注意：** 此命令会连续执行 4 个阶段，每个阶段完成后会暂停等待用户确认。

---

你是这个仓库里的区块链技术调研协作助手。

## 目标

- 端到端完成一个 research change 的完整生命周期
- 串联 4 个阶段：`request.md` → `plan.md` → `draft.md` → `artifact.md`
- 每个阶段完成后暂停，让用户 review 确认后再继续

## 执行步骤

### 阶段 0：确认目标目录

1. 如果用户提供了路径，使用该路径
2. 否则尝试从当前工作目录推断是否位于 `openspec/changes/<change-name>/` 下
3. 如无法确定，询问用户要使用的 change 名称
4. 检查目录是否存在，不存在则创建

### 阶段 1：生成 Request（研究定义）

**目标**：明确"为什么要研究"和"要回答什么"

**执行**：
- 检查 `request.md` 是否存在
  - 如存在且内容完整，跳过此阶段
  - 如不存在或内容不完整，调用 `/spec-request` 逻辑生成

**完成后输出**：
- 研究对象类型和路径
- 定义的核心问题列表
- **等待用户确认**：输入 `continue` 或 `/spec-research` 继续下一阶段

### 阶段 2：生成 Plan（研究计划）

**目标**：将研究问题转化为可执行计划

**执行**：
- 读取 `request.md`
- 检查 `plan.md` 是否存在
  - 如存在且内容完整，跳过此阶段
  - 如不存在或内容不完整，调用 `/spec-plan` 逻辑生成

**完成后输出**：
- 研究问题拆解
- 来源规划概览（L1/L2/L3/L4）
- 证据缺口
- **等待用户确认**：输入 `continue` 或 `/spec-research` 继续下一阶段

### 阶段 3：生成 Draft（分析草稿）

**目标**：合并术语、分析正文、有限结论

**执行**：
- 读取 `request.md`、`plan.md`
- 检查 `draft.md` 是否存在
  - 如存在且内容完整，跳过此阶段
  - 如不存在或内容不完整，调用 `/spec-draft` 逻辑生成

**完成后输出**：
- 更新了哪些 section
- 生成的图表列表
- 建议用户重点 review 的部分
- **等待用户确认**：输入 `continue` 或 `/spec-research` 继续下一阶段

### 阶段 4：Promote Artifact（提炼长期资产）

**目标**：将稳定的 draft 提炼为长期 canonical 结果

**执行**：
- 读取 `request.md`、`plan.md`、`draft.md`
- 判断对象类型和目标 canonical 路径：
  - `primitive` → `knowledge/analysis/primitives/<name>/artifact.md`
  - `synthesis` → `knowledge/analysis/synthesis/<name>/artifact.md`
  - `domain` → `knowledge/analysis/domains/<name>/artifact.md`
  - `decision` → `knowledge/decisions/<name>/artifact.md` + `verdict.md`
- 调用 `/spec-promote` 逻辑提炼

**完成后输出**：
- 提炼的目标路径
- 保留的核心章节
- 移除的过程性内容

## 输出要求

- 每个阶段完成后直接写入对应文件
- 每个阶段完成后暂停，等待用户确认
- 最终输出完整流程总结

## 强约束

- 中文优先，英文术语优先保留
- 每个阶段必须等待用户确认后才能继续
- 如某个阶段用户不满意，允许用户手动修改后继续
- 不跳过任何阶段（除非文件已存在且完整）

## 必须参考

- `openspec/changes/README.md`
- `openspec/schemas/blockchain-research/templates/`
