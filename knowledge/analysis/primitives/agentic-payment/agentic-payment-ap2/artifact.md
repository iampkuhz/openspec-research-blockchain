# AP2 (Agent Payment Authorization) Protocol - 分析框架

## 目录

- [关键术语](#关键术语)
- [AP2 的本质与表现形式](#ap2-的本质与表现形式)
- [核心概念](#核心概念)
- [生态映射](#生态映射)
- [7 层模型位置](#7-层模型位置)
- [能力边界](#能力边界)
- [相关协议关系](#相关协议关系)
- [参考资料](#参考资料)

---

## 关键术语

| 术语 | 定义 | 作用 |
|------|------|------|
| AP2 | Agent Payment Authorization Protocol，agentic payment 授权层概念模型 | 本研究的核心对象 |
| 策略引擎 (Policy Engine) | 授权策略决策逻辑，决定"谁可以在什么条件下执行什么操作" | AP2 核心组件 |
| 签名验证 (Signature Verification) | 验证请求签名有效性的机制 | AP2 基础组件 |
| 信任注册表 (Trust Registry) | 信任名单和凭证管理 | AP2 凭证组件 |
| 机器可执行策略 | 可由 agent 自动解析和执行的授权策略 | AP2 场景特殊需求 |
| 跨 agent 委托 | agent 将权限委托给其他 agent 的机制 | AP2 场景特殊需求 |
| [SIWE](../../account-abstraction/eip-4361-siwe/artifact.md) | Sign-In with Ethereum，EIP-4361 规范的身份认证协议 | AP2 依赖的身份认证下层 |
| [DID Auth](../../decentralized-identity/did-auth/artifact.md) | Decentralized Identity Authentication，W3C 去中心化身份认证 | AP2 可用的身份认证方式 |
| VC | Verifiable Credential，W3C 可验证凭证 | AP2 信任注册表可用的凭证类型 |
| [Authorization](../agentic-payment-acp/artifact.md) | 授权机制 | AP2 核心功能 |
| Trust Assumption | 信任假设 | 安全模型基础 |
| Signature Scheme | 签名方案 | 授权技术实现 |
| Credential Management | 凭证生命周期管理 | VC (Verifiable Credentials)、API Keys |

---

## AP2 的本质与表现形式

### AP2 是什么

| 维度 | 说明 |
|------|------|
| **它是什么** | 一套标准化的授权接口架构，定义了策略引擎的组件、接口和协议 |
| **表现形式** | 接口规范（API 定义）+ 策略语言（Policy Language）+ 参考实现 |
| **类比理解** | 类似 OAuth 2.0 定义授权框架，但 AP2 专注于 agent 场景的机器可执行策略 |
| **在 7 层模型中的位置** | L5: Trust / Authorization 层 |

### AP2 定义的核心接口

| 接口 | 职责 | 示例方法 |
|------|------|----------|
| **策略决策接口** | 接收授权请求，返回决策结果 | `Authorize(action, context, credentials) → Grant/Deny` |
| **签名验证接口** | 验证请求签名的有效性 | `VerifySignature(signature, message) → bool` |
| **信任查询接口** | 查询主体是否在信任名单中 | `IsTrusted(subject) → Allow/Deny` |
| **策略管理接口** | 创建、更新、撤销授权策略 | `CreatePolicy(condition, action, subject) → policy_id` |

### AP2 的核心组件

```
┌─────────────────────────────────────────────────────────┐
│                    AP2 Policy Engine                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────┐ │
│  │ Strategy Parser │  │ Decision Logic  │  │ Condition│ │
│  │  (策略解析器)   │  │  (决策逻辑)     │  │ Evaluator│ │
│  │                 │  │                 │  │(条件评估)│ │
│  └─────────────────┘  └─────────────────┘  └─────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │ Signature       │  │ Trust           │              │
│  │ Verifier        │  │ Registry        │              │
│  │ (签名验证器)    │  │ (信任注册表)    │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

### AP2 解决的核心问题

- agentic payment 场景的特殊授权需求（跨 agent 委托、机器可执行策略）
- 传统授权方案（SIWE, OAuth 2.0, DID Auth）无法直接满足的 agent 场景缺口
- 授权策略引擎的标准化设计模式

### AP2 不解决的问题（范围外）

- L4 层：商务谈判（由 X402/ACP 处理）
- L6 层：agent 发现（由 A2A 处理）
- L3 层：支付传输（由 MPP 处理）
- 具体钱包产品的实现细节

---

## 核心概念

### AP2 核心功能需求

| 功能 | 概念描述 | 实际生态对应 |
|------|----------|--------------|
| Policy Engine | 授权策略决策逻辑 | 智能合约权限检查、Paymaster 策略 |
| Signature Verification | 签名验证技术 | ECDSA、EdDSA、BLS 等签名方案 |
| Trust Registry | 信任名单和凭证管理 | 链上信誉合约、DID 文档 |
| Credential Management | 凭证生命周期管理 | VC (Verifiable Credentials)、API Keys |

---

## 生态映射

### 实际存在的 L5 层项目/机制

| 项目/协议 | 类型 | 状态 | 与 AP2 概念的关系 |
|-----------|------|------|------------------|
| **SIWE** (Sign-In with Ethereum) | 规范 | live (EIP-4361) | 钱包签名授权的标准实现 |
| **SIWX** (Sign-In with X) | 规范系列 | live | 扩展到其他链的签名授权 |
| **DID Auth** / **VC** | 规范 | live (W3C) | 去中心化身份和凭证验证 |
| **EIP-4337 Paymaster** | 规范 | live | 账户抽象中的授权策略 |
| **OAuth 2.0 / OIDC** | 规范 | live | Web2 授权协议的参考 |
| **Macaroon** | 规范 | live | 带权限的令牌系统 |

### 能力对标表

| AP2 概念能力 | SIWE | DID Auth | EIP-4337 Paymaster | OAuth 2.0 |
|--------------|------|----------|-------------------|-----------|
| Signature Verification | ✓ | ✓ | ✓ | ~ |
| Policy Engine | ~ | ~ | ✓ | ✓ |
| Trust Registry | - | ✓ | ~ | - |
| Credential Management | ~ | ✓ | ~ | ✓ |

**图例：** ✓ = 完整支持，~ = 部分支持，- = 不支持/不涉及

---

## 7 层模型位置

**L5: Trust / Authorization**

### 与上下层的关系

| 关系类型 | 相邻层 | 交互内容 |
|----------|--------|----------|
| **上游** | L6: A2A (Discovery) | 接收发现的 agent 信息，进行授权检查 |
| **下游** | L4: X402/ACP (Commerce) | 授权通过后进入商务谈判 |
| **平行** | 其他 L5 实现 | SIWE、DID Auth 等是替代或互补 |

### 7 层模型栈

```
L7: Autonomous Orchestration (编排调度)
         ↓
L6: A2A (Agent 发现和互操作)
         ↓
L5: AP2 (授权和信任验证) ← 本研究
         ↓
L4: X402/ACP (商务谈判)
         ↓
L3: MPP (支付传输)
         ↓
L2: Wallet/Account Execution
         ↓
L1: Asset Primitives & Settlement
```

---

## 能力边界

### AP2 能解决什么

| 能力 | 说明 | 协议原生 |
|------|------|----------|
| 授权策略定义 | 定义 machine-readable 授权策略 | ✓ (概念定义) |
| 策略决策 | 基于签名、信任、条件做出授权决策 | ✓ (概念定义) |
| 跨 agent 委托 | 定义 agent 间权限委托机制 | ✓ (概念定义) |
| 信任名单管理 | 管理可信 agent 和服务名单 | ✓ (概念定义) |

### AP2 不能解决什么

| 能力 | 说明 | 外部依赖 |
|------|------|----------|
| 身份认证 | 仅依赖 SIWE/DID Auth 等外部机制 | SIWE, DID Auth |
| 签名验证执行 | 仅调用外部 Signer | SIWE, DID Auth, 钱包 |
| 支付传输 | 不涉及传输和路由 | MPP |
| 商务谈判 | 不涉及价格和条款协商 | X402/ACP |
| 链上结算 | 不涉及链上执行 | 链协议/智能合约 |

---

## 相关协议关系

### AP2 与 SIWE 的关系

| 层面 | SIWE | AP2 | 关系 |
|------|------|-----|------|
| 定位 | EIP-4361 规范（身份认证） | 概念模型（授权策略） | AP2 依赖 SIWE 进行身份认证 |
| 核心能力 | 签名验证、身份绑定 | 授权策略决策 | SIWE 是 AP2 下层组件 |
| 范围 | Authentication only | Authorization | SIWE 范围外是 AP2 范围内 |

### AP2 与 DID Auth 的关系

| 层面 | DID Auth | AP2 | 关系 |
|------|----------|-----|------|
| 定位 | W3C DID Core + VC（身份和凭证） | 概念模型（授权策略） | AP2 使用 DID Auth 进行身份和凭证验证 |
| 核心能力 | DID 文档、VC 验证 | 授权策略决策 | DID Auth capabilityInvocation 是 AP2 参考 |
| 授权能力 | capabilityInvocation/Delegation（概念） | 机器可执行策略（具体） | AP2 扩展 DID Auth 授权语义 |

### AP2 与 EIP-4337 Paymaster 的关系

| 层面 | EIP-4337 Paymaster | AP2 | 关系 |
|------|-------------------|-----|------|
| 定位 | 账户抽象 gas 代付机制 | agentic payment 授权 | Paymaster 是 AP2 策略引擎参考实现 |
| 策略形式 | 链上合约代码 | 可执行策略凭证 | AP2 参考 Paymaster 的条件验证模式 |
| 验证对象 | UserOperation | Agent 授权请求 | 概念相似，对象不同 |

### 水平关系（与其他 L5 实现）

| 实现方案 | 与 AP2 概念的关系 | 状态 | 适用场景 |
|----------|-------------------|------|----------|
| SIWE | 签名验证参考实现 | live | 以太坊地址绑定场景 |
| DID Auth | 去中心化身份参考 | live | 跨链/跨平台身份 |
| EIP-4337 Paymaster | 策略引擎参考 | live | 智能合约钱包 |
| OAuth 2.0 | Web2 授权参考 | live | 传统 web 服务集成 |

**潜在关系：**
- **互补关系**：SIWE + DID Auth 可组合使用
- **场景选择**：不同场景选择不同的授权机制
- **演进的替代关系**：新技术可能替代旧方案

---

## 参考资料

| 来源 | 说明 |
|------|------|
| EIP-4361 (SIWE) | 以太坊签名身份认证规范 |
| EIP-4337 | 账户抽象规范，Paymaster 机制 |
| W3C DID Core | 去中心化身份标识规范 |
| W3C VC Data Model | 可验证凭证数据模型 |
| a16z Agentic Commerce 研究 | agent 支付商业化分析 |
| Farcaster Mini Apps | agent 应用生态实践 |

---
