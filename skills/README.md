# skills/ — 仓库内置 Skills（Source of Truth）

> **本目录是 skill 定义的真源（source of truth）。**
> `.claude/skills/` 是 Claude Code 的**平铺 symlink 暴露层**，不按 category 嵌套。

这些 skill 是 workflow 的叶子执行单元。

使用顺序应保持渐进式加载：

1. 先从 `AGENTS.md`、`CLAUDE.md`、`harness/workflows/_index.yaml` 判断任务类型
2. 再读取对应 workflow 与 `harness/rules/_phase_index.yaml`
3. 只有在阶段需要具体动作时，才展开到这里对应的 `SKILL.md`

---

## Active Skill 分类索引

### `skills/openspec-flow/` — OpenSpec change 流程能力（7 个）

| Skill | Exposed Name | 用途 |
|-------|-------------|------|
| `route-research-change/` | `openspec-route-research-change` | 判断研究类型（primitive / synthesis / decision） |
| `init-change/` | `openspec-init-change` | 初始化 change 目录与 change.yaml |
| `build-request-plan/` | `openspec-build-request-plan` | 生成或修订 request.md 与 plan.md |
| `build-research-support/` | `openspec-build-research-support` | 端到端执行 research pipeline |
| `build-draft/` | `openspec-build-draft` | 生成或修订 draft.md，含 diagram contract |
| `build-review/` | `openspec-build-review` | 生成 review.md |
| `build-publish-plan/` | `openspec-build-publish-plan` | 生成 publish.md |

### `skills/research-authoring/` — 研究写作与证据能力（6 个）

| Skill | Exposed Name | 用途 |
|-------|-------------|------|
| `extract-evidence/` | `research-extract-evidence` | 提取来源包、证据地图与可追溯 claims |
| `write-source-note/` | `research-write-source-note` | 来源精读笔记 |
| `write-primitive-draft/` | `research-write-primitive-draft` | Primitive 型草稿 |
| `write-synthesis-draft/` | `research-write-synthesis-draft` | Synthesis 型横向比较草稿 |
| `write-decision-draft/` | `research-write-decision-draft` | Decision 型草稿 |
| `build-decision-criteria/` | `research-build-decision-criteria` | 决策标准生成 |

### `skills/knowledge-publishing/` — 发布到 Knowledge 的能力（5 个）

| Skill | Exposed Name | 用途 |
|-------|-------------|------|
| `validate-publish-targets/` | `publish-validate-targets` | 校验 publish_targets 合法性 |
| `render-knowledge-artifact/` | `publish-render-artifact` | 渲染 knowledge artifact |
| `render-decision-verdict/` | `publish-render-verdict` | 渲染 decision verdict |
| `merge-change-into-knowledge/` | `publish-merge-knowledge` | 合并 change 到 knowledge 主线 |
| `review-knowledge-item/` | `publish-review-knowledge` | 评审知识产出物 |

### `skills/governance/` — 规约治理能力（3 个）

| Skill | Exposed Name | 用途 |
|-------|-------------|------|
| `review-research-system/` | `governance-review-system` | 审查 OpenSpec/Harness/Command 一致性 |
| `review-execution-boundaries/` | `governance-review-boundaries` | 审查 skill 边界与 hook 覆盖 |
| `cleanup-legacy-flow/` | `governance-cleanup-legacy` | 清理旧流程产物 |

### `skills/diagrams/` — 图表支撑能力（1 个）

| Skill | Exposed Name | 用途 |
|-------|-------------|------|
| `render-diagram-contract/` | `diagram-render-contract` | 生成 diagram package（brief → puml → validation） |

### `skills/maintenance/` — 维护与更新能力（1 个）

| Skill | Exposed Name | 用途 |
|-------|-------------|------|
| `refresh-existing-topic/` | `maintenance-refresh-topic` | 刷新既有主题，含术语漂移检测 |

---

## Category → Exposed Name 映射表

| Category | Repo path | Exposed name |
|---|---|---|
| `openspec-flow` | `skills/openspec-flow/<skill>` | `openspec-<skill>` |
| `research-authoring` | `skills/research-authoring/<skill>` | `research-<skill>` |
| `knowledge-publishing` | `skills/knowledge-publishing/<skill>` | `publish-<skill>` |
| `governance` | `skills/governance/<skill>` | `governance-<skill>` |
| `diagrams` | `skills/diagrams/<skill>` | `diagram-<skill>` |
| `maintenance` | `skills/maintenance/<skill>` | `maintenance-<skill>` |

---

## Command → Skill 路由表

| Command | Skill packages |
|---|---|
| `/spec-research` | `openspec-route-research-change`, `openspec-init-change`, `openspec-build-request-plan` |
| `/spec-research-step` | `openspec-build-research-support`, `research-extract-evidence`, `research-write-source-note`, `openspec-build-draft`, `openspec-build-review` |
| `/spec-research-publish` | `openspec-build-publish-plan`, `publish-validate-targets`, `publish-render-artifact`, `publish-render-verdict`, `publish-merge-knowledge` |
| `/spec-governance-review` | `governance-review-system`, `governance-review-boundaries`, `governance-cleanup-legacy` |

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

## 新增 Skill 指南

1. 在 `skills/<category>/<skill-name>/` 下创建 `SKILL.md`。
2. 填写 frontmatter：`name` 使用带前缀的全局唯一名称（见上表），`description` 用中文、含触发场景、60-120 字。
3. 在 `.claude/skills/` 下创建相对路径 symlink：`ln -s ../../skills/<category>/<skill-name> <exposed-name>`。
4. 更新本 README 的分类索引与映射表。

---

## 维护要求

新增或调整 skill 时，至少同步更新：

1. 本 README 的索引与映射表
2. 对应 `SKILL.md` 的输入输出
3. 触发它的 workflow / command / agent 文档
4. `.claude/skills/` 下的符号链接
