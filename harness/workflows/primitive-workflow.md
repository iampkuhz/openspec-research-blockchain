# Primitive Workflow

**task_type**：`primitive`
**对应 Workflow**：`harness/workflows/primitive-workflow.md`

---

## 适用场景

- 单个协议/机制/产品的底层研究
- 深度分析组件架构、核心流程、设计取舍、能力边界

## 输入

- `request.md`（声明研究对象、核心问题）
- `plan.md`（声明研究深度、来源规划、图表规划）

## 输出

- `sources/source-pack.md`
- `sources/evidence-map.md`
- `notes/*.md`（来源消化）
- `draft.md`（包含实体分类、图表清单、机制分析、能力边界）
- `review.md`

## 推荐 child change 拆分方式

- 每个 primitive 独立一个 change
- 如单个 primitive 过大，可按子模块拆分（如 "consensus-mechanism" 和 "network-layer"）
- 同研究组的 primitive 共享 research-tag 前缀

## draft.md 写作重点

- **实体分类表**：role / component / data object / state / external system
- **图表决策树**：回答四个判定问题，生成图表清单
- **角色与信任边界总览图**（多角色时必须）
- **角色内部组件图**（必须）
- **跨角色核心流程图**（跨角色交互时必须）
- **状态转换图/表**（显式状态转换时必须）
- **能力归属表**（必须）
- 区分 live / planned / promotional
- 写边界、失败条件、前提条件

## review 重点

- 实体分类是否正确（没有把跨信任边界角色误画成内部组件）
- 图表是否覆盖核心机制
- 能力归属是否清晰
- traceability 是否完整

## Publish target

```text
knowledge/analysis/primitives/<domain_id>/<topic_slug>/artifact.md
```

## 禁止事项

- 不做横向对比（那是 synthesis 的职责）
- 不做场景决策（那是 decision 的职责）
- 不把 promotional 能力写成 live
- 不生成 work-products/*.md
