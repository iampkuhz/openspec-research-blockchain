# Source Workflow - 来源处理

## Goal

获取、验证、归档研究来源，为 `plan.md` 和 `draft.md` 提供证据基础。

## Trigger

- intake workflow 完成后
- `request.md` 已填写

## Required Inputs

- `request.md` 中的研究范围
- 研究问题列表

## 默认执行角色

- @source-evidence-agent

由主会话显式调用 @source-evidence-agent。

@source-evidence-agent 是来源生产者，不负责给出最终研究结论，也不负责正式评审。

## 联网通道优先级

当任务明确要求联网搜索或在线补证据时：

1. 搜索优先使用 `fastmcp-gateway` 暴露的 `searxng_search_web`
2. 网页正文提取优先使用 `crawl4ai` 的 `md`
3. 若上述 MCP 当前不可用，必须先记录不可用原因，再回退到其他通道

## 规则加载策略

### 初始加载（workflow 开始时）

| 规则 | 路径 | 用途 |
|------|------|------|
| `traceability-policy.md` | `harness/rules/general/` | 可追溯性要求（claim→source 映射） |

**注**：证据等级政策见 `openspec/specs/evidence-policy/spec.md`。

### 按需加载（执行到对应步骤前）

| 步骤 | 规则 | 用途 |
|------|------|------|
| 步骤 5（提取关键信息） | `source-validation-rules.md` | 来源验证与证据提取 |
| 步骤 6（验证来源） | `uncertainty-rules.md` | 不确定性处理与置信度标注 |
| 步骤 8（Source Review） | 重新读取 `openspec/specs/evidence-policy/spec.md` | 对照证据等级检查 |

**注意**：规则文件在对话中可能被压缩，**Source Review 前必须重新读取** `openspec/specs/evidence-policy/spec.md`。

## 步骤

### 步骤 1：创建 Sources 目录结构

```
openspec/changes/<change-id>/sources/
├── inbox.yaml         # 原始来源入口
├── fetched/           # 抓取的来源
├── excerpts/          # 来源摘录
└── source-review.md   # 来源评审
```

### 步骤 2：收集来源

根据研究问题，按证据等级收集：

| 等级 | 来源类型 | 用途 |
|------|----------|------|
| L1 | 官方规范/EIP/白皮书 | 核心技术主张 |
| L2 | 参考实现/官方文档 | 技术主张支持 |
| L3 | 官方博客/Release notes | 背景/动机 |
| L4 | 第三方分析/社区讨论 | 社区观点参考 |

### 步骤 3：记录来源到 inbox.yaml

```yaml
version: "1.0"
change_id: <change-id>
created_at: <date>

sources:
  - source_id: <unique-id>
    title: <标题>
    url: <链接>
    type: standard|implementation|blog|discussion
    tier: L1|L2|L3|L4
    status: pending|read|verified
    priority: high|medium|low
    relevant_sections:
      - <章节/内容描述>
    notes: <说明>
```

### 步骤 4：获取来源内容

**对于在线来源**：
1. 访问 URL
2. 抓取内容
3. 归档（PDF/截图/文本）
4. 保存到 `fetched/`

### 步骤 5：提取关键信息

为每个核心来源创建 excerpt：

```markdown
# Excerpt: <source_id>-<section>

**Source**: <title>
**Source ID**: <source_id>
**URL**: <url>
**Location**: <文档中的位置>
**Extracted At**: <date>

## Content

> [引用原文]

## Relevance

[为什么这个来源重要，支持哪些分析]
```

### 步骤 6：验证来源

| 维度 | 检查项 |
|------|--------|
| 权威性 | 是否官方发布 |
| 时效性 | 是否最新 |
| 完整性 | 是否覆盖所需 |
| 一致性 | 与其他来源是否一致 |

### 步骤 7：创建 Source Pack

```yaml
# sources/source-pack.yaml
version: "1.0"
topic: <topic>
generated_at: <date>

sources:
  - source_id: <unique-id>
    title: <标题>
    url: <链接或本地引用>
    source_type: standard|implementation|blog|discussion
    source_tier: L1|L2|L3|L4
    accessed_at: <日期>
    confidence: high|medium|low
    notes: <可选说明>
```

### 步骤 8：编写 Source Review

```markdown
# Source Review

## 来源概览

| 类型 | 数量 |
|------|------|
| L1 | X |
| L2 | X |
| L3 | X |
| L4 | X |

## 核心来源

[列出最关键的 3-5 个来源]

## 证据缺口

[哪些重要内容缺乏来源支持]

## 待确认问题

[需要进一步验证的内容]
```

## 输出

- `sources/inbox.yaml`
- `sources/fetched/*`
- `sources/excerpts/*`
- `sources/source-pack.yaml`
- `sources/source-review.md`

## handoff

标准交接给主会话 orchestrator 的内容：

- 关键来源清单
- 核心 excerpts
- evidence gaps
- conflicts / unresolved ambiguity

## 完成标准

- [ ] 所有计划的来源已收集
- [ ] 来源已归档
- [ ] 关键 excerpts 已提取
- [ ] 证据缺口已识别

## 下一步

→ 由主会话 orchestrator 推进到 plan 阶段

## 异常处理

### 关键来源无法访问

**处理**：
1. 尝试替代来源
2. 记录证据缺口
3. 在 `draft.md` 的 uncertainty 中标注

### 来源之间存在重大冲突

**处理**：
1. 优先采用 L1/L2
2. 记录冲突
3. 降低相关结论置信度

### 只有 L3/L4 来源

**处理**：
1. 降低结论强度
2. 明确标注证据等级
3. 列为待验证
