#!/usr/bin/env python3
"""markdown_utils — Markdown 文档结构工具。

职责：
1. 提取 Markdown headings
2. 检查必要章节
3. 提供简单 section lookup
"""

import re
from pathlib import Path


def extract_headings(content: str) -> list[tuple[int, str, str]]:
    """提取 Markdown  headings。

    返回 [(level, text, full_line), ...]
    """
    pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    results = []
    for match in pattern.finditer(content):
        level = len(match.group(1))
        text = match.group(2).strip()
        results.append((level, text, match.group(0)))
    return results


# 中英文等效章节名映射
SECTION_ALIASES = {
    "Metadata": ["元数据"],
    "Summary": ["摘要", "目标", "请求摘要"],
    "Body": ["正文"],
    "Evidence": ["证据"],
    "Traceability": ["追踪链"],
    "Plan": ["计划", "任务类型"],
    "Scope": ["范围"],
    "Review Target": ["评审目标", "审查目标"],
    "Decision": ["决策", "结论"],
    "Publish Targets": ["发布目标"],
    "Source List": ["来源清单"],
}


def has_heading(content: str, heading_text: str, max_level: int = 3) -> bool:
    """检查是否包含指定标题（不区分大小写，支持中英文等效名）。"""
    headings = extract_headings(content)
    target = heading_text.lower()
    # 获取等效别名
    aliases = SECTION_ALIASES.get(heading_text, [])
    alias_lower = [a.lower() for a in aliases]
    for level, text, _ in headings:
        if level <= max_level:
            text_lower = text.lower()
            if text_lower == target:
                return True
            # 检查是否为编号章节（如 "1. 共识" 对应 Body）
            if heading_text == "Body" and re.match(r"^\d+[\.\s]", text):
                return True
            # 检查别名
            if text_lower in alias_lower:
                return True
    return False


def check_required_sections(content: str, required: list[str]) -> list[str]:
    """检查是否包含所有必要章节。

    返回缺失的章节列表。
    """
    missing = []
    for section in required:
        if not has_heading(content, section):
            missing.append(section)
    return missing


def read_markdown(path: str) -> str:
    """读取 Markdown 文件内容。"""
    return Path(path).read_text(encoding="utf-8")
