# Evidence Policy

## 证据等级

| 等级 | 类型 | 可信度 | 用途 |
|---|---|---|---|
| L1 | 官方规范/EIP/白皮书 | 最高 | 核心技术主张 |
| L2 | 参考实现/官方文档 | 高 | 技术主张支持 |
| L3 | 官方博客/Release notes | 中 | 背景/动机 |
| L4 | 第三方分析/社区讨论 | 低 | 社区观点参考 |

## 主张约束

- 核心技术主张必须有 L1 或 L2 支撑
- L3/L4 支撑的主张必须标注低置信度
- 无来源支撑的新主张不得写入 draft
- 证据不足时必须明确写不确定性

## 来源验证

- 每个来源必须尝试访问验证
- 无法验证时标注原因
- 来源冲突时优先采信 L1/L2

## 与 traceability 的关系

- Evidence policy 定义证据等级
- Traceability rules 定义 claim → source 的追溯机制
- 两者配合使用：traceability 确保每个 claim 有 source，evidence 确保 source 等级适当
