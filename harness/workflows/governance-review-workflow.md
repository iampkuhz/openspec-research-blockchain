# Governance Review Workflow - 规约与架构评审

**注意**：本 workflow 用于规约/架构评审，不用于普通 research 内容评审。

## 目标

评审对 OpenSpec / Harness 规约文件的修改，确保职责边界清晰、不破坏现有架构。

## 触发条件

**任务语义优先，路径辅助**：不要因为文件位于某个路径下就自动使用本 workflow，只有当任务语义涉及规约/架构调整时才使用。

**必须使用本 workflow 的场景**：
- 调整 OpenSpec / Harness 职责边界
- 修改 schema / specs / templates / governance / repository architecture
- 修改用于定义或评审规约分层的 workflow / rules / skills
- 修改 AGENTS.md 中与仓库路由、治理、分层相关的段落
- 评审上述类型的变更

**不要使用本 workflow 的场景**：
- 普通技术调研、知识条目更新
- 来源收集与验证、图表生成
- 一般性的 research workflow 微调
- 与仓库分层无关的 skills 优化

## 必需输入

- 变更文件列表
- 变更说明
- 相关评审人员

## 默认执行角色

- `orchestrator`
- `governance-review-agent`

## 规则加载策略

### 初始加载（workflow 开始时）

**必须读取**：

| 规则 | 路径 | 用途 |
|------|------|------|
| **职责边界规范** | `docs/governance/openspec-harness-boundary.md` | 确认修改符合职责边界 |

### 按需加载（执行到对应步骤前）

| 步骤 | 规则 | 用途 |
|------|------|------|
| 步骤 2（边界检查） | `openspec/schemas/blockchain-research/schema.yaml` | 检查 artifact contract 修改 |
| 步骤 3（约束检查） | `openspec/specs/*/spec.md` | 检查 canonical constraints 修改 |
| 步骤 4（执行检查） | `harness/rules/_index.yaml` | 检查 execution rules 修改 |

## 步骤

### 步骤 1：确认变更类型

| 变更类型 | 说明 | 示例 |
|----------|------|------|
| OpenSpec 修改 | 修改 `openspec/**` | 修改 schema.yaml、specs/、config.yaml |
| Harness 修改 | 修改 `harness/**` | 修改 workflows/、rules/ |
| 导航修改 | 修改 `AGENTS.md` | 更新路由、索引 |
| 边界修改 | 修改 `docs/governance/openspec-harness-boundary.md` | 更新职责边界定义 |

### 步骤 2：职责边界检查

**检查项**：

```yaml
boundary_check:
  - item: OpenSpec 修改是否符合其职责
    description: |
      OpenSpec 应只负责：
      - Artifact Contract 主定义
      - Canonical Templates
      - Schema-level Workflow Semantics
      - Canonical Semantic Constraints
      - Project-level Configuration
    status: pass/fail

  - item: Harness 修改是否符合其职责
    description: |
      Harness 应只负责：
      - Research Execution Playbooks
      - Execution-facing Governance
      - Execution-facing Procedures
      - Research Writing Guidance
    status: pass/fail

  - item: 是否有职责越界
    description: |
      检查是否有：
      - Harness 定义了 canonical policy（应属 OpenSpec）
      - OpenSpec 定义了 execution details（应属 Harness）
    status: pass/fail

  - item: 是否有重复定义
    description: |
      检查同一内容是否在 OpenSpec 和 Harness 中重复定义
    status: pass/fail
```

### 步骤 3：影响范围分析

**检查项**：

```yaml
impact_analysis:
  - item: 哪些 workflows 会受影响
    status: done/pending

  - item: 哪些 rules 会受影响
    status: done/pending

  - item: 哪些 skills 会受影响
    status: done/pending

  - item: 现有 knowledge assets 是否会受影响
    status: done/pending

  - item: 是否需要迁移现有内容
    status: done/pending
```

### 步骤 4：一致性检查

**检查项**：

```yaml
consistency_check:
  - item: 与 openspec/schemas/blockchain-research/schema.yaml 一致
    status: pass/fail

  - item: 与 openspec/specs/ 一致
    status: pass/fail

  - item: 与 harness/workflows/ 一致
    status: pass/fail

  - item: 与 harness/rules/ 一致
    status: pass/fail

  - item: 术语使用一致
    status: pass/fail
```

### 步骤 5：编写评审意见

```markdown
# Governance Review

## 变更概述

[描述本次变更的内容]

## 职责边界检查

| 检查项 | 结果 | 说明 |
|--------|------|------|
| OpenSpec 职责符合性 | pass/fail | |
| Harness 职责符合性 | pass/fail | |
| 职责越界检查 | pass/fail | |
| 重复定义检查 | pass/fail | |

## 影响范围

- 受影响的 workflows：
- 受影响的 rules：
- 受影响的 skills：
- 需要迁移的内容：

## 一致性检查

| 检查项 | 结果 | 说明 |
|--------|------|------|
| schema.yaml | pass/fail | |
| openspec/specs/ | pass/fail | |
| harness/workflows/ | pass/fail | |
| harness/rules/ | pass/fail | |

## 必须修复的问题

| ID | 严重性 | 描述 |
|----|--------|------|
| | high/medium/low | |

## 评审结论

- [ ] approved - 可直接合并
- [ ] approved with minor fixes - 修复后可直接合并
- [ ] needs revision - 需要重大修改后重新评审
```

### 步骤 6：确认修复

评审人确认修复：

```yaml
# 在评审记录中
resolution:
  ISSUE-001:
    resolved: true
    resolved_at: <date>
    notes: ""
```

## 输出

- `openspec/changes/<change-id>/review/governance-review.md`

## 完成标准

- [ ] 职责边界检查完成
- [ ] 影响范围分析完成
- [ ] 一致性检查完成
- [ ] 问题已记录
- [ ] High 问题已修复

## 异常处理

### 发现职责越界

**处理**：
1. 记录越界内容
2. 移动到正确的层（OpenSpec 或 Harness）
3. 更新所有引用点

### 发现重复定义

**处理**：
1. 识别 canonical 定义（应在 OpenSpec）
2. 删除 Harness 中的重复定义
3. 更新 Harness 引用指向 OpenSpec

### 发现破坏性变更

**处理**：
1. 评估影响范围
2. 制定迁移计划
3. 在 changelog 中标注 breaking changes
