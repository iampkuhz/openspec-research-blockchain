# Governance Review Workflow — `/spec-governance-review` 执行规约

**对应 Command**：`/spec-governance-review`
**输出**：`openspec/changes/<change-id>/review/governance-review.md`

---

## 触发条件

**必须使用本 workflow 的场景**：
- 调整 OpenSpec / Harness 职责边界
- 修改 schema / specs / templates / governance / repository architecture
- 修改 `.claude/commands/` 或 `.claude/agents/` 中与仓库路由、角色合同、阶段编排相关的内容
- 修改 AGENTS.md 中与仓库路由、治理、分层相关的段落
- 评审上述类型的变更
- 周期性 repo-wide 规约卫生审计、孤岛文件扫描、死引用清理（原 spec-system-audit 场景已合并至此）

**不要使用本 workflow 的场景**：
- 普通技术调研、知识条目更新
- 来源收集与验证、图表生成
- 一般性的 research workflow 微调

## 默认执行角色

- `governance-review-agent`
- 如需 repo-wide audit：`spec-system-audit-agent`

## 执行步骤

### 步骤 1：确认变更类型

| 变更类型 | 说明 |
|---|---|
| OpenSpec 修改 | 修改 `openspec/**` |
| Harness 修改 | 修改 `harness/**` |
| Command 修改 | 修改 `.claude/commands/**` |
| Agent 修改 | 修改 `.claude/agents/**` |
| 导航修改 | 修改 `AGENTS.md` |
| 边界修改 | 修改 `docs/governance/**` |

### 步骤 2：检查 openspec schema 与 harness 是否一致

- schema.yaml 定义的 artifact graph 是否与 harness workflows 的执行步骤冲突
- harness rules 是否引用了 schema 中不存在的 artifact id
- harness workflows 是否重新定义了和 schema.yaml requires/templates 冲突的流程

### 步骤 3：检查 command routing 是否一致

- active commands 是否在 `_index.yaml` 中有对应 workflow
- deprecated commands 是否只在兼容入口提及
- command → skill → workflow 的映射是否清晰

### 步骤 4：检查 skill boundaries 是否一致

- 每个 skill 是否只负责可复用执行能力
- skill 是否不定义 artifact 正式语义
- skill 是否不直接生成 knowledge 正文

### 步骤 5：检查 harness rules 是否可映射到 validators

- 每个 artifact rule 是否有推荐的 validator
- 每个 gate 是否有对应的 hook 脚本
- registry.yaml 中的 validator 是否覆盖关键 gates

### 步骤 6：检查 hook coverage 是否覆盖关键 gates

- post-request / post-plan / post-draft / pre-publish / post-publish gates
- 是否有 validator 缺失
- validator 脚本是否存在且可执行

### 步骤 7：输出

输出问题清单、修复计划，必要时执行小范围规约修改。

推荐结构：

```markdown
# Governance Review

## 变更概述

## 问题清单
| # | 类别 | 严重性 | 位置 | 描述 |

## 修复计划
| # | 操作 | 影响范围 |

## 已执行修复
| # | 文件 | 修改内容 |

## 遗留风险
```
