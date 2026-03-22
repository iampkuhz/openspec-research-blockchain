# Prompt：生成 Plan

请基于已有的 `request.md` 生成或改写 `plan.md`。

## 任务

输出一个集中 review 文件，合并以下职责：

- 问题收紧
- 研究预算
- 来源规划
- 证据缺口
- 后续确认问题

## 强约束

- `plan.md` 不是分析正文
- 必须区分 `L1 / L2 / L3 / L4`
- 必须写 `evidence gap` 与 `unresolved ambiguity`
- 对 `primitive`，必须显式列出后续确认问题，例如：
  - 为什么不直接改传统 transaction 路径
  - 关键角色分别位于哪一层
  - 哪些能力不是 protocol-native
