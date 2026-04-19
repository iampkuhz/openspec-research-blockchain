# AI Coding Review 工程框架决策分析

**Change ID**: ai-coding-review-decision
**研究类型**: decision / scenario
**聚焦主题**: 区块链（Solidity）、后端服务、Java 生态
**排除范围**: 前端 / 全栈场景

## 决策背景

团队需要自建 AI coding review 工程框架，服务于内部多项目的 code review 流程。在正式投入开发前，需系统评估业界主流方案，制定分阶段技术规划。

**Hard Constraints**：数据隔离（代码不流出内部网络）、Solidity 为首要区块链语言、Java/JVM/Spring 覆盖、PR/MR 集成、可扩展自定义规则。

**Soft Preferences**：review 反馈 5 分钟内、低维护成本、渐进式采用。

## 候选方案对比

### 五条技术路线

| 方案 | 代表 | 核心特征 | 三主题综合适配 | 隐私 | 上市时间 |
|------|------|----------|---------------|------|----------|
| 1. SaaS AI Review Tool | CodeRabbit, Codium PR-Agent | 全托管 SaaS，零运维 | Medium | No（代码外发） | 天 |
| 2. Static Analysis + AI Augmentation | SonarQube/Semgrep + LLM | 静态分析基座 + LLM 语义增强 | **High** | Partial（静态层本地） | 周 |
| 3. IDE/Inline AI Review | GitHub Copilot Chat, Cursor | 开发者编码中即时反馈 | Low | No（代码外发） | 天 |
| 4. CI/CD AI Gate | GitHub Actions/GitLab CI + LLM pipeline | CI 管道触发，作为 merge quality gate | **High** | Partial（LLM 可本地） | 周-月 |
| 5. Self-hosted LLM Framework | Open-weight LLM + AST/Code Graph | 完全自建，全栈可控 | High（需定制） | **Yes** | 月-季度 |

### 关键判断

1. **方案 3 定位为 developer experience 补充**，不应作为 formal review pipeline 的替代。
2. **方案 1 在 data isolation hard constraint 下不可作为长期方案**，仅可作为临时验证。
3. **方案 2 和方案 4 是最优起点**：静态分析在区块链安全审计和 Java 生态已有深厚积累，LLM 可作为解释和补充层。
4. **方案 5 是长期目标**，需团队积累足够的 review 数据、规则体系和 engineering 资源后才具备 ROI。

### 三主题适配要点

| 主题 | 关键检查项 | 最优方案 | 理由 |
|------|-----------|----------|------|
| 区块链（Solidity） | Reentrancy、Access Control、Gas Optimization | 方案 2/4 | slither/Semgrep 已有成熟规则覆盖已知漏洞模式 |
| 后端 | 并发安全、性能反模式、架构一致性 | 方案 2 | SonarQube/Semgrep 在静态分析上有深厚积累 |
| Java | Spring 最佳实践、依赖安全、JVM 性能 | 方案 2 | SonarQube Java plugin + Checkstyle + SpotBugs 生态成熟 |

## AI Review 工具演进规律

从 Lint（Phase 0）到 AI-Native Review（Phase 4）的共性规律：

1. **规则驱动 → 理解驱动**：纯规则检测无法发现未知模式，纯 LLM 缺乏精确代码结构理解，混合方案是方向。
2. **单文件 → 跨文件/跨模块**：通过 Code Graph 实现精确跨模块依赖分析是 Phase 4 的核心能力。
3. **通用 → 领域定制**：差异化壁垒来自领域规则库（Solidity 安全模式、Spring 最佳实践）积累。
4. **本地 → SaaS → 混合**：数据隔离需求推动混合部署回归。

**对自建框架的启示**：不要从 Phase 4 开始，所有成功的 AI review 工具都建立在强大的静态分析基础设施之上。

## 分阶段推荐

### Phase 1：基础覆盖与验证（1-2 个月）

- **技术路线**：方案 2（Static+AI）为主 + 方案 3（IDE/Inline）为辅
- **关键动作**：部署 SonarQube/Semgrep 基座，配置 Solidity + Java + 后端规则包；LLM 增强层并行验证 cloud API 效果与 local LLM 可行性；建立 review 质量度量 baseline
- **退出条件**：若 Static+AI 满足 80% 需求，Phase 2 继续深化；若 data isolation 成为 blocker，Phase 2 转向方案 5

### Phase 2：核心能力建设（3-6 个月）

- **技术路线**：方案 4（CI/CD AI Gate）深化 + 方案 2 持续优化
- **关键动作**：构建统一 AI review CI pipeline；开发自定义规则引擎（Solidity 安全模式、Spring 最佳实践）；评估 local LLM 部署可行性；建立 review feedback loop
- **关键决策点**：Phase 2 中期决定是否引入 local LLM，依据为 data isolation 要求、cloud LLM 成本、local LLM 准确率差距

### Phase 3：智能化演进（6-12 个月+）

- **技术路线**：方案 5（Self-hosted LLM Framework）渐进引入
- **关键动作**：部署 open-weight LLM；构建 AST/Code Graph 分析层；针对 Solidity/Spring 场景 fine-tuning；按项目敏感度分批替换 cloud LLM
- **关键前提**：足够 engineering 资源（1-2 人 dedicated）；GPU infra 已就绪；Phase 2 已积累足够 review 数据

### 设计原则

1. 从静态分析起步，不要跳过 Phase 0-1 直接从 LLM 开始
2. 能力累积而非替换，Phase N 不废弃 Phase N-1 的能力
3. 真正的差异化壁垒是领域规则库积累，而非通用 LLM 能力
4. Phase 3 是否引入取决于 Phase 1-2 验证结果和团队实际资源

## 风险矩阵

| 风险 | 影响阶段 | 严重程度 | 缓解措施 |
|------|----------|----------|----------|
| Solidity 规则覆盖不足 | Phase 1 | High | 优先集成 slither 和社区规则包 |
| LLM review 准确率不达预期 | 全阶段 | High | Phase 1 快速验证；设置 human-in-the-loop |
| Data isolation 要求高于预期 | Phase 1-2 | High | Phase 1 确认 compliance 要求；Phase 2 提前规划 local LLM |
| GPU infra 成本超预算 | Phase 3 | Medium | cloud GPU rental 折中；按项目分批迁移 |
| 自定义规则维护成本过高 | Phase 2-3 | Medium | 优先覆盖高频规则；建立规则 lifecycle 管理 |

## 未决问题

1. Open-weight model 在 Solidity code review 上的具体准确率数据（需团队 PoC 验证）
2. slither/Semgrep Solidity 规则包的覆盖率和 false positive rate（需 Phase 1 实际运行验证）
3. 自建 LLM vs SaaS 方案的成本 breakeven point（取决于代码量、review 频率、model 选择）
4. AST/Code Graph 分析层对 review 准确率的量化提升（建议 Phase 3 设计对照实验）

## 证据说明

本文证据等级标注遵循 Confirmed / Partial / Unclear 三级体系。具体产品能力断言（语言覆盖数、演进时间线、定价等）在 request 阶段排除了来源收集，参考资料标记为 `[未验证] 网络限制`。进入 apply 阶段前建议补充 source_id 精确追溯。
