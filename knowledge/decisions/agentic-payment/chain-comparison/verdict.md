> 状态：初始 verdict。故意保持条件性，不输出绝对排名。

# 结论

## 结论范围

这份 verdict 只回答“当前这个 `agentic-payment` 场景比较应如何开始”，不回答最终谁胜出。

## 当前可以成立的结论

- 当前候选集合很可能不是天然同层，必须先归一化后再比较。
- 如果场景重点是 EVM 侧的 smart account、sponsor 和可编程支付路径，那么 `Ethereum` / `Base` 应优先作为高预算对照组。
- `Solana` 值得作为不同账户模型与执行路径的对照对象，但需要独立底层研究支撑。
- `Tempo`、`Arc` 在对象边界尚未确认前，不应被写进确定性排名。

## 结论成立的前提

- 需要继续补候选对象的官方技术材料。
- 需要把 Base 与 Ethereum 的“继承能力”与“链侧特性”拆开。
- 需要补一个非 EVM 侧的底层 `primitive` 作为稳固对照。

## 不应过度推出的结论

- 不能直接把官方 blog 或生态宣传话术写成“适合 agentic payment”的确定结论。
- 不能把支付中间层或服务层对象与基础链对象放在完全同一个能力层上打分。

## 未决问题

- `Tempo`、`Arc` 的原生边界与证据等级。
- `agentic-payment` 场景对 settlement certainty 的最低要求。
- 各候选对象的 fee abstraction 是否真的能支撑持续自动化支付。

## 后续动作

- 创建更多 candidate-specific `primitive`
- 补充 `comparison-main-table` 与 `comparison-technical-table`
- 补充更高等级证据后再尝试给出更明确的 shortlist
