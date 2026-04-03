# 图表评审检查清单

## 目的

提供图表评审的系统性检查项，分为两个阶段：
1. **Brief 评审** - 评估输入需求的质量
2. **PlantUML 评审** - 评估输出图的质量

---

## 阶段 1: Brief 评审

### 检查项 1: 完整性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 架构图：层数 ≥ 3 | | |
| 架构图：组件数 ≥ 3 | | |
| 架构图：跨组件流程 ≥ 1 | | |
| 时序图：参与者数 ≥ 2 | | |
| 时序图：消息数 ≥ 1 | | |
| 必填字段完整 (diagram_id, title, summary) | | |

### 检查项 2: 一致性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| ID 唯一性（无重复） | | |
| 引用有效性（from/to 指向存在的组件） | | |
| 层归属有效（component.layer 指向存在的层） | | |
| 术语使用一致 | | |

### 检查项 3: 清晰度

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 标题反映核心内容 | | |
| 摘要说明图的用途 | | |
| 组件/参与者职责描述清晰 | | |
| 流程描述有主谓宾 | | |

### 检查项 4: 可渲染性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 组件数 5-15 个（超过建议分层） | | |
| 流程数 3-15 条（超过建议分解） | | |
| 包含 layout.direction 设置 | | |

### Brief 评审输出

```yaml
# diagrams/reviews/<diagram-id>-brief-review.yaml
brief_path: assets/briefs/xxx.yaml
reviewed_at: 2024-01-15

dimensions:
  completeness: pass|warn|fail
  consistency: pass|warn|fail
  clarity: pass|warn|fail
  renderability: pass|warn|fail

overall: approved|conditional|blocked
issues:
  - severity: blocker|major|minor
    dimension: completeness
    description: 问题描述
    suggestion: 修复建议
```

---

## 阶段 2: PlantUML 评审

### 维度 1: 覆盖性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 所有层已落图 | | |
| 所有组件已落图 | | |
| 所有流程已落图 | | |
| 组件 alias 与 brief 一致 | | |
| 无未经批准的新增组件 | | |

### 维度 2: 准确性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 组件/概念定义准确 | | |
| 关系语义正确 | | |
| 流程顺序正确 | | |
| 符合官方规范 | | |
| 无事实错误 | | |

### 维度 3: 可读性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 5 秒内理解主旨 | | |
| 布局清晰（无重叠/拥挤） | | |
| 标签简洁 | | |
| 注释必要且适度 | | |
| 颜色使用合理 | | |
| 打印后清晰 | | |

### 维度 4: 规范性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 使用纵向布局 (架构图) | | |
| 包含 `skinparam nodesep/ranksep` | | |
| 图例包含（如 brief 要求） | | |
| 箭头标注完整 | | |
| 简化内容已标注 | | |

### 维度 5: 一致性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 与同一 topic 其他图一致 | | |
| 符号使用一致 | | |
| 命名规范一致 | | |
| 配色方案一致 | | |

### PlantUML 评审输出

```yaml
# diagrams/reviews/<diagram-id>-puml-review.yaml
diagram_id: erc4337-architecture-l2
diagram_path: diagrams/source/erc4337-architecture.puml
reviewed_at: 2024-01-15

dimensions:
  coverage: pass|warn|fail
  accuracy: pass|warn|fail
  readability: pass|warn|fail
 规范性：pass|warn|fail
  consistency: pass|warn|fail

overall: approved|conditional|rejected
issues:
  - id: ISSUE-001
    severity: high|medium|low
    dimension: accuracy
    description: 问题描述
    suggestion: 修复建议
    status: open|resolved

summary:
  accuracy: pass
  consistency: pass
  readability: pass
  completeness: pass
 规范性：pass
  overall: approved
```

---

## 严重性定义

| 严重性 | 描述 | 处理 |
|--------|------|------|
| **Blocker/High** | 事实错误、误导、引用断裂 | 必须修复 |
| **Major/Medium** | 不规范、不一致、描述模糊 | 建议修复 |
| **Minor/Low** | 可改进、可优化 | 酌情修复 |

---

## 评审流程

### Step 1: Brief 评审（生成前）

```
1. 执行 python3 scripts/validate_brief.py
2. 检查完整性、一致性、清晰度、可渲染性
3. 输出 brief-evaluation.yaml
4. 状态为 blocked 时，先修复 brief
```

### Step 2: 自审（生成后）

```
作者自行检查：
- [ ] 覆盖性检查
- [ ] 规范性检查
- [ ] 简化标注
- [ ] 来源引用
```

### Step 3: 技术评审

```
评审人：领域专家
检查：准确性、完整性
输出：技术评审意见
```

### Step 4: 可读性评审

```
评审人：非本领域人员
检查：5 秒理解测试
输出：理解障碍点
```

### Step 5: 修订

```
- [ ] 修复 High 严重性问题
- [ ] 修复或记录 Medium 问题
- [ ] 更新评审记录
```

---

## 评审通过标准

**Brief 评审通过**：
- 无 Blocker 问题
- Major 问题已修复或记录

**PlantUML 评审通过**：
- 无 High 严重性问题
- Medium 问题已修复或记录
- 简化已标注
- 来源已引用
- 评审人已签字
