# Design: <Change Title>

## Overview

[设计方案概述]

## Research Questions

### Q1: <问题>

** Motivation**: [为什么问这个问题]

** Expected Answer Type**: definition/mechanism/comparison/evaluation

### Q2: <问题>

...

## Source Plan

### L1 Sources

| Source | Type | Status |
|--------|------|--------|
| EIP-XXX | standard | pending/read/verified |
| Whitepaper | standard | pending/read/verified |

### L2 Sources

| Source | Type | Status |
|--------|------|--------|
| Reference Repo | implementation | pending/read/verified |
| Docs | documentation | pending/read/verified |

### L3 Sources

| Source | Type | Usage |
|--------|------|-------|
| Blog | official-blog | background/motivation |

## Output Structure

```
knowledge/topics/<domain>/<topic>/
├── overview.md
├── atoms/
│   ├── definition.md
│   ├── prerequisites.md
│   ├── core-mechanism.md
│   ├── module-evolution.md
│   ├── limits-and-assumptions.md
│   └── open-questions.md
├── claims/
│   ├── facts.yaml
│   └── inferences.yaml
├── sources/
│   ├── source-pack.yaml
│   └── primary-notes.md
└── diagrams/ (如有)
```

## Key Claims to Extract

- [ ] claim about definition
- [ ] claim about mechanism
- [ ] claim about performance

## Diagrams to Create

| ID | Type | Purpose |
|----|------|---------|
| arch-overview | component | 展示架构 |
| flow | sequence | 展示流程 |

## Terminology Plan

| Term | Category | Layer | Source |
|------|----------|-------|--------|
| Term 1 | protocol-entity | protocol | EIP-XXX |
| Term 2 | protocol-action | protocol | EIP-XXX |

## Evidence Gaps to Record

- [ ] gap about X
- [ ] gap about Y

## Validation Plan

- [ ] 自审 checklist
- [ ] 技术评审
- [ ] 可读性评审
