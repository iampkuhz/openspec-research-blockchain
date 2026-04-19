# Brief 质量评估规则

## 目的

评估 `architecture-brief.yaml` 或 `sequence-brief.yaml` 的输入质量，确保需求清晰再生成图表。

## 评估维度

### 维度 1: 完整性

**架构 Brief 必检项**：

| 检查项 | 标准 |
|--------|------|
| 层数 | 至少 3 层 |
| 组件数 | 至少 3 个 |
| 流程数 | 至少 1 条跨组件流程 |
| 字段完整 | `diagram_id`, `title`, `summary`, `layers`, `components`, `flows` 必填 |

**时序 Brief 必检项**：

| 检查项 | 标准 |
|--------|------|
| 参与者数 | 至少 2 个 |
| 消息数 | 至少 1 条 |
| 消息编号 | 必须有唯一 ID (如 M1, M2) |
| 字段完整 | `diagram_id`, `title`, `summary`, `participants`, `messages` 必填 |

### 维度 2: 一致性

**检查项**：

| 检查项 | 说明 |
|--------|------|
| ID 唯一性 | `layers[].id`, `components[].id`, `participants[].id` 必须唯一 |
| 引用有效性 | `flows[].from` / `flows[].to` 必须引用存在的 `components[].id` |
| 层归属有效 | `components[].layer` 必须引用存在的 `layers[].id` |
| 命名一致 | `name` 字段全文使用同一术语 |

### 维度 3: 清晰度

**检查项**：

| 检查项 | 说明 |
|--------|------|
| 标题明确 | 标题能反映图的核心内容 |
| 摘要有效 | `summary` 不是空话，能说明图的用途 |
| 职责清晰 | 每个组件/参与者有职责描述 |
| 流程可理解 | 流程描述有主谓宾，不是模糊词汇 |

### 维度 4: 可渲染性

**检查项**：

| 检查项 | 说明 |
|--------|------|
| 复杂度适中 | 组件数 5-15 个，超过建议分层 |
| 流程数适中 | 流程数 3-15 条，超过建议分解 |
| 布局约束 | 包含 `layout.direction` 和 `skinparam` 设置 |

## 问题分级

| 严重性 | 定义 | 处理 |
|--------|------|------|
| **Blocker** | 必填字段缺失、引用断裂 | 暂停生成，先修复 brief |
| **Major** | 描述模糊、复杂度过高 | 建议修复，可降级生成 |
| **Minor** | 格式不统一、可优化 | 记录，酌情修复 |

## 校验流程

```
1. Schema 校验 → 由 diagram global skill 内部执行
2. 完整性检查 → 必检项清单
3. 一致性检查 → 引用有效性
4. 清晰度检查 → 人工/语义判断
5. 输出评估报告 → 通过/需修复/暂停
```

## 评估输出格式

```yaml
# brief-evaluation.yaml
brief_path: assets/briefs/erc4337-architecture.yaml
evaluated_at: 2024-01-15T10:00:00Z

dimensions:
  completeness:
    status: pass|warn|fail
    issues: []
  consistency:
    status: pass|warn|fail
    issues: []
  clarity:
    status: pass|warn|fail
    issues: []
  renderability:
    status: pass|warn|fail
    issues: []

overall:
  status: approved|conditional|blocked
  severity: blocker|major|minor
  summary: 评估摘要

recommendations:
  - 建议 1
  - 建议 2
```
