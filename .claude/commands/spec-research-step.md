---
description: 推进当前 change 的下一步，自动检测缺失产物并生成
argument-hint: "[change-id | change-path]"
---

# spec-research-step

推进当前 change 的下一步。

用户传入参数：`$ARGUMENTS`（change-id 或 change 路径，可选）

## 语言输出约束

- 所有过程说明、阶段汇报默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## OpenSpec Research Flow Contract

本命令必须遵守当前仓库的 `blockchain-research` schema。

主流程：

```text
request.md -> plan.md -> sources/source-pack.md -> sources/evidence-map.md -> [notes/<source-slug>.md]* -> [claims/<claim-slug>.md]* -> draft.md -> review.md -> publish.md -> knowledge/**
```

执行前必须读取：

- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/schema.yaml`
- 当前 change 的 `change.yaml`
- `openspec/schemas/blockchain-research/profiles/<task_type>.schema.yaml`
- `openspec/schemas/blockchain-research/operations/<change_operation>.schema.yaml`

硬性约束：

- `draft.md` 是当前 change 的唯一主候选产物。
- 不得生成 `work-products/*.md`。
- 不得直接写 `knowledge/**`，除非当前命令是 `/spec-research-publish`，且 `publish.md` 已定义合法映射。
- 复杂任务必须拆成多个 child changes。
- decision 任务必须明确 `decision-criteria.md -> draft.md#Verdict Draft -> decision-verdict.md -> knowledge/decisions/**/verdict.md` 的关系。

## 可用 Skill packages

| Capability | Skill name | Skill path | Fallback |
|---|---|---|---|
| 来源包与证据面构建 | `openspec-build-research-support` | `skills/openspec-flow/build-research-support/SKILL.md` | 使用本命令的内联步骤 |
| 来源提取 | `research-extract-evidence` | `skills/research-authoring/extract-evidence/SKILL.md` | 使用本命令的内联步骤 |
| 来源精读笔记 | `research-write-source-note` | `skills/research-authoring/write-source-note/SKILL.md` | 使用本命令的内联步骤 |
| 草稿生成 | `openspec-build-draft` | `skills/openspec-flow/build-draft/SKILL.md` | 使用本命令的内联步骤 |
| 评审生成 | `openspec-build-review` | `skills/openspec-flow/build-review/SKILL.md` | 使用本命令的内联步骤 |
| Primitive 草稿 | `research-write-primitive-draft` | `skills/research-authoring/write-primitive-draft/SKILL.md` | 使用本命令的内联步骤 |
| Synthesis 草稿 | `research-write-synthesis-draft` | `skills/research-authoring/write-synthesis-draft/SKILL.md` | 使用本命令的内联步骤 |
| Decision 草稿 | `research-write-decision-draft` | `skills/research-authoring/write-decision-draft/SKILL.md` | 使用本命令的内联步骤 |
| 决策标准 | `research-build-decision-criteria` | `skills/research-authoring/build-decision-criteria/SKILL.md` | 使用本命令的内联步骤 |

如果 Claude Code 未自动加载上述 skill，必须按本命令内联步骤执行，不得中止。

## 执行步骤

### 1. 定位 change

如果 `$ARGUMENTS` 为空：

- 扫描 `openspec/changes/` 下最近的未完成 change
- 选择有 `request.md` 但缺少后续产物的 change

如果 `$ARGUMENTS` 指定了 change-id 或路径：

- 读取 `openspec/changes/<change-id>/change.yaml`

### 2. 读取模型

- 根据 `change.yaml` 的 `task_type` 加载对应 profile
- 根据 `change_operation` 加载对应 operation

### 3. 自动检测下一步

按以下优先级检测当前 change 缺少的产物：

| 缺少的文件 | 下一步动作 | 调用的 skill |
|------------|-----------|-------------|
| `sources/source-pack.md` | 生成来源包 | `research-extract-evidence` |
| `sources/evidence-map.md` | 生成证据地图 | `research-extract-evidence` |
| `sources/notes/*.md` | 生成来源笔记 | `research-write-source-note` |
| `sources/claims/*.md` | 提取声明 | `research-extract-evidence` |
| `decision-criteria.md`（仅 decision 类型） | 生成决策标准 | `research-build-decision-criteria` |
| `draft.md` | 生成草稿 | `openspec-build-draft` / `research-write-primitive-draft` / `research-write-synthesis-draft` / `research-write-decision-draft` |
| `review.md` | 生成评审 | `openspec-build-review` |

### 4. 执行下一步

根据步骤 3 的判断，调用对应 skill 生成缺失产物。

如果当前 change 缺少的产物太多（例如既没有 sources 也没有 draft），从优先级最高的第一步开始，**不要一次性生成所有产物**。

### 5. 拆分检查

如果执行过程中发现当前 change 实际需要多个最终 Knowledge artifact：

- 停止当前操作
- 建议用户拆成多个 child changes
- 不继续推进

## 完成总结

汇报：

- 当前 change 路径
- 执行了哪一步（生成了什么文件）
- 下一步建议（调用 `/spec-research-step` 继续，或在 draft 完成后调用 `/spec-research-publish`）
