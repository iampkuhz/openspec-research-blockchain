# 工作流

## 核心思路

本仓库不是“立项 -> 设计 -> 开发任务”的实现型流程，而是“问题定义 -> 计划与证据 -> 机制分析与有限结论 -> 提炼长期资产”的研究型流程。

统一主链如下：

1. 定义对象层级
2. 选择研究路径
3. 手工写 `request.md`
4. 生成并 review `plan.md`
5. 按需补 `dependencies.md` / `decision-criteria.md` / `evidence-matrix.md`
6. 生成并 review `draft.md`
7. 提炼长期 `reference.md` / `verdict.md`

## 1. 定义对象层级

优先回答这不是“我要研究什么技术”，而是“我要在什么层级研究它”：

- `primitive`：单协议 / 单机制 / 单能力点
- `synthesis`：关系、演进、分层分析
- `domain`：长期主题域地图与知识组织层
- `decision`：场景化比较、选型、判断

更准确地说：

- 技术分析主链：`primitive -> [optional synthesis] -> domain`
- `decision` 是独立的场景应用层
- `primitive` 和 `synthesis` 与哪些 `domain` 相关，不通过父路径强绑定，而通过依赖声明表达

## 2. 选择研究路径

- `deep-dive`：适用于 `primitive`
- `evolution`：适用于 `synthesis`
- `scenario`：适用于 `decision`

`domain` 不是主要路径之一，而是长期维护的总览入口与知识组织层。

## 3. 手工写 `request.md`

`request.md` 只做三件事：

- 定义问题
- 划定范围
- 写明非目标

注意：

- 这一步不要求你已经搞清完整流程
- 机制细节、层级划分、能力归属判断，放到 `plan.md` 的“后续确认问题”

## 4. 生成并 review `plan.md`

`plan.md` 合并了计划层与来源规划层。

至少要回答：

- 这轮必须回答什么
- 哪些问题要放到后续确认
- 预算是 `deep / focused / light` 哪一档
- `L1/L2/L3/L4` 分别先看什么
- 当前缺什么证据
- 什么条件下算本轮可交付

对 `primitive`，推荐把以下问题放进“后续确认问题”：

- 为什么不直接改传统 transaction 路径
- `bundler`、`EntryPoint`、`paymaster` 分别位于哪一层
- 哪些能力属于 protocol-native，哪些只是 official ecosystem 或 third-party

## 5. 按需补可选文件

不是每轮都要开所有文件。

默认判断：

- `dependencies.md`
  适合 `synthesis / domain / decision`
- `decision-criteria.md`
  只适合 `decision`
- `evidence-matrix.md`
  适合有争议主张、证据等级不稳或比较判断较多的 case

## 6. 生成并 review `draft.md`

`draft.md` 合并了旧的 glossary、analysis、verdict。

推荐顺序：

1. 关键术语
2. 分析入口
3. 机制拆解
4. 设计原因
5. 边界与前提
6. 与相邻对象的关系
7. 当前可确认结论
8. 当前不能确认的部分
9. 后续补证

约束：

- 术语区必须是列表
- 先机制，后价值
- 先事实，后判断
- 必须说明为什么这样设计，而不是那样设计
- 必须区分 protocol-native、official ecosystem、third-party
- 必须区分 live、planned、promotional

## 7. 提炼长期资产

本仓库区分：

- `openspec/changes/<change-name>/`：当前一轮研究过程
- `knowledge/analysis/` 和 `knowledge/decisions/`：长期正式资产

因此每轮研究完成后，应执行一次“提炼”动作：

- 只把 durable 结果提升到 `knowledge/analysis/` 或 `knowledge/decisions/`
- 不把 `request.md`、`plan.md`、`evidence-matrix.md` 原样留在长期目录中
- `primitive / synthesis / domain` 的稳定结果默认提炼为 `reference.md`
- `decision` 的 `verdict.md` 可以作为长期文件保留
- 术语层默认折叠进 `reference.md` 的“关键术语”区
