# 依赖关系

| 依赖对象 | 层级 | 预算 | 强度 | 抽取内容 | 为什么这个深度足够 | 不重复什么 |
| --- | --- | --- | --- | --- | --- | --- |
| `knowledge/analysis/primitives/eip-4337/` | `primitive` | `deep` | `hard` | `UserOperation`、`EntryPoint`、`paymaster` 等关键边界 | 它是 AA 主题的机制锚点 | 不复制完整流程细节 |
| `knowledge/analysis/synthesis/aa-eip-evolution/` | `synthesis` | `focused` | `medium` | AA 相关对象的关系、演进与分层框架 | 主题地图只需稳定的分层语言 | 不复制全部演进叙事 |
