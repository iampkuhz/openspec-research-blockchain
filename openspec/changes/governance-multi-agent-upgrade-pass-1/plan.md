## 研究对象

- 对象类型：domain
- 研究路径：domain overview
- 相关 domains：repository-governance, research-execution, agent-orchestration

## 问题拆解

1. 盘点现有执行面真源：`AGENTS.md`、OpenSpec、Harness、Claude 命令层之间的职责边界。
2. 确定第一版 agent roster，并明确哪些职责合并、哪些职责保持独立。
3. 设计命令层驱动的协作协议，包括激活条件、并行边界、handoff artifact、fallback。
4. 把 agent contract 正式落到 `harness/agents/`，并让 workflow 与命令层改为消费它们。
5. 修正会直接干扰 multi-agent 质量的关键入口漂移，如资产模型、长期输出、依赖声明与旧 skill 名称。

## 待确认问题

- Q1：第一版是否只做 Claude Code 侧落地，而把 Qoder 维持为 skeleton？
- Q2：source-evidence 与 traceability audit 的边界应该如何保持“生产者/审计者分离”？
- Q3：diagram 能力是常驻 agent 还是条件 agent？本轮决定为条件 agent 后，哪些 workflow 需要显式声明激活条件？
- Q4：publish 阶段除 artifact 提炼外，是否同时承担 update impact scan？本轮决定合并为同一角色后，需要哪些 workflow 与 skill 同步调整？
- Q5：旧 `knowledge/topics`、`dependencies.md`、`evidence-matrix.md` 残留本轮清理到什么深度？本轮采取“只修关键入口与关键执行面文件”的策略。

## 交付范围

| 范围 | 交付物 | 本轮策略 |
|------|--------|----------|
| 治理文档 | `guides/*.md` | 必须 |
| Agent 注册表 | `harness/agents/_index.yaml` | 必须 |
| Agent contract | `harness/agents/*.md` | 必须 |
| Workflow 升级 | `research-pipeline.md`、`review-workflow.md`、`source-workflow.md`、`merge-workflow.md`、`governance-review-workflow.md` | 必须 |
| Claude 命令升级 | `.claude/commands/spec-*.md` | 必须 |
| 关键入口对齐 | `AGENTS.md`、`README.md`、关键 rules / skills | 必须 |
| Qoder 骨架 | `.qoder/agents/README.md` | 推荐 |
| Qoder 命令重写 | `.qoder/commands/*.md` | 排除 |

## 研究深度

- deep

本轮不是只给建议，而是直接把第一版架构落地到仓库中，形成可继续迭代的基线。

## 依赖声明（synthesis/decision 必需）

本次为 governance / domain 改造，不适用 research object 级依赖声明。  
但执行上依赖以下内部基线文件作为真源输入：

### 依赖对象列表

| 对象 | 类型 | 当前状态 | 所需深度 | 当前深度 | 差异处理 |
|------|------|----------|----------|----------|----------|
| `openspec/config.yaml` | governance baseline | 已存在 | deep | deep | 直接引用 |
| `openspec/schemas/blockchain-research/schema.yaml` | governance baseline | 已存在 | deep | deep | 直接引用 |
| `docs/governance/openspec-harness-boundary.md` | governance baseline | 已存在 | deep | deep | 直接引用 |
| `harness/workflows/research-pipeline.md` | execution baseline | 已存在 | deep | deep | 增量重写 |
| `.claude/commands/spec-*.md` | execution baseline | 已存在 | deep | deep | 增量重写 |

### 依赖详细说明

#### OpenSpec / Boundary Baseline

- **依赖原因**：决定哪些内容属于正式规则，哪些属于执行层编排
- **抽取内容**：资产模型、阶段语义、边界约束、apply 规则
- **不重复内容**：不在 `Harness` 中重新定义 artifact contract
- **差异处理**：若发现执行层文档与正式规则冲突，以 OpenSpec / boundary 为准

#### Workflow / Command Baseline

- **依赖原因**：multi-agent 升级必须建立在现有阶段主链上，而不是另起一套平行体系
- **抽取内容**：现有阶段责任、输入输出、质量闸门、命令触发方式
- **不重复内容**：不复制整个 spec 正文到命令层
- **差异处理**：在保持阶段主链不变的前提下，把单 agent 步骤重构为 orchestrated execution

### 补充调研计划

| 对象 | 当前深度 | 所需深度 | 补充范围 | 优先级 |
|------|----------|----------|----------|--------|
| `.qoder/agents/` 运行时格式 | none | light | 仅补 README 骨架，不在本轮深挖可执行格式 | medium |

## 来源规划

### L1 来源（规范层）

| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| `openspec/config.yaml` | config | 项目级流程与 apply 入口 | `[已验证]` |
| `openspec/schemas/blockchain-research/schema.yaml` | schema | artifact contract 与对象模型 | `[已验证]` |
| `docs/governance/openspec-harness-boundary.md` | governance | OpenSpec / Harness 边界 | `[已验证]` |

### L2 来源（实现层）

| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| `harness/workflows/research-pipeline.md` | workflow | 当前端到端执行链 | `[已验证]` |
| `harness/workflows/review-workflow.md` | workflow | 当前评审链 | `[已验证]` |
| `.claude/commands/spec-research.md` | command | 当前 Claude 端到端入口 | `[已验证]` |
| `.claude/commands/spec-plan.md` | command | 当前 plan 阶段入口 | `[已验证]` |
| `.claude/commands/spec-draft.md` | command | 当前 draft 阶段入口 | `[已验证]` |
| `.claude/commands/spec-artifact.md` | command | 当前 artifact 阶段入口 | `[已验证]` |

### L3 来源（生态层）

| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| `README.md` | repo-doc | 仓库外显入口，存在旧语义漂移 | `[已验证]` |
| `skills/README.md` | repo-doc | skill 注册表入口 | `[已验证]` |
| `skills/maintenance/merge-change-into-knowledge/SKILL.md` | skill | apply 相关执行面文档，存在旧路径 | `[已验证]` |
| `skills/maintenance/refresh-existing-topic/SKILL.md` | skill | update 相关执行面文档，存在旧路径 | `[已验证]` |

### L4 来源（解读层）

| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| `openspec/changes/primitive-a2a-agentic-payment-protocol/` | internal example | 用于观察当前 change packet 的实际落盘形态 | `[已验证]` |

## 证据矩阵（可选）

| 主张 | 证据等级 | 置信度 | 缺口 / 歧义 |
|------|----------|--------|-------------|
| 本仓库当前主问题是“执行层缺少角色合同”，而不是“正式规则层缺失” | L1 | high | 无 |
| 第一版 agent 不宜超过 5 个常驻角色 | L2 | high | 属于架构判断，非正式规则 |
| `.qoder/agents/` 目前为空，适合先补 skeleton 而非完整 runtime | L2 | high | 具体 runtime contract 仍未标准化 |

## 证据缺口

- Qoder 侧 agent runtime 约定未在仓库中形成正式文档
- 某些旧 rules 仍保留 atom/topic 时代语义，本轮只能优先清理关键入口
- 当前没有针对 multi-agent orchestration 的自动化测试脚本，本轮以文档合同 + 基本一致性检查为主

## 完成标准

- [ ] `guides/` 下形成可顺序执行的升级指导文档
- [ ] `harness/agents/` 下形成第一版 agent registry 与 contract
- [ ] `research-pipeline` 与相关 workflow 能明确 agent 激活与 handoff
- [ ] `.claude/commands/spec-*.md` 升级为 agent-aware 入口
- [ ] 关键入口漂移完成第一轮收口
- [ ] 至少完成一次基本验证，确认新增文件和关键引用关系自洽

## 排除范围

- 不在本轮创建新的 OpenSpec spec 来描述 multi-agent 运行时细节
- 不在本轮实现完整的 review 自动化或 agent 调度器代码
- 不在本轮强制所有历史 change packet 回填到新 contract
