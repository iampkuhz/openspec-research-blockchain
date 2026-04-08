# spec-request

辅助生成或完善 research change 的 `request.md` 文件。

**用法：**
- `/spec-request`
- `/spec-request openspec/changes/<change-name>/`
- `/spec-request /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 request 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/request.md`
- `openspec/specs/request-generation/spec.md`
- `harness/agents/_index.yaml`

本命令默认由 @research-author-agent contract 驱动。

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 如果用户提供了路径，使用该路径
   - 否则尝试从当前工作目录推断
   - 如无法确定，再询问用户要创建或使用的 change 名称

2. **补齐 request 语义**
   - 研究对象类型
   - 研究路径
   - 核心问题
   - 触发原因
   - 范围边界
   - 已知输入

3. **并行策略**
   - 可并行：
     - 读取 schema、template、现有 `request.md`
     - 扫描当前 change 下已有文件，判断是否已有可复用背景
   - 必须串行：
     - 目标 change 目录确认
     - `request.md` 的最终写入

4. **冰箱策略**
   - 如果用户上下文不足，但仍能界定最小研究方向：
     - 先写最小可用 `request.md`
     - 将未解信息体现在核心问题、范围边界或已知输入中
     - 在总结中输出冰箱清单
   - 如果连对象类型或研究路径都无法安全判断：
     - 停止并询问，不假装完成

5. **生成或增量修订 `request.md`**
   - 严格按正式 spec 与模板执行
   - 不提前写正文结论

6. **完成总结**
   - 使用的 change 路径
   - 对象类型和路径
   - 定义了哪些核心问题
   - 建议下一步是否需要先补 `sources/` 再进入 `/spec-plan`
   - 冰箱清单（如有）
