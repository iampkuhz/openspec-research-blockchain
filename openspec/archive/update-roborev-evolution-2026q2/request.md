- 对象类型：primitive
- 研究路径：evolution
- 相关 domains：ai-code-review

## 当前要回答的问题

1. 定义层：RoboRev 是什么？它如何定义 commit 级持续代码审查？管什么/不管什么？
2. 机制层：RoboRev 的架构经历了怎样的阶段跃迁？ACP 协议化的核心变化是什么？
3. 边界层：RoboRev 与 PR 级 review 工具（CodeRabbit、Qodo Merge）的边界在哪里？
4. 关系层：RoboRev 在 AI agent 代码审查生态中的定位？

## 为什么现在要研究

既有 artifact（`knowledge/analysis/primitives/ai-code-review/roborev-evolution/artifact.md`）在上一轮研究中因环境限制，来源未实际回源验证。本次研究需要：
- **必须回源**到 RoboRev GitHub 仓库（roborev-dev/roborev）验证关键主张，包括 commit diff、release notes
- 验证三阶段划分（CLI -> ACP 协议化 -> 沙箱/生产就绪）是否准确
- 验证 ACP 协议的具体规范和技术实现
- 使用 PlantUML 而非 ASCII 图
- 确保所有核心主张有 L2（源码）来源支撑

## 范围

### 覆盖对象

RoboRev（roborev-dev/roborev）项目，Go 实现的 commit 级 AI code review 工具。

### 覆盖链/协议

Git post-commit hook、ACP（Agent Client Protocol）、CLI 与 HTTP daemon 架构。

### 时间窗口

RoboRev 项目 inception 至今的全部公开演进历史。

## 非目标

- 不深入 ACP 协议之外的其他 agent 协议机制
- 不覆盖竞品完整机制

## 已知输入

- 既有 artifact：`knowledge/analysis/primitives/ai-code-review/roborev-evolution/artifact.md`（仅作为参考基线，本次研究必须独立回源验证）

## 预期输出

- artifact.md：RoboRev 功能演进的深度分析，所有核心主张必须有实际回源的来源支撑
