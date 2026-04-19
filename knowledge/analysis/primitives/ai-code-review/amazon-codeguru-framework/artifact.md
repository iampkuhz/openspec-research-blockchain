<!--
研究元数据：
- 研究深度：deep
- 对象类型：primitive
- 研究路径：deep-dive
- 相关 domains：ai-code-review, ml-driven, aws-ecosystem, java-ecosystem
- 创建时间：2026-04-19
- 来源 change：amazon-codeguru-framework
- 状态：stable
-->

<!-- 目录 -->
- [概述](#概述)
- [关键术语](#关键术语)
- [角色与信任边界](#角色与信任边界)
- [组件架构](#组件架构)
- [核心流程](#核心流程)
- [功能演进路径](#功能演进路径)
- [可用性变更与替代路径](#可用性变更与替代路径)
- [设计取舍](#设计取舍)
- [能力边界](#能力边界)
- [可确认结论](#可确认结论)
- [Evidence Gap](#evidence-gap)
- [参考资料](#参考资料)

## 概述

Amazon CodeGuru Reviewer 是 AWS 于 2019 年 Re:Invent 发布的 AI 驱动代码审查服务。它采用 **"program analysis + machine learning" 双引擎架构**，对提交到代码仓库（CodeCommit、GitHub、Bitbucket、GitHub Enterprise Server）的代码变更进行自动审查，输出关于代码质量、性能反模式、并发安全和资源泄漏的建议。其独特之处在于对 Java 场景的深度优化——通过 JVM 字节码分析补充源码级静态分析的盲区。[L1, L3]

**关键现状**：截至 2025 年 11 月 7 日，AWS 已停止 CodeGuru Reviewer 的新建仓库关联功能，现有用户可继续使用已关联的仓库。CodeGuru 的代码分析能力已迁移至 Amazon Q Developer（代码审查）和 Amazon Inspector（代码扫描），Detector Library 也已统一归入 Amazon Q 品牌下。[L1]

| 维度 | 说明 |
|------|------|
| 它是什么 | AWS 托管的 AI 代码审查 SaaS 服务，融合程序分析与 ML 推荐引擎，对代码变更提供自动化 review 建议；**当前已进入可用性缩减阶段，不再接受新仓库关联** |
| 表现形式 | SaaS 服务（AWS Console + CLI + API + IDE 插件 + CI/CD 集成），完全闭源 |
| 类比理解 | 类似于 SonarQube（静态分析）与 GitHub Copilot Review（ML 建议）的结合体，但深度集成 AWS 生态，且对 Java 字节码有原生分析能力 |
| 在模型中的位置 | 属于 CI/CD Pipeline 中的自动化代码质量关卡（gate），位于代码提交之后、合并之前；在 AI Code Review 领域中属于"托管式、ML 增强型"路径；当前正处于向 Amazon Q Developer 迁移的过渡期 |

## 关键术语

| 术语 | 定义 | 在本题中的作用 |
|------|------|---------------|
| CodeGuru Reviewer | AWS 的 AI 代码审查服务，本文研究的核心对象；2025 年 11 月 7 日起停止新建仓库关联 | 定义研究边界与生命周期状态 |
| Program Analysis | 程序分析，基于规则和静态分析技术对代码进行缺陷检测 | 双引擎架构中的一极，与 ML 互补 |
| ML Recommendation Engine | CodeGuru 内部的机器学习推荐引擎，基于 AWS 内部代码库训练，输出代码改进建议 | 核心组件之一，理解其能力与限制 |
| Static Analysis Engine | 基于规则的静态代码分析引擎，检测已知的反模式和最佳实践违反 | 核心组件之二，与 ML 引擎互补 |
| Bytecode Analysis | 对 Java 编译后的 JVM 字节码进行分析，检测运行期行为特征（如资源泄漏路径、锁竞争模式） | Java 专项优化的核心机制，CodeGuru 的差异化能力 |
| Review | 一次完整的代码审查操作，包含代码提交、分析执行、结果生成 | 基本工作单元 |
| Recommendation | 单次 review 产出的具体建议项，包含严重级别、分类、修复建议 | 输出物基本单位 |
| Code Review Association | 将 Review 与具体代码仓库和 Pull Request / Merge Request 关联的配置 | 集成机制，2025 年 11 月 7 日后不可新建 |
| Amazon Q Detector Library | 原 CodeGuru Reviewer 的检测器库，现已迁移至 Amazon Q 品牌下，覆盖 Java、Python、TypeScript 等 18 种语言 | 能力继承与演进的关键证据 |
| Amazon Q Developer | AWS 的 AI 开发者助手，继承了 CodeGuru Reviewer 的代码审查能力（SAST、secrets 检测、依赖漏洞检测、代码质量检测） | CodeGuru Reviewer 的主要替代路径 |
| Amazon Inspector | AWS 的自动化漏洞管理服务，新增代码扫描能力（GitHub/GitLab 仓库自动发现与扫描） | CodeGuru Reviewer 的另一替代路径 |

## 角色与信任边界

```
  +---------------------------------------------------------------+
  |                    客户侧 (Customer Account)                    |
  |                                                               |
  |  +----------+    +--------------+    +--------------------+   |
  |  |Developer |    |Source Code   |    |CI/CD Pipeline      |   |
  |  |(IDE/CLI) |    |Repository    |    |(CodePipeline/      |   |
  |  |          |    |(CodeCommit/  |    | GitHub Actions)    |   |
  |  |          |    | GitHub/      |    |                    |   |
  |  |          |    | Bitbucket)   |    |                    |   |
  |  +----+-----+    +------+-------+    +---------+----------+   |
  |       |                 |                      |             |
  |       |                 |  Code Diff           |             |
  |       |                 |  (Trigger Review)     |             |
  |       |                 v                      |             |
  |       |         +---------------+              |             |
  |       |         |  IAM Role     |              |             |
  |       |         |  (权限委托)    |              |             |
  |       |         +-------+-------+              |             |
  |       |                 |                      |             |
  |=======|=================|======================|=============|
  |       |                 |   信任边界            |             |
  |=======|=================|======================|=============|
  |       |                 v                      |             |
  |       |    +----------------------------+      |             |
  |       |    |  AWS CodeGuru Reviewer     |      |             |
  |       |    |  (托管服务)                 |      |             |
  |       |    |                            |      |             |
  |       |    |  +--------+ +-----------+  |      |             |
  |       |    |  |ML      | |Static     |  |      |             |
  |       |    |  |Engine  | |Analyzer   |  |      |             |
  |       |    |  +--------+ +-----------+  |      |             |
  |       |    |  +----------------------+  |      |             |
  |       |    |  |Bytecode Analyzer     |  |      |             |
  |       |    |  |(Java-specific)       |  |      |             |
  |       |    |  +----------------------+  |      |             |
  |       |    +-------------+--------------+      |             |
  |       |                  |                     |             |
  |       |    +-------------v--------------+      |             |
  |       |    |  Review Recommendations     |      |             |
  |       |    +-------------+---------------+      |             |
  |       |                  | 建议返回              |             |
  |       v                  v                      v             |
  |  +------------------------------------------------------+    |
  |  |              结果呈现层                                  |    |
  |  |  AWS Console / PR Comments / CLI Output / IDE          |    |
  |  +------------------------------------------------------+    |
  +---------------------------------------------------------------+
```

**信任边界说明**：

| 边界 | 跨越内容 | 信任假设 |
|------|----------|----------|
| 客户代码 -> CodeGuru 服务 | 代码 diff、仓库元数据 | 客户信任 AWS 不对代码内容进行未授权访问；通过 IAM 角色委托最小权限 [L1] |
| CodeGuru -> 客户仓库 | Review 建议（PR/MR comments） | 仓库需授予 CodeGuru 写评论的权限；通过 OAuth/GitHub App 授权 [L1] |
| CodeGuru 内部组件之间 | 代码数据、分析结果 | AWS 内部信任，不对外暴露 |
| 客户代码 -> Amazon Q Developer（替代路径） | 代码内容（IDE 插件或 GitHub/GitLab 集成） | 由 Amazon Q 数据处理协议约束 [L1] |

**关键信任假设**：
- 客户代码在传输和静态分析过程中受 AWS 安全责任模型保护 [L1]
- CodeGuru 的 ML 模型训练使用客户代码的方式受 AWS 数据处理协议约束（AWS 声明不将客户代码用于训练其他客户的模型）[L1]
- IAM 角色是跨信任边界的唯一授权机制 [L1]

## 组件架构

CodeGuru Reviewer 采用 **"program analysis + ML recommendation" 双引擎架构**，其中 program analysis 引擎内部包含基于规则的静态分析子模块和 Java 专用的字节码分析子模块。三个分析子模块并行工作，结果在聚合层去重和排序后输出。[L1, L3]

**架构说明**：Program analysis（静态分析 + 字节码分析）与 ML recommendation 是两个独立的分析引擎族。字节码分析是 program analysis 引擎中专为 Java 设计的子模块，而非与双引擎并列的第三个独立引擎。

```
+-------------------------------------------------------------+
|                  CodeGuru Reviewer Service                   |
|                                                             |
|  +-------------------------------------------------------+  |
|  |              Code Ingestion Layer                      |  |
|  |  +-----------+  +-----------+  +-----------------+    |  |
|  |  |Git Diff   |  |Full       |  |Bytecode         |    |  |
|  |  |Parser     |  |Repo Index |  |Extractor        |    |  |
|  |  +-----+-----+  +-----+-----+  +--------+--------+    |  |
|  +--------+--------------+-------------------+------------+  |
|           |              |                   |               |
|  +--------v--------------v-------------------v------------+  |
|  |              Analysis Layer                             |  |
|  |                                                         |  |
|  |  +-----------------+  +----------------------------+   |  |
|  |  |ML Recommendation|  |Program Analysis Engine     |   |  |
|  |  |Engine           |  |                            |   |  |
|  |  |                 |  |  +--------------------+    |   |  |
|  |  |- Pattern-based  |  |  |Rule-based Checker  |    |   |  |
|  |  |  recommendations|  |  +--------------------+    |   |  |
|  |  |- Trained on AWS |  |                            |   |  |
|  |  |  internal code  |  |  +--------------------+    |   |  |
|  |  +--------+--------+  |  |AWS Best Practice   |    |   |  |
|  |           |           |  |Rule Base           |    |   |  |
|  |           |           |  +--------------------+    |   |  |
|  |           |           |                            |   |  |
|  |           |           |  +---------------------+   |   |  |
|  |           |           |  |Bytecode Analyzer    |   |   |  |
|  |           |           |  |(Java-specific)      |   |   |  |
|  |           |           |  |- Data flow analysis |   |   |  |
|  |           |           |  |- Resource leak paths|   |   |  |
|  |           |           |  |- Concurrency issues|   |   |  |
|  |           |           |  +---------------------+   |   |  |
|  |           |           +-------------+--------------+   |  |
|  +-----------+-------------------------+------------------+  |
|              |                         |                     |
|  +-----------v-------------------------v------------------+  |
|  |              Aggregation & Output Layer                 |  |
|  |                                                         |  |
|  |  +-----------------+  +----------------------------+   |  |
|  |  |Recommendation   |  |Output Formatter            |   |  |
|  |  |Aggregator       |  |- PR comments               |   |  |
|  |  |(dedup, rank,    |  |- Console dashboard         |   |  |
|  |  | severity scoring)|  |- CLI/SDK output           |   |  |
|  |  +-----------------+  +----------------------------+   |  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
```

### 组件详述

#### 1. ML Recommendation Engine [L3]

**功能**：基于机器学习模型生成代码改进建议。

**已知特性**：
- 训练数据来源于 AWS 内部代码库（包含大量 Java 和 Python 代码）以及开源代码库 [L3]
- 模型学习的是 "代码变更 -> reviewer 建议 -> 最终修改" 的模式，而非简单的语法错误检测 [L3]
- 输出的是 **建议性** (recommendation) 而非 **阻断性** (blocking) 结果 [L1]
- 覆盖的问题类型包括：代码复杂度、资源管理、并发安全、异常处理、最佳实践等 [L3]

**限制（闭源导致的不确定性）**：
- 具体模型架构（transformer-based、sequence-to-sequence、classifier-based 等）未公开
- 训练数据的具体规模、标注策略、数据清洗流程未公开
- 模型更新频率和方式（在线学习 vs 离线批量训练）未公开

#### 2. Program Analysis Engine（含静态分析与字节码分析）[L1]

**功能**：基于预定义规则集进行静态代码分析，Java 场景下附加字节码层面深度分析。

**静态分析子模块**：
- 规则覆盖 Java、Python 等支持的语言 [L1]
- 规则类型包括：AWS 最佳实践（如 AWS SDK 使用不当）、通用编程反模式、安全漏洞模式 [L1]
- 规则库由 AWS 持续维护和更新 [L3]
- 与 ML 引擎互补：规则引擎覆盖已知的确定性问题，ML 引擎覆盖更模糊的模式匹配 [L3]

**字节码分析子模块（Java 专项）**：
- 这是 CodeGuru Reviewer 区别于其他 code review 工具的核心差异化能力 [L3]
- Java 源码层面的静态分析无法捕获编译器优化后的实际执行路径 [L3]
- 字节码层面可以观察到：实际的 try-finally 块展开、异常传播路径、锁获取/释放的精确位置、lambda 表达式的实际调用链 [L4]
- 对资源泄漏检测尤为重要：源码中的 try-with-resources 在编译后会被展开为复杂的 try-finally 结构，字节码分析可以更精确地追踪资源是否在所有退出路径上被正确释放 [L4]

**字节码分析覆盖的检测类别** [L1]：

| 检测类别 | 示例 | 字节码分析的优势 |
|----------|------|-----------------|
| 资源泄漏 | 未关闭的 InputStream、Connection | 追踪编译后的 finally 块中的所有退出路径 |
| 并发问题 | 不正确的 synchronized 使用、潜在死锁 | 观察实际的 monitor 操作指令 |
| 性能反模式 | 低效的字符串拼接、不必要的对象创建 | 分析实际的字节码指令序列 |
| 异常处理 | 过度宽泛的 catch、异常吞没 | 追踪异常在编译后的传播路径 |

**AWS Best Practice Rule Base**：
- AWS SDK 使用最佳实践（如正确使用 AWS SDK client、资源管理）[L1]
- AWS 服务集成的常见陷阱（如 DynamoDB 查询模式、S3 操作）[L1]
- 云原生最佳实践（如凭证管理、超时配置、重试策略）[L1]
- 规则持续更新，反映 AWS 服务的最佳实践演进 [L3]

## 核心流程

以下展示从代码提交到 review 建议返回的完整流程，以 GitHub PR 集成场景为例。

### Happy Path：GitHub PR 触发 Review

```
Developer          GitHub Repo          CodeGuru Reviewer         AWS IAM
    |                  |                       |                    |
    |--(1) Push code-->|                       |                    |
    |                  |                       |                    |
    |--(2) Create PR-->|                       |                    |
    |                  |                       |                    |
    |                  |--(3) Webhook--------->|                    |
    |                  |   (PR event)          |                    |
    |                  |                       |                    |
    |                  |                       |--(4) Assume Role-->|
    |                  |                       |<-(5) Credentials---|
    |                  |                       |                    |
    |                  |<-(6) Fetch diff--------|                    |
    |                  |--(7) Diff data-------->|                    |
    |                  |                       |                    |
    |                  |                       |  (8) Analyze:      |
    |                  |                       |  - ML Engine       |
    |                  |                       |  - Static Analyzer |
    |                  |                       |  - Bytecode (Java) |
    |                  |                       |                    |
    |                  |<-(9) Post PR comments--|                    |
    |                  |                       |                    |
    |<-(10) View recommendations               |                    |
    |                  |                       |                    |
```

**流程步骤说明**：

- **【S1-S2】代码提交与 PR 创建**：开发者在本地完成代码变更后 push 到 GitHub，并创建 Pull Request。这是触发 review 的起点。

- **【S3】Webhook 触发**：GitHub 通过 webhook 将 PR 事件通知 CodeGuru Reviewer。CodeGuru 需要预先通过 Code Review Association 配置与仓库的关联关系 [L1]。**注意：2025 年 11 月 7 日后，无法新建此关联。**

- **【S4-S5】权限获取**：CodeGuru 通过 AssumeRole 获取访问仓库的临时凭证。这体现了 AWS 的标准安全模式——CodeGuru 本身不存储仓库凭证，而是通过 IAM 角色委托获取最小权限访问 [L1]。

- **【S6-S7】代码获取**：CodeGuru 从仓库拉取 PR 的 diff 数据（变更的文件列表和具体内容），以及相关的完整文件内容用于上下文分析 [L4]。

- **【S8】并行分析**：ML 引擎、静态分析引擎、字节码分析子模块（Java 场景）并行执行。Java 场景下，如果代码仓库中包含编译后的 .class/.jar 文件，字节码分析子模块也会被激活 [L3]。

- **【S9】建议回写**：分析结果以 PR comment 的形式回写到 GitHub，每条 recommendation 包含严重级别、分类、具体建议和修复示例 [L1]。

- **【S10】开发者查看与处理**：开发者在 PR 页面直接查看 CodeGuru 的建议，可以选择接受、忽略或讨论 [L1]。

### 异常路径

| 异常场景 | 触发条件 | 处理结果 |
|----------|----------|----------|
| 代码无法编译（Java） | 字节码分析需要编译后的 .class 文件 | 字节码分析跳过，仅执行 ML 和静态分析 [L3] |
| 权限不足 | IAM Role 缺少必要权限 | Review 失败，返回错误信息 [L1] |
| 仓库不可访问 | 网络问题或仓库 API 限流 | Review 标记为 Failed，可重试 [L2] |
| 代码量过大 | 单次 PR 变更超过服务限制 | 分析可能被截断或延迟，具体阈值未公开 [L4] |
| ML 服务暂时不可用 | AWS 内部服务问题 | 静态分析结果仍会返回，ML 建议缺失 [L4] |

### Review 生命周期状态转换

| 当前状态 | 触发事件 | 转换结果 | 说明 |
|----------|----------|----------|------|
| Created | Review 创建请求 | Pending | Review 已创建，等待代码拉取 |
| Pending | 代码获取成功 | InProgress | 分析引擎开始执行 |
| Pending | 代码获取失败 | Failed | 权限不足或仓库不可访问 |
| InProgress | 所有分析引擎完成 | Completed | 建议生成完毕 |
| InProgress | 分析超时或内部错误 | Failed | 服务异常 |
| Completed | - | 终态 | 结果可查看，不可变更 |
| Failed | 手动重试 | Pending | 重新进入分析流程 |

## 功能演进路径

根据公开资料，CodeGuru Reviewer 的功能演进可分为以下四个阶段。

### 阶段一：发布与 Java 专注（2019 Q4 - 2020 Q2）

**时间节点**：2019 年 12 月，AWS re:Invent 2019 [L3]

**关键特性**：
- 初始发布，支持 Java 语言 [L3]
- 集成 Amazon CodeCommit 和 GitHub [L1]
- 核心能力：ML recommendation engine + 基于规则的静态分析 [L3]
- 字节码分析（bytecode analysis）作为 Java 专属能力引入 [L3]
- 定位：自动代码审查，减少人工 review 负担 [L3]

**设计动机**：
- AWS 内部积累了大量 code review 数据，具备了训练 ML 模型的基础 [L3]
- Java 是 AWS 企业内部使用最广泛的语言，选择 Java 作为首发语言具有最大的内部和外部价值 [L4]

### 阶段二：能力扩展与语言支持（2020 Q3 - 2022）

**关键特性**：
- 扩展支持 Python 语言 [L1]
- 增加对 Bitbucket Cloud 和 Bitbucket Server 的支持 [L1]
- CLI 工具发布，支持本地代码分析（无需完整仓库关联）[L1]
- 规则库持续扩展，覆盖更多 AWS 服务最佳实践 [L3]
- 与 CodePipeline 深度集成，支持 CI/CD 流水线中的自动审查关卡 [L1]

**Python 支持的特殊性**：
- Python 没有字节码分析（JVM 字节码分析是 Java 特有），Python 支持纯依赖 ML 引擎和规则引擎 [L3]
- 这意味着 Python 用户的分析深度与 Java 用户不同，Java 场景下的字节码分析是 Java 用户的独占优势 [L4]

### 阶段三：深化与生态整合（2023 - 2024）

**关键特性**：
- Amazon CodeGuru 品牌整合，Reviewer 与 Profiler 统一入口 [L3]
- GitHub Enterprise Server 支持 [L1]
- 更细粒度的建议分类和严重级别管理 [L1]
- 与 AWS IAM Identity Center 集成改进 [L2]
- 定价模型优化（基于代码行数/分析次数的计费）[L1]
- 与 Amazon Q Developer（原 CodeWhisperer）的生态协同 [L3]
- 支持 Amazon S3 作为代码源（通过 GitHub Actions）[L1]

### 阶段四：可用性缩减与能力迁移（2025 年 11 月至今）

**关键事件**：2025 年 11 月 7 日，AWS 宣布 CodeGuru Reviewer 停止新建仓库关联 [L1]

**具体影响**：
- **不可新建**：无法创建新的 repository association [L1]
- **可用延续**：已关联的仓库可继续使用 CodeGuru Reviewer [L1]
- **能力迁移**：代码分析能力转移至两个替代服务 [L1]：
  - **Amazon Q Developer**：代码审查能力（SAST、secrets 检测、依赖漏洞检测、代码质量检测），支持 IDE 插件、GitHub、GitLab
  - **Amazon Inspector**：代码扫描能力（自动发现 GitHub/GitLab 仓库、扫描软件漏洞和意外网络暴露）
- **Detector Library 品牌迁移**：原 "Amazon CodeGuru Reviewer Detector Library" 已更名为 "Amazon Q Detector Library"，覆盖 18 种语言 [L1]

**Detector Library 数据（迁移后，Java 与 Python 已验证）** [L1]：

| 语言 | 检测器数量 | 说明 |
|------|-----------|------|
| Java | 132 | 覆盖资源泄漏、并发安全、SQL 注入、XSS 等 |
| Python | 131 | 覆盖 SQL 注入、OS 命令注入、资源泄漏等 |
| TypeScript / C# / 其他 | 具体数量以官方页面为准 | 覆盖 Go, Ruby, C, C++, PHP, Kotlin, Scala, Shell, JavaScript, JSX, CloudFormation, Terraform 等 |

**演进趋势总结**：

| 维度 | 阶段一 (2019-2020) | 阶段二 (2020-2022) | 阶段三 (2023-2024) | 阶段四 (2025-) |
|------|-------------------|-------------------|-------------------|----------------|
| 语言覆盖 | Java only | Java + Python | Java + Python | 迁移至 Amazon Q（18 种语言） |
| 仓库支持 | CodeCommit + GitHub | + Bitbucket | + GHES + S3 | GitHub + GitLab（通过 Amazon Q/Inspector） |
| 分析引擎 | ML + Rules + 字节码 | 同左 | 同左（ML 模型持续迭代） | Amazon Q SAST + Inspector 扫描 |
| 集成方式 | 手动触发 / webhook | CI/CD pipeline | 全面集成 + CLI | IDE 插件 + GitHub/GitLab 集成 |
| 服务状态 | GA | 扩展期 | 成熟期 | **可用性缩减期** |
| 核心差异化 | Java 字节码分析 | 多语言 + 多仓库 | 生态整合 + 精细化 | 品牌整合至 Amazon Q |

## 可用性变更与替代路径

本节专门分析 2025 年 11 月 7 日 CodeGuru Reviewer 可用性变更的影响，以及 AWS 提供的替代路径。[L1]

### 可用性变更详情

**变更内容**：As of November 7, 2025, you can't create new repository associations in Amazon CodeGuru Reviewer. You can only use CodeGuru Reviewer with existing repository associations. [L1]

**影响分析**：

| 用户类型 | 影响 | 说明 |
|----------|------|------|
| 新用户（无现有仓库关联） | 无法使用 CodeGuru Reviewer | 必须选择 Amazon Q Developer 或 Amazon Inspector |
| 已有仓库关联的用户 | 可继续使用已关联的仓库 | 无法新增关联，可继续对已有仓库执行 review |
| 需要新增仓库的用户 | 无法关联新仓库 | 新项目必须使用替代服务 |

### 替代路径：Amazon Q Developer

Amazon Q Developer 继承了 CodeGuru Reviewer 的核心代码审查能力，并提供更广泛的语言支持：[L1]

| 能力 | CodeGuru Reviewer | Amazon Q Developer |
|------|-------------------|-------------------|
| SAST（静态应用安全测试） | 部分（通过规则引擎） | 支持 |
| Secrets 暴露检测 | 支持（集成 Secrets Manager） | 支持 |
| 依赖漏洞检测（SCA） | 不直接支持 | 支持 |
| 代码质量检测 | 支持（ML + 规则） | 支持 |
| 集成方式 | PR comments, Console, CLI | IDE 插件, GitHub, GitLab Duo |
| 语言覆盖 | Java, Python | 18 种语言 |
| 字节码分析 | Java 专属 | 未明确是否继承 |

**关键差异**：
- Amazon Q Developer 的集成方式从"仓库级 webhook 触发"转向"IDE 内实时 + PR 级异步"
- Amazon Q Developer 支持 GitLab（CodeGuru Reviewer 不支持）
- Amazon Q Developer 的 Detector Library 覆盖 18 种语言（远超 CodeGuru 的 2 种）
- **字节码分析能力是否在 Amazon Q Developer 中保留，官方文档未明确说明**（evidence gap）

### 替代路径：Amazon Inspector

Amazon Inspector 新增了代码扫描能力，侧重于安全维度：[L1]

| 能力 | CodeGuru Reviewer | Amazon Inspector Code Scanning |
|------|-------------------|-------------------------------|
| 仓库自动发现 | 不支持 | 支持（GitHub, GitLab） |
| 软件漏洞扫描 | 不直接支持 | 支持 |
| 意外网络暴露检测 | 不支持 | 支持 |
| 代码质量检测 | 支持 | 不侧重 |
| 分析触发 | PR 触发 + 全仓库分析 | 自动发现 + 扫描 |

**关键差异**：
- Amazon Inspector 侧重安全扫描（vulnerability + network exposure），CodeGuru Reviewer 侧重代码质量
- Amazon Inspector 支持仓库自动发现，降低了配置成本
- 两者能力互补，而非完全替代

## 设计取舍

| 取舍维度 | 选择 | 放弃 | 原因与 Trade-off |
|----------|------|------|-----------------|
| **分析引擎架构** | ML + program analysis 双引擎 | 纯 ML 或纯规则 | 纯 ML 误报率高且不可解释；纯规则覆盖度有限。双引擎互补：规则处理确定性问题，ML 处理模糊模式。Trade-off：增加系统复杂度和运维成本。[L3] |
| **Java 字节码分析** | 分析 JVM 字节码 | 仅分析 Java 源码 | 字节码层面可捕获编译器优化后的实际行为（资源泄漏路径、锁竞争）。Trade-off：需要构建编译产物，增加了使用门槛（用户必须提供 .class 文件才能启用完整分析）。[L4] |
| **建议性质** | 建议性（非阻断性） | 强制阻断 | CodeGuru 定位为"辅助"而非"门禁"，尊重开发者的最终判断权。Trade-off：可能被团队忽略，缺乏强制执行机制。[L3] |
| **闭源策略** | 完全闭源 SaaS | 开源核心或混合模式 | AWS 商业策略决定。ML 模型和规则库是核心商业资产。Trade-off：社区无法贡献规则、无法审计 ML 模型的偏见、无法自托管。[L4] |
| **训练数据来源** | AWS 内部代码 + 开源 | 仅开源或仅客户代码 | AWS 内部代码库包含大量企业级 review 数据，质量高。Trade-off：内部代码的模式可能与非 AWS 用户的代码模式不同，存在领域偏差风险。[L4] |
| **集成方式** | Webhook + 轮询 | 仅 CLI 或仅 IDE | 多通道集成最大化覆盖面。Trade-off：不同集成方式的分析结果可能不一致（CLI 本地分析 vs 服务端分析）。[L2] |
| **服务生命周期策略** | 可用性缩减而非直接下线 | 立即终止或无限期维持 | 现有用户可继续使用，避免突然中断；同时引导新用户至 Amazon Q/Inspector。Trade-off：双轨维护增加运营成本。[L1] |

## 能力边界

### 强项

| 能力 | 说明 | 证据等级 |
|------|------|----------|
| Java 字节码分析 | JVM 字节码层面的资源泄漏、并发安全检测是其他通用 code review 工具不具备的能力 | L3 |
| AWS 最佳实践覆盖 | 对 AWS SDK 使用、云服务集成的最佳实践检测是独家优势 | L1 |
| ML 模式学习 | 基于 AWS 内部 review 数据训练的模型能捕捉人类 reviewer 的经验模式 | L3 |
| CI/CD 原生集成 | 与 AWS CodePipeline 的深度集成使其自然融入 AWS 用户的 DevOps 流程 | L1 |
| Detector Library 规模 | Java 132 个检测器、Python 131 个检测器，覆盖 OWASP Top 10 和 CWE Top 25 | L1 |

### 弱项

| 能力 | 说明 | 证据等级 |
|------|------|----------|
| 非 Java 语言深度 | Python 等语言缺少字节码分析层，分析深度不如 Java | L3 |
| 误报控制 | ML 建议的误报率较高（社区反馈），缺乏精确的误报抑制机制 | L4 |
| 可定制性 | 规则库不可扩展（用户无法添加自定义规则），ML 模型不可微调 | L2 |
| 自托管 | 完全 SaaS 化，不支持 on-premise 部署，对合规要求高的场景不适用 | L1 |
| 可解释性 | ML 建议的推理过程不透明，开发者难以理解"为什么给出这个建议" | L4 |
| 服务生命周期 | 已进入可用性缩减阶段，新用户无法使用，长期维护不确定 | L1 |
| 字节码分析迁移 | 不确定 Amazon Q Developer 是否继承了字节码分析能力 | L4 |

### Live / Planned / Deprecated

| 状态 | 能力 | 说明 |
|------|------|------|
| **Live（现有仓库）** | 全部功能 | 已关联的仓库可继续使用所有分析功能 |
| **Live** | Amazon Q Developer 代码审查 | SAST、secrets 检测、依赖漏洞检测、代码质量检测 |
| **Live** | Amazon Inspector 代码扫描 | 自动仓库发现、软件漏洞扫描、网络暴露检测 |
| **Deprecated（新关联）** | CodeGuru Reviewer 新建仓库关联 | 2025 年 11 月 7 日起不可新建 |
| **不确定** | CodeGuru Reviewer 最终终止 | 官方未公布终止日期 |

## 可确认结论

以下结论基于现有公开资料，按证据等级排列：

**【L1 证据 - 官方文档确认】**
1. Amazon CodeGuru Reviewer 是 AWS 托管的 AI 代码审查 SaaS 服务，支持 Java 和 Python。
2. 支持 CodeCommit、GitHub、Bitbucket、GitHub Enterprise Cloud、GitHub Enterprise Server、Amazon S3（通过 GitHub Actions）作为代码源。
3. 支持通过 AWS Console、CLI、API、PR comments 查看审查结果。
4. 审查结果为建议性（recommendation），非阻断性（blocking）。
5. 通过 IAM 角色进行跨账户/跨服务的权限管理。
6. **截至 2025 年 11 月 7 日，不可创建新的仓库关联，已有仓库关联可继续使用。**
7. 代码分析能力已迁移至 Amazon Q Developer（代码审查）和 Amazon Inspector（代码扫描）。
8. Detector Library 已迁移至 Amazon Q 品牌下，覆盖 18 种语言（Java 132 个检测器、Python 131 个）。
9. 服务支持 10 个 AWS 区域，每区域月度 review 配额为 5,000 次。
10. CLI 工具支持本地代码分析，无需完整的仓库关联。
11. 支持通过 `aws-codeguru-reviewer.yml` 文件抑制特定文件/目录的分析。

**【L2 证据 - API/实现层确认】**
12. 定价基于分析的代码行数（LOC），有免费额度。

**【L3 证据 - 官方演讲/博客确认】**
13. 2019 Re:Invent 首次发布，初始仅支持 Java。
14. 采用 program analysis + ML recommendation 的双引擎架构。
15. Java 场景下支持字节码分析，可检测资源泄漏、并发安全等问题。
16. ML 模型训练数据来源包含 AWS 内部代码库。
17. 后续扩展支持了 Python、Bitbucket、GitHub Enterprise Server。
18. 开发者反馈机制可帮助改进 ML 模型的推荐质量。

**【L4 证据 - 社区/推测，需降级使用】**
19. ML 模型的具体架构可能基于 transformer 或 sequence-to-sequence 模型（基于 AWS 同期其他 ML 服务的架构推测）。
20. 社区反馈 ML 建议的误报率在早期版本较高，后续有所改善。
21. 完全闭源的策略限制了其在强合规要求场景中的应用。
22. Python 等非 Java 语言用户的分析深度显著低于 Java 用户（缺少字节码分析层）。
23. Amazon Q Developer 是否继承了 Java 字节码分析能力尚未明确（关键不确定性）。

## Evidence Gap

以下因 CodeGuru Reviewer 闭源策略导致的证据缺口已显式列出：

1. **ML 模型架构**：AWS 未公开 ML 模型的具体架构（transformer / CNN / custom），无法确认是 fine-tune 开源模型还是自研。
2. **训练数据来源与规模**：仅能从 AWS 宣传中推测使用了内部代码库，具体规模和标注方式未知。
3. **字节码分析的具体规则**：Java 字节码层面的分析规则未公开，无法确认覆盖的 JVM 反模式范围。
4. **ML 与规则引擎的冲突处理**：当 ML 建议和静态规则建议冲突时如何处理，无公开文档说明。
5. **模型更新频率**：ML 模型的更新周期和方式（在线学习 / 离线训练 / 增量更新）未知。
6. **服务终止时间表**：2025 年 11 月 7 日后，现有仓库关联可继续使用多久？是否有最终终止日期？
7. **Amazon Q / Inspector 与 CodeGuru Reviewer 的能力映射**：哪些检测器是原样迁移，哪些是新增，哪些已移除？
8. **字节码分析能力继承**：Amazon Q Developer 是否继承了 Java 字节码分析能力，官方文档未明确说明。
9. **分析性能数据**：分析延迟、吞吐量等性能指标未公开。

## 参考资料

| 来源 | 说明 |
|------|------|
| [AWS CodeGuru Reviewer User Guide - What is CodeGuru Reviewer?](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/welcome.html) | 官方产品文档，描述功能、支持语言、仓库、访问方式 |
| [AWS CodeGuru Reviewer API Reference](https://docs.aws.amazon.com/codeguru/latest/reviewer-api/Welcome.html) | API 能力边界定义 |
| [CodeGuru Reviewer Availability Change](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/codeguru-reviewer-availability-change.html) | 2025 年 11 月 7 日可用性变更官方声明 |
| [How CodeGuru Reviewer Works](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/how-codeguru-reviewer-works.html) | 工作机制说明 |
| [Amazon Q Detector Library](https://docs.aws.amazon.com/codeguru/detector-library/index.html) | 迁移后的检测器库，含 Java 132 / Python 131 检测器列表 |
| [CodeGuru Reviewer Endpoints and Quotas](https://docs.aws.amazon.com/general/latest/gr/codeguru-reviewer.html) | 10 个区域端点，月度配额 5000/区域 |
| [AWS CodeGuru Reviewer 产品页面](https://aws.amazon.com/codeguru/reviewer/) | 官方功能定位、定价信息 |
| [AWS Blog - Amazon CodeGuru](https://aws.amazon.com/blogs/aws/amazon-codeguru/) | 2019 年发布博客 |
| [AWS DevOps Blog - CodeGuru 分类](https://aws.amazon.com/blogs/devops/category/amazon-codeguru/) | 使用案例、新功能公告 |
| [AWS CLI codeguru-reviewer 命令参考](https://docs.aws.amazon.com/cli/latest/reference/codeguru-reviewer/) | CLI 操作能力 |
