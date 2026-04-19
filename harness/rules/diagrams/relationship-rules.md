# 关系规则

## 目的

定义架构 brief 中 `flows` 字段的语义规范，以及 skill 生成 PlantUML 时的关系映射规则。

## 核心原则

### 原则 1: Brief 只声明意图，不指定 PlantUML 语法

**brief 中的 flow**：
```yaml
flows:
  - id: S1
    from: user
    to: web_portal
    description: 提交订单
```

**PlantUML 生成**由 skill 根据 `component.type` 自动选择：
- `actor` → `component`：实线箭头
- `component` → `database`：实线箭头
- 依赖关系：虚线箭头（如在注释中说明）

### 原则 2: 关系语义由 brief schema 约束，不由本规则重复定义

**唯一真相**：`assets/validation/architecture-brief.schema.json`

本规则只说明：
- flow 描述文案的规范
- 关系可见性的判断
- 隐式关系的标注方式

---

## Flow 描述规范

### 文案要求

| 要求 | 说明 |
|------|------|
| 使用动宾结构 | "提交订单"、"预占库存" |
| 避免模糊词 | 不用"处理"、"相关"、"连接" |
| 简洁明确 | 不超过 20 字 |
| 与技术术语一致 | 复用 glossary 中的定义 |

### 文案示例

| 场景 | 错误 | 正确 |
|------|------|------|
| 用户请求 | "用户操作" | "提交订单请求" |
| 服务调用 | "调用服务" | "预占库存" |
| 数据写入 | "存数据" | "写入订单记录" |
| 依赖关系 | "有关系" | "依赖配置中心" |

---

## 关系可见性

### 必须画出的关系

**必须**在 `flows` 中声明并落图：
- 核心业务依赖（如订单服务 → 订单库）
- 跨层调用（如应用层 → 数据层）
- 外部系统交互（如支付网关）

### 可以省略的关系

**可以**不在 `flows` 中声明：
- 琐碎的依赖（如日志收集）
- 隐含的基础设施（如服务发现、配置中心）
- 与当前主题无关的关系

**省略时需在 `out_of_scope` 中列出**：
```yaml
out_of_scope:
  - 监控告警指标
  - 配置中心依赖
  - 日志收集链路
```

---

## 隐式关系标注

### 何时使用隐式关系

当某些依赖对理解很重要，但不需要在图中画出时：

```yaml
# brief 中
out_of_scope:
  - 服务发现（所有服务隐式依赖 Consul）
```

### PlantUML 注释说明（由 skill 生成）

```plantuml
note bottom of diagram
  <b>隐式依赖</b>
  所有服务隐式依赖 Consul（服务发现）
  本图未画出
end note
```

---

## 关系一致性

### 禁止的混用

**禁止**在同一 brief 中：
- 同一对组件之间声明多条重复 flows
- flow 的 `from`/`to` 引用不存在的组件

### 箭头方向

**规范**：
- `from` = 依赖方/调用方
- `to` = 被依赖方/被调用方

**示例**：
```yaml
# 正确：订单服务依赖订单库
- from: order_service
  to: order_db
  description: 写入订单记录

# 错误：方向反了
- from: order_db
  to: order_service
  description: 接收订单写入
```

---

## 时序图关系规范（单独说明）

时序图的 `messages` 与架构图的 `flows` 不同：

| 字段 | 架构图 `flows` | 时序图 `messages` |
|------|----------------|-------------------|
| 编号 | `S1`, `S2`... | `M1`, `M2` / `R1`, `R2` |
| 类型 | 无（隐式为调用） | `sync`, `return`, `async` |
| 方向 | `from` → `to` | `from` → `to` |
| 描述 | 动宾短语 | 消息内容 |

---

## 检查清单

### Brief 作者检查

- [ ] flow 描述是否使用动宾结构
- [ ] flow 的 `from`/`to` 引用存在的组件
- [ ] 隐式依赖是否在 `out_of_scope` 中说明
- [ ] 无重复的 flows 声明

### Skill 生成检查

- [ ] 根据 `component.type` 选择正确的 PlantUML 关系符号
- [ ] 所有 flows 都落图
- [ ] 箭头方向与 `from`/`to` 一致
- [ ] 隐式依赖在图中标注（如适用）

## 相关文件

- `harness/rules/diagrams/diagram-policy.md`：图表总政策
- `harness/rules/diagrams/annotation-rules.md`：注释规范
- `harness/rules/diagrams/brief-quality-rules.md`：Brief 质量评估
- `feipi-plantuml-generate-architecture-diagram/SKILL.md`：架构图生成 skill
- `feipi-plantuml-generate-sequence-diagram/SKILL.md`：时序图生成 skill
