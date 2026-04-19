# Spec System Audit Workflow - 规约体系审计与清理

**注意**：本 workflow 用于审查仓库规约体系本身的触发链、索引链与渐进式加载，不用于普通 research 内容写作。

## 目标

对仓库规约体系做 repo-wide hygiene audit，确保：

- 每个关键规约文件都有明确触发点
- 入口层、索引层、叶子层的加载顺序合理
- 不存在 direct orphan、低概率孤岛、dead reference 与失效脚本 gate
- multi-agent / phase / output contract 之间保持一致
- 周期性手工清理时有稳定的执行入口与输出格式

## 触发条件

使用本 workflow 的典型场景：

- 定期全量复查 `AGENTS.md`、`CLAUDE.md`、`.claude/**`、`openspec/**`、`harness/**`
- 大批 governance 改动后做一次系统卫生检查
- 怀疑某些规约文件没有触发点、引用失效或加载路径不合理
- 需要批量清理旧命令名、旧脚本路径、旧对象模型说明

## 不适用场景

- 普通 technical research
- 单条知识条目的 request / plan / draft / review
- 只评审某个具体 governance diff 的边界归属

若任务重点是“评审某次具体治理改动是否越界”，优先使用 `governance-review-workflow.md`。

## 必需输入

- 审计范围（repo-wide / 目录 / 文件）
- 运行模式：
  - `audit-only`
  - `audit-fix`
- 可选 report path

## 默认执行角色

- `spec-system-audit-agent`

## 可选升级角色

- `governance-review-agent`

仅当审计发现 OpenSpec / Harness / `.claude` 的职责边界争议、需要架构级重构时，由主会话决定是否升级调用。

## 规则加载策略

### 初始加载（workflow 开始时）

必须读取：

| 文件 | 用途 |
|------|------|
| `AGENTS.md` | 仓库总入口与任务路由 |
| `CLAUDE.md` | Claude 场景入口与路由提醒 |
| `.claude/README.md` | Claude 命令 / agent / settings 索引 |
| `docs/governance/openspec-harness-boundary.md` | OpenSpec / Harness 边界判断 |
| `harness/workflows/_index.yaml` | workflow 入口索引 |
| `harness/rules/_index.yaml` | rule 域索引 |
| `harness/rules/_phase_index.yaml` | phase 加载索引 |

### 按需加载（只在对应检查项展开）

| 检查项 | 读取对象 |
|--------|----------|
| command / agent 路由 | `.claude/commands/**`、`.claude/agents/**` |
| workflow → rule → spec 链路 | `harness/workflows/**`、`harness/rules/**`、`openspec/specs/**` |
| schema / template / config 一致性 | `openspec/config.yaml`、`openspec/schemas/**`、`openspec/specs/**` |
| 叶子操作入口 | `skills/**`、`scripts/**` |
| 历史说明 / 本地说明 | `docs/governance/**`、`harness/reports/**`、`.claude/settings.local.json` |

## 审计步骤

### 步骤 1：归一化 scope 与模式

先确认：

- scope 是 repo-wide 还是局部目录
- 本轮只审计还是允许直接修复
- 是否需要输出为 report 文件

### 步骤 2：构建触发链与加载链

从索引层向下追踪：

1. 入口文件是否指向正确索引
2. workflow 是否能把任务路由到合适 phase / agent / rule
3. 叶子文件是否只在真正需要时才展开

### 步骤 3：做体系级检查

至少覆盖以下检查项：

| 类别 | 检查内容 |
|------|----------|
| Triggerability | 文件是否有明确触发点 |
| Progressive Loading | 是否遵循入口 → 索引 → 叶子 |
| Dead References | 路径、命令名、脚本名、agent 名是否存在 |
| Gate Validity | workflow 中声明的 script / validation gate 是否真实可用 |
| Output Contract | 阶段产物、agent 写入范围、workflow 输出是否一致 |
| Boundary Hygiene | OpenSpec / Harness / `.claude` / docs 分层是否清晰 |
| Multi-Agent Hygiene | author / specialist 边界是否污染 |

### 步骤 4：分类问题

每个问题必须落入以下至少一类：

- `direct orphan`
- `low-probability orphan`
- `dead reference`
- `loading gap`
- `loading overreach`
- `boundary drift`
- `stale example`
- `invalid gate`

### 步骤 5：生成 cleanup queue

清理顺序默认按风险高低排序：

1. 失效路径、失效命令、失效脚本 gate
2. 没有触发点的索引或叶子文件
3. 会把任务错误路由到别处的说明
4. 会导致上下文污染的 multi-agent 边界问题
5. 历史示例、过时注释、低风险措辞漂移

### 步骤 6：按需修复

仅在 `audit-fix` 模式下执行。

修复原则：

- 先修 index / route / reference，再修 wording
- 能通过索引补触发点，不通过复制规则正文补
- 高置信修复直接做；边界归属不清时交回主会话

### 步骤 7：复检

修复后至少重新执行：

- 引用可达性扫描
- 关键 YAML / JSON 解析检查
- 必要时的脚本存在性或 gate 路径复检

## 输出格式

默认输出为会话总结；如用户要求落盘，可写为 `harness/reports/spec-system-audit-YYYY-MM-DD.md` 或当前 governance change 下的 review 文件。

推荐结构：

```markdown
# Spec System Audit

## Scope
- mode:
- targets:

## Findings Summary
| category | count | notes |

## Direct Orphans
- ...

## Low-Probability Orphans
- ...

## Dead References / Invalid Gates
- ...

## Cleanup Queue
1. ...
2. ...

## Applied Fixes
- ...

## Residual Risks
- ...
```

## 完成标准

- [ ] scope 与模式已明确
- [ ] 触发链与加载链已检查
- [ ] orphan / dead reference / invalid gate 已分类
- [ ] cleanup queue 已按优先级输出
- [ ] 若进入修复模式，已完成至少一轮复检

## 异常处理

### 发现 direct orphan

1. 先判断应由哪个索引或 workflow 触发
2. 补充明确引用点
3. 复检是否仍是孤岛

### 发现 dead reference / invalid gate

1. 优先修正文档引用
2. 如对应对象已废弃，删除旧说明并补新入口
3. 避免保留“看起来能执行、实际不存在”的路径

### 发现 boundary drift

1. 记录冲突位置
2. 交回主会话判断是否升级到 `governance-review-agent`
3. 在边界未澄清前，不要自行扩张修复范围
