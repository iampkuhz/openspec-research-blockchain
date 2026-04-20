---
object_type: decision
domain_id: ai-code-review
title: "AI Code Review 分阶段落地决策 - 最终推荐"
research_type: scenario
updated_at: 2026-04-20
change_id: cr-decision-ai-coding-review-decision-refresh
baseline_change_id: ai-coding-review-decision
---

## 最终推荐

采用 **"Qodo Merge 起步 → CodeRabbit 增强 → RoboRev 补层 → Self-hosted 收敛"** 的四阶段方案。

| 阶段 | 时间 | 核心动作 | 主力工具 |
|------|------|----------|----------|
| Phase 1 | 1-2 个月 | LLM-Enabled PR Review 基础部署，建立 review 质量基线 | Qodo Merge 开源版 + cloud LLM API |
| Phase 2 | 3-6 个月 | Context-Aware + Learning 增强，集成 SAST 确定性基线 | CodeRabbit Pro（默认）/ Qodo Merge Pro（备选） |
| Phase 3 | 6-9 个月 | Multi-Layer Review 覆盖，引入 commit 级审查 + fix/refine 闭环 | RoboRev + 可选 Open Code Review discourse |
| Phase 4 | 9-12 个月+ | Self-hosted LLM 部署，data isolation 终极收敛 | Self-hosted LLM（Ollama/vLLM） |

## 核心决策理由

1. **Phase 1 选 Qodo Merge**：5 种部署方式 + 6 大 Git 平台 + 多模型路由 = 最大部署灵活性，适合快速验证
2. **Phase 2 默认选 CodeRabbit Pro**：Living Memory learnings 系统 + 5-agent 并行 = 最强 Context Engineering 能力，符合"低维护成本"soft preference
3. **Phase 3 引入 RoboRev**：commit 级审查与 PR 级工具正交互补，fix/refine 闭环覆盖 AI agent 产出物场景
4. **Phase 4 Self-hosted**：解决 data isolation hard constraint 的终极合规路径

## 关键前提条件

- **UQ-1（最高优先级）**：Phase 1 即确认 data isolation 合规边界——代码经 cloud LLM API 传输但声称不存储是否可接受。若不可接受，直接切换至 Phase 4 路线
- **Phase 1 触发 Phase 2**：pilot ≥ 20 个 PR，review 接受率 ≥ 50%，平均反馈时间 ≤ 5 分钟
- **Phase 4 前提**：GPU 基础设施就绪，≥ 500 个 PR review 数据积累，1-2 名 dedicated engineering 资源

## 核心风险（High Severity）

| 风险 | 缓解措施 |
|------|----------|
| Data isolation 合规解释冲突 | Phase 1 即确认；如不可接受，直接切换 self-hosted 路线 |
| Solidity 深度安全审查覆盖不足 | Phase 1 集成 Slither；Phase 2 对核心合约引入 Certora/Manticore |
| LLM review 准确率不达预期 | "建议模式"起步；review quality metric 持续跟踪 |

## 与 Baseline 决策的关系

本 decision 为 `knowledge/decisions/ai-coding-review-decision`（change ID: `ai-coding-review-decision`）的刷新版本。保持一致：Static+AI 基线思想、渐进式建设节奏、Self-hosted 长期目标。新增：具体产品选型、commit 级审查层、阶段触发/退出标准。

## 证据等级

全证据链为 L4（基线推断），无 L1/L2 直接验证。建议后续安排 source-evidence-agent 回源关键 L1/L2 来源。
