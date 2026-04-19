#!/bin/bash
#
# 渲染 PlantUML 图表
#
# 用法:
#   scripts/maintenance/render.sh <diagram-file.puml> [--output-dir <dir>]
#

set -e

# 默认输出目录
OUTPUT_DIR="${OUTPUT_DIR:-diagrams/build}"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --validate)
            VALIDATE=true
            shift
            ;;
        *)
            DIAGRAM_FILE="$1"
            shift
            ;;
    esac
done

if [ -z "$DIAGRAM_FILE" ]; then
    echo "Usage: $0 <diagram-file.puml> [--output-dir <dir>]"
    exit 1
fi

# 检查文件存在
if [ ! -f "$DIAGRAM_FILE" ]; then
    echo "Error: Diagram file not found: $DIAGRAM_FILE"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 获取文件名（不含扩展名）
BASENAME=$(basename "$DIAGRAM_FILE" .puml)

echo "Rendering: $DIAGRAM_FILE"
echo "Output dir: $OUTPUT_DIR"

# 检查 PlantUML 是否可用
if command -v plantuml &> /dev/null; then
    # 使用本地 PlantUML
    plantuml -tsvg -o "$OUTPUT_DIR" "$DIAGRAM_FILE"
    plantuml -tpng -o "$OUTPUT_DIR" "$DIAGRAM_FILE"
    echo "Generated: $OUTPUT_DIR/${BASENAME}.svg"
    echo "Generated: $OUTPUT_DIR/${BASENAME}.png"
else
    # 尝试使用 Java 运行 PlantUML JAR
    if command -v java &> /dev/null; then
        PLANTUML_JAR="${PLANTUML_JAR:-plantuml.jar}"
        if [ -f "$PLANTUML_JAR" ]; then
            java -jar "$PLANTUML_JAR" -tsvg -o "$OUTPUT_DIR" "$DIAGRAM_FILE"
            java -jar "$PLANTUML_JAR" -tpng -o "$OUTPUT_DIR" "$DIAGRAM_FILE"
            echo "Generated: $OUTPUT_DIR/${BASENAME}.svg"
            echo "Generated: $OUTPUT_DIR/${BASENAME}.png"
        else
            echo "Error: PlantUML JAR not found at $PLANTUML_JAR"
            echo "Install PlantUML or set PLANTUML_JAR environment variable"
            exit 1
        fi
    else
        echo "Error: Neither plantuml command nor Java found"
        echo "Please install PlantUML: brew install plantuml (macOS) or apt-get install plantuml (Linux)"
        exit 1
    fi
fi

# 验证输出
if [ "$VALIDATE" = true ]; then
    if [ -f "$OUTPUT_DIR/${BASENAME}.svg" ]; then
        echo "Validation: SVG generated successfully"
    else
        echo "Error: SVG generation failed"
        exit 1
    fi
fi

echo "Done!"
