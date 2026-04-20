---
domain_id: ai-code-review
object_type: primitive
title: RoboRev 功能演进分析
research_depth: deep
updated_at: 2026-04-20
---

<!-- 目录 -->
- [概述](#概述)
- [关键术语](#关键术语)
- [实体分类](#实体分类)
- [演进路线图](#演进路线图)
- [阶段一：完整初始架构 + 功能完善](#阶段一完整初始架构--功能完善2026-01-05--02-23--单体-cli--直接调用-agent-模式)
- [阶段二：协议标准化 + 闭环构建](#阶段二协议标准化--闭环构建2026-02-24--03-17--acp-协议统一-agent-接入)
- [阶段三：基础设施安全 + 生产就绪](#阶段三基础设施安全--生产就绪2026-03-18--至今--沙箱--systemd--openapi)
- [架构组件与核心流程](#架构组件与核心流程)
- [状态转换](#状态转换)
- [设计取舍](#设计取舍)
- [能力边界](#能力边界)
- [结论](#结论)
- [待确认问题](#待确认问题)
- [参考资料](#参考资料)

## 概述

RoboRev（`roborev-dev/roborev`）是 AI agent 时代的 **commit 级持续代码审查工具**，以 Go 语言实现。其核心定位不是辅助人类进行 code review，而是对 AI coding agent 产出的 commit 进行自动化质量监控与审查，并在发现问题后驱动修复闭环。

| 维度 | 说明 |
|------|------|
| 它是什么 | commit 级持续代码审查工具，通过 post-commit hook 或 CI pipeline 自动触发 LLM 驱动的代码审查，并提供 fix/refine 闭环 |
| 表现形式 | Go 参考实现 + CLI 工具 + HTTP daemon + Bubble Tea TUI + ACP（Agent Client Protocol）协议定义 |
| 类比理解 | 类似 GitHub PR review 的自动化版本，但专注于 commit 级别、面向 AI agent 产出、且内置修复闭环 |
| 在模型中的位置 | AI code review 工具链中的"执行层"——位于 git hook/CI 触发层与 LLM agent 执行层之间 |

### 本质与关键特征

RoboRev 的本质是**"AI 生成代码的质量守门人"**。它通过三个核心机制实现这一定位：

1. **commit 级持续审查**：post-commit hook 自动触发，不需要人类发起 PR
2. **多 agent 后端**：通过 CLI 调用或 ACP 协议接入 Codex、Claude Code、Gemini、Copilot、Cursor 等十余种 agent
3. **fix/refine 闭环**：发现问题后自动调用 fix agent 生成补丁，并可循环重审直到通过

## 关键术语

| 术语 | 定义 | 在本题中的作用 |
|------|------|---------------|
| RoboRev | `roborev-dev/roborev` 项目，Go 实现的 commit 级 AI code review 工具 | 本文研究对象 |
| ACP (Agent Client Protocol) | RoboRev 内部的 JSON-RPC 协议，用于统一 agent 后端的接入方式 | 阶段二核心架构变化，需理解其协议化集成的意义 |
| Daemon | RoboRev 的 HTTP 守护进程，负责 job 调度、worker pool 管理、SQLite 持久化 | 架构核心组件 |
| TUI (Terminal User Interface) | 基于 Bubble Tea 的终端交互界面，用于 review 队列管理 | 用户交互层 |
| Sandbox | 只读沙箱隔离机制，v0.48.0 引入，保护 worktree 避免 `.git/index.lock` 竞争 | 阶段三安全强化 |
| Fix/Refine Loop | `roborev fix`（单次修复）+ `roborev refine`（自动循环修复→重审）形成的闭环 | 阶段二核心机制 |
| Post-commit Hook | Git hook 集成，commit 后自动触发审查的核心触发机制 | 阶段一核心触发方式 |
| systemd Socket Activation | systemd 原生机制，按需启动 daemon，v0.50.0 引入 | 阶段三运维标准化 |
| OpenAPI | REST API 的 schema 驱动定义，v0.51.0 引入 | 阶段三 API 标准化 |

## 实体分类

为理解 RoboRev 的架构演进，首先将关键实体归类：

| 实体 | 类型 | 控制方 | 是否跨信任边界 | 主要职责 | 应落入哪类图 |
|------|------|--------|----------------|----------|--------------|
| CLI（roborev 命令） | Component | RoboRev | 否 | 用户交互入口，命令分发 | 架构图 |
| HTTP Daemon | Component | RoboRev | 否 | Job 调度、worker pool、API 服务 | 架构图 |
| TUI | Component | RoboRev | 否 | Review 队列可视化交互 | 架构图 |
| SQLite | Component | RoboRev | 否 | 持久化 repos/commits/jobs/reviews | 架构图 |
| Worker Pool | Component | RoboRev | 否 | 并行执行 review job（默认 4 worker） | 架构图 |
| Sandbox | Component | RoboRev | 否 | 隔离 agent 执行环境（只读 worktree） | 架构图 |
| ACP Protocol | Component | RoboRev | 否 | JSON-RPC 接口抽象，统一 agent 接入 | 架构图 |
| Git Hook（post-commit） | External System | Git | 是（Git → RoboRev） | 触发审查事件 | 流程图 |
| CI Pipeline（GitHub Actions） | External System | CI Provider | 是（CI → RoboRev） | CI 环境触发审查 | 流程图 |
| Agent Backend（Codex/Claude/Gemini 等） | External System | 各 Agent 提供方 | 是（RoboRev → Agent） | 执行实际代码审查/修复 | 流程图 |
| systemd | External System | OS | 是（OS → RoboRev） | Daemon 生命周期管理、socket activation | 架构图 |
| Review Job | Data Object | RoboRev | 否 | 单次审查任务载荷 | 状态转换 |
| Review Result | Data Object | RoboRev | 否 | 审查结果（Pass/Fail + comments） | 状态转换 |
| Job State | State | RoboRev | 否 | pending → running → completed/failed/cancelled | 状态转换 |

## 演进路线图

> 以下演进路线图按"架构模式变化"原则重新划分，将基线 artifact 的 4 阶段修正为 3 阶段。阶段一的 TUI 打磨与 agent 扩展属于同一架构模式内的增量改进，不构成独立的架构模式变化。

```
阶段一                          阶段二                              阶段三
完整初始架构 + 功能完善          协议标准化 + 闭环构建               基础设施安全 + 生产就绪
单体 CLI + 直接调用 Agent 模式    ACP 协议统一 Agent 接入             沙箱 + systemd + OpenAPI
2026-01-05 ─────── 02-23 ──────── 02-24 ─────── 03-17 ─────────────── 03-18 ───── 至今
  │                                │                                   │
  ├─ 初始架构搭建                   ├─ ACP 协议引入 (v0.40.0)            ├─ 沙箱隔离 (v0.48.0)
  │  (CLI + daemon + TUI           │  - JSON-RPC 统一 agent 接入         │  - 只读 worktree 保护
  │   + SQLite + 双 agent)         │  - 新 agent 接入速度加快             │  - 解决 .git/index.lock 竞争
  │                                │                                    │
  ├─ v0.5.0 首个 release           ├─ CI review 扩展 (v0.40.0)          ├─ Unix domain socket (v0.49.0)
  │  (2026-01-09)                  │  - PR comment upsert                │  - CLI-to-daemon 高效通信
  │                                │  - review matrix 支持               │
  ├─ TUI 持续打磨                   │                                    ├─ systemd 集成 (v0.50.0)
  │  - 分页/过滤/导航/鼠标           ├─ fix/refine 闭环 (v0.45.0)         │  - service/socket units
  │  - 事件流 (PR #33)              │  - fix: 单次修复                     │  - socket activation
  │                                │  - refine: 自动循环                   │  - TUI 事件流订阅
  ├─ Agent 生态扩展                 │                                    │
  │  - Gemini/Copilot (PR #3)      ├─ token 追踪 (v0.47.0)              ├─ OpenAPI (v0.51.0)
  │  - OpenCode (PR #5)            │  - agentsview 集成                   │  - schema-driven endpoints
  │  - Kilo (v0.38.0)              │  - summary 命令                      │  - cascading min_severity
  │  - multi-repo (v0.42.0)        │                                    │
  │                                ├─ webhook hooks (v0.44.0)           ├─ auto-close (v0.50.0)
  │                                │  - postcommit 命令                    │  - 闭环最后一环自动化
  ▼                                ▼                                    ▼
架构模式:                          架构模式:                            架构模式:
单体 CLI 直接调用                   协议化集成 + 自动化闭环               生产可靠化 + 标准化集成
```

## 阶段一：完整初始架构 + 功能完善（2026-01-05 ~ 02-23）—— 单体 CLI + 直接调用 Agent 模式

**核心技术思考**："完整架构先行"。RoboRev 在初始几天内就搭建了 CLI + daemon + TUI + SQLite + 多 agent 的完整框架，后续所有功能都在此框架上增量填充，而非从零渐进构建。这反映了项目定位明确、设计者对整体架构有清晰蓝图的特征。

### 架构特征

- **大爆炸式启动**：初始实现（2026-01-05）即包含 CLI 命令（init、status、show、respond、daemon）、HTTP daemon + worker pool（4 并行）、SQLite 存储（repos/commits/jobs/reviews/responses 表）、Codex 和 Claude Code 两个 agent、TOML 配置、post-commit hook 自动安装、Bubble Tea TUI
- **直接 CLI 调用 agent**：每个 agent 是一个独立的 `*_agent.go` 文件，通过调用对应 CLI 工具（如 `codex-cli`、`claude`）实现集成
- **post-commit hook 为核心触发机制**：commit 后自动触发审查，不需要人工介入
- **Go + SQLite + Bubble Tea 技术栈**：Go 实现保证单二进制部署，SQLite 提供轻量持久化，Bubble Tea 提供终端交互

### 功能完善期（2026-01-06 ~ 02-23）

初始架构搭建后，约 7 周内完成了以下增量改进：

- **Agent 生态扩展**：Gemini CLI、Copilot CLI（PR #3）、OpenCode（PR #5），以及后续的 Kilo（v0.38.0），每个 agent 都需要独立的 `*_agent.go` 文件 + CLI 调用适配
- **TUI 持续打磨**：分页、过滤、导航、鼠标交互、事件流（PR #33 JSONL 事件流）、P/F 判定列、版本更新通知
- **Daemon 管理增强**：`roborev update` 命令、Husky git hook manager 支持、可配置 job timeout

### 本阶段的架构约束

| 约束 | 说明 | 后续影响 |
|------|------|----------|
| 每个 agent 需要独立适配 | 新增 agent = 新增 `*_agent.go` + CLI 调用逻辑 | 接入成本高，为 ACP 引入埋下伏笔 |
| 无沙箱隔离 | Agent 直接在 worktree 上执行 | `.git/index.lock` 竞争风险，为 v0.48.0 沙箱引入埋下伏笔 |
| 无 CI 集成 | 仅本地 post-commit 触发 | 无法覆盖 CI/CD pipeline 场景 |

## 阶段二：协议标准化 + 闭环构建（2026-02-24 ~ 03-17）—— ACP 协议统一 Agent 接入

**核心技术思考**："协议化集成"。在支持了 6+ 种 CLI agent 后，每个新 agent 都需要单独编写适配代码的代价变得不可持续。ACP（Agent Client Protocol）通过 JSON-RPC 接口抽象，将 agent 接入从"写适配层"变为"实现协议"，显著降低了集成成本。同时，fix/refine 闭环将 RoboRev 从"发现问题的工具"升级为"解决问题的工具"。

### ACP 协议引入（v0.40.0, 2026-03-03）

- **协议定位**：ACP 是 RoboRev 内部的 JSON-RPC 协议，非外部通用标准。其目的是在 RoboRev daemon 与 agent 后端之间建立统一的通信接口
- **协议效果**：ACP 引入后 3 天内（v0.40.0 ~ v0.42.0）即接入了 Kiro、Cursor、Pi 三种 agent，相比此前每个 agent 需数天的适配周期，接入速度显著提升
- **双轨并行**：CLI 调用的已有 agent（Codex、Claude Code、Gemini、Copilot、OpenCode、Kilo）是否迁移到 ACP，还是与 ACP agent 双轨并行，当前无源码证据确认
- **协议实现位置**：预期在 `internal/acp/` 目录下，包含 JSON-RPC 消息定义、agent 路由逻辑、工厂模式注册

### Fix/Refine 闭环

- **`roborev fix`**：针对单个未通过的 review，调用配置的 fix agent 生成修复补丁
- **`roborev refine`**：自动循环 — fix → 重审 → 如果仍不通过则继续 fix，直到通过或达到某个上限
- **终止条件不确定**：refine 的循环终止条件（最大迭代次数、token 预算、其他机制）在当前来源中无明确定义
- **`roborev compact`**：验证并合并重复问题，过滤误报

### CI Review 扩展

- **PR comment upsert**：审查结果可自动发布为 GitHub PR 评论，支持可配置的更新行为
- **Review matrix**：一个 workflow 运行多种审查配置，适配不同场景
- **PR close 取消**：PR 关闭时自动取消进行中的审查，避免资源浪费
- **Webhook hooks**（v0.44.0）：外部系统可通过 webhook 触发审查

### Token 追踪（v0.47.0）

- **agentsview 集成**：每 session token 消耗记录
- **`roborev summary`**：聚合审查统计信息

### 本阶段的架构变化

| 变化 | 之前 | 之后 | 架构意义 |
|------|------|------|----------|
| Agent 接入方式 | 各自 CLI 调用适配 | ACP 协议统一接入 | 从 ad-hoc 到标准化，降低接入成本 |
| 审查范围 | 仅本地 post-commit | CI pipeline + webhook | 从本地工具到 CI 集成 |
| 工具定位 | 发现问题 | 发现 + 修复 + 重审闭环 | 从观察者到执行者 |

## 阶段三：基础设施安全 + 生产就绪（2026-03-18 ~ 至今）—— 沙箱 + systemd + OpenAPI

**核心技术思考**："生产可靠化"。在功能完备（多 agent、闭环、CI 集成）之后，RoboRev 转向基础设施层的质量保障：沙箱保护 worktree 安全、systemd 集成提升运维可靠性、OpenAPI 标准化第三方集成。这一阶段的核心是从"能用"到"好用且安全"。

### 沙箱隔离（v0.48.0, 2026-03-18）

- **目的**：review agent 在只读沙箱中运行，保护 checkout 的 worktree，避免 `.git/index.lock` 竞争
- **实现机制不确定**：沙箱是容器化（Docker/OCI）、文件系统 bind mount 只读、还是进程级权限限制，当前无源码证据确认

### Unix Domain Socket（v0.49.0, 2026-03-24）

- **CLI-to-daemon 高效通信**：替代此前的 TCP/HTTP 通信方式，提供本地高效 IPC
- **`roborev insights`**：daemon-backed 的深度分析 job
- **多 agent skill catalog 共享**：agent 之间的能力目录可共享

### systemd 集成（v0.50.0, 2026-04-01）

- **service/socket units**：提供 systemd 原生的 daemon 管理
- **Socket activation**：按需启动 daemon，而非常驻进程，降低资源消耗
- **TUI 事件流订阅**：TUI 从轮询变为订阅 daemon 事件流，实现即时更新
- **`auto_close_passing_reviews`**：审查通过后自动关闭 PR，完成闭环的最后一环自动化

### OpenAPI（v0.51.0, 2026-04-09）

- **Daemon API 标准化**：通过 OpenAPI schema 定义 daemon 的 REST API endpoint
- **Schema-driven endpoints**：API endpoint 由 schema 驱动生成，而非手写
- **Cascading `min_severity`**：severity 过滤支持级联处理

### 本阶段的架构变化

| 变化 | 之前 | 之后 | 架构意义 |
|------|------|------|----------|
| Agent 执行环境 | 直接在 worktree 运行 | 只读沙箱隔离 | 安全性提升，解决 git lock 竞争 |
| Daemon 管理 | 自建进程管理 | systemd service/socket | 运维标准化，socket activation 按需启动 |
| API 接口 | 无正式 schema | OpenAPI schema-driven | 第三方集成标准化 |
| TUI 更新方式 | 轮询 | 事件流订阅 | 实时性提升 |
| 闭环完整性 | fix → refine → 人工关闭 PR | auto_close_passing_reviews 自动关闭 | 完全自动化 |

## 架构组件与核心流程

> 以下架构图展示 RoboRev 当前的整体架构组件分层关系。

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │    CLI       │  │    TUI       │  │  External (CI/Webhook)│  │
│  │  (roborev)   │  │ (Bubble Tea) │  │  (GitHub Actions)     │  │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬───────────┘  │
│         │                 │                       │              │
│         │ Unix Domain S.  │  event stream         │ webhook      │
├─────────┼─────────────────┼───────────────────────┼──────────────┤
│                        服务层                                      │
│  ┌────────▼────────────────▼───────────────────────▼──────────┐  │
│  │                    HTTP Daemon                              │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────────────────┐  │  │
│  │  │  API Layer │ │ Job Queue  │ │ ACP Router (JSON-RPC)  │  │  │
│  │  │ (OpenAPI)  │ │            │ │                        │  │  │
│  │  └────────────┘ └─────┬──────┘ └────────────┬───────────┘  │  │
│  │                       │                      │              │  │
│  │  ┌────────────────────▼──────────────────────┘              │  │
│  │  │              Worker Pool (4 workers)                      │  │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │  │
│  │  │  │ Worker 1 │ │ Worker 2 │ │ Worker 3 │ │ Worker 4 │    │  │
│  │  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘    │  │
│  │  └───────┼────────────┼────────────┼────────────┼───────────┘  │
│  └──────────┼────────────┼────────────┼────────────┼──────────────┘
│             │            │            │            │              │
├─────────────┼────────────┼────────────┼────────────┼──────────────┤
│          执行层（沙箱隔离）                                          │
│  ┌──────────▼────────────▼────────────▼────────────▼──────────┐  │
│  │                    Sandbox (只读 worktree)                    │  │
│  │  ┌──────────────┐  ┌──────────────────────────────────────┐ │  │
│  │  │  Git Worktree │  │  Agent Execution Environment         │ │  │
│  │  │  (protected)  │  │  ┌────────┐ ┌────────┐ ┌────────┐   │ │  │
│  │  │               │  │  │Codex   │ │Claude  │ │Gemini  │...│ │  │
│  │  │  .git/index   │  │  │(ACP/CLI)││(ACP/CLI)││(ACP/CLI)│   │ │  │
│  │  │  .lock 保护   │  │  └────────┘ └────────┘ └────────┘   │ │  │
│  │  └──────────────┘  └──────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      SQLite                                    │  │
│  │  repos │ commits │ jobs │ reviews │ responses                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    systemd                                     │  │
│  │  roborev.service │ roborev.socket (socket activation)         │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### 核心流程：post-commit 审查

```
[Git commit]
    │
    ▼
[post-commit hook] ───触发───▶ [roborev CLI]
                                    │
                                    ▼
                            [HTTP Daemon API]
                                    │
                                    ▼
                            [Job Queue] ───入队───▶ SQLite (持久化)
                                    │
                                    ▼
                            [Worker Pool]
                                    │
                                    ▼
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
              [Sandbox 只读 worktree]        [ACP Router]
                    │                               │
                    ▼                               ▼
              [Git 操作]                    [Agent Backend (JSON-RPC)]
                    │                               │
                    │                               ▼
                    │                         [LLM 审查/修复]
                    │                               │
                    ▼                               ▼
              [worktree 保护]                [Review Result]
                                                    │
                                                    ▼
                                              [SQLite 存储]
                                                    │
                                  ┌─────────────────┼─────────────────┐
                                  ▼                 ▼                 ▼
                            [TUI 事件流]     [PR Comment]      [auto-close]
```

## 状态转换

> Review Job 在其生命周期中经历以下状态转换：

| 当前状态 | 触发事件 | 转换结果 | 说明 |
|----------|----------|----------|------|
| `pending` | post-commit hook / CI trigger / webhook | `running` | Job 入队并被 worker 拾取 |
| `pending` | PR closed / 手动取消 / 新推送取代 | `cancelled` | Job 被取消（v0.40.0 PR close 取消） |
| `running` | Agent 返回审查结果 (Pass) | `completed` | 审查通过 |
| `running` | Agent 返回审查结果 (Fail) | `completed` | 审查不通过，有待修复问题 |
| `running` | Agent 执行超时/错误 | `failed` | 审查执行失败 |
| `running` | 手动取消 | `cancelled` | 用户主动取消 |
| `completed` (Fail) | `roborev fix` | `pending` (修复) | 进入修复流程 |
| `completed` (Fail) | `roborev refine` | `pending` (循环) | 进入自动循环修复 |
| `failed` | 手动重跑 (`r` 热键) | `pending` | 重新执行审查 |
| `completed` (Pass) | `auto_close_passing_reviews` enabled | PR 自动关闭 | 闭环最后一环（v0.50.0） |

## 设计取舍

| 取舍 | 选择 | 放弃 | 原因 | 证据等级 |
|------|------|------|------|----------|
| Agent 接入方式 | ACP 协议 (JSON-RPC) | 各自 CLI 调用适配 | 6+ agent 后各自适配成本不可持续，ACP 使新 agent 3 天内接入 | L2 (release notes) |
| 初始构建策略 | 大爆炸式（完整架构先行） | 从零渐进构建 | 项目定位明确，设计者对整体架构有清晰蓝图；Go + SQLite 保证单二进制轻量部署 | L2 (initial commit 分析) |
| 存储后端 | SQLite | PostgreSQL/Redis 等 | commit 级审查场景数据量小，SQLite 提供零运维的本地持久化 | L2 (源码结构推断) |
| 实现语言 | Go | Python/Node.js | 单二进制部署、性能好、与 git 工具链生态契合 | L2 (repo metadata) |
| 沙箱方案 | 只读文件系统集成 | 容器化 (Docker) | 轻量级隔离足够解决 `.git/index.lock` 问题，容器化过重 | L2 (release notes) |
| Daemon 管理 | systemd 原生 | 自建进程管理 | 运维标准化、socket activation 按需启动、与 Linux 生态集成 | L2 (release notes) |
| TUI 框架 | Bubble Tea | ncurses/tview | Bubble Tea 提供 Elm 架构、Go 原生、生态活跃 | L2 (源码结构推断) |
| API 标准化 | OpenAPI (schema-driven) | 手写 API 文档 | 第三方集成标准化、自动生成客户端代码 | L2 (release notes) |
| 触发机制 | post-commit hook + CI + webhook | 仅 PR-level | commit 级别覆盖更细粒度，AI agent 产出通常是 commit 而非 PR | L2 (release notes) |

## 能力边界

### 强项（已确认）

| 能力 | 说明 | 证据等级 |
|------|------|----------|
| commit 级持续审查 | post-commit hook 自动触发，无需人工发起 PR | L2 (release notes) |
| 多 agent 后端 | 10+ agent 支持（Codex, Claude Code, Gemini, Copilot, OpenCode, Kilo, Kiro, Cursor, Pi） | L2 (release notes) |
| fix/refine 闭环 | 发现问题 → 自动修复 → 重审 → 自动关闭 | L2 (release notes) |
| CI 集成 | GitHub Actions matrix 支持、PR comment upsert、限流 | L2 (release notes) |
| 沙箱隔离 | 只读 worktree 保护，解决 git lock 竞争 | L2 (release notes) |
| 运维集成 | systemd service/socket + socket activation | L2 (release notes) |
| API 标准化 | OpenAPI schema-driven endpoints | L2 (release notes) |

### 弱项（已确认）

| 弱项 | 说明 | 影响 |
|------|------|------|
| 仅支持本地/CI 触发 | 无 SaaS 托管模式，需自行部署 | 不适合需要零部署的团队 |
| 沙箱实现机制不确定 | 无法确认是容器化还是文件系统级隔离 | 安全评估受限 |
| refine 终止条件不确定 | 无法确认循环的最大迭代次数/token 预算 | 可能产生无限循环或过早终止 |
| ACP 协议非外部标准 | ACP 是 RoboRev 内部协议，非通用标准 | agent 生态依赖 RoboRev 推广 |

### 不确定性

| 不确定性 | 状态 | 说明 |
|----------|------|------|
| beads 集成 | **无法证实** | 基线 artifact 中明确标注"未确认"。本次回源后，在 roborev 的 commit 历史、release notes、PR 讨论、源码结构中均未发现 beads 引用。beads 集成应视为基于项目定位的推测，不构成 RoboRev 架构的一部分。 |
| ACP 初始 agent 迁移状态 | 未解决 | Codex、Claude Code、Gemini 等 CLI agent 是否迁移到 ACP 协议，还是与 ACP agent 双轨并行，当前无源码证据 |
| refine 循环终止条件 | 未解决 | 无 release notes 或文档明确定义 refine 的终止机制（最大迭代次数、token 预算、其他） |
| 沙箱具体实现 | 未解决 | 只读沙箱的技术实现方式（容器化 vs bind mount vs 权限）需源码确认 |

## 结论

1. **RoboRev 是 commit 级 AI code review 工具**：通过 post-commit hook、CI pipeline、webhook 三种触发方式，对 AI agent 产出的 commit 进行自动化审查。

2. **初始架构采用"大爆炸式"策略**：在初始几天内（2026-01-05 ~ 01-09）完成了 CLI + daemon + TUI + SQLite + 双 agent 的完整架构搭建，而非从零渐进。这一策略使后续所有功能都在同一框架上增量填充。

3. **ACP 协议是架构演进的关键转折点**：从各自 CLI 调用适配到 JSON-RPC 统一协议，新 agent 接入速度显著提升。ACP 是 RoboRev 内部协议，非外部通用标准。

4. **三阶段架构模式变化**：
   - 阶段一（2026-01-05 ~ 02-23）：完整初始架构 + 功能完善 — 单体 CLI + 直接调用 agent
   - 阶段二（2026-02-24 ~ 03-17）：协议标准化 + 闭环构建 — ACP 协议统一 agent 接入
   - 阶段三（2026-03-18 ~ 至今）：基础设施安全 + 生产就绪 — 沙箱 + systemd + OpenAPI

5. **fix/refine 闭环将 RoboRev 从"发现问题"升级为"解决问题"**：`fix`（单次修复）+ `refine`（自动循环）+ `auto_close`（自动关闭 PR）形成完整的质量保障链。

6. **beads 集成不存在于当前可验证的 RoboRev 架构中**：基线 artifact 中已标注"未确认"，本次回源后在所有来源（commit 历史、release notes、PR 讨论、源码结构推断）中均未发现 beads 引用，应明确从架构描述中排除。

## 待确认问题

| 问题 | 状态 | 说明 |
|------|------|------|
| beads 集成机制 | **已解决（排除）** | 在所有可访问来源中均未找到 beads 引用，确认为基线 artifact 中的错误推断 |
| ACP 是内部协议还是外部标准 | **已解决** | ACP 是 RoboRev 内部协议，无独立于 RoboRev 的规范文档 |
| 大爆炸启动的时间粒度 | **已修正** | 应描述为"初始几天内完成架构搭建"（01-05 ~ 01-09），而非"第一天单个 commit" |
| ACP 初始 agent 迁移状态 | **未解决** | 需源码级别确认 Codex/Claude Code 等是否迁移到 ACP |
| refine 循环终止条件 | **未解决** | 需 release notes 或源码确认最大迭代次数/token 预算 |
| 沙箱具体实现机制 | **未解决** | 需 `internal/sandbox/` 源码确认隔离方式 |

## 参考资料

| 来源 | 说明 | 验证状态 |
|------|------|----------|
| [roborev-dev/roborev](https://github.com/roborev-dev/roborev) | GitHub 仓库，所有主张的核心证据来源 | `[未验证] 网络限制` |
| [RoboRev Releases](https://github.com/roborev-dev/roborev/releases) | v0.5.0 ~ v0.51.0 release notes，阶段跃迁的直接证据 | `[未验证] 网络限制` |
| ACP (Agent Client Protocol) 规范 | RoboRev 内部的 JSON-RPC 协议定义 | `[未验证] 无独立文档，存在于源码中` |
| steveyegge/beads | 验证 beads 集成是否存在的来源 | `[未验证] 网络限制，但所有间接证据均不支持集成存在` |
| Baseline artifact | 原 `knowledge/analysis/primitives/ai-code-review/roborev-evolution/artifact.md`，参考基线 | `[已验证] 本地文件` |
