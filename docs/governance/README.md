# Governance Docs Index

治理文档索引。只有任务语义涉及规约分层、路由、仓库架构时才进入这里。

---

## 文档列表

| 文件 | 角色 | 何时读取 |
|------|------|----------|
| `openspec-harness-boundary.md` | OpenSpec / Harness 边界规范 | 修改 schema/specs/templates/workflows/rules/.claude/AGENTS 路由时 |
| `knowledge-directory-model-redesign.md` | `knowledge/` 目录模型的历史设计说明 | 需要理解当前目录模型为何演化成现在这样，或评估进一步目录迁移时 |

---

## 使用顺序

1. 先读 `openspec-harness-boundary.md` 判断改动归属哪一层。
2. 如任务涉及长期资产目录演进或历史决策回溯，再补读 `knowledge-directory-model-redesign.md`。

---

## 边界说明

- 本目录文档默认是 **governance / rationale** 资产，不直接替代 OpenSpec canonical spec。
- 当某项设计已经沉淀为正式规则时，应以 `openspec/config.yaml`、`openspec/schemas/.../schema.yaml` 和 `openspec/specs/*/spec.md` 为准。
