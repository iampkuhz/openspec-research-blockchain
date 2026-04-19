# 场景决策资产

这里存放长期维护的场景决策资产。

## 目录结构

```
knowledge/decisions/
  <domain_id>/
    README.md                 # 可选，仅写边界与收录范围
    <topic_slug>/
      artifact.md             # 决策分析正文
      verdict.md              # 条件性结论
```

## 交付物

每个 decision 对象交付：

- `artifact.md`：场景定义、比较维度、依赖抽取、对比分析
- `verdict.md`：条件性结论（单独文件，不与 artifact 混写）

## domain 分组

`<domain_id>` 与 primitive 共用同一注册表（`analysis/_registry/domains.yaml`）。

## 与其他目录的关系

| 目录 | 用途 | 与 decisions 的关系 |
|------|------|-------------------|
| `knowledge/analysis/` | 事实分析 | decisions 消费 analysis 的分析结果 |
| `openspec/changes/` | 过程层 | decisions 的 inputs，通过后提升到 decisions |
