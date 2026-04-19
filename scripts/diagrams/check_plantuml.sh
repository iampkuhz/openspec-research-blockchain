#!/bin/bash

# PlantUML 语法校验脚本
# 用法：bash scripts/diagrams/check_plantuml.sh <input.puml> [--svg-output <output.svg>]
# 使用本地 PlantUML server (端口 8199) 进行语法校验和 SVG 生成

set -e

INPUT_FILE=""
SVG_OUTPUT=""
SERVER_PORT="${AGENT_PLANTUML_SERVER_PORT:-8199}"
SERVER_URL="http://localhost:$SERVER_PORT"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --svg-output)
            SVG_OUTPUT="$2"
            shift 2
            ;;
        *)
            INPUT_FILE="$1"
            shift
            ;;
    esac
done

if [[ -z "$INPUT_FILE" ]]; then
    echo "Error: Input file not specified"
    echo "Usage: bash $0 <input.puml> [--svg-output <output.svg>]"
    exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: File not found: $INPUT_FILE"
    exit 1
fi

echo "=== PlantUML Syntax Check ==="
echo "Input: $INPUT_FILE"
echo "Server: $SERVER_URL"

# 检查 server 是否可达（检查端口是否监听）
if ! nc -z localhost "$SERVER_PORT" 2>/dev/null; then
    echo "Error: PlantUML server at $SERVER_URL is not reachable"
    echo "syntax_result=error"
    exit 1
fi

echo "PlantUML server is reachable"

# 读取 PlantUML 内容
PUML_CONTENT=$(cat "$INPUT_FILE")

# 通过 POST 到 /svg endpoint 来验证语法（如果 SVG 能生成，语法就正确）
SVG_RESULT=$(curl -s -X POST "$SERVER_URL/svg" --data-binary @"$INPUT_FILE" 2>&1)

# 检查返回结果是否是有效的 SVG
if echo "$SVG_RESULT" | grep -q "<svg"; then
    echo "SVG generated successfully"
    echo "syntax_result=ok"

    # 如果指定了 SVG 输出路径，保存 SVG
    if [[ -n "$SVG_OUTPUT" ]]; then
        echo "$SVG_RESULT" > "$SVG_OUTPUT"
        echo "SVG saved to: $SVG_OUTPUT"
    fi
else
    # 检查是否是错误响应
    if echo "$SVG_RESULT" | grep -qi "error\|Error\|ERROR"; then
        echo "PlantUML reported an error:"
        echo "$SVG_RESULT" | head -20
        echo "syntax_result=error"
        exit 1
    fi

    echo "Unknown response from server:"
    echo "$SVG_RESULT" | head -10
    echo "syntax_result=error"
    exit 1
fi

exit 0
