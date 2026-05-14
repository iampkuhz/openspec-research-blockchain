# Task 26 — Governance Gate Hardening

## 目标

将 governance_check gate 变为稳定、可解释、可复跑的质量门。

## 发现与修复

### 1. Dispatcher JSON 解析失败

**问题**：`run_validator()` 按行解析 stdout，validator 输出 pretty JSON（多行缩进）时无法解析，合法 JSON 被整段塞进 `warnings`。

**修复**：`dispatch.py` 的 `run_validator()` 改为：
1. 优先 `json.loads(full stdout)` — 支持 pretty JSON
2. Fallback：brace-matching 提取第一个完整 JSON 对象
3. 最终 fallback：按 exit code 构建 result，metadata 包含 `returncode`

**新增测试**：`test_dispatch.py` 新增 `TestDispatchPrettyJsonParsing` 类，覆盖真实 validator 输出。

### 2. Advisory Validator 阻断 Gate

**问题**：`reference_integrity` 声明 `blocking=false` 但 `status=fail`，gate 聚合只看 status 不看 per-validator blocking 意图，导致 advisory failure 实际阻断提交。

**决策**：方向 A — `reference_integrity` 对治理 gate 必须是 blocking（规约文件死链造成上下文浪费和错误路由）。

**修复**：
- `aggregate_results()` 现在尊重 per-validator `blocking` — non-blocking validator 的 fail/error 降级为 warn
- `reference_integrity` 改为 `blocking=True`
- **新增测试**：`test_gate_result.py` — 8 个测试覆盖 advisory/blocking 聚合语义

### 3. 5 个 Dead Reference

| 文件 | 引用 | 处理 |
|------|------|------|
| `harness/workflows/research-publish-flow.md` | `diagram.svg` | 改为 `<diagram.svg>` 占位符 |
| `harness/rules/diagrams/diagram-policy.md` | `diagrams/x.puml` | 改为 `diagrams/<id>/diagram.puml` |
| `harness/rules/writing/structure-rules.md` | `./atoms/core-mechanism.md` | 改为 `./<domain>/<topic-slug>.md` |
| `openspec/changes/README.md` | `../archive/` → `openspec/archive/`（不存在） | 改为 `archive/`（同目录，实际存在） |
| `.claude/agents/publish-agent.md` | `diagram.svg` | 改为 `<diagram.svg>` 占位符 |

## 修改文件

| 文件 | 变更 |
|------|------|
| `scripts/hooks/dispatch.py` | run_validator 支持 pretty JSON |
| `scripts/hooks/lib/gate_result.py` | aggregate_results 尊重 per-validator blocking |
| `scripts/hooks/validators/reference_integrity.py` | blocking=false → true |
| `scripts/hooks/tests/test_dispatch.py` | 新增 pretty JSON 测试 |
| `scripts/hooks/tests/test_gate_result.py` | **新文件** — 8 个聚合语义测试 |
| `harness/workflows/research-publish-flow.md` | 修复 diagram.svg 引用 |
| `harness/rules/diagrams/diagram-policy.md` | 修复示例路径占位符 |
| `harness/rules/writing/structure-rules.md` | 修复内部引用占位符 |
| `openspec/changes/README.md` | 修复归档链接 |
| `.claude/agents/publish-agent.md` | 修复 diagram.svg 引用 |
| `scripts/hooks/tests/fixtures/` | 更新 fixture 匹配当前 validator 输出 |
| `.agent/decisions.md` | 新增 6.1/6.2 决策记录 |

## 验证命令

```
python3 -m pytest scripts/hooks/tests -q          # 42 passed ✅
python3 scripts/hooks/validators/reference_integrity.py . governance_check  # exit 0, total_errors=0 ✅
python3 scripts/hooks/validators/phase_index.py . governance_check          # exit 0 ✅
python3 scripts/hooks/validators/schema_package.py . governance_check       # exit 0 ✅
dispatch.py governance_check smoke test                                     # exit 0, status=pass ✅
```

## 剩余风险

| 风险 | 级别 | 说明 |
|------|------|------|
| `.agent/task-results/*.md` 大量未跟踪 | Low | 历史任务产物，属于 V2 run 状态记录，建议批量提交 |
| 预存的 branch 修改（harness/README.md 等 V1 fix） | Low | 不属于本轮，需单独处理 |
| Fixture JSON 字段顺序变化 | Low | 测试通过，非语义差异 |
