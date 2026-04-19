> 状态：初始 decision artifact（由 `reference.md`、`criteria.md`、`dependencies.md` 合并修复 output contract）。

# Agentic Payment 链候选比较

## 场景定义

目标场景：一个 agent 或自动化系统需要在明确策略边界内持续执行支付动作，并且系统方需要知道哪些能力是链原生、哪些依赖钱包 / SDK / 第三方支付层。

## 关键术语

- 术语：`Agentic Payment`
  - 一句话定义：由 agent 或自动化系统在既定策略、预算或授权边界内执行的支付行为。
  - 在本题中的作用：它决定了本案例不是泛支付比较，而是"自动化且受约束"的支付比较。
- 术语：`Spend Policy`
  - 一句话定义：对支付对象、金额、频率、条件等做机器可执行约束的策略。
  - 在本题中的作用：是判断"可编程授权"是否真正成立的关键。
- 术语：`Fee Abstraction`
  - 一句话定义：让支付者不必严格按默认 gas / fee 模式承担成本的能力集合。
  - 在本题中的作用：直接影响 agentic payment 的 UX 和集成复杂度。
- 术语：`Settlement Certainty`
  - 一句话定义：支付被视为"足够完成"所需的确认与最终性条件。
  - 在本题中的作用：它决定系统是否适合自动化执行闭环。
- 术语：`Integration Surface`
  - 一句话定义：开发者接入某候选对象时实际面对的 SDK、API、钱包、节点与基础设施接口集合。
  - 在本题中的作用：很多"理论可行"方案最后卡在这个层面。

## 能力层拆解

在当前场景下，至少要拆成以下能力层：

1. 授权层：代理或程序能否在受约束条件下发起支付。
2. 执行层：支付动作如何被构造、验证、提交和结算。
3. fee 层：gas / fee 能否被抽象、代付或策略化处理。
4. 集成层：SDK、API、钱包或基础设施是否让开发者能稳定接入。

如果候选对象并不都覆盖这四层，就不应被直接写进同一排名表。

## 设计原因

为什么要先处理"候选是否同层"这个问题？

- 因为 `Ethereum`、`Base`、`Solana` 更像基础链或执行环境候选。
- `Tempo`、`Arc` 可能更接近协议栈、支付轨道或服务层候选。

如果不先拆层，后续结论就会把协议原生能力、官方生态能力、第三方服务封装混写为同一个"平台能力"。

## 决策标准

### 硬条件

| 标准 | 为什么是硬条件 | 如何验证 | 当前状态 |
| --- | --- | --- | --- |
| 受约束授权能力 | 没有它就无法安全地让 agent 自主支付 | 查官方规范、账户模型、授权机制 | partial |
| 可验证的执行与结算路径 | 没有它就无法把支付接入业务闭环 | 查交易 / program / smart account 执行路径 | partial |
| 明确的 fee handling 方案 | 没有它，agent 体验与成本不可控 | 查原生费用模型与 sponsor 路径 | partial |
| 可接入的开发接口 | 没有稳定接口，理论能力难以落地 | 查官方 SDK / API / repo | partial |

### 软偏好

| 标准 | 为什么重要 | 如何比较 | 当前状态 |
| --- | --- | --- | --- |
| 对自动化工作流友好 | 降低编排复杂度 | 看是否有成熟 account / policy / automation patterns | unclear |
| 生态配套完整度 | 影响落地速度 | 看官方生态与可靠 infra | unclear |
| EVM 兼容或迁移便利度 | 影响现有团队接入成本 | 看账户与工具链迁移成本 | partial |

### 待决问题

| 问题 | 为什么阻断判断 | 需要补什么证据 |
| --- | --- | --- |
| `Tempo` 到底是链、协议还是服务层对象？ | 不同层对象不可直接同表排名 | 官方技术文档与产品边界说明 |
| `Arc` 的原生能力边界是什么？ | 无法判断哪些结论属于官方或第三方封装 | 官方 docs / repo / API |
| `Base` 相对 `Ethereum` 的差异应落在哪些维度？ | 否则容易重复计分或误判"继承能力" | 官方 chain docs 与 AA 支持资料 |

## 依赖关系

本 case 不重写 AA 底层研究，而是只抽取与 `agentic-payment` 直接相关的能力条件。

| 依赖对象 | 层级 | 预算 | 抽取内容 | 为什么这个深度足够 | 不重复什么 |
| --- | --- | --- | --- | --- | --- |
| `knowledge/analysis/domains/account-abstraction/` | `domain` | `focused` | 术语边界、能力分层语言 | 需要统一语境，但不需要主题全景全文 | 不复制 domain 的全部问题地图 |
| `knowledge/analysis/primitives/eip-4337/` | `primitive` | `focused` | smart account、sponsor、execution entrypoint 相关条件 | 当前只抽取与支付自动化直接相关的部分 | 不复制完整流程细节 |
| `knowledge/analysis/synthesis/aa-eip-evolution/` | `synthesis` | `focused` | AA 路线分层框架 | 需要避免错层比较 | 不复制全部演进叙事 |
| `future primitive: solana-payment-capabilities` | `primitive` | `focused` | 账户模型、fee payer、program execution 相关条件 | 对照组需要机制级支撑 | 当前尚未建档，先保留为待办 |

## 边界与前提

当前这个 case 还不能做绝对排名，至少有三个原因：

- 候选集合的对象层次尚未完全归一。
- `Tempo` 与 `Arc` 的官方技术边界仍需直接核对。
- `Ethereum` / `Base` / `Solana` 的比较还需要更多场景特定证据，而不是泛链印象。

## 当前可确认与待确认项

### 当前可确认

- 这是一个必须以场景标准驱动的比较问题。
- 候选对象很可能不是天然同层，需要先归一化。

### 待确认

- `Tempo`、`Arc` 的对象边界与原生能力定义。
- 各候选在自动化支付、策略约束和 fee abstraction 上的直接官方证据。

## 与相邻对象的关系

- 该 case 依赖 `EIP-4337` 这类底层研究来判断 EVM 侧可编程支付能力。
- 该 case 依赖 `aa-eip-evolution` 来避免在 AA 相关能力上错层比较。

## 价值与影响

即使当前不输出最终排名，这个 case 依然有价值，因为它先把真正应比较的能力维度锁定下来：

- 能否做受约束授权
- 能否可靠执行与结算
- 能否合理处理 fee 和 sponsor
- 开发者是否真的可接入
