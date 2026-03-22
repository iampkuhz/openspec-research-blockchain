# 工作流

## 核心思路

本仓库不是“立项 -> 设计 -> 开发任务”的实现型流程，而是“问题定义 -> 证据组织 -> 机制分析 -> 有限结论”的研究型流程。

统一工作流如下：

1. 定义对象层级
2. 选择研究路径
3. 定义范围与预算
4. 建立 sources 与 glossary
5. 完成 analysis
6. 输出 verdict
7. 把结果挂回更高层研究

## 1. 定义对象层级

优先回答这不是“我要研究什么技术”，而是“我要在什么层级研究它”：

- `primitive`：单协议 / 单机制 / 单能力点
- `synthesis`：关系、演进、分层分析
- `domain`：长期主题域地图与知识组织层
- `decision`：场景化比较、选型、判断

更准确地说：

- 技术分析主链：`primitive -> synthesis -> domain`
- `decision` 是独立的场景应用层
- `primitive` 和 `synthesis` 与哪些 `domain` 相关，不通过父路径强绑定，而通过依赖声明表达

## 2. 选择研究路径

- `deep-dive`：适用于 `primitive`
- `evolution`：适用于 `synthesis`
- `scenario`：适用于 `decision`

`domain` 不是主要路径之一，而是长期维护的总览入口与知识组织层。

## 3. 定义范围与预算

在 `brief.md` 中至少回答：

- 当前问题到底要回答什么
- 哪些问题不回答
- 依赖哪些下层研究
- 每个依赖是 `deep`、`focused` 还是 `light`
- 为什么只需要这个深度

## 4. 建立证据与术语层

优先维护三个文件：

- `sources.md`
- `glossary.md`
- `evidence-matrix.md`

这样做的目的，是先锁定概念边界和证据边界，再进入正文分析。

## 5. 写 `analysis.md`

推荐顺序：

1. 对象是什么
2. 它解决什么问题
3. 它的机制如何工作
4. 为什么这样设计
5. 它的边界在哪里
6. 与相邻方案的关系是什么
7. 当前题目的结论到底能落到哪一层

## 6. 写 `verdict.md`

`verdict.md` 不是摘要页，而是“有限结论页”。

必须包含：

- 当前能确定什么
- 当前不能确定什么
- 结论依赖哪些证据
- 结论适用于什么前提
- 哪些宣传性表述应排除在外

## 7. 挂回上层研究

当 `primitive` 研究成熟后，它可以被：

- `synthesis` 用来分析关系与演进
- `domain` 用来更新主题地图与长期知识组织
- `decision` 用来支持具体判断

但上层研究不能复制下层全文，只能：

- 声明依赖
- 按预算抽取
- 在本题语境下重组

## 8. 从 change packet 提升为长期资产

本仓库区分：

- `openspec/changes/<change-name>/`：当前一轮研究过程
- `knowledge/analysis/` 和 `knowledge/decisions/`：长期正式资产

因此每轮研究完成后，应执行一次“提炼”动作：

- 只把 durable 结果提升到 `knowledge/analysis/` 或 `knowledge/decisions/`
- 不把 `request.md`、`brief.md`、`sources.md`、`evidence-matrix.md` 原样留在长期目录中
- `primitive / synthesis / domain` 的结论默认并入 `analysis.md`
- `decision` 的 `verdict.md` 可以作为长期文件保留

## 推荐节奏

### 快速启动

- 先写 `request.md`
- 再写 `brief.md`
- 先列 `sources.md` 的待读清单
- 先补 5 到 10 张 glossary 卡

### 进入分析

- 先做机制拆解
- 再做关系与边界
- 最后再写价值与结论

### 定期维护

- `domain` 定期更新主题地图
- `primitive` 在核心规范变动时更新
- `synthesis` 在出现新 EIP / 新机制关系时更新
- `decision` 在场景假设、候选方案或证据状态变化时更新
