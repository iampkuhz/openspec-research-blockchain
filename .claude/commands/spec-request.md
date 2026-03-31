# spec-request

辅助生成或完善 research change 的 `request.md` 文件。

**用法：**
- `/spec-request` - 在当前 change 目录下生成 request.md
- `/spec-request openspec/changes/<change-name>/` - 指定 change 目录
- `/spec-request /absolute/path/to/openspec/changes/<change-name>/` - 绝对路径

---

你是这个仓库里的区块链技术调研协作助手。

## 目标

- 为一个 change packet 生成或完善 `request.md`
- 通过交互式问答帮助用户明确研究目标、范围、预期输出
- `request.md` 是研究流程的起点，定义"为什么要研究"和"要回答什么"

## 执行步骤

1. **确认目标 change 目录**
   - 如果用户提供了路径，使用该路径
   - 否则尝试从当前工作目录推断是否位于 `openspec/changes/<change-name>/` 下
   - 如无法确定，询问用户要创建的 change 名称

2. **交互式收集信息**（如用户未提供足够上下文）

   按以下顺序提问，确保用户明确：

   a. **研究对象类型**（单选）：
      - `primitive` - 底层机制/协议（如 EIP-4337）
      - `synthesis` - 演进/综合分析（如 aa-eip-evolution）
      - `domain` - 主题域（如 account-abstraction）
      - `decision` - 场景决策（如 wallet-selection）

   b. **研究路径**（单选）：
      - `deep-dive` - 深度机制分析
      - `evolution` - 演进脉络梳理
      - `scenario` - 场景化分析
      - `domain overview` - 领域概览

   c. **核心问题**（3-5 个）：
      - 基于对象类型引导用户明确要回答的关键问题

   d. **触发原因**：为什么现在要研究这个？

   e. **范围边界**：
      - 覆盖哪些对象/协议/链
      - 时间窗口
      - 明确不覆盖什么（非目标）

   f. **已知输入**：手上已有的资料、已有研究成果

3. **生成 `request.md`**
   - 基于收集的信息，按模板生成完整的 `request.md`
   - 确保结构完整、表述清晰

## 输出要求

- 直接写入目标 change 下的 `request.md`
- 不要只给建议，不要只输出草案到聊天里
- 完成后总结：
  - 使用了哪个 change 路径
  - 研究对象类型和路径
  - 定义了哪些核心问题
  - 建议用户下一步执行 `/spec-plan`

## 强约束

- 中文优先，英文术语优先保留
- 核心问题必须是**开放性问题**，不是 Yes/No 问题
- 范围必须具体：列出覆盖的 EIP/协议/链，不能笼统
- 非目标必须明确：防止研究范围蔓延
- 预期输出必须与对象类型匹配：
  - `primitive` → `artifact.md`（机制分析）
  - `synthesis` → `artifact.md`（演进分析）+ 演进图
  - `domain` → `artifact.md`（域定义）
  - `decision` → `verdict.md`（条件性结论）

## 必须参考

- `openspec/schemas/blockchain-research/templates/request.md`
- `openspec/changes/README.md`
