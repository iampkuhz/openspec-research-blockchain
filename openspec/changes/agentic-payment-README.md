# Agentic Payment 研究索引

本目录索引 Agentic Payment 7 层模型相关的完整研究。

## 研究概览

**研究对象：** Agentic Payment 协议栈

**核心框架：** 7 层模型

```
L7: Autonomous Orchestration
L6: Agent Discovery & Interop     ← A2A
L5: Trust / Authorization         ← AP2
L4: Commerce Negotiation          ← X402, ACP
L3: Machine Payment Transport     ← MPP
L2: Wallet / Account Execution
L1: Asset Primitives & Settlement
```

## 研究成果

### Primitive 分析（5 个）

| 协议 | 层 | 路径 |
|------|-----|------|
| A2A | L6 | [knowledge/analysis/primitives/agentic-payment-a2a/artifact.md](../../knowledge/analysis/primitives/agentic-payment-a2a/artifact.md) |
| AP2 | L5 | [knowledge/analysis/primitives/agentic-payment-ap2/artifact.md](../../knowledge/analysis/primitives/agentic-payment-ap2/artifact.md) |
| MPP | L3 | [knowledge/analysis/primitives/agentic-payment-mpp/artifact.md](../../knowledge/analysis/primitives/agentic-payment-mpp/artifact.md) |
| X402 | L4 | [knowledge/analysis/primitives/agentic-payment-x402/artifact.md](../../knowledge/analysis/primitives/agentic-payment-x402/artifact.md) |
| ACP | L4 | [knowledge/analysis/primitives/agentic-payment-acp/artifact.md](../../knowledge/analysis/primitives/agentic-payment-acp/artifact.md) |

### Synthesis 分析（1 个）

| 主题 | 路径 |
|------|------|
| 7 层模型综合分析 | [knowledge/analysis/synthesis/agentic-payment-7layer/artifact.md](../../knowledge/analysis/synthesis/agentic-payment-7layer/artifact.md) |

## Change 目录

过程文件位于：

- `openspec/changes/agentic-payment-a2a/`
- `openspec/changes/agentic-payment-ap2/`
- `openspec/changes/agentic-payment-mpp/`
- `openspec/changes/agentic-payment-x402/`
- `openspec/changes/agentic-payment-acp/`
- `openspec/changes/agentic-payment-7layer/`

## 快速导航

**典型支付流：**

```
A2A (发现) → AP2 (授权) → X402/ACP (谈判) → MPP (传输) → L2/L1 (执行)
```

**L4 层双协议关系：**

| 维度 | X402 | ACP |
|------|------|-----|
| 基础 | HTTP 402 | 独立协议 |
| 复杂度 | 轻量级 | 重量级 |
| 适用场景 | 简单支付请求 | 复杂商务谈判 |

## Evidence Gap

所有协议均为 2025-2026 emergent 概念，官方规范来源待确认。

当前分析基于：
- 用户提供的 7 层模型框架
- 协议名称和位置的一般性推断
- 支付系统架构的通用知识

需要进一步验证：
- 各协议的官方规范来源
- X402 与 ACP 的精确定义和关系
- 各协议的实现进度和状态
