# 知识更新政策

## 目的

定义如何安全地更新现有知识，确保一致性和向后兼容。

## 更新触发条件

### 必须更新知识当

1. **来源变更**
   - 规范/标准更新（如 EIP、RFC、协议规范版本升级）
   - 参考实现有 breaking changes
   - 官方宣布废弃某机制或特性

2. **发现错误**
   - 机制描述有误
   - 术语使用错误
   - 证据等级不足的主张被证伪

3. **知识演进**
   - 新的 primitive 被定义
   - 新的比较维度出现
   - 生态有重大变化

### 不需要更新当

1. 仅文字表述优化（不影响语义）
2. 补充示例（不改变机制）
3. 格式调整

## 更新流程

### 标准更新流程

```
1. 创建 OpenSpec `change`
   - 类型：update-topic 或 refactor-topic
   - 在 request.md 说明更新原因

2. 读取现有知识
   - 读取 `topic` 的 artifact.md 或 `atom`s
   - 读取相关的 comparison/principle

3. 评估影响范围
   - 哪些 `atom`s 需要更新
   - 哪些 comparisons 需要重新评估
   - 哪些 `topic`s 依赖此知识

4. 执行更新
   - 更新目标 `atom`s
   - 更新 `claim`s
   - 更新 changelog.md

5. 验证
   - 运行 `traceability` 检查
   - 运行术语一致性检查
   - Review

6. Merge
   - 将 `change` 产物合并到 knowledge/
   - 更新 indexes
```

### 紧急更新流程

仅适用于修复严重错误：

```
1. 创建 minimal `change` 记录
2. 直接修复 knowledge/
3. 在 changelog.md 说明紧急原因
4. 后续补充完整 `evidence`
```

## 更新类型

### Type 1: Atom 更新

**影响范围**：单个 `atom`
**流程**：轻量流程

**request.md 模板**：
```yaml
change_type: atom-update
target: <topic>/<atom-name>.md
sections:
  - <section-name>
reason: <更新原因>
```

### Type 2: Topic 更新

**影响范围**：整个 `topic`
**流程**：标准流程

**request.md 模板**：
```yaml
change_type: topic-update
target: <topic-name>
atoms:
  - <atom-1>
  - <atom-2>
reason: <更新原因，如规范版本升级>
```

### Type 3: 重构 Topic

**影响范围**：`topic` 结构
**流程**：完整流程 + 额外 review

**request.md 模板**：
```yaml
change_type: topic-refactor
target: <topic-name>
changes:
  - <变更描述 1>
  - <变更描述 2>
reason: <重构原因>
```

## 向后兼容性

### 术语兼容性

**禁止**在不通知的情况下：
- 重命名已有术语
- 改变术语边界
- 移除已定义的术语

**必须**：
- 在 changelog.md 中标注 breaking changes
- 保留 deprecated terms 的说明
- 更新所有引用点

### 结构兼容性

**禁止**：
- 删除 `atom` 而不留说明
- 改变 `atom` 语义

**必须**：
- 在 changelog.md 记录结构变更
- 更新 topic-template 索引

### Claim 兼容性

当更新导致 `claim` 变化：

| 变化类型 | 处理方式 |
|----------|----------|
| 修正错误 | 标记 `claim` 为 deprecated，新增 `claim` |
| 补充细节 | 更新原 `claim`，记录版本 |
| 改变结论 | 保留原 `claim` 为 historical，新增 `claim` |

## 依赖管理

### 更新有依赖的 topic

当 `topic` A 依赖 `topic` B，更新 B 时：

```
1. 检查 A 的 dependencies.md
2. 评估 B 的更新是否影响 A
3. 如影响，触发 A 的 refresh
4. 在 A 的 changelog.md 记录
```

### 依赖强度定义

在 `dependencies.md` 中声明依赖关系：

```yaml
dependencies:
  - topic: <topic-name>
    strength: <strong|light>
    budget: <deep|focused>
```

**依赖强度枚举**：

| strength | 说明 | 触发 refresh 条件 |
|----------|------|------------------|
| `strong` | B 的变化很可能影响 A | B 的任何更新 |
| `light` | 仅复用术语或概念 | B 的核心机制变化 |

**检查预算枚举**：

| budget | 说明 | 检查范围 |
|--------|------|----------|
| `deep` | 需要深度 re-read | 全文检查 + claims 验证 |
| `focused` | 仅需检查特定方面 | 依赖的相关 atoms |

## Changelog 格式

### 文件位置

`changelog.md` 必须位于 `topic` 目录下。

### 必填字段

每个 changelog 条目必须包含：

```yaml
changelog:
  - version: "<semver 版本>"
    date: <YYYY-MM-DD>
    change_id: <change-id>
    type: <update|refactor>

    summary: "<更新摘要>"

    changes:
      - atom: <atom-name>
        action: <updated|added|removed|renamed>
        sections:
          - <section-name>
        summary: "<变更摘要>"

    breaking_changes: []  # 如有，列出并说明
    deprecated_claims: [] # 如有，列出 claim IDs
    new_claims: []        # 如有，列出 claim IDs

    related_changes:
      - change_id: <related-change-id>
        relationship: "<关系说明>"
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | Topic 版本号，遵循 semver |
| `date` | date | 更新日期 |
| `change_id` | string | 对应的 change ID |
| `type` | enum | 更新类型：`update` 或 `refactor` |
| `summary` | string | 本次更新的高层摘要 |
| `changes` | array | 详细变更列表 |
| `changes[].atom` | string | 被更新的 atom 名称 |
| `changes[].action` | enum | 操作类型 |
| `changes[].sections` | array | 被更新的具体章节 |
| `changes[].summary` | string | 该变更的摘要 |
| `breaking_changes` | array | Breaking changes 列表 |
| `deprecated_claims` | array | 被废弃的 claim IDs |
| `new_claims` | array | 新增的 claim IDs |
| `related_changes` | array | 相关的其他 changes |

## 版本标记

### Topic 版本格式

在 topic overview 文件（如 `overview.md`）的 frontmatter 中声明：

```yaml
---
topic: <topic-name>
version: "<semver 版本>"
last_updated: <YYYY-MM-DD>
last_change_id: <change-id>
---
```

### Atom 版本格式

在 `atom` 文件顶部使用 HTML 注释声明：

```html
<!--
  Atom: <atom-name>
  Version: <semver 版本>
  Last Updated: <YYYY-MM-DD>
  Change: <change-id>
-->
```

### 版本号规范

遵循 semver 格式：`<major>.<minor>.<patch>`

| 变更类型 | 版本号更新 |
|----------|------------|
| breaking change | `major` + 1 |
| 新增内容/大幅更新 | `minor` + 1 |
| 小幅修正/勘误 | `patch` + 1 |
