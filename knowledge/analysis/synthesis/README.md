# Synthesis（合成/演进分析）

这里存放演进或综合分析的长期 artifact。

## 目录结构

```
synthesis/
├── aa-eip-evolution/         # AA 领域 EIP 演进分析
├── cross-chain-evolution/    # 未来扩展：跨链技术演进
└── scaling-comparison/       # 未来扩展：扩容方案对比
```

## 按主题组织

Synthesis 按**研究主题**组织，每个主题分析多个对象之间的关系：

- **演进分析（evolution）**：分析多个对象的历史演进关系
  - 如：`aa-eip-evolution` 分析 EIP-4337、EIP-7702、EIP-7560 的演进关系
  
- **对比分析（comparison）**：分析多个对象的特性对比
  - 如：`scaling-comparison` 对比 Optimistic Rollup vs ZK Rollup

## 交付物

每个 synthesis 默认只保留：
- `artifact.md`：演进/综合分析文档
- 演进图、关系图等（PlantUML 或 Markdown 表格）

## 依赖管理

Synthesis 必须显式声明对下层 primitive 的依赖：

- 必须在 `plan.md` 中声明依赖的 primitive
- 必须检查每个依赖 primitive 的深度是否满足需求
- 如果 primitive 缺失或深度不足，必须在 plan 中规划补充调研
- 不得重写下层 primitive 的全文，只能引用和综合

## 与上层 domain 的关系

- 一个 synthesis 可以被多个 domain 复用
- 与哪些 domain 相关，应通过 `plan.md`、正文链接来声明
- Synthesis 不通过目录路径被锁死为某个 domain 的子节点

## 新增 synthesis 的流程

1. 创建 change packet：`./scripts/new_change.sh synthesis <topic>-pass-1`
2. 编写 `request.md` → 生成 `plan.md`（含依赖声明） → 生成 `draft.md` → 提炼 `artifact.md`
3. 放入 `synthesis/` 目录

## 图表要求

Synthesis 必须包含的图表：
- **演进时间线图**：优先使用 Markdown 表格或 Mermaid timeline
- **问题层分布图**：优先使用 Markdown 表格或 Mermaid graph
- **演进关系图**：优先使用 Mermaid 关系图或 PlantUML 组件图
- **对比表格**：必须使用 Markdown 表格
