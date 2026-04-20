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
                ├─ knowledge_artifact.py       → scripts/general/check_knowledge_artifacts.py
                ├─ knowledge_artifact_toc.py   → scripts/general/check_artifact_toc.py
                ├─ draft_diagram_contract.py   → scripts/research/validate_draft_diagram_contract.py
                ├─ document_structure.py       → scripts/general/check_document_structure.py
                ├─ process_file.py             → scripts/general/check_process_files.py
                ├─ unarchived_changes.py       → scripts/general/check_unarchived_changes.py
                ├─ frontmatter.py              → scripts/general/check_frontmatter.py
                ├─ knowledge_tree.py           → scripts/general/validate_knowledge_tree.py
                └─ traceability.py             → scripts/general/check_traceability.py
```

### 数据流

```
Event (PostToolUse / pre-commit / manual)
  → settings.json / .githooks/pre-commit
    → dispatch.py --run --event EVENT [--files ...]
      → 加载 registry.yaml
      → 按 event + path_patterns 匹配规则
      → 按 args_mode 执行 validator adapter
      → 汇总结果，blocking error 则退出码 1
```

---

## Registry 维度说明

| 维度 | 说明 | 示例值 |
|------|------|--------|
| `id` | 校验器唯一标识 | `knowledge-artifact` |
| `event` | 触发事件 | `post_tool_use` / `pre_commit` / `manual` |
| `phases` | 适用研究阶段 | `[draft]` / `[artifact, review]` |
| `path_patterns` | glob 模式（相对于仓库根目录） | `["knowledge/**/*.artifact.md"]` |
| `validator` | adapter 脚本名（相对于 validators/） | `knowledge_artifact.py` |
| `args_mode` | 文件传参方式 | `one_per_file` / `files` / `none` |
| `severity` | 严重性 | `error` / `warning` |
| `blocking` | 是否阻止操作 | `true` / `false` |
| `timeout` | 超时秒数 | `30` |
| `enabled` | 快速开关 | `true` / `false` |
| `description` | 人类可读说明 | — |

---

## 使用方式

### CLI 接口

```bash
# 查看所有注册校验器
python3 scripts/hooks/dispatch.py --list

# 查看特定事件下的校验器
python3 scripts/hooks/dispatch.py --list --event post_tool_use

# 模拟运行（只展示匹配，不执行）
python3 scripts/hooks/dispatch.py --dry-run --event post_tool_use --files path/to/file.md

# 实际运行（post_tool_use 事件）
python3 scripts/hooks/dispatch.py --run --event post_tool_use --files path/to/file.md

# 运行 git staged 文件的 pre_commit 事件
python3 scripts/hooks/dispatch.py --run --event pre_commit --staged

# 手动运行特定 validator
python3 scripts/hooks/dispatch.py --run --event manual --validator traceability --extra-args --topic eip-4337

# JSON 格式输出
python3 scripts/hooks/dispatch.py --list --event post_tool_use --output-json
```

### 作为 Claude Hook 触发

`.claude/settings.json` 已配置为 PostToolUse → dispatch.py → 按 event + path 自动匹配。
不需要在 settings.json 中硬编码每条规则。

### 作为 Git Hook 触发

`.githooks/pre-commit` 委托给 dispatch.py 的 `--event pre_commit --staged` 模式。
自动获取 staged 文件并匹配 registry 中 event=pre_commit 的规则。

---

## 如何扩展

### 新增一个 Validator

1. **编写校验脚本**：放在 `scripts/general/`、`scripts/research/` 或对应目录
   - 接受文件路径作为命令行参数
   - 退出码 0 = 通过，1 = 失败
   - stdout/stderr 输出人类可读信息

2. **创建 adapter**：在 `scripts/hooks/validators/` 新建薄包装脚本
   - 调用原始脚本，传递参数
   - 保留原始退出码和输出
   - 参考已有的 `knowledge_artifact.py` 等

3. **注册规则**：在 `harness/hooks/registry.yaml` 添加条目
   - 设置 event、path_patterns、validator、severity、blocking 等
   - 确保 `id` 唯一

4. **测试**：
   ```bash
   python3 scripts/hooks/dispatch.py --list --event YOUR_EVENT
   python3 scripts/hooks/dispatch.py --dry-run --event YOUR_EVENT --files path/to/file.md
   python3 scripts/hooks/dispatch.py --run --event YOUR_EVENT --files path/to/file.md
   ```

### 新增一个 Event

1. 在 `harness/hooks/registry.yaml` 中添加 `event: YOUR_EVENT` 的规则
2. 在 `.claude/settings.json` 或 `.githooks/` 中添加对应的事件入口
3. 入口格式：调用 `dispatch.py --run --event YOUR_EVENT --files ...`

### 新增一个 Phase Gate

1. 在 `harness/hooks/registry.yaml` 中添加规则，设置 `phases: [YOUR_PHASE]`
2. 设置 `event: manual` 以便在 workflow 阶段切换时手动调用
3. 可选：在 workflow 文档中添加阶段入口说明

### 禁用/启用 Validator

只需修改 `harness/hooks/registry.yaml` 中对应条目的 `enabled: false/true`。
不需要修改任何代码或配置。

### 调整 Path Pattern

修改 `harness/hooks/registry.yaml` 中对应条目的 `path_patterns` 列表。
支持标准 glob 语法：`*`、`**`、`?`、`[...]`。

---

## 与 Phase/Workflow 的对齐

Registry 中的 `phases` 字段与 `harness/rules/_phase_index.yaml` 中的阶段声明对齐：

| Phase | 描述 | 典型 validator |
|-------|------|----------------|
| `request` | 研究请求定义 | `process-file` |
| `plan` | 研究计划生成 | `process-file` |
| `draft` | 集中研究写作 | `draft-diagram-contract`, `document-structure` |
| `artifact` | 长期资产提炼 | `knowledge-artifact`, `knowledge-artifact-toc`, `frontmatter` |
| `review` | 研究评审 | `knowledge-artifact`, `document-structure`, `traceability` |

`event` 与执行层的对应关系：

| Event | 触发源 | 说明 |
|-------|--------|------|
| `post_tool_use` | Claude Code Write/Edit hook | 文件写入时实时校验 |
| `pre_commit` | Git pre-commit hook | 提交前批量校验 |
| `manual` | 手动调用 | 按需运行特定 validator |

---

## 校验器索引

| ID | Event | Path | Severity | Blocking | 说明 |
|----|-------|------|----------|----------|------|
| `knowledge-artifact` | post_tool_use | `knowledge/**/artifact.md`, `knowledge/**/verdict.md` | error | true | 校验 artifact frontmatter 与 contract |
| `knowledge-artifact-toc` | post_tool_use | `knowledge/**/artifact.md`, `knowledge/**/verdict.md` | error | true | 校验 TOC 覆盖 |
| `draft-diagram-contract` | post_tool_use | `openspec/changes/*/draft.md` | error | true | 校验 diagram contract |
| `document-structure` | post_tool_use | `knowledge/**/*.md`, `openspec/changes/**/*.md` | error | true | 校验 Markdown 结构约束 |
| `process-file` | pre_commit | `openspec/changes/*/request.md`, `plan.md` | error | true | 校验 process 文件最小字段 |
| `unarchived-changes` | pre_commit | `knowledge/**` | warning | false | 检查未归档 change（advisory） |
| `frontmatter` | pre_commit | `knowledge/**/*.md` | error | true | 校验 frontmatter（默认关闭） |
| `knowledge-tree` | pre_commit | `knowledge/**` | error | true | 校验 knowledge 树结构（默认关闭） |
| `traceability` | manual | — | warning | false | 检查可追溯性（手动指定 --topic） |
