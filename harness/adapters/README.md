# harness/adapters/ — Tool-Neutral Adapter Layer

**定位**：本目录定义 Claude Code 与 Qoder 共用的 adapter 约定，避免两套工具各自复制规则。

**不是这里的职责**：
- 不定义 OpenSpec 正式规则（那是 `openspec/specs/**` 的职责）
- 不定义 Harness 执行步骤（那是 `harness/workflows/**` 与 `harness/rules/**` 的职责）
- 不存放具体 tool 的 SKILL.md 或 agent 正文

---

## 职责

| 文件 | 用途 |
|------|------|
| `agent-adapter-contract.md` | 抽象 agent 合同字段，Claude Code 与 Qoder 的 agent 定义都应引用此文件 |
| `tool-capability-matrix.md` | 记录 Claude Code 与 Qoder 的字段映射、能力差异与降级策略 |

---

## 与上位层的关系

```
openspec/specs/**          ← 正式规则本体（artifact contract、canonical policy）
harness/workflows/**       ← 执行手册（步骤、路由、阶段）
harness/rules/**           ← 质量规则
harness/adapters/**        ← tool-neutral adapter 约定（本目录）
.claude/**                 ← Claude Code 入口（commands、agents、skills、settings）
.qoder/**                  ← Qoder 入口（commands、agents、skills、settings）
```

Adapter 层不重新定义正式规则，只解决"同一份语义如何在不同 tool 的 frontmatter 和目录结构中表达"。

---

## 入口文件索引

| Tool | Agent 目录 | Skill 目录 | Command 目录 | Settings |
|------|-----------|-----------|-------------|----------|
| Claude Code | `.claude/agents/` | `.claude/skills/` | `.claude/commands/` | `.claude/settings.json` |
| Qoder | `.qoder/agents/` | `.qoder/skills/` | `.qoder/commands/` | `.qoder/settings.json` |

Skill 真源在 `skills/` 目录下，`.claude/skills/` 是 symlink 暴露层。Qoder adapter 应优先引用 `skills/` 真源，而不是复制 `.claude/skills/` 的 SKILL.md 正文。
