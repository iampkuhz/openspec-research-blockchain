# spec-plan

为当前仓库中的一个 research change 生成或改写 plan.md。

**用法：**
- `/spec-plan`
- `/spec-plan openspec/changes/<change-name>/`
- `/spec-plan /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 目标

- 为一个 change packet 生成或改写 `plan.md`
- `plan.md` 合并"研究计划 + 来源规划"
- 它不是分析正文，而是第一轮集中 review 文件

## 执行步骤

1. 先确认目标 change 目录。
2. 如果用户在命令后提供了路径，就使用该路径。
3. 如果用户没有提供路径：
   - 先尝试从当前工作目录推断是否位于某个 `openspec/changes/<change-name>/` 下
   - 否则优先使用仓库中最近正在编辑、且同时包含 `request.md` 的 change 目录
   - 如果仍无法唯一判断，再简短询问用户
4. 读取该 change 下的 `request.md`
5. 如存在已有 `plan.md`，基于它增量改写，而不是整份重写
6. 按本仓库规则生成或更新 `plan.md`

## 输出要求

- 直接写入目标 change 下的 `plan.md`
- 不要只给建议，不要只输出草案到聊天里
- 完成后总结：
  - 使用了哪个 change 路径
  - 更新了哪些 section
  - 建议用户重点 review 哪些部分

## 强约束

- 中文优先，英文术语优先保留
- `plan.md` 必须包含：
  - 研究对象（类型、路径、相关 domains）
  - 问题拆解
  - 待确认问题
  - 交付范围
  - 研究深度（deep/focused/light）
  - 来源规划（L1/L2/L3/L4）
  - 证据缺口
  - 完成标准
  - 排除范围
- 对 `primitive`，把以下类型的问题写入"待确认问题"：
  - 为什么不直接改传统 transaction 路径
  - 关键角色分别位于哪一层
  - 哪些能力不是 protocol-native
- 不提前写分析正文
- 不提前给确定性结论

## 必须参考

- `openspec/schemas/blockchain-research/templates/plan.md`
