# 图表评审检查清单

## 目的

提供图表评审的系统性检查项，分为三个阶段：
1. **覆盖规划检查** - 评估是否把该画的图想清楚了
2. **Brief 评审** - 评估输入需求的质量（仅限 PlantUML 类型）
3. **图表评审** - 评估输出图的质量

**重要**：本清单用于执行层评审，正式规则来源为 `harness/rules/diagrams/diagram-policy.md`。

---

## 阶段 0: 覆盖规划与类型合规性检查（新增）

**在进入详细评审前，首先检查：**
1. 该对象是否已经明确"需要哪些视图"
2. 图表类型选择是否合规

### 检查项 0: 视图覆盖规划是否完整（primitive / mechanism-heavy 必查）

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 是否先有实体分类表（role / component / data / state / external）？ | | |
| 是否先有图表清单表，说明每张图回答什么问题？ | | |
| 有多角色或 trust assumption 时，是否规划了角色与信任边界总览图？ | | |
| 是否为每个 materially 不同的核心角色规划了内部组件图，或写清可复用 canonical 图？ | | |
| 有跨角色交互时，是否规划了跨角色核心流程图？ | | |
| 有显式状态 / round / epoch / timeout / challenge 时，是否规划了状态图或状态表？ | | |

**违规处理**：
- ❌ 没有实体分类表或图表清单表 → **Blocker**，先补规划再画图
- ❌ 多角色机制缺角色边界图 → **Blocker**
- ❌ 明显 stateful 机制却没有状态视图 → **Major**

### 检查项 1: PlantUML 类型是否在支持范围内

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 如使用 PlantUML，是否为 Architecture 或 Sequence 类型？ | | |
| 如为 Architecture/Sequence，是否通过全局 skill 生成？ | | |
| `diagrams/<id>/diagram.puml` 文件是否存在？ | | |

**违规处理**：
- ❌ 使用 PlantUML 但类型为 State/Activity/Deployment → **Blocker**，必须降级为 Mermaid/表格/ASCII
- ❌ 使用 PlantUML 但 `diagram.puml` 不存在 → **Blocker**，必须重新执行 skill

### 检查项 2: Contract Comment 完整性（PlantUML 类型）

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| PlantUML block 前是否有 `<!-- diagram: ... -->` comment？ | | |
| comment 格式是否正确？ | | |
| `puml` 路径是否指向存在的 `diagram.puml`？ | | |

**验证命令**：
```bash
# 检查 diagram.puml 文件是否存在
ls ./diagrams/<diagram-id>/diagram.puml
```

### 检查项 3: Unsupported Type 硬塞检测

**如何发现"把不支持的图硬塞成 PlantUML"**：

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 是否为状态机图却使用 PlantUML？ | | |
| 是否为部署图却使用 PlantUML？ | | |
| 是否为活动图却使用 PlantUML？ | | |
| 是否为比较总览图却使用 PlantUML？ | | |
| 是否有手写的 `@startuml ... @enduml` 但无 diagram.puml？ | | |

**检测技巧**：
- 搜索 `@startuml` 但无 `<!-- diagram:` → 可能为手写
- 搜索 `stateDiagram` / `activityDiagram` in PlantUML → unsupported type
- 有 diagram 但无 `diagrams/<id>/diagram.puml` → 可能为手写

**违规处理**：
- ❌ Unsupported type 使用 PlantUML → **Major**，建议降级为 Mermaid/表格/ASCII
- ❌ 手写 PlantUML 无 contract → **Blocker**，必须删除或重新执行 skill

---

## 阶段 1: Brief 评审（PlantUML 类型）

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

## 阶段 2: PlantUML 评审（仅限 PlantUML 类型）

### 维度 1: 覆盖性

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 该图回答的问题是否与图表清单一致？ | | |
| 是否把角色、组件、状态区分正确？ | | |
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
```

---

## 阶段 3: Fallback 类型评审（Mermaid/表格/ASCII）

### Mermaid 评审

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| GitHub/GitLab 预览可渲染 | | |
| 无语法错误 | | |
| 复杂度适中（状态<10，节点<15） | | |
| 标签清晰 | | |

### Markdown 表格评审

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 对齐清晰 | | |
| 表头语义明确 | | |
| 列数适中（3-6 列） | | |
| 内容简洁 | | |

### ASCII 草图评审

| 检查项 | 是/否 | 备注 |
|--------|------|------|
| 等宽字体下可读 | | |
| 已标注"ASCII 草图" | | |
| 用于快速说明（非核心图表） | | |

---

## 严重性定义

| 严重性 | 描述 | 处理 |
|--------|------|------|
| **Blocker** | 类型不合规、手写 PlantUML 无 contract、validation 失败 | 必须修复，draft 不得完成 |
| **High** | 事实错误、误导、引用断裂 | 必须修复 |
| **Medium** | 不规范、不一致、描述模糊 | 建议修复 |
| **Low** | 可改进、可优化 | 酌情修复 |

---

## 评审流程

### Step 0: 类型合规性检查（自动化）

```bash
# 执行 contract 校验
python3 scripts/research/validate_draft_diagram_contract.py <change-dir>/draft.md
```

**通过标准**：
- 返回码为 0
- 所有 PlantUML blocks 通过 validation

### Step 1: Brief 评审（PlantUML 类型，生成前）

```
1. 执行 python3 scripts/validate_brief.py（skill 自动执行）
2. 检查完整性、一致性、清晰度、可渲染性
3. 输出 brief-evaluation.yaml
4. 状态为 blocked 时，先修复 brief
```

### Step 2: 自审（生成后）

```
作者自行检查：
- [ ] 类型合规性（非 Architecture/Sequence 不得使用 PlantUML）
- [ ] Contract comment 完整
- [ ] diagram.puml 文件存在
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
- [ ] 修复 Blocker/High 严重性问题
- [ ] 修复或记录 Medium 问题
- [ ] 更新评审记录
```

---

## 评审通过标准

**类型合规性**：
- ✅ 所有 PlantUML 类型为 Architecture 或 Sequence
- ✅ 所有 PlantUML 通过全局 skill 生成
- ✅ 所有 PlantUML 有 `diagram.puml` 文件（位于 `openspec/changes/<change-id>/diagrams/`）
- ✅ `artifact.md` / `draft.md` 中嵌入完整 PlantUML 代码块

**Brief 评审通过**：
- ✅ 无 Blocker 问题
- ✅ Major 问题已修复或记录

**PlantUML 评审通过**：
- ✅ 无 High 严重性问题
- ✅ Medium 问题已修复或记录
- ✅ 简化已标注
- ✅ 来源已引用
- ✅ 评审人已签字

**Fallback 评审通过**：
- ✅ Mermaid 可渲染
- ✅ 表格清晰
- ✅ ASCII 可读

---

## 附录：快速检查命令

```bash
# 检查 diagram.puml 文件是否存在
ls openspec/changes/<change-id>/diagrams/<diagram-id>/diagram.puml

# 搜索手写 PlantUML（无 skill 生成记录）
# 注意：draft.md / artifact.md 中必须嵌入完整代码块
```
