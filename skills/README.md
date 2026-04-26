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

## 分类索引

### `skills/openspec-flow/` — OpenSpec change 流程能力

| Skill | 用途 |
|-------|------|
| `route-research-change/` | 判断研究类型（primitive / synthesis / decision） |
| `init-change/` | 初始化 change 目录与 change.yaml |
| `build-request/` | 生成或修订 request.md |
| `build-plan/` | 生成或修订 plan.md |
| `build-research-support/` | 来源包与证据面构建 |
| `build-draft/` | 生成或修订 draft.md |
| `build-review/` | 生成 review.md |
| `build-publish-plan/` | 生成 publish.md |

### `skills/research-authoring/` — 研究写作与证据能力

| Skill | 用途 |
|-------|------|
| `extract-source-pack/` | 从 URL 提取来源包 |
| `build-evidence-map/` | 生成证据地图 |
| `write-source-note/` | 来源精读笔记 |
| `extract-claims/` | 从笔记中提取声明 |
| `write-source-reading-draft/` | 来源阅读型草稿 |
| `write-primitive-draft/` | Primitive 型草稿 |
| `write-primitive-definition/` | 定义型 primitive |
| `write-primitive-evolution/` | 演进型 primitive |
| `write-primitive-mechanism/` | 机制型 primitive |
| `write-synthesis-draft/` | Synthesis 型草稿 |
| `write-decision-draft/` | Decision 型草稿 |
| `build-decision-criteria/` | 决策标准生成 |

### `skills/knowledge-publishing/` — 发布到 Knowledge 的能力

| Skill | 用途 |
|-------|------|
| `validate-publish-targets/` | 校验 publish_targets 合法性 |
| `render-knowledge-artifact/` | 渲染 knowledge artifact |
| `render-decision-verdict/` | 渲染 decision verdict |
| `merge-change-into-knowledge/` | 合并 change 到 knowledge 主线 |
| `review-knowledge-item/` | 评审知识产出物 |

### `skills/governance/` — 规约治理能力

| Skill | 用途 |
|-------|------|
| `review-openspec-contracts/` | 审查 OpenSpec 合约一致性 |
| `review-command-routing/` | 审查 command 与 skill 路由 |
| `review-skill-boundaries/` | 审查 skill 职责边界 |
| `review-harness-rules/` | 审查 Harness 规则一致性 |
| `review-hook-coverage/` | 审查 Hook 覆盖率 |
| `cleanup-legacy-flow/` | 清理旧流程产物 |

### `skills/diagrams/` — 图表支撑能力

| Skill | 用途 |
|-------|------|
| `render-diagram-contract/` | 生成 diagram package（brief → puml → validation） |

### `skills/maintenance/` — 维护与清理能力

| Skill | 用途 |
|-------|------|
| `refresh-existing-topic/` | 刷新现有主题 |
| `detect-term-drift/` | 检测术语漂移 |

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

## 维护要求

新增或调整 skill 时，至少同步更新：

1. 本 README 的索引
2. 对应 `SKILL.md` 的输入输出
3. 触发它的 workflow / command / agent 文档
4. `.claude/skills/` 下的符号链接
