# Verdict: AI Coding Review 工程框架分阶段建设方案

**Change ID**: ai-coding-review-decision
**研究类型**: decision / scenario
**评审状态**: approved with minor fixes（无 high severity 问题）
**决策日期**: 2026-04-19

## 最终推荐

采用**分阶段渐进式建设方案**：Phase 1 Static+AI → Phase 2 CI/CD Gate → Phase 3 Self-hosted。

## 各阶段推进与转向条件

### Phase 1 → Phase 2 推进条件

- Static+AI 方案经验证满足 80% 以上 review 需求
- 三聚焦主题（区块链/后端/Java）的静态分析规则包已配置并产生有效 review findings
- review 质量度量 baseline 已建立

### Phase 1 → Phase 2 转向条件（转向方案 5）

- data isolation 被确认为不可妥协的 hard constraint，且 cloud LLM API 验证无法满足合规要求
- 此时 Phase 2 应以 Self-hosted LLM 为方向，而非 CI/CD Gate

### Phase 2 → Phase 3 推进条件

- 足够的 engineering 资源（1-2 人 dedicated）
- GPU infra 已就绪或可通过 cloud GPU rental 解决
- Phase 2 已积累足够的 review 数据用于 fine-tuning
- local LLM 准确率与 cloud API 差距在可接受范围内

### Phase 2 → Phase 3 替代条件（不引入 Self-hosted）

- GPU 成本或人力投入不可承受
- 继续使用 CI/CD Gate + cloud LLM API，通过 prompt 优化和 caching 降低成本

## 核心风险与缓解

| 风险 | 严重程度 | 缓解措施 |
|------|----------|----------|
| Solidity 规则覆盖不足 | High | 优先集成 slither 和社区 Solidity 规则包；自建规则时参考 Known Attack Patterns |
| LLM review 准确率不达预期 | High | Phase 1 快速验证；建立 review quality metric；设置 human-in-the-loop |
| Data isolation 要求高于预期 | High | Phase 1 即确认 compliance 要求；Phase 2 提前规划 local LLM |
| GPU infra 成本超预算 | Medium | cloud GPU rental 作为折中；按项目敏感度分批迁移 |
| 自定义规则维护成本过高 | Medium | 优先覆盖高频规则；建立规则 lifecycle 管理 |

## 证据等级汇总

| 结论类别 | 证据等级 | 说明 |
|----------|----------|------|
| 方案 2/4 在聚焦主题的适配度 | L1/L2 | 基于静态分析工具的官方文档和社区实践 |
| 方案 1/3 的 data isolation 限制 | L1 | SaaS 方案需将代码发送至 vendor 服务器 |
| 演进规律总结 | L2/L3 | 基于公开产品时间线和社区分析 |
| 分阶段推荐的 ROI 判断 | L2/L4 | 基于业界演进经验和团队约束推理 |
| Open-weight model 在 Solidity 上的准确率 | L4 | 缺乏统一 benchmark，需团队 PoC 验证 |

**注意**：本文在 request 阶段排除了来源收集，具体产品能力断言（语言覆盖数、演进时间线、定价等）缺乏 source_id 精确追溯。建议在 apply 阶段前补充来源验证。
