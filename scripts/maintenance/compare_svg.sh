#!/bin/bash
#
# 比较两个 SVG 图表的差异
#
# 用法:
#   scripts/diagrams/compare_svg.sh <old.svg> <new.svg>
#

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <old.svg> <new.svg>"
    exit 1
fi

OLD_SVG="$1"
NEW_SVG="$2"

if [ ! -f "$OLD_SVG" ]; then
    echo "Error: File not found: $OLD_SVG"
    exit 1
fi

if [ ! -f "$NEW_SVG" ]; then
    echo "Error: File not found: $NEW_SVG"
    exit 1
fi

# 提取文本内容进行比较（忽略坐标等格式差异）
echo "Comparing text content..."

OLD_TEXT=$(grep -oP '(?<=<text[^>]*>)[^<]+' "$OLD_SVG" 2>/dev/null | sort)
NEW_TEXT=$(grep -oP '(?<=<text[^>]*>)[^<]+' "$NEW_SVG" 2>/dev/null | sort)

if [ "$OLD_TEXT" = "$NEW_TEXT" ]; then
    echo "Text content: SAME"
else
    echo "Text content: DIFFERENT"
    echo ""
    echo "Old only:"
    comm -23 <(echo "$OLD_TEXT") <(echo "$NEW_TEXT") | head -20
    echo ""
    echo "New only:"
    comm -13 <(echo "$OLD_TEXT") <(echo "$NEW_TEXT") | head -20
fi

# 比较组件数量
OLD_COMPONENTS=$(grep -c '<rect\|<ellipse\|<polygon' "$OLD_SVG" 2>/dev/null || echo 0)
NEW_COMPONENTS=$(grep -c '<rect\|<ellipse\|<polygon' "$NEW_SVG" 2>/dev/null || echo 0)

echo ""
echo "Component count: Old=$OLD_COMPONENTS, New=$NEW_COMPONENTS"

# 比较连线数量
OLD_LINES=$(grep -c '<line\|<path' "$OLD_SVG" 2>/dev/null || echo 0)
NEW_LINES=$(grep -c '<line\|<path' "$NEW_SVG" 2>/dev/null || echo 0)

echo "Connection count: Old=$OLD_LINES, New=$NEW_LINES"

echo ""
echo "Done!"
