# spec-plan

为当前仓库中的一个 research change 生成或改写 `plan.md`。

**用法：**
- `/spec-plan`
- `/spec-plan openspec/changes/<change-name>/`
- `/spec-plan /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 plan 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/plan.md`
- `openspec/specs/plan-generation/spec.md`

本命令由 @research-author-agent contract 驱动。

4. **并行策略**
   - 可并行：
     - @research-author-agent 起草问题拆解、交付范围、研究深度、完成标准
     - @source-evidence-agent 生成或更新 `sources/source-review.md`
   - 必须串行：
     - `plan.md` 最终定稿
     - 依赖声明与证据缺口的最终收口

5. **冰箱策略**
   - 对暂时无法确认的来源、依赖深度、待补链接，不阻塞整份 `plan.md`
   - 统一写入：
     - “待确认问题”
     - “来源规划”
     - “证据缺口”
   - 但不能把 blocked item 冒充为已验证结论

6. **生成或更新 `plan.md`**
   - 基于已有内容增量修订，而不是无差别重写
   - 不提前写分析正文
   - 显式写清研究深度、来源规划、图表范围、证据缺口、完成标准

7. **完成总结**
   - 使用的 change 路径
   - 更新了哪些 section
   - 是否还需要补 `sources/`
   - 建议用户重点 review 哪些部分
   - 冰箱清单及其解冻条件
