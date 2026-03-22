> 状态：示范性 glossary 卡，后续应继续补充。

# 术语卡

## 术语：UserOperation

- 一句话定义： `EIP-4337` 中提交给 `bundler` 的操作对象，而不是链原生 transaction。
- 在本题中的作用： 它帮助说明 4337 为什么能在不直接改动共识路径的情况下组织账户逻辑。
- 易混淆概念： transaction、meta-transaction。
- 最小例子： 用户签名后提交 `UserOperation`，最终由 `bundler` 打包进入 `EntryPoint`。

## 术语：Bundler

- 一句话定义： 收集、筛选、模拟并打包 `UserOperation` 的角色。
- 在本题中的作用： 它是 4337 流程里的关键中介。
- 易混淆概念： sequencer、block builder。
- 最小例子： bundler 先决定哪些 `UserOperation` 能进入本次打包。

## 术语：EntryPoint

- 一句话定义： 4337 流程中的统一入口合约，用于组织验证与执行。
- 在本题中的作用： 它是理解 4337 边界和角色分工的核心对象。
- 易混淆概念： 普通钱包合约、协议共识层入口。
- 最小例子： 打包后的调用通过 `EntryPoint` 统一进入账户验证逻辑。

## 术语：Paymaster

- 一句话定义： 在 4337 语境中，为用户操作承担 gas 支付或支付规则判断的一类角色。
- 在本题中的作用： 它直接关系到“gas abstraction 到底属于哪一层”的判断。
- 易混淆概念： 链原生 fee market、任意 sponsor 服务。
- 最小例子： 某个 app 只赞助特定 `UserOperation` 类型的 gas。

## 术语：Alt Mempool

- 一句话定义： 相对链原生 transaction mempool 而言，面向 `UserOperation` 的独立收集与传播路径。
- 在本题中的作用： 它帮助解释 4337 为什么不等同于“修改原有交易池规则”。
- 易混淆概念： 链原生 mempool、任意 off-chain queue。
- 最小例子： `UserOperation` 先进入特定的收集路径，再由 bundler 处理。
