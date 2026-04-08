# spec-draft

为当前仓库中的一个 research change 生成或改写 `draft.md`。

**用法：**
- `/spec-draft`
- `/spec-draft openspec/changes/<change-name>/`
- `/spec-draft /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 draft 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/draft.md`
- `openspec/specs/draft-generation/spec.md`
- `openspec/specs/diagram-policy/spec.md`

本命令由 @research-author-agent contract 驱动。

4. **并行策略**
   - 可并行：
     - @research-author-agent 写概述、术语表、设计取舍、能力边界、相关协议对比
     - @diagram-agent 准备实体分类、图表清单、diagram package
     - 如存在未验证链接或关键 evidence gap，可定向唤回 @source-evidence-agent
   - 必须串行：
     - diagram contract 校验
     - `draft.md` 最终冻结版本

5. **先执行图表决策树**
   - 实体分类
   - 四个判定问题
   - 图表清单表
   - 覆盖缺口检查

6. **冰箱策略**
   - 对未通过 contract 的图、未解决的证据缺口、暂时无法确认的结论，放入冰箱清单
   - 同步写入：
     - `draft.md` 的“待确认问题”
     - `draft.md` 的不确定性表述
   - required 图未完成时，可以先写非图部分，但不能声称 `draft.md` 已完成

7. **生成或更新 `draft.md`**
   - 先写术语表，再写分析正文
   - 必须区分 live / planned / promotional
   - 不确定性必须显式写出

8. **diagram contract 校验**
   - PlantUML 只能通过用户级 skill 生成
   - 写完 `draft.md` 后必须执行 diagram contract 校验脚本

9. **完成总结**
   - 使用的 change 路径
   - 更新了哪些 section
   - 是否启用了 @diagram-agent
   - diagram contract 校验结果
   - 冰箱清单及其解冻条件
