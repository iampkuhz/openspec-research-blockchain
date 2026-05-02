# OpenSpec / Harness / Hook / Script / Knowledge 边界

**本文件位置**：`harness/governance/openspec-harness-boundary.md`
**用途**：定义 OpenSpec / Harness / Command / Skill / Hook / Script / Knowledge 的正式职责边界。
**真源**：以 `openspec/schemas/blockchain-research/schema.yaml` 为 artifact graph 的 source of truth。

---

## 职责分层

| 层 | 拥有者 | 职责 | 典型路径 |
|---|---|---|---|
| **Artifact Contract** | OpenSpec | artifact graph、对象模型、产物路径、模板、apply 规则 | `openspec/schemas/**/schema.yaml`、`openspec/schemas/**/templates/` |
| **Execution Rules** | Harness | 质量门禁、执行步骤、artifact 规则、research 规则 | `harness/workflows/`、`harness/rules/` |
| **User Entrypoint** | Command | 用户入口、任务路由、本次任务边界 | `.claude/commands/` |
| **Reusable Capability** | Skill | 可复用执行能力、多步骤策略、脚本与模板组织 | `.claude/skills/`、`skills/` |
| **Deterministic Validation** | Hook / Script | 确定性校验、质量 gate 落地 | `scripts/hooks/validators/`、`harness/hooks/registry.yaml` |
| **Long-lived Asset** | Knowledge | 最终长期研究资产 | `knowledge/analysis/`、`knowledge/decisions/` |

## 核心原则

### 1. OpenSpec schema 是 artifact graph 的 source of truth

- artifact 有哪些、依赖什么模板、apply 到哪里、requires 什么字段，以 `openspec/schemas/blockchain-research/schema.yaml` 为准
- `openspec/config.yaml` 决定 workflow 配置与 apply 规则
- `openspec/specs/**` 是正式政策的 canonical 定义

### 2. Harness 不重新定义 artifact graph

- Harness 只解释：怎么执行、质量门禁是什么、边界在哪里
- Harness rules 可以引用 artifact id（如 `request`、`plan`、`draft`、`publish`），但不能发明 schema 中没有的新 artifact id
- Harness workflows 解释执行步骤，但不能和 `schema.yaml` 的 `requires` / `templates` 冲突

### 3. Command 是用户入口

- Command 负责接收用户需求、判断 change 类型、初始化 change
- Command 不应包含具体的写作步骤或质量规则
- Active commands：`/spec-research`、`/spec-research-step`、`/spec-governance-review`

### 4. Skill 是可复用能力

- Skill 负责具体执行策略（如路由 change、构建 draft、验证 publish targets）
- 一个 skill 可被多个 command 调用
- Skill 不负责定义 artifact 的正式语义

### 5. Hook / Script 是确定性校验

- Hook validator 是规则落地的确定性形式
- Hook 优先读取 `change.yaml` 中的声明，不通过路径硬猜语义
- Hook 不替代 review.md 的人类评审

### 6. Knowledge 是最终资产

- 长期资产只沉淀到 `knowledge/analysis/` 和 `knowledge/decisions/`
- `publish.md` 是进入 knowledge 的唯一边界
- 禁止直接修改 `knowledge/` 主线，必须通过 change + publish 流程

## 冲突处理

当两层定义冲突时：

1. Artifact graph / 模板 / apply 规则 → 以 OpenSpec schema 为准
2. 执行步骤 / 质量门禁 → 以 Harness 为准（但不能与 schema 冲突）
3. 用户入口 / 路由 → 以 Command 为准
4. 执行策略 → 以 Skill 为准
5. 校验逻辑 → 以 Hook script 为准

## 不在本文件的职责

- 不在这里展开 `harness/workflows/**` 的执行步骤
- 不在这里重写 `openspec/schemas/**` 的正式规则
- 不在这里列出 skill 清单或 agent 合同
