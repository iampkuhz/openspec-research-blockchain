# Qoder Agents Skeleton

该目录当前仅保留第一版 multi-agent 升级的骨架说明。

本轮不在这里定义完整 runtime contract。  
当前真源位于：

- `harness/agents/_index.yaml`
- `harness/agents/*.md`

后续如需补齐 Qoder 侧 agent 运行时格式，应遵循以下顺序：

1. 保持 OpenSpec / Harness 边界不变
2. 优先复用 `harness/agents/` 中的角色定义
3. 仅在 Qoder 运行时确有额外字段时新增映射层
