---
domain_id: ai-cr-tools
object_type: primitive
title: roborev 功能演进分析
research_depth: deep
updated_at: 2026-04-19
---

<!-- 目录 -->
- [项目概览](#项目概览)
- [阶段一：完整初始架构](#阶段一完整初始架构2026-01-05--01-09--v050)
- [阶段二：TUI 成熟 + Agent 生态扩展](#阶段二tui-成熟--agent-生态扩展2026-01-10--02-23)
- [阶段三：ACP 协议 + CI Review + Fix/Refine Loop](#阶段三acp-协议--ci-review--fixrefine-loop2026-02-24--03-17--v039--v047)
- [阶段四：Daemon 强化 + 沙箱 + OpenAPI](#阶段四daemon-强化--沙箱--openapi2026-03-18--至今--v048--v051)
- [架构变迁总结](#架构变迁总结)
- [关键里程碑时间线](#关键里程碑时间线)
- [结论](#结论)

## 项目概览

> roborev（roborev-dev/roborev）是 AI agent 时代的 commit 级持续审查工具，Go 实现，~863 stars。创建于 2026-01-05，544+ commits。定位不是传统人工 CR，而是 AI 编码 agent 产出质量监控。

---

## 阶段一：完整初始架构（2026-01-05 ~ 01-09）— v0.5.0

**时间**: 2026-01-05 至 2026-01-09

**背景**: roborev 以"大而全"的初始实现启动，第一天就包含了 CLI + daemon + TUI + SQLite + 多 agent 支持，不同于大多数项目从零开始渐进构建。

**核心功能**（初始 commit 已包含）:
- CLI 命令：init、status、show、respond、daemon
- HTTP daemon + worker pool（4 个并行审查）
- SQLite 存储：repos、commits、jobs、reviews、responses
- Codex 和 Claude Code 两个 agent 支持
- 按 repo 和全局配置（TOML）
- post-commit hook 自动安装
- 端口冲突自动处理的 daemon 启动
- Bubble Tea TUI：交互式队列管理

**早期快速迭代（一周内）**:
- PR #3: 添加 Gemini CLI、Copilot CLI 支持
- PR #5: 添加 OpenCode agent 支持
- PR #8: `roborev update` 命令 + TUI 新版本通知
- PR #11: Husky git hook manager 支持
- PR #13: post-commit hook 生成重构，消除代码重复
- PR #16: 可配置 job timeout
- PR #17: TUI 键盘导航在 review 间切换
- PR #18: TUI 视图自适应终端宽度
- PR #19: 按 repo 过滤模态框
- PR #20: TUI 分页
- PR #24: TUI 队列 P/F (Pass/Fail) 判定列
- PR #26: `h` 热键隐藏已处理 review
- PR #33: JSONL 事件流，审查完成通知
- PR #35: `r` 热键重跑失败/取消的 job

**架构特征**:
- **大爆炸启动**：初始实现就包含了完整的 CLI + daemon + TUI + 存储 + 多 agent
- Go + Bubbletea TUI + SQLite + Huma REST API
- post-commit hook 是核心触发机制
- Agent 通过 CLI 调用方式集成（Codex CLI、Claude Code CLI）

**关键里程碑**:
- 2026-01-05: 初始 commit，一天内完成完整架构搭建
- v0.5.0 (2026-01-09): 首个 release（注：release notes 具体功能范围未完全确认，至少包含 README 文档与截图更新）

---

## 阶段二：TUI 成熟 + Agent 生态扩展（2026-01-10 ~ 02-23）

**时间**: 2026-01-10 至 2026-02-23

**背景**: 在完整初始架构基础上，TUI 持续改进用户体验，agent 生态快速扩展。

**核心功能**:
- **TUI 持续打磨**：
  - 分支显示 + 已处理 review 颜色区分（PR #29）
  - Nix flake 构建系统（PR #30）
  - 过滤、分页、导航、事件流等持续完善
- **Agent 扩展**：
  - Gemini CLI、Copilot CLI（PR #3）
  - OpenCode（PR #5）
  - 后续陆续添加 Kilo、Kiro、Cursor、Pi 等
- **v0.38.0** (2026-02-26):
  - Kilo agent 支持（通过 `kilo` CLI）
  - `roborev wait` 接受多个 job ID
  - TUI 鼠标交互
  - daemon 生命周期管理（`roborev update`）
  - `roborev fix` 跳过已解决的 review

**架构特征**:
- Agent 通过统一的 CLI 调用接口扩展（每个 agent 是一个独立的 `*_agent.go` 文件）
- TUI 从基础队列管理发展为完整交互体验（分页、过滤、鼠标、颜色区分）
- Nix flake 支持，面向开发者的构建系统完善

---

## 阶段三：ACP 协议 + CI Review + Fix/Refine Loop（2026-02-24 ~ 03-17）— v0.39 ~ v0.47

**时间**: 2026-02-24 至 2026-03-17

**背景**: 引入 Agent Client Protocol（ACP）标准化 agent 集成，同时构建完整的 fix/refine 闭环，从本地 post-commit 扩展到 CI pipeline。

**核心功能**:
- **v0.40.0** (2026-03-03): **ACP 支持**
  - Agent Client Protocol 支持，可接入更多本地 agent 后端
  - Kiro agent 集成（通过 `kiro-cli`）
  - 可配置的 PR comment upsert 行为
  - CI review matrix 支持（一个 workflow 运行多种审查配置）
  - PR 审查限流 + PR 关闭时取消审查
- **v0.42.0** (2026-03-06):
  - 多 repo workspace 支持
  - Cursor agent 支持
  - Pi coding agent 支持
  - 生成的 patch 文件保存
  - 新推送取代进行中的审查时跳过限流
  - Claude review 失败报告改进
- **v0.44.0** (2026-03-07):
  - TUI 全局鼠标交互禁用开关
  - `roborev postcommit` 和 hook 设置
  - webhook review hooks
  - `excluded_commit_patterns`
  - `auto_filter_branch`
- **v0.45.0** (2026-03-09):
  - `--min-severity` 用于 `fix` 和 `refine`
  - 复制 review 时包含 review comments
  - 安全地复用当前分支兼容的 review sessions
- **v0.47.0** (2026-03-17):
  - `roborev summary`：聚合审查统计
  - TUI 控制 socket + `--no-quit` 标志
  - Agent token 用量追踪 + token backfill

**架构变迁**:
- **ACP 协议**：从各自 CLI 调用统一到 Agent Client Protocol，降低新 agent 接入成本。在支持 5+ 种 CLI agent 后，每个新 agent 都需要单独的 `*_agent.go` 文件 + CLI 调用适配。ACP 协议通过统一的 JSON-RPC 接口抽象，新 agent 只需实现 ACP 协议即可接入，不再需要自定义适配层。这从 v0.40.0 之后新增 agent 的速度明显加快（Kiro、Cursor、Pi 在 3 天内全部接入）可以得到验证。
- **CI review**：从本地 post-commit 扩展到 CI pipeline 集成（matrix 支持、限流、取消）
- **fix/refine loop**：`roborev fix` + `roborev refine` 形成审查 → 修复 → 重审闭环
  - `roborev fix`：针对单个未通过的 review，调用配置的 fix agent 生成修复补丁
  - `roborev refine`：自动循环 — fix → 重审 → 如果仍不通过则继续 fix，直到通过或达到上限
  - `roborev compact`：验证并合并重复问题，过滤误报
  - v0.50.0 引入 `auto_close_passing_reviews`，闭环的最后一环自动化
- **Token 追踪**：`agentsview` 集成，每 session token 消耗记录
- **beads 集成**（未确认）：与 steveyegge/beads 的集成细节在当前可获得的 commit 历史与 release notes 中未直接出现。从 roborev "accountability for every line of generated code" 的定位推断，beads 可能用于将 review findings 转化为可追踪的 issue/task，形成从发现问题到修复完成的完整审计链。此推断需补充 beads 相关 PR 讨论记录后确认。

**关键里程碑**:
- v0.40.0: ACP 协议引入，agent 路由标准化
- v0.44.0: `postcommit` 命令 + webhook hooks，触发机制完善
- v0.47.0: `summary` 命令 + token 追踪，可观测性提升

---

## 阶段四：Daemon 强化 + 沙箱 + OpenAPI（2026-03-18 ~ 至今）— v0.48 ~ v0.51

**时间**: 2026-03-18 至今

**背景**: 基础设施强化，daemon 稳定性、安全性、可集成性成为重点。

**核心功能**:
- **v0.48.0** (2026-03-18): **沙箱隔离**
  - Review agent 在只读沙箱中运行，保护 checkout 的 worktree
  - 避免 `.git/index.lock` 竞争
- **v0.49.0** (2026-03-24):
  - daemon-backed `roborev insights` jobs
  - Unix domain socket 支持（CLI-to-daemon 通信）
  - `ROBOREV_COLOR_MODE` 颜色输出控制
  - 多 agent skill catalog 共享
- **v0.50.0** (2026-04-01): **自动关闭 + systemd**
  - `auto_close_passing_reviews` 自动关闭通过的审查
  - bundled `roborev-refine` skills（Codex 和 Claude）
  - systemd service/socket units + socket activation
  - TUI 订阅 daemon 事件流，即时更新
- **v0.51.0** (2026-04-09): **OpenAPI + severity 过滤**
  - OpenAPI 支持 daemon API，schema-driven 端点
  - cascading `min_severity` 处理
  - review-level 过滤
  - 分支审查 prompt 包含每 commit 审查结果

**架构变迁**:
- **沙箱隔离**：只读沙箱保护 worktree，解决 agent 执行与 git 操作冲突
- **systemd 集成**：从自建 daemon 到 systemd 原生 service/socket
- **OpenAPI**：daemon API 标准化，便于第三方集成
- **事件流订阅**：TUI 从轮询变为订阅 daemon 事件流

**关键里程碑**:
- v0.48.0: 沙箱隔离，安全性提升
- v0.50.0: systemd 集成 + auto-close，运维友好
- v0.51.0: OpenAPI，第三方集成标准化

---

## 架构变迁总结

### 演进路径

```
完整初始架构（CLI+daemon+TUI+SQLite+双agent）(2026-01-05, v0.5.0)
    ↓
TUI 成熟 + Agent 生态扩展（6+ agent）(2026-01-10 ~ 02-23)
    ↓
ACP 协议 + CI Review + Fix/Refine 闭环 (2026-02-24 ~ 03-17, v0.40-v0.47)
    ↓
Daemon 强化 + 沙箱 + systemd + OpenAPI (2026-03-18 ~ 至今, v0.48-v0.51)
```

### Agent 生态扩展时间线

| 时间 | Agent | 集成方式 |
|------|-------|----------|
| 2026-01-05 | Codex | CLI 调用（初始） |
| 2026-01-05 | Claude Code | CLI 调用（初始） |
| 2026-01-06 | Gemini CLI | CLI 调用 |
| 2026-01-06 | Copilot | CLI 调用 |
| 2026-01-08 | OpenCode | CLI 调用 |
| 2026-02-26 | Kilo | CLI 调用 |
| 2026-03-03 | Kiro | ACP 协议 |
| 2026-03-03 | ACP 协议 | 标准化协议引入 |
| 2026-03-06 | Cursor | ACP 协议 |
| 2026-03-06 | Pi | ACP 协议 |

### 抛弃的架构

| 被抛弃 | 时间 | 原因 |
|--------|------|------|
| 各自 CLI 调用（无标准协议） | 2026-03-03 | ACP 协议标准化 |
| 轮询式 TUI 更新 | 2026-04-01 | 事件流订阅（v0.50.0） |
| 自建 daemon 管理 | 2026-04-01 | systemd service/socket（v0.50.0） |

### 采用的架构

| 采用 | 时间 | 原因 |
|------|------|------|
| ACP 协议 | 2026-03-03 | 降低新 agent 接入成本 |
| 只读沙箱 | 2026-03-18 | 保护 worktree，避免 git lock 竞争 |
| Unix domain socket | 2026-03-24 | CLI-to-daemon 高效通信 |
| systemd socket activation | 2026-04-01 | 运维标准化 |
| OpenAPI | 2026-04-09 | 第三方集成标准化 |

---

## 关键里程碑时间线

```
2026-01-05  初始实现（CLI + daemon + TUI + SQLite + Codex + Claude Code）
2026-01-06  Gemini + Copilot + OpenCode agent 支持
2026-01-09  v0.5.0 首个 release
2026-01-10  TUI P/F 判定列 + 过滤 + 分页
2026-02-26  v0.38.0 Kilo agent + fix 跳过已解决 review
2026-03-03  v0.40.0 ACP 协议 + CI review matrix + Kiro
2026-03-06  v0.42.0 多 repo + Cursor + Pi agent
2026-03-07  v0.44.0 postcommit 命令 + webhook hooks
2026-03-17  v0.47.0 summary 命令 + token 追踪
2026-03-18  v0.48.0 只读沙箱隔离
2026-03-24  v0.49.0 Unix domain socket + insights
2026-04-01  v0.50.0 auto-close + systemd + 事件流
2026-04-09  v0.51.0 OpenAPI + severity 过滤（最新稳定版）
```

---

## 结论

roborev 的演进呈现**"大爆炸启动 + 渐进式完善"**的趋势：

1. **大爆炸启动**：第一天就包含完整的 CLI + daemon + TUI + SQLite + 双 agent，不同于大多数项目从零开始
2. **Agent 生态快速扩展**：两周内支持 6+ 种 agent（Codex、Claude Code、Gemini、Copilot、OpenCode、Kilo、Kiro、Cursor、Pi）
3. **协议标准化**：从各自 CLI 调用 → ACP 协议 → OpenAPI，逐步标准化集成接口
4. **闭环构建**：post-commit → review → fix → refine → summary → auto-close，形成完整的质量保障链

项目总生命周期约 3.5 个月（2026-01-05 ~ 至今），544+ commits，平均每 1-2 天一个 release。演进速度极快，是目前最活跃的 AI CR 项目。

### 不确定性说明

| 条目 | 状态 | 说明 |
|------|------|------|
| beads 集成机制 | 未确认 | 基于项目定位的推断，需补充 PR 讨论记录后确认 |
| v0.5.0 具体内容 | 部分确认 | release notes 功能范围未完全确认 |
| ACP 内部实现细节 | 未确认 | 协议使用有明确 release 证据，但内部代码实现路径需源码级别确认 |
