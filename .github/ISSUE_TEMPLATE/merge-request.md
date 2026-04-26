---
name: 研究产出合并
description: 将 `openspec/changes/` 中的研究产出合并到 `knowledge/` 长期资产
title: "[Merge] "
labels: ["merge"]
body:
  - type: markdown
    attributes:
      value: |
        请按以下模板填写合并请求。用于将已完成评审的 change 合并到长期知识库。

  - type: input
    id: change_id
    attributes:
      label: Change ID
      description: 对应的 `openspec/changes/` 目录名
      placeholder: e.g. primitive-did-auth
    validations:
      required: true

  - type: dropdown
    id: merge_type
    attributes:
      label: 合并类型
      options:
        - 新增（创建长期资产）
        - 更新（修改已有长期资产）
    validations:
      required: true

  - type: textarea
    id: summary
    attributes:
      label: 研究结论摘要
      description: 简要总结本研究的核心发现
    validations:
      required: true

  - type: textarea
    id: verification
    attributes:
      label: 验收确认
      description: 确认以下检查项是否通过
      value: |
        - [ ] draft.md 已完成评审
        - [ ] sources/ 已收集并验证
        - [ ] 证据等级符合要求（L1/L2 优先）
        - [ ] 术语与已有 glossary 一致
    validations:
      required: true
