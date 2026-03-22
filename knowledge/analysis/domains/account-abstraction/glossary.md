> 状态：示范性 glossary 卡。后续应继续扩充。

# 术语卡

## 术语：Account Abstraction

- 一句话定义： 一个主题性目标，关注账户表达、授权、验证和执行入口如何从传统 EOA 模式中解耦。
- 在本题中的作用： 它是当前 domain 的总入口，不等同于某一个 EIP。
- 易混淆概念： `EIP-4337`、smart wallet、delegation。
- 最小例子： “研究 AA” 不等于 “只研究 4337”，还可能涉及授权模型、gas 代付和执行路径。

## 术语：EOA

- 一句话定义： Externally Owned Account，传统由私钥直接控制的账户模型。
- 在本题中的作用： 是多数 AA 讨论的参照系。
- 易混淆概念： smart contract account。
- 最小例子： 用户直接签名并发送链原生交易，是典型 EOA 路径。

## 术语：Smart Contract Account

- 一句话定义： 由合约逻辑定义验证和执行规则的账户。
- 在本题中的作用： 很多 AA 路线都希望把账户能力转移到可编程逻辑中。
- 易混淆概念： 普通钱包合约、托管账户。
- 最小例子： 账户可以定义多签、session key 或自定义验证策略。

## 术语：UserOperation

- 一句话定义： `EIP-4337` 语境下，由用户提交给 bundler 的操作对象，而不是链原生交易。
- 在本题中的作用： 它帮助区分“用户请求对象”和“最终上链交易对象”。
- 易混淆概念： transaction、meta-transaction。
- 最小例子： 用户发送 `UserOperation`，bundler 打包后由 `EntryPoint` 执行。

## 术语：Paymaster

- 一句话定义： 在 `EIP-4337` 语境中，为某些操作承担 gas 支付或支付策略判断的角色。
- 在本题中的作用： 它对应 AA 里最容易被高估或误写的一类能力。
- 易混淆概念： 协议原生 gas abstraction。
- 最小例子： 某个 app sponsor 用户操作的 gas，并不等于链原生支持任意 sponsor 模式。
