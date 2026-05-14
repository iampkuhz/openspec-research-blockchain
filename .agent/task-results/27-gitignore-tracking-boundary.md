# Task 27 — .gitignore Tracking Boundary Fix

## 复现命令

```bash
# 确认误伤
git check-ignore -v scripts/hooks/lib/gate_result.py
# 输出: .gitignore:30:lib/  scripts/hooks/lib/gate_result.py

git check-ignore -v openspec/changes/README.md
# 输出: .gitignore:68:/openspec/changes/  openspec/changes/README.md

# 确认未追踪
git ls-files --stage scripts/hooks/lib/gate_result.py openspec/changes/README.md
# 输出: 空（两个文件都不在索引中）
```

## 根因

1. `scripts/hooks/lib/gate_result.py` 被 `.gitignore` 第 30 行通用 `lib/` 规则匹配。该规则原意是忽略 Python build artifact 中的 `lib/` 目录，但意外匹配了 `scripts/hooks/lib/`。
2. `openspec/changes/README.md` 被第 9 行 `!openspec/changes/README.md` negate 规则允许，但被第 68 行 `/openspec/changes/` 重新忽略。git 使用最后匹配规则，negate 被覆盖。

## 修复内容

### `.gitignore` 变更

**第 30 行 `lib/` 之后新增：**
```
# 但追踪 hooks 核心 helper（不是 Python build artifact）
!scripts/hooks/lib/
!scripts/hooks/lib/*.py
```

**第 68 行 `/openspec/changes/` 替换为注释：**
```
# /openspec/changes/ — 默认忽略已在第 8 行声明；negate 规则在第 9-12 行
# 此处不再重复，避免覆盖前面的 !openspec/changes/README.md
```

### 整理效果

- `openspec/changes/*`（第 8 行）：默认忽略 change 目录内容
- `!openspec/changes/README.md`（第 9 行）：允许索引文件入库
- `!openspec/changes/*.md`（第 10 行）：允许 change 级别的 .md 文件
- `!openspec/changes/governance-*/`（第 11-12 行）：允许 fixture 目录
- `/openspec/changes/`（已移除）：不再重复，避免冲突
- `!scripts/hooks/lib/`（新增）：反忽略 hooks lib 目录
- `!scripts/hooks/lib/*.py`（新增）：反忽略 hooks lib 下的 Python 文件

## Stage 文件列表

| 文件 | 说明 |
|---|---|
| `scripts/hooks/lib/gate_result.py` | 统一 gate result 输出协议（核心聚合逻辑） |
| `scripts/hooks/lib/__init__.py` | 包标识 |
| `scripts/hooks/lib/path_policy.py` | 路径分类与验证 |
| `scripts/hooks/lib/yaml_loader.py` | YAML 加载工具 |
| `scripts/hooks/lib/change_context.py` | change 上下文加载 |
| `scripts/hooks/lib/markdown_utils.py` | Markdown 工具 |
| `openspec/changes/README.md` | change 目录索引（上一轮死链修复） |
| `.gitignore` | 误伤修复 |
| `scripts/hooks/tests/test_gitignore_tracking.py` | clean-checkout 回归测试 |

## 验证命令与结果

```bash
# .gitignore 修复验证
git check-ignore -v scripts/hooks/lib/gate_result.py openspec/changes/README.md
# 结果：两个路径均被 negate 规则匹配（不被 ignore）

# 追踪验证
git ls-files --stage scripts/hooks/lib/gate_result.py openspec/changes/README.md
# 结果：两个路径均出现

# 治理 validator
python3 scripts/hooks/validators/reference_integrity.py . governance_check
# 结果: pass
python3 scripts/hooks/validators/phase_index.py . governance_check
# 结果: pass
python3 scripts/hooks/validators/schema_package.py . governance_check
# 结果: pass

# Dispatcher smoke test
python3 scripts/hooks/dispatch.py --change tmp/governance-check-smoke --gate governance_check --json
# 结果: pass, exit 0

# 全部测试
python3 -m pytest scripts/hooks/tests -q
# 结果: 64 passed
```

## 剩余风险

1. **`sources/` 目录的类似 negate 问题**：`/sources/*` + `!/sources/README.md` 模式当前无冲突，但若未来在 `sources/` 之后新增另一个忽略同一目录的规则，可能出现与 `openspec/changes/` 相同的覆盖问题。已在测试中覆盖。
2. **通用 `lib/` 规则仍可能误伤其他嵌套 `lib/` 目录**：当前仓库只有 `scripts/hooks/lib/` 一个嵌套 `lib/`。如果未来新增其他 `lib/` 目录需要追踪，需要类似地添加 negate 规则。
3. **`.agent/` 目录**：本轮重建了被精简 commit 删除的 `.agent/` 文件（ledger、decisions、task-results）。这些文件此前被有意删除，本次重建仅为了本轮任务要求，是否需要长期保留待后续决策。
