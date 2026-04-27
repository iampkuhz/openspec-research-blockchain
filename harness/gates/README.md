# Gate Registry — machine-readable source of truth

本文件是质量门禁（gate）定义的 **machine-readable source of truth**。

## 关联图

```
schema.yaml
  -> rules/_index.yaml
  -> gates/registry.yaml          ← 本文件
  -> hooks/registry.yaml          ← hook event -> gate runner 映射
  -> scripts/hooks/dispatch.py    ← gate runner 入口
  -> validators/registry.yaml     ← validator name -> script 映射
  -> validators/*.py              ← 具体校验逻辑
  -> validation/*.json            ← 每次 change 执行结果
```

## 字段说明

| 字段 | 说明 |
|------|------|
| `stage` | gate 阶段标识，对应 dispatch 的 `--gate` 参数 |
| `blocking` | true 表示失败时必须阻断（exit 2） |
| `artifact` | 本 gate 保护的主要产物类型 |
| `files.required` | 该阶段应存在的文件列表 |
| `validators` | 引用的 validator name（见 `scripts/hooks/validators/registry.yaml`） |
| `rule_refs` | 关联的 harness rules 文件（人读规则源） |
| `output.path` | gate 执行结果 JSON 的输出路径 |

## 与相关文件的关系

- **`harness/governance/quality-gates.md`** 是人读说明，不承担机器定义
- **`harness/hooks/registry.yaml`** 只负责 hook event -> gate runner 映射
- **`scripts/hooks/validators/registry.yaml`** 只负责 validator name -> script 映射
- **`validation/*.json`** 是每次 change 执行 gate 后的结果记录
