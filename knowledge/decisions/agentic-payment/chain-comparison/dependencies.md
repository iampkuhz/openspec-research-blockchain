> 状态：示范性依赖说明。

# 依赖关系

## 依赖范围

本 case 不重写 AA 底层研究，而是只抽取与 `agentic-payment` 直接相关的能力条件。

## 依赖表

| 依赖对象 | 层级 | 预算 | 抽取内容 | 为什么这个深度足够 | 不重复什么 |
| --- | --- | --- | --- | --- | --- |
| `knowledge/analysis/domains/account-abstraction/` | `domain` | `focused` | 术语边界、能力分层语言 | 需要统一语境，但不需要主题全景全文 | 不复制 domain 的全部问题地图 |
| `knowledge/analysis/primitives/eip-4337/` | `primitive` | `focused` | smart account、sponsor、execution entrypoint 相关条件 | 当前只抽取与支付自动化直接相关的部分 | 不复制完整流程细节 |
| `knowledge/analysis/synthesis/aa-eip-evolution/` | `synthesis` | `focused` | AA 路线分层框架 | 需要避免错层比较 | 不复制全部演进叙事 |
| `future primitive: solana-payment-capabilities` | `primitive` | `focused` | 账户模型、fee payer、program execution 相关条件 | 对照组需要机制级支撑 | 当前尚未建档，先保留为待办 |

## 复用说明

- `artifact.md` 只引用当前场景真正需要的能力条件。
- `verdict.md` 只引用那些已经有足够证据支撑的抽取结果。

## 缺口

- 非 EVM 侧的底层 `primitive` 研究还不够，会限制最终比较深度。
