---
name: 新研究请求
description: 提出一个新的研究主题（primitive / synthesis / decision）
title: "[Research] "
labels: ["research"]
body:
  - type: markdown
    attributes:
      value: |
        请按以下模板填写研究请求。请求被接受后将在 `openspec/changes/` 下创建对应 change。

  - type: dropdown
    id: research_type
    attributes:
      label: 研究类型
      description: 选择本研究属于的类型
      options:
        - primitive（单一协议/机制的深入分析）
        - synthesis（多主题的横向对比/综合）
        - decision（场景判断与条件性结论）
    validations:
      required: true

  - type: textarea
    id: research_question
    attributes:
      label: 核心问题
      description: 本研究要回答的关键问题列表
      placeholder: |
        1. ...
        2. ...
    validations:
      required: true

  - type: textarea
    id: scope
    attributes:
      label: 研究范围
      description: 包括什么、不包括什么
    validations:
      required: true

  - type: textarea
    id: sources
    attributes:
      label: 已知来源
      description: 已知的论文、文档、URL 等来源
      placeholder: |
        - URL: ...
        - 论文: ...
    validations:
      required: false

  - type: textarea
    id: additional_context
    attributes:
      label: 补充说明
      description: 其他背景信息或相关上下文
    validations:
      required: false
