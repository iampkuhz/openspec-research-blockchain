# Apply Workflow - 应用到知识库

## 目标

将通过评审的 `change` 产物应用到 `knowledge/` 主线。

**注意**：本流程由 OpenSpec `apply` 命令执行，不是手动 merge。

## 触发条件

- Review workflow 完成
- 评审结论为 approved 或 approved with minor fixes
- 所有 high severity 问题已修复

## 必需输入

- `openspec/changes/<change-id>/` 完整内容
- `draft.md`（集中 review 稿）
- 评审结论

## 规则加载策略

### 初始加载（workflow 开始时）

| 规则 | 路径 | 用途 |
|------|------|------|
| `repo-governance.md` | `harness/rules/general/` | 仓库治理约束 |
| `update-policy.md` | `harness/rules/general/` | 更新政策（向后兼容处理） |
| `traceability-policy.md` | `harness/rules/general/` | 可追溯性要求 |

**注意**：规则文件在对话中可能被压缩，**步骤 3（执行 Apply）前建议重新读取** `update-policy.md` 确认向后兼容处理。

## 步骤

### 步骤 1：确认 Apply 条件

检查：
- [ ] 评审结论为 approved
- [ ] 所有 high severity 问题已修复
- [ ] `draft.md` 内容完整

### 步骤 2：确定 Apply 位置

根据研究对象类型确定目标位置：

| 类型 | 目标位置 | 产物 |
|------|----------|------|
| **primitive** | `knowledge/analysis/primitives/<domain>/<topic>/` | `artifact.md` |
| **synthesis** | `knowledge/analysis/synthesis/<topic>/` | `artifact.md` |
| **domain** | `knowledge/analysis/domains/<domain>/` | `artifact.md` |
| **decision** | `knowledge/decisions/<domain>/<topic>/` | `artifact.md` + `verdict.md` |

### 步骤 3：执行 Apply

```bash
# 使用 OpenSpec apply 命令
openspec apply --change <change-id>
```

Apply 命令会根据 `openspec/config.yaml` 的 apply 段执行：

1. 将稳定的事实分析提升到 `knowledge/analysis/`
2. 将稳定的场景判断提升到 `knowledge/decisions/`
3. 过程文件（`request.md`、`plan.md`）保留在 `openspec/changes/`
4. 术语区默认并入 `artifact.md` 或 `verdict.md`

### 步骤 4：更新 Indexes

```bash
# 更新 topic 索引
python scripts/general/build_index.py
```

### 步骤 5：提交 Commit

```bash
git add knowledge/
git commit -m "Apply <change-id>: <summary>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
"
```

## 输出

- `knowledge/analysis/` 或 `knowledge/decisions/` 更新
- Git commit

## 完成标准

- [ ] 产物已应用到正确位置
- [ ] Indexes 已更新
- [ ] Commit 已创建

## 异常处理

### Apply 冲突

**处理**：
1. 手动解决冲突
2. 确保不丢失内容
3. 记录冲突原因

### 评审后又有新来源

**处理**：
1. 如 minor，记录到后续更新计划
2. 如 major，创建新的 `change`
