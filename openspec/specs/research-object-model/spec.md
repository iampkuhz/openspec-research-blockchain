# 研究对象模型规范

## 目的

定义本仓库允许的研究对象类型、研究路径、依赖关系和长期落位方式。

---

## 研究对象类型

### primitive

**定义**：单个协议、EIP、机制或能力单元的深度研究。

**重点**：
- 本质定义与边界
- 角色与信任边界
- 角色内部组件与跨角色流程
- 设计取舍与能力边界

**长期落位**：
- `knowledge/analysis/primitives/<domain_id>/<topic_slug>/artifact.md`

### synthesis

**定义**：多个对象之间的演进、关系、比较或分类分析。

**重点**：
- 演进框架与时间线
- 各对象定位与问题层
- 演进关系、互补关系和趋势判断
- 对依赖 primitive 的有限抽取与横向比较

**长期落位**：
- `knowledge/analysis/synthesis/<topic_slug>/artifact.md`

### decision

**定义**：面向具体场景的比较、选型和条件性判断。

**重点**：
- 场景定义
- 决策标准
- 候选方案比较
- 条件性 verdict 与风险说明

**长期落位**：
- `knowledge/decisions/<domain_id>/<topic_slug>/artifact.md`
- `knowledge/decisions/<domain_id>/<topic_slug>/verdict.md`

---

## 非对象类型

### domain

`domain` 是 taxonomy / 浏览分组概念，用于组织 `primitive` 与 `decision` 的目录结构。

**重要约束**：
- `domain` 不是独立 `object_type`
- 不创建独立的长期 `artifact.md`
- 只作为路径分组和候选枚举来源存在

---

## 研究路径

| 路径 | 适用类型 | 含义 |
|------|----------|------|
| `deep-dive` | `primitive` | 深度分析单个对象 |
| `evolution` | `synthesis` | 研究多个对象的演进关系 |
| `scenario` | `decision` | 面向具体场景做比较与判断 |

---

## 研究深度

| 深度 | 含义 |
|------|------|
| `deep` | 全面深挖，形成高复用 reference |
| `focused` | 聚焦特定问题深入分析 |
| `light` | 快速确认基本事实与边界 |

**使用规则**：
- `primitive` 的长期 `artifact.md` 必须显式标记 `research_depth`
- 上层研究引用下层对象时，必须检查其当前深度是否满足本轮需求

---

## 依赖管理

### 基本原则

1. 上层不重复下层全文，只抽取与当前问题直接相关的结论。
2. `synthesis` / `decision` 必须在 `plan.md` 中显式声明依赖对象、所需深度与差异处理。
3. 若依赖对象缺失或深度不足，必须规划补充调研，不能静默降低要求。

### 依赖对象允许范围

| 当前对象 | 允许依赖 |
|----------|----------|
| `primitive` | 相邻 `primitive`（用于边界对比） |
| `synthesis` | `primitive` |
| `decision` | `primitive`、`synthesis` |

---

## 过程产物与长期产物

### 过程产物

位于 `openspec/changes/<change-id>/`：
- `request.md`
- `plan.md`
- `draft.md`
- `decision-criteria.md`（decision 可选）
- `sources/`
- `diagrams/`
- `review/`

### 长期产物

位于 `knowledge/`：
- `primitive` → `artifact.md`
- `synthesis` → `artifact.md`
- `decision` → `artifact.md` + `verdict.md`

**约束**：
- 过程产物不进入长期目录
- `decision-criteria.md` 不提升为长期 `criteria.md`
- `diagrams/` 保留在 change 目录作为审计线索，不复制到长期目录
