# .claude/skills — Claude Code Project Skill 暴露层

**本目录是 Claude Code 的项目级 skill 暴露层，必须平铺，不按 category 嵌套。**

## 结构说明

- 每个条目是相对路径 symlink，指向 `skills/<category>/<skill>/`。
- 真实 skill 源文件在 `skills/<category>/<skill>/SKILL.md`。
- 每个 symlink 的名称（exposed name）必须等于目标 SKILL.md 的 frontmatter `name`。

## 暴露技能列表

| Exposed Name | Repo Path | 描述 |
|---|---|---|
| `diagram-render-contract` | `skills/diagrams/render-diagram-contract` | 生成 diagram package |
| `governance-cleanup-legacy` | `skills/governance/cleanup-legacy-flow` | 清理旧流程产物 |
| `governance-review-boundaries` | `skills/governance/review-execution-boundaries` | 审查 skill 边界 |
| `governance-review-system` | `skills/governance/review-research-system` | 审查系统一致性 |
| `maintenance-refresh-topic` | `skills/maintenance/refresh-existing-topic` | 刷新既有主题 |
| `openspec-build-draft` | `skills/openspec-flow/build-draft` | 生成 draft.md |
| `openspec-build-publish-plan` | `skills/openspec-flow/build-publish-plan` | 生成 publish.md |
| `openspec-build-request-plan` | `skills/openspec-flow/build-request-plan` | 生成 request/plan |
| `openspec-build-research-support` | `skills/openspec-flow/build-research-support` | 端到端 pipeline |
| `openspec-build-review` | `skills/openspec-flow/build-review` | 生成 review.md |
| `openspec-init-change` | `skills/openspec-flow/init-change` | 初始化 change |
| `openspec-route-research-change` | `skills/openspec-flow/route-research-change` | 路由研究类型 |
| `publish-merge-knowledge` | `skills/knowledge-publishing/merge-change-into-knowledge` | 合并到 knowledge |
| `publish-render-artifact` | `skills/knowledge-publishing/render-knowledge-artifact` | 渲染 artifact |
| `publish-render-verdict` | `skills/knowledge-publishing/render-decision-verdict` | 渲染 verdict |
| `publish-review-knowledge` | `skills/knowledge-publishing/review-knowledge-item` | 评审知识产出 |
| `publish-validate-targets` | `skills/knowledge-publishing/validate-publish-targets` | 校验发布目标 |
| `research-build-decision-criteria` | `skills/research-authoring/build-decision-criteria` | 生成决策标准 |
| `research-extract-evidence` | `skills/research-authoring/extract-evidence` | 提取证据材料 |
| `research-write-decision-draft` | `skills/research-authoring/write-decision-draft` | Decision 草稿 |
| `research-write-primitive-draft` | `skills/research-authoring/write-primitive-draft` | Primitive 草稿 |
| `research-write-source-note` | `skills/research-authoring/write-source-note` | 来源精读笔记 |
| `research-write-synthesis-draft` | `skills/research-authoring/write-synthesis-draft` | Synthesis 草稿 |

## 维护

新增 skill 时：
1. 在 `skills/<category>/<skill>/` 下创建 SKILL.md。
2. 在本目录创建相对路径 symlink：`ln -s ../../skills/<category>/<skill> <exposed-name>`。
3. SKILL.md frontmatter `name` 必须等于 `<exposed-name>`。

重新生成所有 symlink：

```bash
bash scripts/maintenance/install_repo_skills.sh --write
```
