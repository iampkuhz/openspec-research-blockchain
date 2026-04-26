# Hook System — 统一校验调度

**职责层级**：Harness execution layer。
- 不定义 OpenSpec 正式规则（`openspec/specs/`）
- 不替代 workflow 执行步骤（`harness/workflows/`）
- 只负责把正式规则映射为可执行、可路由、可组合的校验条目

**边界原则**：
- 校验的「什么算通过」属于 OpenSpec 正式规则
- 校验的「何时触发、对谁触发、以什么严重性执行」属于本注册表
- 校验的「如何执行」属于 validator adapter 脚本

---

## 核心原则

1. **Hooks 是确定性质量门禁**，不是人类评审的替代
2. **Hooks 不替代 review.md**：review 是独立的人类评审过程
3. **Hooks 优先读取 change.yaml**，不通过路径硬猜 task_type
4. **Hooks 不定义 artifact 正式语义**，那是 OpenSpec 的职责

## 三类 Gate

| Gate 类型 | 触发时机 | 推荐 validator |
|---|---|---|
| post-write | 文件写入后 | `required_files`、`markdown_sections`、`source_pack`、`evidence_map`、`document_structure` |
| pre-publish | publish.md 生成前 | `publish_targets`、`traceability` |
| post-publish | knowledge 文件写入后 | `knowledge_artifact`、`knowledge_artifact_toc`、`document_structure` |

## 架构概览

```
.claude/settings.json          ← Claude Code 事件绑定（薄入口）
.githooks/pre-commit           ← Git pre-commit（薄入口）
        │
        ▼
scripts/hooks/dispatch.py      ← 统一调度器：匹配 + 执行 + 报告
        │
        ├─ harness/hooks/registry.yaml    ← 声明式注册表
        │
        └─ scripts/hooks/validators/      ← Validator adapter 层
                ├─ knowledge_artifact.py
                ├─ knowledge_artifact_toc.py
                ├─ draft_diagram_contract.py
                ├─ document_structure.py
                ├─ process_file.py
                ├─ unarchived_changes.py
                ├─ frontmatter.py
                ├─ knowledge_tree.py
                ├─ traceability.py
                ├─ required_files.py
                ├─ markdown_sections.py
                ├─ source_pack.py
                ├─ evidence_map.py
                └─ work_product.py (legacy, 语义已迁移为 draft_contract)
```

## 数据流

```
Event (PostToolUse / pre-commit / manual)
  → settings.json / .githooks/pre-commit
    → dispatch.py --run --event EVENT [--files ...]
      → 加载 registry.yaml
      → 按 event + path_patterns 匹配规则
      → 按 args_mode 执行 validator adapter
      → 汇总结果，blocking error 则退出码 1
```

## CLI 接口

```bash
# 查看所有注册校验器
python3 scripts/hooks/dispatch.py --list

# 查看特定事件下的校验器
python3 scripts/hooks/dispatch.py --list --event post_tool_use

# 模拟运行（只展示匹配，不执行）
python3 scripts/hooks/dispatch.py --dry-run --event post_tool_use --files path/to/file.md

# 实际运行
python3 scripts/hooks/dispatch.py --run --event post_tool_use --files path/to/file.md

# 运行 git staged 文件的 pre_commit 事件
python3 scripts/hooks/dispatch.py --run --event pre_commit --staged

# 手动运行特定 validator
python3 scripts/hooks/dispatch.py --run --event manual --validator traceability --extra-args --topic eip-4337
```

## Validator 索引

| ID | Event | Path | Severity | Blocking | 说明 |
|---|---|---|---|---|---|
| `knowledge-artifact` | post_tool_use | `knowledge/**/artifact.md`, `knowledge/**/verdict.md` | error | true | 校验 artifact frontmatter 与 contract |
| `knowledge-artifact-toc` | post_tool_use | `knowledge/**/artifact.md`, `knowledge/**/verdict.md` | error | true | 校验 TOC 覆盖 |
| `draft-diagram-contract` | post_tool_use | `openspec/changes/*/draft.md` | error | true | 校验 diagram contract |
| `document-structure` | post_tool_use | `knowledge/**/*.md`, `openspec/changes/**/*.md` | error | true | 校验 Markdown 结构约束 |
| `process-file` | pre_commit | `openspec/changes/*/request.md`, `plan.md` | error | true | 校验 process 文件最小字段 |
| `unarchived-changes` | pre_commit | `knowledge/**` | warning | false | 检查未归档 change（advisory） |
| `frontmatter` | pre_commit | `knowledge/**/*.md` | error | true | 校验 frontmatter（默认关闭） |
| `knowledge-tree` | pre_commit | `knowledge/**` | error | true | 校验 knowledge 树结构（默认关闭） |
| `traceability` | manual | — | warning | false | 检查可追溯性（手动指定 --topic） |

## 与 Phase/Workflow 的对齐

Registry 中的 `phases` 字段与 `harness/governance/quality-gates.md` 中的 gate 声明对齐。
