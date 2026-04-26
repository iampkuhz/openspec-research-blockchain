# skills/ — 仓库内置 Skills

> **迁移状态**：本目录是 skill 定义的真源（source of truth）。
> `.claude/skills/` 包含指向本目录的符号链接。
> 新增或修改 skill 时，请在 `skills/` 下操作，然后在 `.claude/skills/` 下创建对应符号链接。

这些 skill 是 workflow 的叶子执行单元。

使用顺序应保持渐进式加载：

1. 先从 `AGENTS.md`、`CLAUDE.md`、`harness/workflows/_index.yaml` 判断任务类型
2. 再读取对应 workflow 与 `harness/rules/_phase_index.yaml`
3. 只有在阶段需要具体动作时，才展开到这里对应的 `SKILL.md`

---

## Active Skill 分类索引

### `skills/openspec-flow/` — OpenSpec change 流程能力（7 个）

| Skill | 用途 |
|-------|------|
| `route-research-change/` | 判断研究类型（primitive / synthesis / decision） |
| `init-change/` | 初始化 change 目录与 change.yaml |
| `build-request-plan/` | 生成或修订 request.md 与 plan.md（合并自 build-request + build-plan） |
| `build-research-support/` | 端到端执行 research pipeline（request → plan → draft → review → artifact） |
| `build-draft/` | 生成或修订 draft.md，含 diagram contract |
| `build-review/` | 生成 review.md |
| `build-publish-plan/` | 生成 publish.md |

### `skills/research-authoring/` — 研究写作与证据能力（6 个）

| Skill | 用途 |
|-------|------|
| `extract-evidence/` | 提取来源包、证据地图与可追溯 claims（合并自 extract-source-pack + build-evidence-map + extract-claims） |
| `write-source-note/` | 来源精读笔记 |
| `write-primitive-draft/` | Primitive 型草稿（聚合 definition/evolution/mechanism 子章节规则） |
| `write-synthesis-draft/` | Synthesis 型横向比较草稿 |
| `write-decision-draft/` | Decision 型草稿 |
| `build-decision-criteria/` | 决策标准生成 |

### `skills/knowledge-publishing/` — 发布到 Knowledge 的能力（5 个）

| Skill | 用途 |
|-------|------|
| `validate-publish-targets/` | 校验 publish_targets 合法性 |
| `render-knowledge-artifact/` | 渲染 knowledge artifact |
| `render-decision-verdict/` | 渲染 decision verdict |
| `merge-change-into-knowledge/` | 合并 change 到 knowledge 主线 |
| `review-knowledge-item/` | 评审知识产出物 |

### `skills/governance/` — 规约治理能力（3 个）

| Skill | 用途 |
|-------|------|
| `review-research-system/` | 审查 OpenSpec 合约、command 路由与 Harness 规则一致性（合并自 review-openspec-contracts + review-command-routing + review-harness-rules） |
| `review-execution-boundaries/` | 审查 skill 边界与 hook 覆盖（合并自 review-skill-boundaries + review-hook-coverage） |
| `cleanup-legacy-flow/` | 清理旧流程产物 |

### `skills/diagrams/` — 图表支撑能力（1 个）

| Skill | 用途 |
|-------|------|
| `render-diagram-contract/` | 生成 diagram package（brief → puml → validation） |

### `skills/maintenance/` — 维护与更新能力（1 个）

| Skill | 用途 |
|-------|------|
| `refresh-existing-topic/` | 刷新现有主题，含术语漂移检测 |

---

## Command → Skill 路由表

| Command | Primary Skills |
|---|---|
| `/spec-research` | route-research-change, init-change, build-request-plan |
| `/spec-research-step` | build-research-support, extract-evidence, write-source-note, build-draft, build-review |
| `/spec-research-publish` | build-publish-plan, validate-publish-targets, render-knowledge-artifact, render-decision-verdict, merge-change-into-knowledge |
| `/spec-governance-review` | review-research-system, review-execution-boundaries, cleanup-legacy-flow |

---

## 合并与降级 Skill 索引

以下 skill 已合并或降级，不再作为 active skill 暴露：

| 旧 Skill | 去向 | 类型 |
|---|---|---|
| `build-request` | → `build-request-plan` | 合并 |
| `build-plan` | → `build-request-plan` | 合并 |
| `extract-source-pack` | → `extract-evidence` | 合并 |
| `build-evidence-map` | → `extract-evidence` | 合并 |
| `extract-claims` | → `extract-evidence` | 合并 |
| `write-source-reading-draft` | → `write-primitive-draft` | 合并 |
| `write-primitive-definition` | → `write-primitive-draft/references/definition/` | 降级为参考 |
| `write-primitive-evolution` | → `write-primitive-draft/references/evolution/` | 降级为参考 |
| `write-primitive-mechanism` | → `write-primitive-draft/references/mechanism/` | 降级为参考 |
| `review-openspec-contracts` | → `review-research-system` | 合并 |
| `review-command-routing` | → `review-research-system` | 合并 |
| `review-harness-rules` | → `review-research-system` | 合并 |
| `review-skill-boundaries` | → `review-execution-boundaries` | 合并 |
| `review-hook-coverage` | → `review-execution-boundaries` | 合并 |
| `detect-term-drift` | → `refresh-existing-topic` | 合并为章节 |

详细说明见 `skills/_deprecated/` 下的各 `MIGRATED.md`。

---

## 用户级 Skills（全局）

以下 global skills 不在本仓库内维护，但 workflow 会显式依赖它们：

| Skill | 用途 | 常见触发点 |
|-------|------|------------|
| `feipi-plantuml-generate-architecture-diagram` | 生成 PlantUML 架构图 | diagram / draft 阶段 |
| `feipi-plantuml-generate-sequence-diagram` | 生成 PlantUML 时序图 | diagram / draft 阶段 |

---

## 使用原则

### 1. 先 workflow，后 skill

不要从 skill 反推流程。应先确定当前处于哪个 workflow / phase，再打开对应 `SKILL.md`。

### 2. skill 只负责叶子动作

`SKILL.md` 负责输入输出、调用时机、叶子动作约束。不复制上位 workflow / spec 的完整正文。

### 3. 以阶段入口为真源

若 `SKILL.md` 与 harness workflow、schema、spec 冲突，以后者为准。

---

## Skill 保留标准

新建 skill 前必须满足至少 2 条：

1. 有明确独立触发场景
2. 有独立输入和输出
3. 有独立质量标准
4. 有专属 references/scripts/templates
5. 会被多个 command 或 agent 重复使用
6. 对应高风险边界（publish / verdict / merge / validation）
7. 内容足够复杂，不适合放进另一个 skill 的章节

**何时不应该创建新 skill**：

- 它只是某个文档的章节写法 → 放入 target skill 的 `references/`
- 它只是一个 checklist → 放入 rule 文件
- 它只是某个 validator 的解释 → 放入 validator 注释
- 它与已有 skill 职责重叠 → 合并
- 它没有独立触发价值 → 不创建

---

## 维护要求

新增或调整 skill 时，至少同步更新：

1. 本 README 的索引
2. 对应 `SKILL.md` 的输入输出
3. 触发它的 workflow / command / agent 文档
4. `.claude/skills/` 下的符号链接
