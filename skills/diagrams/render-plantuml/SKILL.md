# Skill: Render PlantUML

## Purpose

渲染 PlantUML 源文件为 SVG/PNG 格式，并进行基础验证。

## Triggers

用户请求：
- "渲染这个图"
- "生成 SVG"
- "预览 PlantUML"

## Required Inputs

- **source_file**: PlantUML 源文件路径 (.puml)

## Forbidden Inputs / Anti-patterns

- 不要渲染未通过语法检查的文件
- 不要输出过大的图片（考虑简化）
- 不要忽略渲染错误

## Files to Read

- PlantUML source file
- `harness/rules/diagrams/annotation-rules.md` - 注释规则

## Files to Write

### 1. Rendered Output

`openspec/changes/<change-id>/diagrams/build/<diagram-id>.svg`
`openspec/changes/<change-id>/diagrams/build/<diagram-id>.png`

### 2. Render Log (如出错)

`openspec/changes/<change-id>/diagrams/build/<diagram-id>.log`

## Local Validation Steps

1. 检查 PlantUML 语法
2. 执行渲染
3. 验证输出文件存在
4. 检查输出大小

## Output Contract

```yaml
diagram_id: <diagram-id>
source_path: <path to .puml>
output_svg: <path to .svg>
output_png: <path to .png>
status: success|failed
error: <error message if failed>
```

## Quality Gate

- [ ] 语法检查通过
- [ ] SVG 生成成功
- [ ] PNG 生成成功
- [ ] 输出文件大小合理

## Failure Modes

### 语法错误

**处理**：报告具体错误位置和原因。

### 渲染超时

**处理**：图可能过于复杂，建议简化。

### 输出过大

**处理**：建议拆分或简化图。

## When to Stop and Ask for Manual Triage

- 持续渲染失败原因不明
- 输出质量严重不达标
- 需要特殊 PlantUML 配置
