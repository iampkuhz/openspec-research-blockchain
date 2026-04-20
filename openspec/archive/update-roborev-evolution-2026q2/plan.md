## 研究对象

- 对象类型：primitive
- 研究路径：evolution
- 相关 domains：ai-code-review

## 问题拆解

### 核心问题（必须在 draft 中回答）

1. 定义层：RoboRev 是什么？它如何定义 commit 级持续代码审查？管什么/不管什么？
2. 机制层：RoboRev 的架构经历了怎样的阶段跃迁？每个阶段新增了什么架构模式、抛弃了什么旧路径？ACP 协议化的核心变化是什么？
3. 边界层：RoboRev 与 PR 级 review 工具（CodeRabbit、Qodo Merge）的边界在哪里？哪些能力是 RoboRev 原生提供的，哪些依赖外部组件？
4. 关系层：RoboRev 在 AI agent 代码审查生态中的定位？ACP 是内部协议还是可外部复用的标准？

### 后续确认问题

1. ACP 协议的完整 JSON-RPC 方法定义有哪些？（需源码确认 `internal/acp/`）
2. 已有的 CLI agent（Codex、Claude Code 等）在 ACP 引入后是否迁移？还是双轨并行？
3. `roborev refine` 的循环终止条件是什么？（最大迭代次数、token 预算、或其他机制）
4. 沙箱的具体实现方式是什么？（容器化 vs bind mount vs 进程权限限制）
5. beads 集成是否真实存在？（基线 artifact 中标注为"未确认"，需源码/commit 历史验证）

## 交付范围

本次产出：
- request.md（已有，需确认是否需修订）
- plan.md
- sources/（通过 MCP 工具回源验证）
- draft.md（含 PlantUML 架构图和时序图）

## 研究深度

- deep：全面深挖 RoboRev 从 inception 至今的架构演进，所有核心主张必须有 L2（源码/release notes）来源支撑

## 来源规划

### L1 来源（规范层）

| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| ACP 协议定义（`internal/acp/` 源码） | implementation | JSON-RPC 接口规范、消息格式、agent 路由逻辑 | `[未验证]` 需抓取源码 |
| Go module 定义（`go.mod`） | implementation | 确认依赖技术栈（Bubble Tea、SQLite 驱动等） | `[未验证]` 需抓取源码 |

### L2 来源（实现层）

| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| [roborev-dev/roborev GitHub 仓库](https://github.com/roborev-dev/roborev) | repo | README、整体架构描述 | `[未验证]` 需 MCP 抓取 |
| [RoboRev Releases](https://github.com/roborev-dev/roborev/releases) | repo | v0.5.0 ~ v0.51.0+ release notes，阶段跃迁的直接证据 | `[未验证]` 需 MCP 抓取 |
| [commit 历史](https://github.com/roborev-dev/roborev/commits/main) | repo | 验证大爆炸启动、ACP 引入时间点、beads 引用 | `[未验证]` 需 MCP 抓取 |
| `internal/` 目录结构 | repo | 确认组件分层（daemon、acp、sandbox、tui、cli 等） | `[未验证]` 需 MCP 抓取 |
| `cmd/` 目录结构 | repo | CLI 命令入口（roborev init、status、fix、refine、compact、summary 等） | `[未验证]` 需 MCP 抓取 |
| 配置文件 schema（TOML） | repo | 验证配置模型和 agent 注册方式 | `[未验证]` 需 MCP 抓取 |
| systemd unit 文件 | repo | v0.50.0 引入的 service/socket 定义 | `[未验证]` 需 MCP 抓取 |
| OpenAPI schema | repo | v0.51.0 引入的 API 定义 | `[未验证]` 需 MCP 抓取 |

### L3 来源（生态层）

| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| RoboRev 官方博客/文档（如有） | blog | 设计理念、roadmap | `[未验证]` 需搜索确认是否存在 |
| GitHub Issues/Discussions | discussion | 社区反馈、feature request | `[未验证]` 需搜索 |

### L4 来源（解读层）

| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| 既有 artifact `knowledge/analysis/primitives/ai-code-review/roborev-evolution/artifact.md` | analysis | 参考基线，用于对比修正 | `[已验证]` 本地文件已读取 |

## 证据矩阵

| 主张 | 所需证据等级 | 来源 | 置信度 |
|------|-------------|------|--------|
| 三阶段架构模式划分 | L2 (release notes + commit 历史) | Releases + commits | high |
| ACP 协议引入时间与效果 | L2 (源码 + release notes) | `internal/acp/` + v0.40.0 release | high |
| 大爆炸式初始架构 | L2 (initial commits) | 2026-01-05 ~ 01-09 commits | high |
| fix/refine 闭环机制 | L2 (源码 + release notes) | `cmd/fix.go`、`cmd/refine.go` + v0.45.0 | medium |
| 沙箱隔离机制 | L2 (源码) | `internal/sandbox/` | medium |
| systemd 集成 | L2 (源码 + release notes) | systemd unit files + v0.50.0 | high |
| OpenAPI 集成 | L2 (源码 + release notes) | OpenAPI schema + v0.51.0 | high |
| beads 集成不存在 | L2 (commit 历史 + 源码结构) | 全仓库搜索 beads 引用 | high |

## 证据缺口

1. **ACP 完整协议规范**：需要 `internal/acp/` 下完整的 JSON-RPC 方法定义、消息 schema
2. **refine 终止条件**：需要源码确认循环终止机制
3. **沙箱实现细节**：需要 `internal/sandbox/` 确认隔离方式
4. **CLI agent 迁移状态**：需要确认已有 agent 是否迁移到 ACP

## 完成标准

- [x] request.md 已存在且结构完整
- [ ] plan.md 完成
- [ ] 所有 L2 来源（GitHub repo、release notes、关键源码）已通过 MCP 工具实际抓取并写入 `sources/excerpts/`
- [ ] sources/source-review.md 完成
- [ ] draft.md 完成，包含：
  - 关键术语表（表格形式）
  - 实体分类表
  - 图表决策树 + 图表清单
  - PlantUML 架构图（角色与信任边界）
  - PlantUML 时序图（核心流程）
  - 三阶段演进路线图（ASCII/Mermaid timeline）
  - 设计取舍表
  - 能力边界（强项/弱项/不确定性）
  - 有限结论（标注证据等级）
  - 待确认问题
  - 参考资料表（`[[source-type] description](url)` 格式）
- [ ] 所有核心主张有 L2 来源支撑，不得全部停留在 L4 推断

## 排除范围

- 不深入 ACP 协议之外的其他 agent 协议（如 MCP、A2A）的完整机制
- 不覆盖竞品（CodeRabbit、Qodo Merge）的完整机制分析
- 不做商业化/市场定位分析
