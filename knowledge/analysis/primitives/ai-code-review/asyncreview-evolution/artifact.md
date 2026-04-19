---
domain_id: ai-cr-tools
object_type: primitive
title: AsyncReview 功能演进分析
research_depth: deep
updated_at: 2026-04-19
---

<!-- 目录 -->
- [项目概览](#项目概览)
- [阶段一：项目骨架与基础 CLI](#阶段一项目骨架与基础-cli2026-01-24--01-29)
- [阶段二：CLI 实现与 npx 一键运行](#阶段二cli-实现与-npx-一键运行2026-01-26--01-29)
- [阶段三：Agentic 代码库访问](#阶段三agentic-代码库访问2026-01-30--01-31--v020)
- [阶段四：多轮 RLM + Deno 运行时](#阶段四多轮-rlm--deno-运行时2026-02-02--v030--v05x)
- [阶段五：RLM 原生工具迁移 + 本地模式](#阶段五rlm-原生工具迁移--本地模式2026-02-10--03-09--v06x)
- [阶段六：静止期](#阶段六静止期2026-03-10--至今)
- [架构变迁总结](#架构变迁总结)
- [关键里程碑时间线](#关键里程碑时间线)
- [结论](#结论)

## 项目概览

> AsyncReview（AsyncFuncAI/AsyncReview）是一个基于 RLM（Recursive Language Models）的开源 Agentic 代码审查工具，数百 stars，Python 实现。核心差异是不做一次性 diff 分析，而是通过"思考 → 生成代码 → 沙箱执行 → 观察结果 → 递归迭代"的循环获取全仓库上下文。

---

## 阶段一：项目骨架与基础 CLI（2026-01-24 ~ 01-29）

**时间**: 2026-01-24（Initial commit）至 2026-01-29

**背景**: 项目以两步 Initial commit 启动。第一步仅创建 README，第二步构建了完整项目骨架。

**核心功能**:
- `cr/` 核心模块：`diff_rlm.py`（RLM 审查引擎）、`github.py`（GitHub API）、`render.py`（渲染）、`suggestions.py`（建议生成）、`types.py`（类型定义）
- 前端 Web UI（React + Vite）：`web/src/` 包含 DiffViewer、ChatPanel、BugsPanel、PRSummary 等组件
- Deno 沙箱配置：`deno.json` 在初始骨架中就存在，说明沙箱是设计之初就规划的
- CLI 入口：`start.sh`、`pyproject.toml`、`uv.lock`

**架构特征**:
- 模块化设计：`cr/` 目录分离关注点（diff 处理、RLM 执行、GitHub 交互、渲染）
- 前后端分离：Python 后端 + React 前端
- Deno 沙箱在第一天就写入配置，但实际执行引擎尚未实现

**关键里程碑**:
- 2026-01-24: Initial commit（空 README）
- 2026-01-25: Initial Commit（完整项目骨架，39 个文件）

---

## 阶段二：CLI 实现与 npx 一键运行（2026-01-26 ~ 01-29）

**时间**: 2026-01-26 至 2026-01-29

**背景**: 在骨架基础上实现可运行的 CLI，降低用户使用门槛。

**核心功能**:
- 实现 AsyncReview CLI，支持 GitHub PR 和 Issue 审查，带输出格式化
- 添加 `npx asyncreview review` 支持，用户无需本地安装即可运行
- README 添加截图、介绍视频和用户附件链接

**架构特征**:
- TypeScript CLI 层（`npx/src/`）通过 Python runner 桥接 Python 后端
- 用户只需 `npx asyncreview review --url <PR-url>` 即可使用
- 仍是一次性 diff 分析，RLM 能力有限

**关键里程碑**:
- 第一个可运行的 CLI 实现
- npx 支持，降低使用门槛

---

## 阶段三：Agentic 代码库访问（2026-01-30 ~ 01-31）— v0.2.0

**时间**: 2026-01-30 至 2026-01-31

**背景**: 从"只看 diff"升级为"可探索整个仓库"，这是第一次架构跃迁。

**核心功能**:
- **v0.2.0 — Agentic codebase access for PR reviews**
  - 新增 `repo_tools.py`：FETCH_FILE、LIST_DIR、SEARCH_CODE 三种工具
  - RLM 现在可以获取 diff 之外的文件，理解项目依赖关系
  - 使用 GitHub 的 `filename:` 限定符进行智能文件名搜索
  - 改进步骤进度显示，展示 RLM 的推理/代码/输出
- 添加 GitHub Token 支持，可审查私有仓库
- **添加 asyncreview skill** — 可被其他 agent（Claude、Cursor 等）作为 Skill 调用

**架构变迁**:
- 新增 `repo_tools.py`：RLM 的工具集从"分析 diff"扩展到"探索仓库"
- 工具拦截器模式：RLM 生成的工具调用被拦截并转为 GitHub API 请求
- Skill 集成：`skills/asyncreview/SKILL.md` 定义文件，支持 vercel/skills 兼容的 agent

**关键里程碑**:
- v0.2.0 是第一个有版本号的 release
- Skill 集成从此成为项目的核心定位之一（"被其他 agent 调用"而非独立工具）

---

## 阶段四：多轮 RLM + Deno 运行时（2026-02-02）— v0.3.0 → v0.5.x

**时间**: 2026-02-01 至 2026-02-03（项目最密集的演进期）

**背景**: 从单轮 RLM 升级为多轮有状态的递归推理，同时引入 Deno 沙箱作为 Python 运行时。这一天产生了 v0.3.0 → v0.4.0 → v0.5.0 → v0.5.9 共 10+ 个版本。

**核心功能**:
- **Enhance RLM agent with multi-turn state for repo tools** — RLM 现在有状态，可多轮迭代
- **Implement robust Python runtime environment management with Deno support** — 引入 Deno 作为沙箱运行时，新增 build/release 基础设施
- CI/CD 密集修复：
  - 使用 dspy 2.x 实现 CI/CD 兼容
  - 使用 dspy 2.5.x 并优先检查 PATH 中的 python
  - 使用 Python 3.11 + dspy 3.1.2 支持 RLM
  - hybrid bundled deps + pip fallback 解决 Python 版本不匹配

**架构变迁**:
- DSPy 框架深度集成：`dspy.RLM()` 成为核心执行引擎
- Deno 沙箱选型：用 Deno 提供隔离的 Python REPL 执行环境，而非直接 subprocess
- npx CLI 架构变化：TypeScript 层管理 Python 运行时（下载、安装、版本兼容）
- `AGENTIC_TOOLS_PROMPT` 和 `_process_tool_requests()` 出现（约 200 行自定义工具调度代码）

**关键里程碑**:
- 一天内 10+ 次 release 说明项目在快速迭代 CI/CD 和运行时兼容性
- Deno 沙箱从设计阶段的 `deno.json` 变为实际运行的运行时

---

## 阶段五：RLM 原生工具迁移 + 本地模式（2026-02-10 ~ 03-09）— v0.6.x

**时间**: 2026-02-10 至 2026-03-09

**背景**: 简化架构，从自定义工具调度迁移到 DSPy RLM 原生 `tools=[]` 参数，同时添加本地文件夹支持。

**核心功能**:
- **Migrate RLM to use native tools[] and simplify review flow**
  - 移除 `AGENTIC_TOOLS_PROMPT` 常量（约 60 行）
  - 移除 `_process_tool_requests()` 和 `_run_rlm_with_tools()` 方法（约 140 行）
  - 移除未使用的状态字典（`_repo_files`、`_repo_dirs`、`_search_results`）
  - 使用直接 `rlm.aforward()` 调用
  - 更新类文档引用原生 DSPy RLM tools
  - 实现 `on_step` 回调使用 `result.trajectory`
- **本地目录支持**
  - `local_fetcher.py`：本地目录上下文构建
  - `LocalRepoTools`：本地文件系统访问（list_directory、search_code）
  - TypeScript CLI 层添加 `--path` 选项
- 强化 RLM prompt 防止幻觉
- 安全修复：LocalRepoTools.search_code() 中的 shell 注入漏洞
- 合并 PR #5 添加本地文件夹支持

**架构变迁**:
- **抛弃**：约 200 行自定义工具调度代码（`AGENTIC_TOOLS_PROMPT` + `_process_tool_requests` + `_run_rlm_with_tools`）
- **采用**：DSPy RLM 原生 `tools=[]` 参数，工具函数通过 `_create_tool_functions()` 返回 `dict[str, Callable]`
- 新增本地模式：`--path` 选项，不需要 GitHub Token 即可审查本地 PR/代码
- 安全修复：shell 注入漏洞（`grep` 命令从 `shell=True` 改为列表式 subprocess）

**关键里程碑**:
- 这是一次重大架构简化，移除约 200 行自定义代码
- v0.6.1 (2026-02-08) 是最后一个有 release notes 的版本

---

## 阶段六：静止期（2026-03-10 ~ 至今）

**时间**: 2026-03-10 至今（约 6 周）

**状态**:
- 最后推送：2026-03-09（PR #5 合并）
- 无新 release
- 存在未合并的 PR：
  - PR #6: "Add 8 deep code understanding and GitHub context tools for RLM agent"（open）
  - PR #9: "Gitea support + multi-forge URL parsing groundwork"（open）
  - PR #11: "feat: add AtomGit/GitCode support"（open）

**分析**:
- 项目在 v0.6.1 后进入相对静止期
- 未合并的 PR 显示演进方向：更多代码理解工具、更多 Git 平台支持

---

## 架构变迁总结

### 演进路径

```
一次性 diff 分析 (2026-01-25)
    ↓
Agentic 仓库探索 + 工具拦截器 (2026-01-30, v0.2.0)
    ↓
Skill 集成 — 被其他 agent 调用 (2026-01-31)
    ↓
多轮 RLM + Deno 沙箱运行时 (2026-02-02, v0.4.0)
    ↓
RLM 原生工具迁移 — 简化约 200 行代码 (2026-02-10)
    ↓
本地模式支持 — --path 选项 (2026-03-09, v0.6.1)
```

### 抛弃的架构

| 被抛弃 | 时间 | 原因 |
|--------|------|------|
| 自定义工具调度（约 200 行） | 2026-02-10 | DSPy RLM 原生 tools[] 更简洁 |
| 一次性 diff 分析 | 2026-01-30 | 上下文不足，需要全仓库探索 |
| AGENTIC_TOOLS_PROMPT 常量 | 2026-02-10 | 原生工具参数无需 prompt 包装 |

### 采用的架构

| 采用 | 时间 | 原因 |
|------|------|------|
| repo_tools 工具拦截器 | 2026-01-30 | RLM 需要超越 diff 的上下文 |
| Deno 沙箱 | 2026-02-02 | 安全执行 Python 代码 |
| Skill 集成 | 2026-01-31 | 定位从独立工具变为 agent 的"眼睛" |
| DSPy RLM 原生 tools[] | 2026-02-10 | 简化架构，减少维护成本 |

### 技术栈选择考量

- **DSPy 而非直接调用 LLM API**：RLM 需要状态管理和递归迭代，DSPy 提供框架支持
- **Deno 沙箱而非 subprocess**：安全性隔离，防止 RLM 生成的恶意代码影响宿主环境
- **npx CLI 桥接**：降低用户使用门槛，不需要 Python 环境
- **仅支持 Gemini**：DSPy RLM 与 Gemini 集成最成熟

---

## 关键里程碑时间线

```
2026-01-24  Initial commit（空 README）
2026-01-25  完整项目骨架（cr/ + web/ + deno.json）
2026-01-26  CLI 实现 + npx 一键运行
2026-01-30  v0.2.0 — Agentic codebase access (repo_tools)
2026-01-31  Skill 集成 + GitHub Token 支持
2026-02-02  多轮 RLM + Deno 沙箱，10+ 次 release 修复 CI/CD
2026-02-03  v0.5.9 — 强化 RLM prompt 防止幻觉
2026-02-08  v0.6.1 — Runtime release
2026-02-10  RLM 原生工具迁移 + 本地模式（约 200 行代码简化）
2026-03-09  PR #5 合并，本地文件夹支持完成
2026-03-10~ 静止期，无新 release
```

---

## 结论

AsyncReview 的演进呈现明显的**"能力递增 + 架构简化"**趋势：

1. **能力递增**：从一次性 diff 分析 → 全仓库探索 → 多轮递归推理 → 本地模式
2. **架构简化**：从约 200 行自定义工具调度 → DSPy RLM 原生 tools[]（减少维护负担）
3. **定位演变**：从独立 CR 工具 → 被其他 agent 调用的 Skill（"eyes and reasoning" for agents）

项目总生命周期仅约 6 周（2026-01-24 ~ 2026-03-09），但经历了 4 次重大架构变更。当前的静止期（6 周无更新）可能表明项目在等待 DSPy RLM 框架的进一步成熟，或团队在探索新的演进方向。
