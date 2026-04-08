# Governance Multi-Agent Upgrade - Draft

## 概述

本轮改造把仓库执行层从“单 agent 顺序执行 + 阶段命令分散约定”升级为“以 orchestrator 为入口、以 `Harness` 为真源、以 agent contract 为边界”的第一版 multi-agent 模式。

目标不是追求 agent 数量，而是降低三个实际问题：

- 作者自己找证据、自己写正文、自己判断证据充分性的自证偏差
- 阶段命令与 workflow 各自存一套执行逻辑，容易漂移
- diagram / governance / publish 这些高专门性步骤没有独立激活条件

本轮采用 `5 + 2` 架构：

- 常驻：`orchestrator`、`research-author-agent`、`source-evidence-agent`、`review-critic-agent`、`publish-agent`
- 条件启用：`diagram-agent`、`governance-review-agent`

## 术语表

| 术语 | 定义 | 在本题中的作用 |
|------|------|----------------|
| orchestrator | 负责任务分类、激活 agent、控制 handoff 与整合结果的入口角色 | 第一版 multi-agent 的总调度者 |
| agent contract | 定义某个 agent 的职责、输入、输出、可读写范围、禁止行为的执行文档 | 避免 agent 角色漂移 |
| always-on agent | 几乎所有研究流程都会启用的角色 | 形成基础 roster |
| conditional agent | 只在满足特定语义条件时启用的角色 | 避免 roster 膨胀 |
| handoff artifact | agent 之间交接的正式文件或结构化结论 | 保证上下文传递稳定 |
| baseline alignment | 在升级前对齐关键入口的现有语义，消除旧路径与旧模型残留 | 避免 agent 读到不同“真相” |

## 组件架构

本轮不新增调度代码，而是先把编排结构正式化：

| 层 | 文件位置 | 责任 |
|----|----------|------|
| 正式规则层 | `openspec/config.yaml`、`openspec/schemas/...`、`openspec/specs/...` | 定义 artifact contract、资产模型、正式约束 |
| 执行编排层 | `harness/workflows/`、`harness/agents/`、`harness/rules/` | 定义 agent 激活、执行顺序、质量闸门、执行检查 |
| 命令入口层 | `.claude/commands/` | 选择 workflow，调用 active agents，汇报结果 |
| 过程资产层 | `openspec/changes/<change-id>/` | request / plan / draft / sources / review / guides |
| 长期资产层 | `knowledge/analysis/`、`knowledge/decisions/` | apply 后的 canonical 资产 |

## 核心流程

- 【S1】`orchestrator` 读取 `AGENTS.md`、workflow index、agent index，判断这是普通 research、update，还是 governance 改造。
- 【S2】如为普通 research，`orchestrator` 激活 `research-author-agent` 负责 `request / plan / draft` 主链，同时按需要并行激活 `source-evidence-agent` 与 `diagram-agent`。
- 【S3】`research-author-agent` 只消费正式规则与活跃 agent 的输出，不在命令层重新定义 artifact contract。
- 【S4】`review-critic-agent` 在 `draft.md` 完成后独立执行 technical review、traceability audit、terminology consistency 检查，并输出 `review/` 目录结果。
- 【S5】当评审通过时，`publish-agent` 执行 artifact 提炼，并在 update 场景下一并判断影响范围与兼容性处理。
- 【S6】如任务语义涉及仓库治理、schema、workflow、rules、AGENTS 路由变更，则额外激活 `governance-review-agent`。

## 设计取舍

| 设计点 | 选项 | 本轮选择 | 原因 |
|--------|------|----------|------|
| 常驻 agent 数量 | 11 个细粒度角色 / 5 个基础角色 | 5 个基础角色 | v1 优先控制复杂度和 handoff 成本 |
| plan 与 analysis | 分拆 / 合并 | 合并为 `research-author-agent` | `plan -> draft` 强连续，拆开收益小 |
| source 与 traceability | 合并 / 分离 | 生产与审计分离 | 避免自证偏差 |
| publish 与 update impact | 分离 / 合并 | 合并为 `publish-agent` | 都属于发布后处理链，强共享上下文 |
| diagram / governance | 常驻 / 条件启用 | 条件启用 | 这两类能力只在特定语义下需要 |

## 能力边界

### 本轮明确支持

- 以 `Harness` 作为 multi-agent 编排真源
- 以 `orchestrator + agent contracts` 驱动 Claude 命令层
- 以 `5 + 2` 角色模型覆盖主要研究路径
- 对关键旧入口做第一轮对齐，减少错误路由

### 本轮明确不支持

- 不提供通用 agent runtime 或 agent 进程管理器
- 不把 multi-agent 运行细节提升为 OpenSpec 正式规则
- 不保证 Qoder 侧立刻具备与 Claude 侧完全相同的执行体验

## 相关协议对比

| 方案 | 特点 | 问题 |
|------|------|------|
| 保持单 agent | 实现最简单 | 难以获得独立审计与高质量并行 |
| 11 个以上细粒度 agent | 职责切分很细 | 上手成本高，handoff 成本高，v1 易失控 |
| `5 + 2` agent | 保留关键独立性，控制复杂度 | 仍需依赖命令层良好编排 |

## 结论

1. multi-agent 升级应落在 `Harness + Commands`，而不是 OpenSpec 正式规则层。
2. 第一版以 `5 + 2` 角色模型最合适：既保留独立 reviewer，又避免 roster 膨胀。
3. 真正要交付给仓库的是三样东西：`agent registry`、`collaboration protocol`、`agent-aware commands`。
4. 在升级 agent 之前，必须先处理会影响 agent 判断的一批关键入口漂移，否则质量会变差而不是变好。

## 待确认问题

| 问题 | 当前状态 | 说明 |
|------|----------|------|
| Qoder agent runtime 的最终格式 | 未解决 | 本轮只补 skeleton，不做完整实现 |
| multi-agent 的自动化回归测试 | 部分解决 | 本轮只形成验收清单和基础检查 |
| 非关键 legacy 文档是否全部清扫 | 未解决 | 留待后续 cleanup change |

## 参考资料

| 来源 | 说明 | 验证状态 |
|------|------|----------|
| `openspec/config.yaml` | 项目级 OpenSpec 配置 | `[已验证]` 本地文件 |
| `openspec/schemas/blockchain-research/schema.yaml` | 研究对象模型与 artifact contract | `[已验证]` 本地文件 |
| `docs/governance/openspec-harness-boundary.md` | OpenSpec / Harness 边界 | `[已验证]` 本地文件 |
| `harness/workflows/research-pipeline.md` | 当前端到端执行流程 | `[已验证]` 本地文件 |
| `.claude/commands/spec-research.md` | 当前 Claude 端到端入口 | `[已验证]` 本地文件 |
