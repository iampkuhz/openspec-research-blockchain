# 图表评审检查清单

## 目的

提供图表评审的系统性检查项。

## 评审维度

### 维度 1: 准确性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 组件/概念是否准确定义 | | |
| 关系语义是否正确 | | |
| 流程顺序是否正确 | | |
| 是否符合官方规范 | | |
| 是否有事实错误 | | |

**评审方法**：
- 对照 L1/L2 来源验证
- 检查术语使用
- 验证流程逻辑

### 维度 2: 抽象层一致性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 是否混用不同抽象层 | | |
| stereotype 是否正确标注 | | |
| 分层是否清晰 | | |
| 关系是否符合层次 | | |

**评审方法**：
- 识别每个组件的 layer
- 检查跨层关系
- 验证标题/注释说明

### 维度 3: 可读性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 组件数量是否合适 (<10) | | |
| 布局是否清晰 | | |
| 标签是否简洁 | | |
| 注释是否必要 | | |
| 颜色使用是否合理 | | |

**评审方法**：
- 5 秒内能否理解主旨
- 打印后是否清晰
- 色盲用户能否区分

### 维度 4: 完整性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 核心组件是否完整 | | |
| 关键关系是否完整 | | |
| 边界情况是否说明 | | |
| 简化是否标注 | | |
| 引用是否完整 | | |

**评审方法**：
- 对照 topic 的 atoms 检查
- 检查是否有缺失环节
- 验证引用来源

### 维度 5: 一致性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 与同一 topic 其他图一致 | | |
| 与其他 topic 的图一致 | | |
| 符号使用一致 | | |
| 命名规范一致 | | |

**评审方法**：
- 对照 diagram-index.md
- 检查组件命名
- 验证关系符号

## 评审流程

### Step 1: 自审

作者完成图后，先自行检查：

```
- [ ] 所有检查项
- [ ] 简化标注
- [ ] 来源引用
```

### Step 2: 技术评审

技术准确性评审：

```
评审人：领域专家
检查：准确性、完整性
输出：技术评审意见
```

### Step 3: 可读性评审

可读性评审：

```
评审人：非本领域人员
检查：能否 5 秒理解主旨
输出：理解障碍点
```

### Step 4: 修订

根据评审意见修订：

```
- [ ] 修复准确性问题
- [ ] 改进可读性
- [ ] 补充缺失内容
- [ ] 更新简化标注
```

## 评审记录格式

```yaml
# 在 diagrams/reviews/<diagram-id>-review.md 中

diagram_id: erc4337-architecture-l2
diagram_path: diagrams/source/erc4337-architecture.puml
review_date: 2024-01-15

reviewers:
  - name: XXX
    role: technical
    reviewed_at: 2024-01-15
  - name: YYY
    role: readability
    reviewed_at: 2024-01-15

issues:
  - id: ISSUE-001
    dimension: accuracy
    severity: high
    description: "EntryPoint 和 Bundler 的关系标注错误"
    suggestion: "应该是 Bundler --> EntryPoint，而非反向"
    status: resolved

  - id: ISSUE-002
    dimension: consistency
    severity: medium
    description: "UserOperation 的 stereotype 未标注"
    suggestion: "添加 <<protocol>> 标注"
    status: resolved

summary:
  accuracy: pass
  consistency: pass
  readability: pass
  completeness: pass
  overall: approved

resolved_at: 2024-01-15
```

## 严重性定义

| 严重性 | 描述 | 处理 |
|--------|------|------|
| High | 事实错误、误导 | 必须修复 |
| Medium | 不规范、不一致 | 建议修复 |
| Low | 可改进、可优化 | 酌情修复 |

## 常见问题模式

### Pattern 1: 关系错误

**症状**：箭头方向错误
**影响**：High
**检查**：对照规范验证

### Pattern 2: 抽象层混用

**症状**：Protocol 和 Ecosystem 混在一起
**影响**：Medium
**检查**：识别每个组件的 layer

### Pattern 3: 过度简化

**症状**：关键组件缺失
**影响**：High
**检查**：对照 atoms 检查

### Pattern 4: 过度复杂

**症状**：组件过多、关系混乱
**影响**：Medium
**检查**：5 秒理解测试

### Pattern 5: 缺少简化标注

**症状**：简化了但未说明
**影响**：Low
**检查**：检查简化说明

## 自动化检查

```bash
# 验证 PlantUML 语法
scripts/diagrams/render.sh --validate <diagram>

# 检查组件命名
scripts/diagrams/validate_diagram_model.py --check-names <diagram>

# 检查引用
scripts/diagrams/check_diagram_references.py <diagram>
```

## 评审通过标准

**必须全部满足**：
- [ ] 无 High 严重性问题
- [ ] Medium 问题已修复或记录
- [ ] 简化已标注
- [ ] 来源已引用
- [ ] 评审人已签字
