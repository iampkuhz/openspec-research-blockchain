# Hook System — 统一质量门禁调度

**职责层级**：Harness execution layer。

## 三层分离

| 层 | 文件 | 职责 |
|---|---|---|
| Gate 定义 | `harness/gates/registry.yaml` | machine-readable gate 定义（blocking、artifact、validators） |
| Hook 绑定 | `harness/hooks/registry.yaml` | Claude Code hook event → dispatch.py 映射 |
| Validator 映射 | `scripts/hooks/validators/registry.yaml` | validator name → script 路径映射 |

## 核心原则

1. **Hooks 是确定性质量门禁**，不是人类评审的替代
2. **hooks/registry.yaml 只负责 event → gate runner**，不重复定义 gate
3. **blocking gate fail 应 exit 2**，用于 Claude Code 阻断
4. **validation/*.json** 是每次 change 执行 gate 的结果记录

## 架构概览

```
.claude/settings.json          ← Claude Code 事件绑定（薄入口）
        │
        ▼
scripts/hooks/dispatch.py      ← Gate 调度器：加载 registry、执行 validators、聚合结果
        │
        ├─ harness/gates/registry.yaml        ← Gate 定义（source of truth）
        ├─ scripts/hooks/validators/registry.yaml  ← Validator name → script 映射
        │
        └─ scripts/hooks/validators/          ← Validator 脚本
                ├─ required_files.py
                ├─ markdown_sections.py
                ├─ change_manifest.py
                ├─ child_change_graph.py
                ├─ source_pack.py
                ├─ evidence_map.py
                ├─ draft_contract.py
                ├─ review_readiness.py
                ├─ publish_targets.py
                ├─ decision_verdict.py
                ├─ knowledge_artifact.py
                ├─ knowledge_tree.py
                └─ traceability.py
```

## 数据流

```
Event (post_write / pre_publish / stop)
  → .claude/settings.json
    → dispatch.py --event EVENT --gate-registry ... --validator-registry ...
      → 加载 gates/registry.yaml 获取 gate 定义
      → 加载 validators/registry.yaml 获取脚本路径
      → 根据 gate 选择 validators 并顺序执行
      → 聚合结果，写入 validation/*.json
      → blocking gate fail 时 exit 2
```

## CLI 接口

```bash
# 按 change 和 gate 运行
python3 scripts/hooks/dispatch.py --change openspec/changes/<id> --gate post_draft

# 运行所有适用 gates
python3 scripts/hooks/dispatch.py --change openspec/changes/<id> --all

# 按事件运行
python3 scripts/hooks/dispatch.py --event pre_publish --change openspec/changes/<id>

# JSON 输出
python3 scripts/hooks/dispatch.py --change openspec/changes/<id> --gate post_draft --json

# 列出所有 gates
python3 scripts/hooks/dispatch.py --list-gates
```

## Gate 索引

| Gate | Artifact | Blocking | Validators |
|---|---|---|---|
| `post_request` | request | true | required_files, markdown_sections, change_manifest |
| `post_plan` | plan | true | required_files, markdown_sections, child_change_graph |
| `post_research` | research_support | false | source_pack, evidence_map, traceability |
| `post_draft` | draft | true | draft_contract, markdown_sections, traceability |
| `post_review` | review | true | review_readiness, markdown_sections |
| `pre_publish` | publish | true | publish_targets, traceability, decision_verdict |
| `post_publish` | knowledge | true | knowledge_artifact, knowledge_tree, traceability |
