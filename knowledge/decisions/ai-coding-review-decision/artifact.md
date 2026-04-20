---
object_type: decision
domain_id: ai-code-review
title: "区块链 + Java 后端场景 AI Code Review 分阶段落地决策"
research_type: scenario
research_depth: scenario
updated_at: 2026-04-20
change_id: cr-decision-ai-coding-review-decision-refresh
baseline_change_id: ai-coding-review-decision
---

<!-- 目录 -->
- [关键术语表](#关键术语表)
- [场景定义](#场景定义)
- [决策标准](#决策标准)
- [候选方案评估](#候选方案评估)
- [对比矩阵](#对比矩阵)
- [分阶段推荐方案](#分阶段推荐方案)
  - [Phase 1：LLM-Enabled PR Review 基础](#phase-1llm-enabled-pr-review-基础第-1-2-个月)
  - [Phase 2：Context-Aware + Learning 增强](#phase-2context-aware--learning-增强第-3-6-个月)
  - [Phase 3：Multi-Layer Review 覆盖](#phase-3multi-layer-review-覆盖第-6-9-个月)
  - [Phase 4：Self-Hosted LLM / 数据隔离收敛](#phase-4self-hosted-llm--数据隔离收敛第-9-12-个月)
- [推荐方案与理由](#推荐方案与理由)
- [风险矩阵与替代方案](#风险矩阵与替代方案)
- [未决问题](#未决问题)
- [证据等级说明](#证据等级说明)

## 关键术语表

| 术语 | 定义 | 来源 |
|------|------|------|
| Context Engineering | 从多来源组装正确信息、以正确结构在正确时机提供给模型的过程 | CodeRabbit primitive |
| Agentic Code Review | LLM 通过工具调用主动探索代码库、执行代码、验证假设的多轮审查 | AsyncReview primitive |
| Hybrid AI Pipeline | 确定性 pipeline 为主干、在关键环节嵌入 agentic loop 的架构 | CodeRabbit primitive |
| Discourse | 多 reviewer 之间的程序化交叉验证（AGREE/CHALLENGE/CONNECT/SURFACE） | Open Code Review primitive |
| Fix/Refine Loop | 发现问题后自动调用 fix agent 生成补丁并循环重审 | RoboRev primitive |
| ACP（Agent Client Protocol）| RoboRev 内部的 JSON-RPC 协议，统一 agent 后端接入 | RoboRev primitive |
| PR Compression Strategy | 处理超大 PR 的 token-aware diff 拟合、文件优先级排序、分块审查策略 | Qodo Merge primitive |
| RLM（Recursive Language Models）| DSPy 框架中的递归语言模型执行模式，支持多轮有状态推理循环 | AsyncReview primitive |
| Living Memory | 从 PR 对话、issue、code guidelines 中持续学习团队 review 偏好并持久化 | CodeRabbit primitive |
| Data Isolation | 本场景的 hard constraint：代码不流出内部网络 | request.md |

## 场景定义

### 场景描述

"区块链 + Java 后端"团队需要在未来 12 个月内分阶段引入 AI code review 能力，服务于内部多项目的 PR 审查流程。团队技术栈覆盖 Solidity 智能合约、链下服务、Java/JVM/Spring 后端。

### 场景约束

**Hard Constraints**：
- **数据隔离**：代码不流出内部网络（与 cloud LLM API 存在直接冲突，详见风险矩阵）
- **Solidity 为首要区块链语言**：需覆盖智能合约安全审查
- **Java/JVM/Spring 覆盖**：需支持 Java 生态的代码审查
- **PR/MR 集成**：需与现有 Git 平台的 PR/MR 流程集成
- **可扩展自定义规则**：支持团队自建领域规则

**Soft Preferences**：
- review 反馈在 5 分钟内
- 低维护成本
- 渐进式采用

### 排除范围

- 不覆盖前端 / 全栈场景
- 不生成详细的实施计划或预算

### 开放问题

1. Data isolation 约束是否允许通过 cloud LLM API 调用（代码以 API 请求方式传输至第三方，但声称不存储/不训练）
2. 团队是否有 dedicated GPU 资源用于 self-hosted LLM
3. 当前 PR 频率和代码库规模的具体数字

## 决策标准

本决策采用 5 项标准，详见 `decision-criteria.md`。以下为权重摘要：

| 标准 | 权重 | 核心判定条件 |
|------|------|-------------|
| 场景匹配度 | 25% | 对 Solidity + Java + PR/MR 的适配度 |
| 部署灵活性与数据隔离 | 25% | 是否支持自托管，以及 data isolation 合规程度 |
| 能力深度 | 20% | 上下文获取、结构化输出、协作审查、反馈学习 |
| 成本与运维负担 | 15% | 直接使用成本和运维复杂度 |
| 合规与安全风险 | 15% | 数据出境、代码外发、供应商锁定风险 |

## 候选方案评估

以下评估全部从 synthesis draft 和对应 primitive artifact 中提取，不得独立推断。

**未纳入独立候选的 primitive 说明**：
- `chatgpt-codereview-framework`: 在 synthesis 中定位为 LLM 能力供给层，非独立 review 产品，已融入各方案的 LLM 后端分析中。
- `supplementary-frameworks`: 在 synthesis 中定位为长尾生态位，Star 规模小且能力已被头部方案覆盖，未作为独立候选。

### 方案 A：CodeRabbit（开源版 + Pro）

**对应 primitive**：`coderabbit-framework`
**架构模式**：Hybrid AI Pipeline → Coordinated Multi-Agent

| 决策标准 | 判定 | 证据 |
|----------|------|------|
| 场景匹配度 | Partial | synthesis 场景评估中区块链场景 ★★★★☆（Solidity 语义理解最好）、后端场景 ★★★★☆、Java 场景 ★★★☆☆。集成 40+ 静态分析工具可补充确定性检查 [SRC: synthesis draft 场景评估] |
| 部署灵活性 | Partial | 开源版（ai-pr-reviewer）为 GitHub Action，可自托管但需自备 OpenAI API key，代码仍需发送至 OpenAI [SRC: coderabbit primitive 开源版组件]。Pro 版为 SaaS，代码经过 CodeRabbit 服务器 [SRC: coderabbit primitive 信任边界图] |
| 能力深度 | Confirmed | 能力矩阵中上下文获取 ★★★★☆（仓库级索引 + context curation）、协作审查 ★★★★★（5 专业化 agent 并行）、反馈学习 ★★★★★（Living Memory + learnings）[SRC: synthesis draft 能力矩阵] |
| 成本与运维 | Partial | 开源版零订阅费但需自备 LLM API key；Pro 版定价不透明 [SRC: coderabbit primitive 证据缺口] |
| 合规风险 | Unclear | Pro 版代码经过第三方服务器，官方声称不用于 LLM 训练但无法技术验证 [SRC: coderabbit primitive FAQ] |

**优势**：Context Engineering 体系成熟（8 来源 context + context curation），5-agent 并行覆盖 PR review 全生命周期，learnings 系统支持团队偏好持续学习，集成 40+ 静态分析工具提供确定性基线。
**失败条件**：若 data isolation 被确认为不可妥协（代码经任何第三方即违规），则 CodeRabbit Pro 不可用；开源版受限于 GitHub 平台，不支持 GitLab/Bitbucket。

### 方案 B：Qodo Merge（开源版 + Pro）

**对应 primitive**：`qodo-merge-evolution`
**架构模式**：RAG + 多模型 → 平台化治理

| 决策标准 | 判定 | 证据 |
|----------|------|------|
| 场景匹配度 | Partial | synthesis 场景评估中区块链场景 ★★★☆☆（通过 path_instructions 可为 .sol 配置专门指令）、后端场景 ★★★★☆（6 平台覆盖 + PR Compression 适合大型后端项目）、Java 场景 ★★★☆☆ [SRC: synthesis draft 场景评估] |
| 部署灵活性 | Confirmed | 开源版（pr-agent）支持 GitHub Action、CLI、Webhook、Docker、GitHub App 五种部署方式，用户自备 LLM API key，可配置任意 LLM 后端 [SRC: qodo-merge primitive 部署灵活性] |
| 能力深度 | Confirmed | 能力矩阵中上下文获取 ★★★★☆（RAG + 动态上下文扩展）、多模型支持 ★★★★★（OpenAI/Claude/Gemini/Bedrock）、平台覆盖 ★★★★★（6 大平台）[SRC: synthesis draft 能力矩阵] |
| 成本与运维 | Confirmed | 开源版零订阅费，用户自备 API key，TOML 配置体系适合企业级定制。RAG（LanceDB）当前状态不确定 [SRC: qodo-merge primitive 能力边界] |
| 合规风险 | Partial | 代码发送至用户自配的 LLM API（如 OpenAI），但不由 Qodo 持有；可通过选择合规 LLM provider（如 Azure OpenAI with zero data retention）缓解 [SRC: qodo-merge primitive LLM 后端路由层] |

**优势**：Git Provider 抽象层支持 6 大 Git 平台，多模型路由避免供应商锁定，PR Compression Strategy 可处理超大 PR，TOML 配置体系支持企业级定制，开源版完全可审计。
**失败条件**：RAG 能力（LanceDB）当前状态不确定，可能在后续版本中已降级维护；无类似 CodeRabbit 的 learnings 系统，团队偏好学习需通过手动更新配置实现。

### 方案 C：AsyncReview

**对应 primitive**：`asyncreview-evolution`
**架构模式**：Agentic RLM 工具循环

| 决策标准 | 判定 | 证据 |
|----------|------|------|
| 场景匹配度 | Unclear | synthesis 场景评估中区块链场景 ★★☆☆☆、后端场景 ★★★☆☆、Java 场景 ★★☆☆☆。无 Solidity/Java 专项优化 [SRC: synthesis draft 场景评估] |
| 部署灵活性 | Partial | 通过 npx CLI 一键运行，支持 GitHub PR 和本地文件夹（--path）两种模式。但仅支持 Gemini LLM 后端 [SRC: asyncreview primitive 设计取舍] |
| 能力深度 | Partial | 能力矩阵中上下文获取 ★★★★★（Agent 主动探索）、协作审查 ★★☆（单 RLM 循环）、反馈学习 ★☆☆（无）[SRC: synthesis draft 能力矩阵] |
| 成本与运维 | Partial | 开源零成本，但仅 Gemini 后端限制了模型选择灵活性 [SRC: asyncreview primitive 设计取舍] |
| 合规风险 | Unclear | 代码发送至 Google Gemini API，项目静止期（2026-03 以来无新推送）可能影响长期维护 [SRC: asyncreview primitive 不确定性] |

**优势**：RLM 递归循环可深入探索全仓库上下文，DSPy 框架原生 tools[] 架构简洁，可被 AI agent 作为 Skill 调用。
**失败条件**：项目静止期原因不明，阶段 4 能力（多平台扩展、深度代码理解）的 PR 均为 open 状态尚未合并；仅支持 Gemini 对 Java/Solidity 场景适配可能不足。

### 方案 D：RoboRev

**对应 primitive**：`roborev-evolution`
**架构模式**：Commit 级持续审查 + 修复闭环

| 决策标准 | 判定 | 证据 |
|----------|------|------|
| 场景匹配度 | Partial | synthesis 场景评估中区块链场景 ★★☆☆☆、后端场景 ★★★☆☆、Java 场景 ★★☆☆☆。无语言专属规则 [SRC: synthesis draft 场景评估] |
| 部署灵活性 | Confirmed | Go 单二进制部署，本地 post-commit hook + CI + webhook 三种触发方式，SQLite 零运维持久化，systemd 集成 [SRC: roborev primitive 能力边界] |
| 能力深度 | Partial | 能力矩阵中自动化程度 ★★★★★（post-commit 自动 + 修复闭环）、反馈学习 ★★★☆☆（fix/refine 闭环）、协作审查 ★★★☆☆（多 agent 后端）[SRC: synthesis draft 能力矩阵] |
| 成本与运维 | Confirmed | Go 单二进制、SQLite 持久化、systemd 管理，运维负担极低。用户自备 agent 后端 API key [SRC: roborev primitive 设计取舍] |
| 合规风险 | Partial | 代码发送至用户配置的 agent 后端（Codex/Claude/Gemini 等），风险取决于选用的 LLM [SRC: roborev primitive 实体分类] |

**优势**：commit 级持续审查可在 PR 之前最早拦截问题，fix/refine 闭环形成完整的"发现 → 修复 → 重审 → 自动关闭"质量保障链，ACP 协议统一 10+ agent 后端接入。
**失败条件**：定位为"AI agent 产出物审查"而非人类 PR 审查，不能替代 PR 级 review 工具；无 SaaS 托管模式，需自行部署。

### 方案 E：Open Code Review

**对应 primitive**：`open-code-review-framework`
**架构模式**：Multi-Agent Discourse 编排层

| 决策标准 | 判定 | 证据 |
|----------|------|------|
| 场景匹配度 | Unclear | synthesis 场景评估中区块链场景 ★★☆☆☆（无 Solidity/blockchain 专属 persona）、后端场景 ★★★☆☆、Java 场景 ★★★☆☆ [SRC: synthesis draft 场景评估] |
| 部署灵活性 | Confirmed | 完全开源（Apache 2.0），通过 Agent Skills 兼容 14 种 AI coding assistant，CLI + Dashboard 双通道，SQLite 状态管理 [SRC: OCR primitive 能力边界] |
| 能力深度 | Confirmed | 能力矩阵中上下文获取 ★★★★★（full agency 自主探索）、结构化输出 ★★★★★（4 种固定响应 + discourse）、协作审查 ★★★★★（28 persona + discourse）[SRC: synthesis draft 能力矩阵] |
| 成本与运维 | Partial | 开源零成本，但 8 阶段 workflow + discourse 的 token 消耗显著高于单次 LLM 调用 [SRC: OCR primitive 设计取舍] |
| 合规风险 | Partial | 代码不经过 OCR 系统，直接由 AI assistant 调用 LLM，风险取决于选用的 AI assistant 和 LLM provider [SRC: OCR primitive 信任边界] |

**优势**：8 阶段结构化 workflow 模拟真实工程团队协作审查，discourse 交叉验证减少 false positive，28 个 reviewer persona 覆盖多视角，filesystem-as-source-of-truth 状态模型可审计。
**失败条件**：无 Solidity/blockchain 专属 reviewer persona；discourse 机制增加额外 LLM 调用轮次，延迟显著增加；需在 AI assistant 内触发，非 CI 自动触发。

**不作为主力方案引入的理由**：Open Code Review 虽在协作审查能力维度评分最高，但其 discourse 机制导致 token 成本和延迟显著增加，且非 CI 自动触发的工作流与团队现有 PR/MR 流程集成度不足。因此在主推荐路线中仅作为 Phase 3 高风险 PR 的可选补充，不作为主力工具。

## 对比矩阵

| 维度 | A: CodeRabbit | B: Qodo Merge | C: AsyncReview | D: RoboRev | E: Open Code Review |
|------|--------------|--------------|---------------|-----------|-------------------|
| **场景匹配** | Partial ★★★★ | Partial ★★★ | Unclear ★★ | Partial ★★ | Unclear ★★ |
| **部署灵活** | Partial（开源可自托管，Pro 仅 SaaS） | Confirmed（5 种部署 + 多模型路由） | Partial（CLI + Skill，仅 Gemini） | Confirmed（Go 单二进制，多 agent） | Confirmed（Apache 2.0，14 种 assistant） |
| **能力深度** | Confirmed ★★★★★ | Confirmed ★★★★ | Partial ★★★ | Partial ★★★ | Confirmed ★★★★★ |
| **成本运维** | Partial（Pro 定价不明） | Confirmed（开源免费 + TOML） | Partial（仅 Gemini 受限） | Confirmed（Go + SQLite 轻量） | Partial（discourse 成本高） |
| **合规风险** | Unclear（Pro 代码过第三方） | Partial（可配合规 LLM） | Unclear（Gemini 依赖） | Partial（取决于 agent 后端） | Partial（取决于 assistant） |
| **Solidity 支持** | ★★★★（LLM 语义理解最佳） | ★★★（path_instructions 可定制） | ★★（无专项） | ★★（无专项） | ★★（无专属 persona） |
| **Java 支持** | ★★★（LLM 可审查） | ★★★（多模型可覆盖） | ★★（Gemini 对 Java 不如 GPT-4） | ★★（无专项） | ★★★（Principal 可做架构审查） |
| **Git 平台** | 3（GitHub/GitLab/Bitbucket） | 6（全覆盖） | 2（GitHub + 本地） | 本地 + CI | 通过 gh CLI |
| **审查粒度** | PR/MR 级 | PR/MR 级 | PR 级 + 本地 | Commit 级 | 会话级 + AI assistant 内 |
| **学习能力** | ★★★★★（Living Memory） | ★★☆（手动配置更新） | ★☆☆（无） | ★★★（fix/refine） | ★★☆（round 迭代） |
| **多 Agent** | ★★★★★（5 专业化） | ★★☆（工具链并行） | ★★☆（单 RLM） | ★★★（多 agent 后端） | ★★★★★（28 persona + discourse） |

## 分阶段推荐方案

基于上述评估，推荐采用 **"PR 级基础 → 上下文增强 → 多层覆盖 → 数据隔离收敛"** 的四阶段渐进式方案。每个阶段能力递增，不废弃前一阶段的能力。

### Phase 1：LLM-Enabled PR Review 基础（第 1-2 个月）

**本阶段升级什么能力**：
- 部署 Qodo Merge 开源版（pr-agent）作为主力 PR review 工具，接入 cloud LLM API（OpenAI GPT-4 或 Claude 3/4）
- 通过 TOML 配置为 Solidity（`.sol`）路径配置 path_instructions，注入智能合约审查指令
- 为 Java 项目配置 Spring/Hibernate 相关的 review 规则
- 可选并行部署 CodeRabbit 开源版（ai-pr-reviewer）用于 A/B 对比

**目标解决什么新问题**：
- 解决"人工 review 对语义层面问题（架构反模式、安全逻辑缺陷、业务一致性）覆盖不足"的问题
- 建立 LLM review 效果的基线度量（review 接受率、false positive 率、平均反馈时间）

**为什么在这个时点出现**：
- 这是满足"阶段一必须 LLM-based"约束的最小可行起点
- Qodo Merge 的 5 种部署方式 + 多模型路由提供了最大的部署灵活性，适合快速验证
- CodeRabbit 开源版可作为并行对照，确认哪款工具在团队代码库上表现更好
- 不应等待"完美方案"——baseline 证据表明所有成功的 AI review 工具都建立在快速验证迭代的基础上

**前提条件**：
- 确认 data isolation 约束的具体合规边界（代码经 cloud LLM API 传输但声称不存储是否可接受）
- 获取 LLM API key（建议同时申请 OpenAI 和 Anthropic 以利用 Qodo Merge 的多模型路由）
- 确定 1-2 个代表性项目作为 pilot（一个 Solidity 合约项目、一个 Java 后端项目）
- PR/MR 所在 Git 平台需为 Qodo Merge 支持的 6 大平台之一

**主要风险与失败模式**：
| 风险 | 严重程度 | 缓解 |
|------|----------|------|
| Data isolation 被解释为禁止任何代码外发 | High | Phase 1 即与法务/安全团队确认 cloud LLM API 调用的合规性；如不可接受，需在 Phase 2 直接转向 local LLM 路线 |
| LLM 在 Solidity 上的 false positive 率过高 | High | 通过 path_instructions 限定审查范围为代码风格 + 已知漏洞模式（重入、delegatecall），暂不做深度逻辑审查 |
| Qodo Merge 的 RAG（LanceDB）已降级 | Medium | Phase 1 不依赖 RAG 能力，仅使用 diff + Dynamic Context Expansion |
| 开发者对 AI review 的接受度低 | Medium | Phase 1 设为"建议模式"而非"阻断模式"，review 结果作为 human review 的补充参考 |

**进入下一阶段的触发条件**：
- Qodo Merge 在 pilot 项目上运行 ≥ 20 个 PR，review 接受率 ≥ 50%（即 half 以上的 AI findings 被 human reviewer 认为有价值）
- 平均反馈时间 ≤ 5 分钟（soft preference）
- Solidity path_instructions 配置已产生有效的 review findings（至少发现过 1 个真实问题）
- Data isolation 合规性已确认

**退出标准（转向替代方案）**：
- 若 Qodo Merge 在 pilot 上表现不佳（接受率 < 30%），切换到 CodeRabbit 开源版作为主力
- 若 data isolation 被确认为禁止任何代码外发，跳过 Phase 2，直接进入 Phase 4（Self-hosted LLM）

### Phase 2：Context-Aware + Learning 增强（第 3-6 个月）

**本阶段升级什么能力**：
- **默认推荐 CodeRabbit Pro**（若 data isolation 合规确认允许 SaaS）：利用 learnings 系统从 PR 对话中学习团队 review 偏好；利用 5-agent 并行（Review + Verification + Chat + Pre-Merge + Living Memory）
- **备选 Qodo Merge Pro**：若团队已有 Qodo Merge TOML 配置深度定制且不愿引入新 SaaS vendor，可使用其 RAG + 多模型路由 + PR Compression 能力
- 配置项目级 code guidelines（`.cursorrules`、`CLAUDE.md` 等）注入 AI review 上下文
- 集成 SAST 工具（Slither for Solidity、SonarQube for Java）作为 AI review 的确定性基线
- 建立 review quality metric dashboard，跟踪 AI review 的准确率、召回率趋势

**Phase 2 方案选择判定**：默认推荐 CodeRabbit Pro。理由是 CodeRabbit 的 learnings 系统（Living Memory）在本场景的"渐进式采用"和"低维护成本"soft preference下具有显著优势——团队 review 偏好可通过 PR 对话自动学习，无需手动更新 TOML 配置。若团队对 data isolation 合规仍有顾虑或希望避免额外 SaaS vendor，则选择 Qodo Merge Pro 作为备选，其多模型路由和 PR Compression 能力在大型后端项目中同样有效。

**目标解决什么新问题**：
- 解决"Phase 1 的 diff-only review 无法理解跨文件依赖和项目上下文"的问题
- 解决"AI review 风格与团队偏好不一致，需要反复人工纠正"的问题
- 解决"纯 LLM 缺乏确定性安全基线"的问题（通过 SAST 集成）

**为什么在这个时点出现**：
- Phase 1 已积累了足够的 PR review 数据来配置 learnings / 团队偏好
- 团队已验证 LLM review 的有效性，可以投入 SaaS 订阅费用
- 行业共性阶段框架表明，从"LLM 直连"到"上下文感知"是必经之路 [SRC: synthesis draft 行业共性阶段框架]

**前提条件**：
- Phase 1 的触发条件已满足
- 团队已积累 ≥ 50 个 PR 的 AI review 数据
- 已确认 CodeRabbit Pro 或 Qodo Merge Pro 的定价和采购流程
- SAST 工具（Slither、SonarQube）已部署并配置基础规则

**主要风险与失败模式**：
| 风险 | 严重程度 | 缓解 |
|------|----------|------|
| CodeRabbit Pro 闭源核心无法审计 | Medium | Phase 1 已用开源版验证效果，Pro 版主要增加 learnings 和 5-agent，核心 review 能力不变 |
| SAST 工具配置和维护成本高 | Medium | 优先使用社区成熟的规则包（Slither 默认规则、SonarQube Java Quality Profile） |
| Learnings 系统引入隐私顾虑 | Medium | 确认 learnings 数据的存储位置和访问控制；可选择不启用 learnings，仅使用手动配置 |
| 双工具并行（Qodo Merge + CodeRabbit）造成噪音 | Medium | 通过 GitHub label 或路径过滤限制 CodeRabbit 的触发范围，与 Qodo Merge 分项目使用 |

**进入下一阶段的触发条件**：
- AI review + SAST 基线覆盖了 80% 以上的常规 review 需求
- Learnings 系统（或等效配置）已收敛到稳定的团队偏好
- Review quality metric 显示 false positive 率持续下降趋势

**退出标准（转向替代方案）**：
- 若 Phase 2 验证发现 AI review 对 Solidity 深度逻辑审查（如闪电贷攻击路径、预言机操纵模式）无能为力，需在 Phase 3 引入形式化验证工具（Certora / Manticore）作为补充

### Phase 3：Multi-Layer Review 覆盖（第 6-9 个月）

**本阶段升级什么能力**：
- 部署 RoboRev 作为 commit 级持续审查工具，覆盖 AI coding agent 产出物的质量保障
- 接入 2+ 种 AI agent 后端（如 Claude Code + Codex），通过 RoboRev 的 ACP 协议统一管理
- 启用 fix/refine 闭环：commit 发现问题 → 自动修复 → 重审 → 自动关闭
- 可选引入 Open Code Review 的 discourse 机制，对高风险 PR 进行多视角交叉验证

**目标解决什么新问题**：
- 解决"AI coding agent 产出的 commit 在 PR 之前无人审查"的问题
- 解决"单一 LLM 视角的盲区"问题（通过 RoboRev 的多 agent 后端 + OCR 的 discourse）
- 解决"review 发现的问题需要人工修复"的问题（通过 fix/refine 闭环）

**为什么在这个时点出现**：
- 团队可能已开始使用 AI coding agent（Cursor、Claude Code、Codex），需要对其产出进行质量保障
- 行业分化路径分析表明，commit 级和 PR 级是互补而非替代的关系 [SRC: synthesis draft 分化维度 2]
- Phase 1-2 已建立了 PR 级 review 基线，Phase 3 在其上游增加 commit 级防护

**前提条件**：
- 团队已在使用或计划使用 AI coding agent
- 已有 Linux 服务器可用于部署 RoboRev daemon（或通过 systemd socket activation）
- 已积累足够的 AI review 数据来确定哪些类型的 PR 需要 discourse 交叉验证

**主要风险与失败模式**：
| 风险 | 严重程度 | 缓解 |
|------|----------|------|
| RoboRev 的 fix/refine 闭环引入新问题 | High | 设置 refine 的最大迭代次数上限（建议 3 次）；fix 结果必须经过 PR review 确认 |
| 多工具并行增加维护复杂度 | Medium | RoboRev（commit 级）和 Qodo Merge（PR 级）职责正交，通过路径过滤避免重复审查 |
| OCR discourse 的 token 成本过高 | Medium | 仅对高风险 PR（如 Solidity 合约核心逻辑变更、权限变更）启用 discourse |
| RoboRev 对 Solidity/Java 无专项规则 | Medium | 通过配置 agent 后端的 system prompt 注入 Solidity/Java 审查指令 |

**进入下一阶段的触发条件**：
- RoboRev 已覆盖 ≥ 80% 的 AI agent 产出 commit
- fix/refine 闭环的平均修复成功率 ≥ 60%
- Discourse 机制（如已引入）在高危 PR 上的 false positive 降低效果已量化

### Phase 4：Self-Hosted LLM / 数据隔离收敛（第 9-12 个月+）

**本阶段升级什么能力**：
- 评估并部署 self-hosted LLM（open-weight model）作为 review 推理引擎
- 将 Qodo Merge / RoboRev 的 LLM 后端从 cloud API 迁移至 self-hosted 端点
- 针对 Solidity 和 Java 场景对 open-weight model 进行 fine-tuning 或 prompt 优化
- 按项目敏感度分批迁移：高敏感项目（核心合约、金融相关服务）优先迁移

**目标解决什么新问题**：
- 解决 data isolation hard constraint 的终极合规问题——代码完全不离开内部网络
- 降低 cloud LLM API 的长期成本（取决于调用量与 self-hosted GPU 成本的 breakeven point）
- 减少对第三方 LLM provider 的供应商锁定

**为什么在这个时点出现**：
- Phase 1-3 已积累了足够的 review 数据用于 fine-tuning
- 行业趋势判断表明，self-learning 和持续学习是方向 [SRC: synthesis draft 趋势判断 6]
- 只有在积累了足够的 review 数据和规则体系后，self-hosted LLM 才有 ROI [SRC: baseline verdict]

**前提条件**：
- GPU 基础设施已就绪（自有 GPU 或 cloud GPU rental）
- Phase 1-3 已积累 ≥ 500 个 PR 的 review 数据
- 有 1-2 名 dedicated engineering 资源负责 self-hosted LLM 的部署和优化
- local LLM 在 pilot 上的准确率与 cloud API 差距在可接受范围内（建议 ≤ 15%）

**主要风险与失败模式**：
| 风险 | 严重程度 | 缓解 |
|------|----------|------|
| Open-weight model 在 Solidity 上准确率不足 | High | 在 Phase 1 即开始收集 Solidity review 数据；Phase 4 初期做对照实验确认准确率差距 |
| GPU 成本超预算 | Medium | cloud GPU rental 作为折中；按项目敏感度分批迁移，先覆盖高敏感项目 |
| Self-hosted LLM 的维护成本高于预期 | Medium | 优先使用社区成熟的部署方案（如 vLLM、Ollama）；不自建训练管线 |
| Fine-tuning 数据不足 | Low | Phase 1-3 持续积累 review 数据；初期可用 zero-shot + prompt 优化替代 fine-tuning |

**进入下一阶段的触发条件**：
- 本阶段为推荐方案的最终阶段，无下一阶段。持续优化和迭代。

## 推荐方案与理由

### 最终推荐

采用 **"Qodo Merge 起步 → CodeRabbit 增强 → RoboRev 补层 → Self-hosted 收敛"** 的四阶段方案。

### 核心理由

1. **Phase 1 选择 Qodo Merge 而非 CodeRabbit**：Qodo Merge 的开源版部署灵活性（5 种部署方式 + 6 大 Git 平台 + 多模型路由）优于 CodeRabbit 开源版（仅 GitHub Action）。在需要快速验证且不确定的早期阶段，部署灵活性是最重要的决策因素。[SRC: synthesis 能力矩阵 + qodo-merge primitive]

2. **Phase 2 默认推荐 CodeRabbit Pro**：CodeRabbit 的 Context Engineering 体系（8 来源 context + context curation + 5-agent 并行 + Living Memory）在能力深度上领先，learnings 系统的自动学习特性最符合"低维护成本"的 soft preference。若团队对 SaaS vendor 增加有顾虑，备选 Qodo Merge Pro。[SRC: synthesis 能力矩阵 + coderabbit primitive]

3. **Phase 3 引入 RoboRev 补 commit 级覆盖**：RoboRev 的 commit 级审查与 PR 级工具正交互补 [SRC: synthesis 分化维度 2]。其 fix/refine 闭环在 AI agent 产出物审查场景中具有独特价值，不可替代。

4. **Phase 4 Self-hosted 解决终极合规**：data isolation 是 hard constraint，但 Phase 1 无法跳过 LLM 直接起步。四阶段方案通过前三个阶段积累数据和验证效果，在 Phase 4 以最低风险迁移到 self-hosted LLM。

### 与 baseline 决策的关系

Baseline 决策（`knowledge/decisions/ai-coding-review-decision`，change ID: `ai-coding-review-decision`）推荐"方案 2（Static+AI）→ 方案 4（CI/CD Gate）→ 方案 5（Self-hosted）"的技术路线。本决策在以下方面与之保持一致：

- **Static+AI 基线思想**：本方案 Phase 1 即集成 SAST 工具作为确定性基线，Phase 2 进一步强化
- **渐进式建设**：四阶段与 baseline 的三阶段节奏一致，但将"Static+AI"和"CI/CD Gate"合并为 Phase 1-2，因为"阶段一必须 LLM-based"的约束不允许纯静态分析起步
- **Self-hosted 作为长期目标**：Phase 4 与 baseline 的方案 5 定位一致

新增内容：
- 明确了具体产品选型（Qodo Merge → CodeRabbit → RoboRev），而非仅技术路线
- 增加了 commit 级审查层（RoboRev），覆盖 AI agent 产出场景
- 明确了每个阶段的触发条件和退出标准

## 风险矩阵与替代方案

### 核心风险

| 风险 | 影响阶段 | 严重程度 | 缓解措施 |
|------|----------|----------|----------|
| **Data isolation 合规解释冲突**：代码经 cloud LLM API 传输被法务/安全团队认定为违规 | Phase 1 | **High** | Phase 1 即确认合规边界；如不可接受，直接切换至 Phase 4 路线（self-hosted LLM），使用 Qodo Merge 开源版 + Ollama 本地模型 |
| **Solidity 深度安全审查覆盖不足**：LLM 可识别重入、delegatecall 等模式，但无法替代形式化验证 | Phase 1-2 | **High** | Phase 1 即集成 Slither 静态分析；Phase 2 对核心合约引入 Certora / Manticore 形式化验证 [SRC: synthesis 区块链场景评估] |
| **LLM review 准确率不达预期**：false positive 率过高导致开发者忽视 AI review | Phase 1-2 | **High** | 设置"建议模式"而非"阻断模式"；建立 review quality metric 持续跟踪；Phase 2 通过 learnings/context engineering 持续优化 |
| **CodeRabbit Pro 闭源核心不可审计** | Phase 2 | Medium | Phase 1 已用开源版验证核心 review 能力；Pro 版增值能力（learnings、5-agent）为锦上添花，非关键依赖 |
| **RoboRev fix/refine 闭环引入新问题** | Phase 3 | Medium | 设置迭代上限（建议 3 次）；fix 结果必须经 PR review 确认 |
| **Self-hosted LLM GPU 成本超预算** | Phase 4 | Medium | Cloud GPU rental 作为折中；按项目敏感度分批迁移 |
| **Qodo Merge LanceDB RAG 已降级** | Phase 1-2 | Low | Phase 1 不依赖 RAG；可通过 path_instructions + Dynamic Context Expansion 替代 |
| **AsyncReview 项目静止期影响** | Phase 1-2（如作为备选） | Low | 不作为主力方案引入，仅作为技术观察对象 |

### 替代方案

**替代路线 A：CodeRabbit-only 路线**
- Phase 1：CodeRabbit 开源版（ai-pr-reviewer）
- Phase 2：CodeRabbit Pro
- Phase 3：CodeRabbit 5-agent 全量启用 + CI/CD Analysis
- Phase 4：评估 CodeRabbit 是否支持 self-hosted 部署（当前不支持，需等待）
- **适用场景**：团队 Git 平台为 GitHub 且无多平台需求，希望最小化运维复杂度
- **缺点**：CodeRabbit 开源版仅支持 GitHub；Pro 版为纯 SaaS，data isolation 问题无法在 Phase 4 通过迁移解决

**替代路线 B：纯开源 + Self-hosted LLM 路线**
- Phase 1：Qodo Merge 开源版 + self-hosted LLM（Ollama / vLLM）
- Phase 2：Open Code Review discourse 机制 + SAST 集成
- Phase 3：RoboRev commit 级审查
- Phase 4：针对 Solidity/Java 场景 fine-tuning
- **适用场景**：data isolation 被确认为绝对不可妥协（代码不能经任何第三方传输）
- **缺点**：open-weight model 在代码审查上的准确率可能显著低于 cloud API，需要更多验证周期和 fine-tuning 投入

## 未决问题

| 编号 | 问题 | 影响阶段 | 解决路径 |
|------|------|----------|----------|
| UQ-1 | Data isolation 约束是否允许 cloud LLM API 调用 | Phase 1 | 需与法务/安全团队确认；这是影响全方案的首要问题 |
| UQ-2 | 团队 GPU 资源状况（是否有可用 GPU、规格、预算） | Phase 4 | 需基础设施团队评估 |
| UQ-3 | 当前 PR 频率、代码库规模（行数、项目数） | Phase 1-2 | 影响工具选型和成本预估 |
| UQ-4 | Open-weight model 在 Solidity code review 上的具体准确率 | Phase 4 | 需 PoC 验证，建议用 pilot 项目的历史 PR 做对照实验 |
| UQ-5 | CodeRabbit Pro 定价和 tier 功能分层 | Phase 2 | 需 source-evidence-agent 补充回源官方 pricing 页面 |
| UQ-6 | Qodo Merge LanceDB RAG 的当前状态 | Phase 1-2 | 需在 pr-agent 代码中搜索 lancedb 引用确认 |
| UQ-7 | Slither + CodeRabbit/SonarQube 的集成方式和规则覆盖 | Phase 1-2 | 需 PoC 验证集成效果 |

## 证据等级说明

本决策的所有候选方案评估均从 synthesis draft 和 primitive artifact 中提取。**系统性限制**：全证据链最深仅到达 L4（基线推断），无 L1/L2 直接证据支撑。具体而言：

- synthesis draft 本身基于 primitive artifact 的综合分析，属于 L3/L4 中间层
- 7 个本轮 primitive artifact 的证据等级同样为 L4（因网络限制未实际回源 L1/L2 验证）
- 核心技术主张（产品能力、部署方式、定价等）均基于公开文档和 GitHub 仓库元数据的间接推断，未经官方 API 响应或实测验证

建议在 apply 后安排 source-evidence-agent 对关键 L1/L2 来源（CodeRabbit/Qodo Merge 官方文档、GitHub API pricing 页面、pr-agent 代码中 lancedb 引用）进行回源验证，以提升证据等级至 L1/L2。
