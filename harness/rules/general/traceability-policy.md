# 可追溯性政策

## 目的

确保所有关键技术主张都能追溯到来源，所有长期资产都能追溯到产生它们的 change packet。

## 术语说明

- `claim`：一个可被验证的技术主张
- `source`：支撑 `claim` 的来源
- `artifact unit`：正文中的一个可定位单元，如段落、表格、图表、结论条目
- `change packet`：`openspec/changes/<change-id>/` 下的一轮研究过程产物

## 可追溯性层级

### L1：`claim` → `source`

每个关键 `claim` 都必须能回到至少一个具体 `source`：

```yaml
- claim_id: claim-001
  statement: "UserOperation 是 ERC-4337 的基本执行单位"
  sources:
    - source_id: eip-4337
      location: "Abstract"
  evidence_level: L1
  confidence: high
```

### L2：`artifact unit` → `claim`

正文中的关键段落、表格、图表或结论条目，必须能说明它依赖哪些 `claim`。

允许方式：

- 在 `draft.md` 中紧邻说明
- 在 review / notes 中建立映射
- 在表格或图注中显式注明证据来源

### L3：`artifact` / `draft` → `sources/`

`draft.md` 和长期 `artifact.md` 不要求逐段附 YAML，但必须满足：

- 对应 change packet 中存在 `sources/`
- `sources/source-review.md` 能解释核心来源与证据缺口
- 关键结论能够回指到 `source_id`

### L4：`knowledge` → `change packet`

长期资产必须能回溯到产生它的 change packet：

- `change_id`
- `change_path`
- merge / apply 对应的 git 记录

## Source Pack 建议格式

```yaml
version: "1.0"
topic: eip-4337
sources:
  - source_id: eip-4337
    title: "ERC-4337: Account Abstraction"
    url: https://eips.ethereum.org/EIPS/eip-4337
    source_tier: L1
    accessed_at: 2026-04-08
    confidence: high
    notes: "核心规范来源"
```

## Excerpt 建议格式

```markdown
# Excerpt: eip-4337-abstract

Source: eip-4337
Location: Abstract
Captured_at: 2026-04-08

> ...

Relevance:
- 支撑 claim-001
- 说明 bundler 的定位
```

## Change Packet 内容

每个 `openspec/changes/<change-id>/` 至少应包含：

```text
<change-id>/
├── change.yaml
├── request.md
├── plan.md
├── sources/
│   ├── source-pack.md
│   └── evidence-map.md
├── notes/
├── claims/
├── draft.md
├── review.md
├── publish.md
└── validation/
```

## 从 Change 到长期资产的追溯

建议至少保留以下信息：

```yaml
change_trace:
  change_id: <change-id>
  change_path: openspec/changes/<change-id>/
  merged_at: 2026-04-08T10:30:00Z
  merge_commit: abc123
  outputs:
    - knowledge/analysis/primitives/account-abstraction/eip-4337/artifact.md
```

## 验证脚本

```bash
python3 scripts/research/validate_sources.py --topic eip-4337
python3 scripts/general/check_traceability.py --topic eip-4337
python3 scripts/research/find_term_drift.py --term bundler --topic eip-4337
```

## 验证规则

**必须通过**：

- 关键 `claim` 可回溯到 `source`
- `draft.md` / `artifact.md` 的核心结论可回指到 change packet 中的来源集合
- 长期资产可回溯到 change packet

**禁止**：

- 无来源的高确定性主张
- 无 change packet 的主线修改
- 用 process file 直接替代长期 artifact
