# OpenSpec Specs

Specs 目录是 OpenSpec 正式规则的存放位置。这里定义了研究工作的约束、模型与策略。

**定位**：OpenSpec 正式规则层。
- 不以 Harness workflow/rule 文件的内容为准时，以本目录的 spec 为准
- 不以 `AGENTS.md` 或 `skills/` 中的描述为准时，以本目录的 spec 为准
- 不以 Claude 侧路由说明为准时，以本目录的 spec 为准

**不是这里的职责**：
- 不在这里定义 workflow 执行步骤（那是 `harness/workflows/` 的职责）
- 不在这里存放研究过程产出（那是 `openspec/changes/` 的职责）
- 不在这里存放长期知识资产（那是 `knowledge/` 的职责）

---

## Spec 索引

| Spec | 路径 | 用途 |
|------|------|------|
| 证据政策 | `evidence-policy/spec.md` | 定义研究工作的证据等级与可追溯性要求 |
| 分析原则 | `analysis-principles/spec.md` | 定义技术分析正文的硬约束（重事实、轻判断） |
| 仓库资产模型 | `repository-asset-model/spec.md` | 定义长期资产类别与过程产物的区分 |
| 研究对象模型 | `research-object-model/spec.md` | 定义研究对象的分类（primitive / synthesis / decision） |
| 标准输出模型 | `canonical-output-model/spec.md` | 定义标准输出格式与结构约束 |

---

## 如何使用

当对以下问题有疑问时，查阅对应 spec：

- **某个技术主张需要什么级别的证据？** → `evidence-policy/spec.md`
- **分析正文应该遵循什么原则？** → `analysis-principles/spec.md`
- **长期资产应该放在哪里？** → `repository-asset-model/spec.md`
- **研究任务属于哪种类型？** → `research-object-model/spec.md`
- **输出格式有什么约束？** → `canonical-output-model/spec.md`

---

## 与 Harness 的关系

```
openspec/specs/          ← OpenSpec 正式规则（what）
harness/rules/           ← 执行规则（when / who）
harness/workflows/       ← 执行步骤（how）
```

当 spec 与 Harness 描述冲突时，以 spec 为准。
