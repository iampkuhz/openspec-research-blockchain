# 01 Baseline Alignment

## 为什么先做基线对齐

multi-agent 最大的隐患不是角色不够，而是不同 agent 读到不同版本的“仓库真相”。

## 本轮优先修的漂移

| 漂移项 | 当前问题 | 本轮处理 |
|--------|----------|----------|
| `knowledge/topics` | 仍出现在 README、maintenance skills、rules 中 | 改为 `knowledge/analysis` / `knowledge/decisions` 主模型 |
| `dependencies.md` | 仍被一些 rules / commands 当作主线文件 | 改为依赖声明并入 `plan.md` |
| `evidence-matrix.md` | 仍被当作 change packet 必需文件 | 改为可选证据矩阵，主线以 `plan.md` / `draft.md` 表达 |
| `promote-canonical` skill 名称 | 与仓库现有 `build-artifact` 不一致 | 对齐到实际 skill 名称 |
| `topic / atom` 旧语义 | 与当前 artifact-only 长期模型冲突 | 只修关键执行面文件，不做全仓大扫除 |

## 修正顺序

1. 更新 `AGENTS.md` 与 `README.md`
2. 更新会被 workflow / commands 直接依赖的 rules
3. 更新 Claude 命令和 maintenance skills
4. 最后补 `.qoder/agents/` 骨架说明

## 本轮不做的清理

- 不逐个清扫所有历史 `topic/atom` 表述
- 不统一重写所有旧 change packet
- 不修改无关的 diagram / comparison 支线文件
