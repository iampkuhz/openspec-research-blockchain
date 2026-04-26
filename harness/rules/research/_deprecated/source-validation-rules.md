# 来源验证规则

## 目的

规范来源的获取、验证和记录流程。

## 来源获取流程

### 步骤 0: 联网通道选择与安全检查

**优先顺序**：
1. 搜索：优先 `fastmcp-gateway` 的 `searxng_search_web`
2. 正文提取：优先 `crawl4ai` 的 `md`
3. 仅当首选 MCP 当前不可用时，才回退到 `WebFetch` / `WebSearch` 或其他本地通道

**重要**：在使用回退通道（如 `WebFetch`）前，必须确认目标域名是否被安全策略拦截。

**拦截场景**：
- `claude.ai` 域名被企业安全策略 blocking
- 特定域名被标记为 "Unable to verify if domain is safe to fetch"

**处理方式**：
1. **立即停止**当前回退通道的重复尝试，不要重复触发
2. **记录拦截**：在 `request.md` 和 `plan.md` 的验证状态中标注 `[未验证] 安全策略拦截`
3. **替代方案**：
   - 如 `searxng_search_web` 可用，优先回到 SearXNG 搜索第三方来源
   - 否则使用 WebSearch 获取第三方来源（如 Mirror、Medium、GitHub）
   - 依赖已有的 L1/L2 来源知识
   - 在 `draft.md` 的"证据缺口"中明确记录

**示例标注**：
```markdown
| 来源 | 类型 | 说明 | 验证状态 |
|------|------|------|----------|
| curve.fi/stableswap-paper.pdf | whitepaper | 官方技术白皮书 | [未验证] 安全策略拦截 |
```

**规约更新**：此规则已记录在 `harness/rules/research/source-validation-rules.md`。

### 步骤 1: 识别来源类型

```yaml
source_types:
  primary:
    - 官方规范文档
    - EIP / RFC
    - 白皮书
    - 参考实现代码

  secondary:
    - 官方博客
    - 技术文档
    - Release notes

  tertiary:
    - 第三方分析
    - 社区讨论
    - 媒体文章
```

### 步骤 2: 获取来源

**必须记录**：
- 获取日期
- 来源 URL
- 归档方式（截图/PDF/文本）

**禁止**仅保存 URL。

### 步骤 3: 提取关键信息

```markdown
# Source Excerpt: <source_id>

**来源**: <title>
**URL**: <url>
**获取日期**: <date>
**位置**: <文档中的位置>

## 相关内容

> [引用原文]

## 相关性分析

[为什么这个来源重要]

## 支持的 Claims

- claim-xxx
- claim-yyy
```

## 来源验证

### 验证等级

| 等级 | 验证方式 | 可信度 |
|------|----------|--------|
| Verified | 官方来源 + 交叉验证 | 最高 |
| Confirmed | 官方来源 | 高 |
| Unverified | 单一来源 | 中 |
| Disputed | 多个冲突来源 | 低 |

### 验证步骤

1. **检查来源权威性**
   - 是否官方发布
   - 作者是否是核心开发者
   - 是否有社区审核

2. **检查时效性**
   - 发布日期
   - 是否有更新版本
   - 是否已废弃

3. **交叉验证**
   - 多个独立来源是否一致
   - 实现是否与规范一致
   - 是否有反例

## 来源冲突处理

### 发现冲突时

1. **记录冲突**：
   ```yaml
   conflict_id: CONF-SRC-001
   description: "Tendermint 延迟数据冲突"
   sources:
     - source_a: Cosmos 文档 (L2)
     - source_b: 第三方测试 (L4)
   discrepancy: "1s vs 2s"
   resolution: 采用 L2 来源
   ```

2. **解决优先级**：
   - L1 > L2 > L3 > L4
   - 更新 > 旧版本
   - 官方 > 第三方

3. **记录决策**：
   - 采用哪个来源
   - 为什么
   - 保留冲突记录

## 来源归档

### 必须归档的场景

1. 关键证据来源
2. 可能被修改的网页
3. 重要但可能删除的内容

### 归档方式

| 类型 | 工具 | 用途 |
|------|------|------|
| PDF | 浏览器打印 | 规范文档 |
| 截图 | 完整网页截图 | 博客文章 |
| 文本 | 复制全文 | 短内容 |
| Wayback | archive.is | 网页快照 |

### 归档元数据

```yaml
archive:
  original_url: https://...
  archived_url: https://...
  archived_at: 2024-01-15
  archive_type: pdf
  archive_path: sources/fetched/eip-4337.pdf
```

## 来源质量评估

### 评估维度

| 维度 | 问题 |
|------|------|
| 权威性 | 是否官方发布？ |
| 时效性 | 是否最新？ |
| 完整性 | 是否覆盖所需内容？ |
| 可验证性 | 是否可交叉验证？ |
| 稳定性 | 是否可能变更？ |

### 评分

```yaml
source_quality:
  source_id: eip-4337
  scores:
    authority: 5    # 官方标准
    timeliness: 4   # 最新但可能更新
    completeness: 5 # 完整规范
    verifiability: 5 # 可交叉验证
    stability: 5    # 标准文档稳定
  overall: 4.8
  recommendation: 核心来源
```

## 来源包格式

```yaml
# source-pack.yaml
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
    archived:
      archived: true
      archive_path: <path>
      archived_at: <date>
    relevant_atoms:
      - definition
      - core-mechanism
    supported_claims:
      - claim-001
      - claim-002
    confidence: high|medium|low
    quality_score: 4.5
    notes: <可选说明>
```
