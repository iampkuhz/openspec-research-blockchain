# OpenSpec Changes

Change 目录是研究过程产物的存放位置。每个 change 代表一项独立研究任务。

**不是这里的职责**：
- 不直接修改 `knowledge/` 主线内容
- 不在此目录手动创建长期资产

**标准结构**：每个 change 目录应遵循以下规范：

```
openspec/changes/<change-id>/
├── request.md          # 研究请求（元数据、研究对象、核心问题）
├── plan.md             # 研究计划（范围、阶段、验收标准）
├── draft.md            # 研究正文（分析、对比、结论）
├── decision-criteria.md # （可选）决策标准
├── sources/            # 来源材料（URL 提取、论文、文档）
├── diagrams/           # 图表文件（PlantUML、PNG、SVG）
└── review/             # 评审记录（review notes、critique）
```

**状态**：
- **活跃**：仍在进行研究或尚未归档的 change
- **已归档**：已合并到 `knowledge/` 并移至 `openspec/changes/archive/`

---

## 活跃 Change 索引

| Change ID | 类型 | 状态 | 创建日期 |
|-----------|------|------|----------|
| `ai-coding-review-comparison` | synthesis | 活跃 | 2026-04-19 |
| `ai-coding-review-decision` | decision | 活跃 | 2026-04-19 |
| `ai-coding-review-roadmap` | primitive | 活跃 | 2026-04-19 |
| `amazon-codeguru-framework` | primitive | 活跃 | 2026-04-19 |
| `asyncreview-evolution` | primitive | 活跃 | 2026-04-19 |
| `asyncreview-evolution-v2` | primitive | 活跃 | 2026-04-19 |
| `chatgpt-codereview-framework` | primitive | 活跃 | 2026-04-19 |
| `chatgpt-codereview-framework-v2` | primitive | 活跃 | 2026-04-19 |
| `coderabbit-framework-v2` | primitive | 活跃 | 2026-04-19 |
| `codium-qodo-framework` | primitive | 活跃 | 2026-04-19 |
| `cr-decision-ai-coding-review-decision-refresh` | decision | 活跃 | 2026-04-20 |
| `cr-primitive-asyncreview-evolution-refresh` | primitive | 活跃 | 2026-04-20 |
| `cr-primitive-chatgpt-codereview-framework-refresh` | primitive | 活跃 | 2026-04-20 |
| `cr-primitive-coderabbit-framework-refresh` | primitive | 活跃 | 2026-04-20 |
| `cr-primitive-open-code-review-framework-refresh` | primitive | 活跃 | 2026-04-20 |
| `cr-primitive-qodo-merge-evolution-refresh` | primitive | 活跃 | 2026-04-20 |
| `cr-primitive-roborev-evolution-refresh` | primitive | 活跃 | 2026-04-20 |
| `cr-primitive-supplementary-frameworks-refresh` | primitive | 活跃 | 2026-04-20 |
| `cr-synthesis-ai-coding-review-comparison-refresh` | synthesis | 活跃 | 2026-04-20 |
| `decision-nanopayment-tech-reserve` | decision | 活跃 | 2026-04-24 |
| `governance-boundary-convergence-v2` | synthesis | 活跃 | 2026-04-20 |
| `open-code-review-framework` | primitive | 活跃 | 2026-04-19 |
| `open-code-review-framework-v2` | primitive | 活跃 | 2026-04-19 |
| `primitive-did-auth` | primitive | 活跃 | 2026-04-11 |
| `primitive-layer2-payment-channels` | primitive | 活跃 | 2026-04-24 |
| `primitive-lightning-network` | primitive | 活跃 | 2026-04-24 |
| `primitive-nano-protocol` | primitive | 活跃 | 2026-04-24 |
| `primitive-siwe-eip-4361` | primitive | 活跃 | 2026-04-11 |
| `primitive-tempo-chain-solution` | primitive | 活跃 | 2026-04-24 |
| `qodo-merge-evolution` | primitive | 活跃 | 2026-04-19 |
| `qodo-merge-evolution-v2` | primitive | 活跃 | 2026-04-19 |
| `review-architecture-evolution` | primitive | 活跃 | 2026-04-19 |
| `review-collaboration-evolution` | primitive | 活跃 | 2026-04-19 |
| `review-customization-evolution` | primitive | 活跃 | 2026-04-19 |
| `review-performance-evolution` | primitive | 活跃 | 2026-04-19 |
| `review-quality-evolution` | primitive | 活跃 | 2026-04-19 |
| `review-security-evolution` | primitive | 活跃 | 2026-04-19 |
| `roborev-evolution` | primitive | 活跃 | 2026-04-19 |
| `roborev-evolution-v2` | primitive | 活跃 | 2026-04-19 |
| `secondary-asyncreview-evolution` | primitive | 活跃 | 2026-04-20 |
| `secondary-chatgpt-codereview-framework` | primitive | 活跃 | 2026-04-20 |
| `secondary-coderabbit-framework` | primitive | 活跃 | 2026-04-20 |
| `secondary-open-code-review-framework` | primitive | 活跃 | 2026-04-20 |
| `secondary-qodo-merge-evolution` | primitive | 活跃 | 2026-04-20 |
| `secondary-roborev-evolution` | primitive | 活跃 | 2026-04-20 |
| `secondary-supplementary-frameworks` | primitive | 活跃 | 2026-04-20 |
| `sonarqube-ai-framework` | primitive | 活跃 | 2026-04-19 |
| `supplementary-frameworks` | primitive | 活跃 | 2026-04-19 |
| `supplementary-frameworks-v2` | primitive | 活跃 | 2026-04-19 |

---

## 归档 Change

已归档的 change 移至 [`archive/`](archive/)，其原始目录结构保持不变。

## 如何创建新 Change

1. 在 `harness/workflows/intake-workflow.md` 查看创建流程
2. 创建 `openspec/changes/<change-id>/` 目录
3. 编写 `request.md`（必需），再按需编写 `plan.md`、`draft.md` 等
4. 按阶段推进：request → plan → draft → review → artifact
