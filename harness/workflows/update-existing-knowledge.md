# Update Existing Knowledge Workflow - 更新现有知识

## 目标

安全地更新 `knowledge/` 中的现有研究，确保一致性和向后兼容。

## 触发条件

- 规范更新（EIP 版本升级）
- 发现错误需要修正
- 生态有重大变化

## 必需输入

- 现有研究路径
- 更新原因
- 新来源或新信息

## 规则加载策略

### 初始加载（workflow 开始时）

| 规则 | 路径 | 用途 |
|------|------|------|
| `update-policy.md` | `harness/rules/general/` | 更新政策（向后兼容处理） |
| `traceability-policy.md` | `harness/rules/general/` | 可追溯性要求 |
| `repo-governance.md` | `harness/rules/general/` | 禁止直接修改 knowledge/ |

**注意**：规则文件在对话中可能被压缩，**步骤 6（处理向后兼容）和步骤 8（Apply）前建议重新读取** `update-policy.md`。

## 步骤

### 步骤 1：读取现有知识

```bash
# 读取现有 artifact.md
cat knowledge/analysis/<path>/<topic>/artifact.md
```

### 步骤 2：评估更新范围

确定更新类型：

| 类型 | 描述 | 示例 |
|------|------|------|
| `minor-update` | 小幅更新 | 补充细节、修正错误 |
| `major-update` | 大幅更新 | 规范版本升级、核心机制变化 |
| `refactor` | 重构 | 结构调整、内容重组 |

### 步骤 3：创建 OpenSpec Change

**必须**创建 change，禁止直接修改 `knowledge/`。

```bash
openspec new change <name> --schema blockchain-research
```

命名：`update-<topic>-<reason>-pass-1`

示例：
- `update-eip-4337-spec-v07-pass-1`
- `update-eip-7702-scope-expansion-pass-1`

### 步骤 4：对比新旧内容

在 `openspec/changes/<change-id>/` 中创建对比文档：

```markdown
# 内容对比

## 主要变化

1. [变化 1]
2. [变化 2]

## 影响分析

- 哪些部分需要更新
- 是否影响依赖者
```

### 步骤 5：执行更新

在 change 目录中更新 `draft.md`，反映新内容。

### 步骤 6：处理向后兼容

**破坏性变更处理**：

1. 在 `draft.md` 中明确标注变化
2. 保留旧内容为历史背景（如需要）
3. 记录影响范围

### 步骤 7：评审

执行 `review-workflow.md`。

### 步骤 8：Apply

通过 OpenSpec apply 流程提升到 `knowledge/`。

## 输出

- `openspec/changes/<change-id>/` 完整内容
- 评审记录
- Git commit

## 完成标准

- [ ] 更新内容已记录
- [ ] 破坏性变更已标注
- [ ] 评审通过
- [ ] Apply 完成

## 异常处理

### 更新导致重大破坏

**处理**：
1. 回滚
2. 重新评估更新范围
3. 考虑版本并存

### 依赖方反对

**处理**：
1. 记录反对意见
2. 评估是否继续
3. 可能考虑版本并存
