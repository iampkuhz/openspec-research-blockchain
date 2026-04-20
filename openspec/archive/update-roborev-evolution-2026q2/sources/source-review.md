# Source Review

## 来源概览

| 类型 | 数量 |
|------|------|
| L1 | 0 |
| L2 | 12 |
| L3 | 0 |
| L4 | 1 |

## 核心来源

1. **GH-README** (L2): RoboRev GitHub 仓库 README - 项目定义、特性列表、命令参考、支持 agent 列表
2. **GH-RELEASES** (L2): v0.5.0 ~ v0.52.0 全部 release notes - 演进阶段划分的直接证据
3. **GH-GOMOD** (L2): go.mod - 确认 ACP 来自 Coder 外部 SDK、PostgreSQL 支持、Huma OpenAPI 框架
4. **GH-INTERNAL-AGENT** (L2): agent 包源码 - 确认 CLI agents 与 ACP agents 双轨并行架构
5. **GH-INTERNAL-WORKTREE** (L2): worktree.go - 确认沙箱是 git worktree 隔离，非容器化
6. **GH-CONFIG** (L2): config.go - 确认 beads 是 hook type，非深度集成
7. **CODER-ACP-SDK** (L2): Coder acp-go-sdk 仓库 - 确认 ACP 是外部标准
8. **GH-INTERNAL-STORAGE** (L2): storage 包 - 确认 SQLite + PostgreSQL 双后端
9. **GH-INTERNAL-DAEMON** (L2): daemon 包 - 确认 HTTP + Unix socket + systemd socket activation
10. **GH-CMD-REFINE** (L2): refine.go - 确认 --max-iterations 默认为 10

## 对基线 artifact 的修正

| 基线主张 | 回源验证结果 | 修正 |
|----------|-------------|------|
| ACP 是 RoboRev 内部协议 | go.mod 使用 `github.com/coder/acp-go-sdk v0.6.3` | **修正**：ACP 是 Coder 的外部 SDK/协议 |
| beads 集成不存在 | README 和 HookConfig.Type 均有 beads 引用 | **修正**：beads 是存在的 hook type 集成 |
| 沙箱实现不确定 | worktree.go 确认是 git worktree 隔离 | **已解决**：git worktree add --detach |
| refine 终止条件不确定 | refine.go 确认 --max-iterations 默认 10 | **已解决**：可通过 --max-iterations 配置 |
| CLI agent 是否迁移到 ACP 不确定 | agent 目录中 CLI agent 文件与 ACP 文件并存 | **已解决**：双轨并行，CLI agent 未迁移 |
| 仅 SQLite 存储 | storage/ 含 postgres.go 和 PostgreSQL 迁移 schema | **修正**：已支持 PostgreSQL |

## 证据缺口

1. **完整的早期 commit 历史**：GitHub API 只能获取到 2026-01-09 的 commits（项目首次公开），无法确认 2026-01-05（repo 创建日）到 01-09 之间是否有私有开发。结论：初始架构可能在私有开发中完成，开源时一次性发布。
2. **ACP 协议完整规范**：acp-go-sdk 的具体 JSON-RPC 方法定义需要查看 Coder SDK 源码，当前只确认了 RoboRev 侧的使用方式。
3. **PostgreSQL 引入时间**：无法从 release notes 中精确定位 PostgreSQL 支持是在哪个版本引入的（release notes 未明确提及）。

## 待确认问题

| 问题 | 状态 | 说明 |
|------|------|------|
| ACP 是内部协议还是外部标准 | **已解决** | ACP 是 Coder 的外部 SDK/协议，非 RoboRev 内部发明 |
| beads 集成是否存在 | **已解决** | beads 是存在的 hook type 集成，README 有提及，HookConfig 支持 |
| 沙箱具体实现 | **已解决** | git worktree 隔离，非容器化 |
| refine 终止条件 | **已解决** | --max-iterations 默认 10，可配置 |
| CLI agent 迁移状态 | **已解决** | CLI agents 与 ACP agents 双轨并行 |
| PostgreSQL 支持 | **已解决** | storage/ 有 postgres.go 和迁移 schema |
