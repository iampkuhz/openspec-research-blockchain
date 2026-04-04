# Apply Workflow - 应用到知识库

## Goal

将通过评审的 `change` 产物应用到 `knowledge/` 主线。

**注意**：本流程由 OpenSpec `apply` 命令执行，不是手动 merge。

## Trigger

- Review workflow 完成
- 评审结论为 approved 或 approved with minor fixes
- 所有 high severity 问题已修复

## Required Inputs

- `openspec/changes/<change-id>/` 完整内容
- `draft.md`（集中 review 稿）
- 评审结论

## Rule Set to Load

- harness/rules/general/repo-governance.md
- harness/rules/general/update-policy.md
- harness/rules/general/traceability-policy.md

## Step-by-Step Procedure

### Step 1: 确认 Apply 条件

检查：
- [ ] 评审结论为 approved
- [ ] 所有 high severity 问题已修复
- [ ] `draft.md` 内容完整

### Step 2: 确定 Apply 位置

根据研究对象类型确定目标位置：

| 类型 | 目标位置 | 产物 |
|------|----------|------|
| **primitive** | `knowledge/analysis/primitives/<domain>/<topic>/` | `artifact.md` |
| **synthesis** | `knowledge/analysis/synthesis/<topic>/` | `artifact.md` |
| **domain** | `knowledge/analysis/domains/<domain>/` | `artifact.md` |
| **decision** | `knowledge/decisions/<domain>/<topic>/` | `artifact.md` + `verdict.md` |

### Step 3: 执行 Apply

```bash
# 使用 OpenSpec apply 命令
openspec apply --change <change-id>
```

Apply 命令会根据 `openspec/config.yaml` 的 apply 段执行：

1. 将稳定的事实分析提升到 `knowledge/analysis/`
2. 将稳定的场景判断提升到 `knowledge/decisions/`
3. 过程文件（`request.md`、`plan.md`）保留在 `openspec/changes/`
4. 术语区默认并入 `artifact.md` 或 `verdict.md`

### Step 4: 更新 Indexes

```bash
# 更新 topic 索引
python scripts/general/build_index.py
```

### Step 5: 提交 Commit

```bash
git add knowledge/
git commit -m "Apply <change-id>: <summary>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
"
```

## Outputs

- `knowledge/analysis/` 或 `knowledge/decisions/` 更新
- Git commit

## Done Criteria

- [ ] 产物已应用到正确位置
- [ ] Indexes 已更新
- [ ] Commit 已创建

## Failure Handling

### Apply 冲突

**处理**：
1. 手动解决冲突
2. 确保不丢失内容
3. 记录冲突原因

### 评审后又有新来源

**处理**：
1. 如 minor，记录到后续更新计划
2. 如 major，创建新的 `change`
