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

## 默认执行角色

- `publish-agent`

`publish-agent` 除 artifact 提炼外，还负责在 update 场景下执行 impact scan 与兼容性检查。

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
- [ ] 评审结论为 approved 或 approved with minor fixes
- [ ] 所有 high severity 问题已修复
- [ ] `draft.md` 内容完整

### 步骤 2：确定 Apply 位置

根据研究对象类型确定目标位置：

| 类型 | 目标位置 | 产物 |
|------|----------|------|
| **primitive** | `knowledge/analysis/primitives/<domain_id>/<topic_slug>/` | `artifact.md` |
| **synthesis** | `knowledge/analysis/synthesis/<topic_slug>/` | `artifact.md` |
| **decision** | `knowledge/decisions/<domain_id>/<topic_slug>/` | `artifact.md` + `verdict.md` |

domain 是分组概念，不作为独立的 object_type，不提供独立的 artifact.md。

### 步骤 2.5：执行 Apply 前校验

在写入 `knowledge/` 前，必须执行三层校验：

| 校验脚本 | 职责 | 失败处理 |
|----------|------|----------|
| `scripts/general/check_frontmatter.py` | 校验 frontmatter 字段、枚举值、deprecated field 拒绝 | 阻止 apply |
| `scripts/general/validate_knowledge_tree.py` | 校验目录结构、registry 一致性 | 阻止 apply |
| `scripts/research/check_artifact_contract.py` | 校验最小章节集合 | 阻止 apply |

任一脚本返回 error 级别问题，不得写入 `knowledge/`。

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

### 步骤 3.5：执行 Update Impact Scan（update 场景）

如本次为更新现有知识：

1. 判断受影响的长期资产路径
2. 记录兼容性处理方式
3. 明确是否需要 follow-up refresh

### 步骤 4：提交 Commit

```bash
git add knowledge/
git commit -m "Apply <change-id>: <summary>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
"
```

### 步骤 5：归档 Change

Apply 完成后，必须将 change 目录移动到归档位置：

```bash
mv openspec/changes/<change-id>/ openspec/changes/archive/<change-id>/
git add openspec/changes/
git commit -m "Archive <change-id>: <summary>"
```

- 归档时保持目录结构不变
- `sources/`、`diagrams/`、`review/` 等审计线索随 change 一起归档
- 未归档的 change 目录视为"进行中"状态

## 输出

- `knowledge/analysis/` 或 `knowledge/decisions/` 更新
- `openspec/changes/archive/<change-id>/` 归档完成
- Git commit

## 完成标准

- [ ] 产物已应用到正确位置
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
