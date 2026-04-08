# Harness Agents

这里定义执行层的 agent roster 与 contract。

- `OpenSpec` 负责正式规则
- `Harness workflows` 负责阶段编排
- `Harness agents` 负责角色边界、输入输出、handoff 与禁止行为

当 workflow 支持 multi-agent 执行时，应优先读取：

1. `harness/agents/_index.yaml`
2. 对应 agent 的 contract 文档
3. 相关 workflow

如果运行环境不支持真实 subagent，也应按相同 contract 串行执行。
