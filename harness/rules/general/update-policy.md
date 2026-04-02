# 知识更新政策

## 目的

定义如何安全地更新现有知识，确保一致性和向后兼容。

## 更新触发条件

### 必须更新知识当

1. **来源变更**
   - 规范更新（EIP 版本升级）
   - 参考实现有 breaking changes
   - 官方宣布废弃某机制

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
1. 创建 OpenSpec change
   - 类型：update-topic 或 refactor-topic
   - 在 request.md 说明更新原因

2. 读取现有知识
   - 读取 topic 的 artifact.md 或 atoms
   - 读取相关的 comparison/principle

3. 评估影响范围
   - 哪些 atoms 需要更新
   - 哪些 comparisons 需要重新评估
   - 哪些 topics 依赖此知识

4. 执行更新
   - 更新目标 atoms
   - 更新 claims
   - 更新 changelog.md

5. 验证
   - 运行 traceability 检查
   - 运行术语一致性检查
   - Review

6. Merge
   - 将 change 产物合并到 knowledge/
   - 更新 indexes
```

### 紧急更新流程

仅适用于修复严重错误：

```
1. 创建 minimal change 记录
2. 直接修复 knowledge/
3. 在 changelog.md 说明紧急原因
4. 后续补充完整 evidence
```

## 更新类型

### Type 1: Atom 更新

**影响范围**：单个 atom
**流程**：轻量流程
**示例**：
```yaml
change_type: atom-update
target: eip-4337/atoms/core-mechanism.md
sections:
  - "Gas Calculation"
reason: "补充 EIP-3860 影响"
```

### Type 2: Topic 更新

**影响范围**：整个 topic
**流程**：标准流程
**示例**：
```yaml
change_type: topic-update
target: eip-4337
atoms:
  - core-mechanism
  - limits-and-assumptions
reason: "EIP-4337 规范版本从 v0.6 更新到 v0.7"
```

### Type 3: 重构 Topic

**影响范围**：topic 结构
**流程**：完整流程 + 额外 review
**示例**：
```yaml
change_type: topic-refactor
target: eip-4337
changes:
  - 拆分 core-mechanism 为 mechanism-overview 和 gas-mechanism
  - 新增 integration-points atom
reason: "提高原子化程度"
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
- 删除 atom 而不留说明
- 改变 atom 语义

**必须**：
- 在 changelog.md 记录结构变更
- 更新 topic-template 索引

### Claim 兼容性

当更新导致 claim 变化：

| 变化类型 | 处理方式 |
|----------|----------|
| 修正错误 | 标记 claim 为 deprecated，新增 claim |
| 补充细节 | 更新原 claim，记录版本 |
| 改变结论 | 保留原 claim 为 historical，新增 claim |

## 依赖管理

### 更新有依赖的 topic

当 topic A 依赖 topic B，更新 B 时：

```
1. 检查 A 的 dependencies.md
2. 评估 B 的更新是否影响 A
3. 如影响，触发 A 的 refresh
4. 在 A 的 changelog.md 记录
```

### 依赖强度

```yaml
dependencies:
  - topic: eip-4337
    strength: strong  # B 的变化很可能影响 A
    budget: deep      # 需要深度 re-read

  - topic: account-abstraction-domain
    strength: light   # 仅复用术语
    budget: focused   # 仅需检查术语一致性
```

## Changelog 格式

```yaml
# 在 topic/changelog.md 中
changelog:
  - version: "1.1"
    date: 2024-01-15
    change_id: primitive-eip-4337-deep-dive-pass-2
    type: update

    summary: "补充 gas 计算细节，更新术语定义"

    changes:
      - atom: core-mechanism
        action: updated
        sections:
          - "Gas Calculation"
        summary: "补充 EIP-3860 对 initCode 的影响"

      - atom: definition
        action: updated
        sections:
          - "Key Terms"
        summary: "更新 UserOperation 定义，明确边界"

    breaking_changes: []
    deprecated_claims:
      - claim-020
      reason: "旧 gas 计算方式不再准确"

    new_claims:
      - claim-025
      - claim-026

    related_changes:
      - change_id: evolution-aa-eip-pass-2
        relationship: "consumes this update"
```

## 版本标记

### Topic 版本

```yaml
# 在 topic overview.md 的 frontmatter 中
---
topic: eip-4337
version: "1.1"
last_updated: 2024-01-15
last_change_id: primitive-eip-4337-deep-dive-pass-2
---
```

### Atom 版本

```yaml
# 在 atom 文件顶部
<!--
  Atom: core-mechanism
  Version: 1.1
  Last Updated: 2024-01-15
  Change: primitive-eip-4337-deep-dive-pass-2
-->
```
