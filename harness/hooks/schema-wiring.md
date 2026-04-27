# Schema Wiring 触发点说明

本文档描述 `blockchain-research` schema package 中，各个组件如何串联以及 gate/hook 校验的触发时机。

## 串联关系

```
change.yaml
  -> schema/profile/operation
  -> harness/gates/registry.yaml          ← Gate 定义（source of truth）
  -> scripts/hooks/validators/registry.yaml  ← Validator name → script 映射
  -> validation/*.json                    ← Gate 执行结果记录
```

## change.yaml 如何声明 validators

change.yaml 中的 validators 段声明三类校验器：

```yaml
validators:
  base:
    - required_files
    - markdown_sections
  profile:
    - traceability
  operation:
    - publish_targets
```

- `base`：公共校验器，对所有 task_type 生效
- `profile`：按 task_type 加载的 profile 专属校验器
- `operation`：按 change_operation 加载的操作专属校验器

## Gate Registry 如何定义 gates

`harness/gates/registry.yaml` 是 gate 定义的 **machine-readable source of truth**：

```yaml
gates:
  post_draft:
    stage: post_draft
    blocking: true
    artifact: draft
    files:
      required:
        - draft.md
    validators:
      - draft_contract
      - markdown_sections
      - traceability
    rule_refs:
      - harness/rules/artifacts/draft-rules.md
    output:
      path: validation/post-draft.json
```

## Validator Registry 如何映射脚本

`scripts/hooks/validators/registry.yaml` 负责 validator name → script 路径映射：

```yaml
validators:
  required_files:
    script: scripts/hooks/validators/required_files.py
    input_contract: change_context
    output_contract: gate_result

  draft_contract:
    script: scripts/hooks/validators/draft_contract.py
    input_contract: artifact_file
    output_contract: gate_result
```

## Hook 绑定如何触发 Gate

`harness/hooks/registry.yaml` 只负责 hook event → dispatch.py 映射：

```yaml
hook_bindings:
  post_write:
    command: "python scripts/hooks/dispatch.py --event post_write --gate-registry ..."
  pre_publish:
    command: "python scripts/hooks/dispatch.py --event pre_publish --gate pre_publish --gate-registry ..."
  stop:
    command: "python scripts/hooks/dispatch.py --event stop --gate-registry ..."
```

## 调用链

```
1. openspec/config.yaml
   → 注册 blockchain-research schema package
   → 指向 openspec/schemas/blockchain-research/schema.yaml

2. schema.yaml
   → x_imports.base 指向 ./base.schema.yaml（公共契约）
   → 根据 task_type 选择 x_profiles/*.schema.yaml
   → 根据 change_operation 选择 x_operations/*.schema.yaml
   → 提供 x_templates/* 作为模板源

3. openspec/changes/<change-id>/change.yaml（由 change.yaml 模板实例化）
   → 声明 task_type / change_operation / execution_scope
   → 声明 artifacts 及其路径 / glob
   → 声明 validators（base / profile / operation 分组）
   → 声明 publish_targets（from → to → type）

4. harness/gates/registry.yaml
   → 定义每个 gate 的 blocking、artifact、validators、rule_refs、output

5. scripts/hooks/validators/registry.yaml
   → validator name → script 路径映射

6. scripts/hooks/dispatch.py
   → 加载 gate registry 和 validator registry
   → 构建 change context
   → 根据 gate 选择 validators 并顺序执行
   → 聚合结果，写入 validation/*.json
   → blocking gate fail 时 exit 2
```

## 关键原则

1. **hooks 不通过路径硬猜语义**：校验器应优先读取 `change.yaml` 中的 `task_type`、`profile` 和 `validators` 来决定运行什么检查。
2. **draft.md 是唯一主候选产物**：不再使用 work-products/*.md 作为正式流程。
3. **schema 是统一的**：`schema.yaml` 是入口，不是四套独立 schema。base + x_profiles + x_operations 共同构成一个 schema package。
4. **gate source of truth 在 gates/registry.yaml**，不在 quality-gates.md 或 hooks/registry.yaml。
