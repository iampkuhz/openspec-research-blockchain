# 06 Quality Gates And Acceptance

## 阶段质量门

| 阶段 | Owner | Gate |
|------|-------|------|
| request | research-author-agent | 对象类型、路径、核心问题、范围、非目标完整 |
| source | source-evidence-agent | 来源分层、关键 excerpts、证据缺口完成 |
| plan | research-author-agent | 来源规划、交付范围、研究深度、完成标准完整 |
| draft | research-author-agent + diagram-agent | 图表清单与 diagram contract 通过，bounded conclusions 明确 |
| review | review-critic-agent | high severity 清零，结论明确 |
| publish | publish-agent | 目标路径正确，长期内容已提炼而非整包照搬 |

## 人工验收场景

1. 新 research change：
   - `/spec-research` 能给出 active agents
   - `source` 与 `draft` 职责不混写
   - `review` 有独立结论

2. update existing knowledge：
   - `publish-agent` 能同时判断 apply 与 impact scan
   - 不再依赖 `knowledge/topics`

3. governance change：
   - 自动激活 `governance-review-agent`
   - 明确 OpenSpec / Harness 边界

## 建议的基础检查

```bash
git diff --check
rg -n "knowledge/topics|dependencies.md|evidence-matrix.md" AGENTS.md README.md harness .claude skills
```

## 后续迭代方向

- 为 multi-agent orchestration 增加回归测试样例
- 为 `.qoder/agents/` 增补运行时格式
- 对更多 legacy rules / skills 做第二轮语义清理
