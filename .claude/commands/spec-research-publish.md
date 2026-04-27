---
description: 发布入口，唯一允许从 change 进入 knowledge/** 的 command
argument-hint: "[change-id | change-path]"
---

# spec-research-publish

发布入口。唯一允许从 change 进入 `knowledge/**` 的 command。

用户传入参数：`$ARGUMENTS`（change-id 或 change 路径）

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

## 参考 Skills

本命令的参考 skill 包如下。优先参考对应 skill 的执行逻辑；如果 Claude Code 未自动加载 skill，则按本命令内联步骤执行。

| Capability | Skill name | Skill path |
|---|---|---|
| 生成 publish.md | build-publish-plan | skills/openspec-flow/build-publish-plan/SKILL.md |
| 校验 publish_targets | validate-publish-targets | skills/knowledge-publishing/validate-publish-targets/SKILL.md |
| 渲染 knowledge artifact | render-knowledge-artifact | skills/knowledge-publishing/render-knowledge-artifact/SKILL.md |
| 渲染 decision verdict | render-decision-verdict | skills/knowledge-publishing/render-decision-verdict/SKILL.md |
| 合并 change 到 knowledge | merge-change-into-knowledge | skills/knowledge-publishing/merge-change-into-knowledge/SKILL.md |

## 执行步骤

### 1. 定位 change

读取 `openspec/changes/<change-id>/change.yaml`。

### 2. 检查前置条件

- 检查 `draft.md` 是否存在且内容完整
- 检查 `review.md` 是否存在
  - 如不存在且无明确豁免，停止并建议先调用 `/spec-research-step` 生成 review
- 检查 `publish.md` 是否存在
  - 如不存在，调用 `build-publish-plan` skill 生成

### 3. 校验 publish_targets

调用 `validate-publish-targets)` skill：

- 验证 publish_targets 的路径与 schema.yaml 的 artifact 模型一致
- 验证 decision 类型是否包含 verdict.md target
- 如校验不通过，停止并报告具体不合规项

### 4. 渲染 knowledge artifact

- primitive / synthesis 类型：调用 `render-knowledge-artifact` skill
  - 生成或更新 `knowledge/analysis/<path>/artifact.md`
- decision 类型：
  - 调用 `render-knowledge-artifact` skill 生成 `knowledge/decisions/<path>/artifact.md`
  - 调用 `render-decision-verdict` skill 生成 `knowledge/decisions/<path>/verdict.md`

### 5. 合并到 knowledge 主线

调用 `merge-change-into-knowledge` skill：

- 更新 knowledge 目录的索引文件（如存在）
- 记录发布元数据（发布时间、change-id、来源路径）

## 禁止事项

- **不得跳过 publish.md** 直接写 `knowledge/**`。
- **不得从 request.md 或 plan.md 直接生成 knowledge/**。
- **不得在 review.md 缺失且无明确豁免的情况下发布**。

## 完成总结

汇报：

- 当前 change 路径
- publish.md 定义的 publish_targets
- 发布了哪些文件到 `knowledge/**`
- decision 类型是否生成了 verdict.md
- 是否更新了 knowledge 索引
