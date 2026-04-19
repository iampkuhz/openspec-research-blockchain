# Knowledge 长期资产

本目录存放本仓库的长期研究资产，分为两类：

- **`analysis/`**：长期事实分析（primitive、synthesis）
- **`decisions/`**：长期场景判断（decision）

## 对象类型

| 类型 | 路径 | 交付物 |
|------|------|--------|
| `primitive` | `analysis/primitives/<domain_id>/<topic_slug>/artifact.md` | 单一协议/机制的长期分析 |
| `synthesis` | `analysis/synthesis/<topic_slug>/artifact.md` | 演进/比较/分类分析 |
| `decision` | `decisions/<domain_id>/<topic_slug>/artifact.md` + `verdict.md` | 场景判断与条件性结论 |

## 目录模型

```
knowledge/
  analysis/
    _registry/
      domains.yaml          # domain 注册表
    primitives/
      <domain_id>/
        <topic_slug>/
          artifact.md
    synthesis/
      <topic_slug>/
        artifact.md
  decisions/
    <domain_id>/
      <topic_slug>/
        artifact.md
        verdict.md
```

## 规则

- 所有长期资产必须通过 OpenSpec change 流程产生（`openspec/changes/` → apply → `knowledge/`）
- 禁止直接修改 `knowledge/` 主线
- 每个 artifact 必须包含符合规范的 frontmatter
- `domain` 是分组概念，不作为独立的 `object_type`

## 证据政策

| 等级 | 来源 | 用途 |
|------|------|------|
| L1 | 官方规范/EIP/白皮书 | 核心技术主张 |
| L2 | 参考实现/官方文档 | 技术主张支持 |
| L3 | 官方博客/Release notes | 背景/动机 |
| L4 | 第三方分析/社区讨论 | 社区观点参考 |

**详情**：`openspec/specs/evidence-policy/spec.md`
