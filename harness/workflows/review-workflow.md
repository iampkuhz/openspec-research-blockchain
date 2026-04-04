# Review Workflow - 知识评审

## Goal

评审研究产出（draft.md），确保准确性、一致性、完整性，为 apply 到 knowledge/ 做准备。

## Trigger

- `draft.md` 完成后
- apply 到 knowledge/ 前

## Required Inputs

- `openspec/changes/<change-id>/draft.md`
- `openspec/changes/<change-id>/plan.md`
- `openspec/changes/<change-id>/sources/`

## Optional Inputs

- 现有相关知识
- 依赖的研究对象

## Rule Set to Load

根据评审对象类型加载：

| 对象类型 | Rules |
|----------|-------|
| primitive | `atom-definition-rules.md` / `atom-mechanism-rules.md` |
| synthesis | `atom-evolution-rules.md` / `note-comparison-rules.md` |
| domain | `atom-definition-rules.md` |
| decision | `note-comparison-rules.md` / decision-criteria |

## Step-by-Step Procedure

### Step 1: 准备评审材料

创建评审目录：

```
openspec/changes/<change-id>/review/
├── checklist.yaml
├── issues.md
└── review-summary.md
```

### Step 2: 技术准确性评审

**检查项**：

```yaml
# review/checklist.yaml
accuracy:
  - item: 所有 `claim` 都有 `source` 支撑
    status: pass/fail
    notes: ""

  - item: 证据等级适当（L1/L2 用于核心 `claim`）
    status: pass/fail
    notes: ""

  - item: 无事实错误
    status: pass/fail
    notes: ""

  - item: 术语使用准确
    status: pass/fail
    notes: ""

consistency:
  - item: 术语一致
    status: pass/fail
    notes: ""

  - item: 与其他知识不冲突
    status: pass/fail
    notes: ""

completeness:
  - item: 核心内容完整
    status: pass/fail
    notes: ""

  - item: 边界条件说明
    status: pass/fail
    notes: ""

  - item: 待决问题列出
    status: pass/fail
    notes: ""
```

### Step 3: 可读性评审

**检查项**：

```yaml
readability:
  - item: 结构清晰
    status: pass/fail
    notes: ""

  - item: 段落长度适当
    status: pass/fail
    notes: ""

  - item: 图表帮助理解（如有）
    status: pass/fail/na
    notes: ""
```

### Step 4: Diagram 评审（如有）

使用 `diagram-review-checklist.md`：

```yaml
diagram_review:
  - item: 抽象层次清晰（规范/实现/生态不混淆）
    status: pass/fail/na

  - item: 关系语义正确
    status: pass/fail/na

  - item: 简化已标注
    status: pass/fail/na
```

### Step 5: 记录问题

```markdown
# Review Issues

## High Severity

### ISSUE-001: 事实错误

**位置**：draft.md，第 3 节

**问题**：[具体描述]

**建议**：[修复建议]

**状态**：open

## Medium Severity

### ISSUE-002: 术语不一致

**位置**：全文

**问题**：混用不同术语

**建议**：统一术语

**状态**：open

## Low Severity

### ISSUE-003: 图表可改进

**位置**：diagrams/build/architecture.svg

**问题**：布局可优化

**建议**：调整组件位置

**状态**：open
```

### Step 6: 编写评审总结

```markdown
# Review Summary

**Change ID**: <change-id>
**Review Date**: <date>
**Reviewers**: <reviewers>

## 总体评价

[整体评价]

## 评审结果

| 维度 | 结果 |
|------|------|
| 准确性 | pass/fail |
| 一致性 | pass/fail |
| 完整性 | pass/fail |
| 可读性 | pass/fail |

## 必须修复的问题

| ID | 严重性 | 描述 |
|----|--------|------|
| ISSUE-001 | high | ... |

## 建议修复的问题

| ID | 严重性 | 描述 |
|----|--------|------|
| ISSUE-002 | medium | ... |

## 评审结论

- [ ] approved - 可直接 apply
- [ ] approved with minor fixes - 修复后 apply
- [ ] needs revision - 需要重大修改后重新评审
```

### Step 7: 修复问题

作者根据评审意见修复：

```
- [ ] 所有 high severity 已修复
- [ ] medium severity 已修复或记录
- [ ] low severity 酌情处理
```

### Step 8: 评审确认

评审人确认修复：

```yaml
# 在 review-summary.md 中
resolution:
  ISSUE-001:
    resolved: true
    resolved_at: <date>
    notes: "已修正"
```

## Outputs

- `review/checklist.yaml`
- `review/issues.md`
- `review/review-summary.md`

## Done Criteria

- [ ] 评审检查完成
- [ ] 问题已记录
- [ ] High 问题已修复
- [ ] 评审结论已给出

## Next Step

→ `merge-workflow.md`（apply 到 knowledge/）

## Failure Handling

### 评审发现重大问题

**处理**：
1. 暂停 apply
2. 重新研究问题
3. 可能需要补充来源
4. 重新评审

### 评审意见不一致

**处理**：
1. 列出分歧点
2. 优先采纳技术评审意见
3. 记录不同意见
