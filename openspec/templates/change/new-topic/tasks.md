# Tasks: <Change Title>

## Task Breakdown

### Phase 1: Source Collection

- [ ] 创建 sources 目录结构
- [ ] 收集 L1 来源
- [ ] 收集 L2 来源
- [ ] 收集 L3/L4 来源（用于背景）
- [ ] 归档来源
- [ ] 创建 inbox.yaml

**Estimated Time**: X hours

**Output**: sources/inbox.yaml, sources/fetched/*, sources/excerpts/*

### Phase 2: Claims Extraction

- [ ] 从 excerpts 提取 facts claims
- [ ] 从 excerpts 提取 inferences claims
- [ ] 关联 claims 到 atoms
- [ ] 创建 claims/facts.yaml

**Estimated Time**: X hours

**Output**: claims/facts.yaml, claims/inferences.yaml

### Phase 3: Atom Writing

#### Definition Atom

- [ ] 编写 atoms/definition.md
- [ ] 提取关键术语
- [ ] 定义边界条件

**Estimated Time**: X hours

#### Mechanism Atom

- [ ] 编写 atoms/core-mechanism.md
- [ ] 解释设计动机
- [ ] 详细说明流程
- [ ] 创建图表（如需要）

**Estimated Time**: X hours

#### Evolution Atom (如适用)

- [ ] 编写 atoms/module-evolution.md
- [ ] 整理时间线
- [ ] 识别驱动因素

**Estimated Time**: X hours

#### Limits and Assumptions

- [ ] 编写 atoms/limits-and-assumptions.md
- [ ] 列出假设条件
- [ ] 说明已知限制

**Estimated Time**: X hours

### Phase 4: Diagram Creation

- [ ] 创建 diagram model
- [ ] 编写 PlantUML source
- [ ] 渲染 diagram
- [ ] diagram review

**Estimated Time**: X hours

**Output**: diagrams/models/*, diagrams/source/*, diagrams/build/*, diagrams/reviews/*

### Phase 5: Review

- [ ] 技术准确性评审
- [ ] 可读性评审
- [ ] diagram review（如适用）
- [ ] 修复问题

**Estimated Time**: X hours

**Output**: review/issues.md, review/review-summary.md

### Phase 6: Merge

- [ ] 确认 merge 条件
- [ ] 复制到 knowledge/
- [ ] 更新 changelog
- [ ] 更新 indexes
- [ ] 提交 commit

**Estimated Time**: X hours

## Dependencies

| Task | Depends On |
|------|------------|
| Phase 2 | Phase 1 |
| Phase 3 | Phase 2 |
| Phase 4 | Phase 3 (atoms ready) |
| Phase 5 | Phase 3, Phase 4 |
| Phase 6 | Phase 5 (review approved) |

## Critical Path

Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 6

## Timeline

| Phase | Start | End | Status |
|-------|-------|-----|--------|
| Phase 1 | date | date | pending/in-progress/completed |
| Phase 2 | date | date | pending/in-progress/completed |
| Phase 3 | date | date | pending/in-progress/completed |
| Phase 4 | date | date | pending/in-progress/completed |
| Phase 5 | date | date | pending/in-progress/completed |
| Phase 6 | date | date | pending/in-progress/completed |
