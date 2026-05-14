#!/usr/bin/env python3
"""reference_integrity — 检测 spec-system 文件中的死引用。

扫描指定目录下的 Markdown 文件，提取本地路径引用，检查目标文件是否存在。
只扫描 spec-system 文件（harness/、openspec/、scripts/、.claude/、AGENTS.md 等），
不扫描 knowledge/** 或真实研究内容。

触发方式：manual / governance gate
输入：目录路径
输出：校验通过返回 0，失败返回非 0 并输出 JSON result
"""

import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from lib.gate_result import make_result

ROOT = Path(__file__).resolve().parent.parent.parent.parent

# 只扫描 spec-system 目录
SCAN_DIRS = ["harness", "openspec", "scripts", ".claude", "docs/governance"]
SCAN_FILES = ["AGENTS.md", "CLAUDE.md", "QODER.md"]

# 排除目录
EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules", "tmp", "knowledge", ".agent"}
# Archive 和历史工作目录不扫描
EXCLUDE_PATH_PREFIXES = {"openspec/changes/archive", "harness/reports/_work"}

# 可选引用模式（这些模式下的文件可以不存在）
OPTIONAL_PATTERNS = [
    r"if present",
    r"if it exists",
    r"optional",
]

# Markdown 本地引用模式
LOCAL_REF_PATTERNS = [
    # `[text](path/to/file.md)` 或 `[text](path/to/file.md#anchor)`
    r'\[([^\]]+)\]\(([^)#]+)(?:#[^)]*)?\)',
    # `@path/to/file.md` 或 `` `path/to/file` ``
    r'`([a-zA-Z0-9_./-]+\.(?:md|yaml|yml|py|json))`',
    # `path/to/file.md` 在行首或作为单独引用
    r'(?<!\[)(?<!\()(?<!`)([a-zA-Z0-9_./-]+/(?:openspec|harness|scripts|\.claude|docs|AGENTS|CLAUDE|QODER)[a-zA-Z0-9_./-]*\.(?:md|yaml|yml|py|json))(?![`])',
]


def is_optional_ref(line: str) -> bool:
    """判断引用是否可能是可选的。"""
    return any(re.search(p, line, re.IGNORECASE) for p in OPTIONAL_PATTERNS)


def resolve_ref(ref_path: str, source_file: Path) -> Path | None:
    """解析相对或绝对引用为实际路径。"""
    ref = ref_path.strip().rstrip("/")
    if not ref or ref.startswith("http") or ref.startswith("mailto:"):
        return None
    # Skip obviously non-path things
    if len(ref) < 3 or ref in ("url", "...", "path"):
        return None
    # Skip template placeholders like <change-id>
    if "<" in ref or ">" in ref:
        return None
    # Must contain a slash or start with ./ or ../ to be a path
    if "/" not in ref and not ref.startswith("./") and not ref.startswith("../"):
        return None
    if ref.startswith("/"):
        return ROOT / ref.lstrip("/")
    return (source_file.parent / ref).resolve()


def extract_refs(content: str, source_file: Path) -> list[tuple[str, Path]]:
    """从 Markdown 内容中提取本地引用。"""
    refs = []
    lines = content.split("\n")

    for line in lines:
        if is_optional_ref(line):
            continue

        # [text](path) 模式
        for match in re.finditer(r'\[([^\]]*)\]\(([^)#]+)(?:#[^)]*)?\)', line):
            path = match.group(2).strip()
            resolved = resolve_ref(path, source_file)
            if resolved:
                refs.append((path, resolved))

        # `path/to/file.ext` 模式（只匹配看起来像文件路径的）
        for match in re.finditer(r'`([a-zA-Z0-9_./-]+(?:openspec|harness|scripts|\.claude|docs)[a-zA-Z0-9_./-]*\.(?:md|yaml|yml|py|json))`', line):
            path = match.group(1).strip()
            resolved = resolve_ref(path, source_file)
            if resolved:
                refs.append((path, resolved))

    return refs


def scan_directory(base_dir: Path) -> list[Path]:
    """扫描目录下的所有 Markdown 文件。"""
    md_files = []
    if base_dir.is_file():
        if base_dir.suffix == ".md":
            md_files.append(base_dir)
        return md_files

    for root_path, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(".md"):
                md_files.append(Path(root_path) / f)
    return md_files


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else str(ROOT)
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "reference_integrity"

    errors = []
    checked_files = []

    # 扫描指定目录
    scan_paths = []
    for d in SCAN_DIRS:
        p = ROOT / d
        if p.exists():
            scan_paths.extend(scan_directory(p))
    for f in SCAN_FILES:
        p = ROOT / f
        if p.exists():
            scan_paths.append(p)

    for md_file in scan_paths:
        # Skip excluded path prefixes
        rel = str(md_file.relative_to(ROOT))
        if any(rel.startswith(p) for p in EXCLUDE_PATH_PREFIXES):
            continue
        checked_files.append(rel)
        try:
            content = md_file.read_text()
            refs = extract_refs(content, md_file)
            for ref_path, resolved in refs:
                if resolved.exists():
                    continue
                # 检查是否是 glob pattern（包含 *）
                if "*" in ref_path or "?" in ref_path:
                    continue
                rel = resolved.relative_to(ROOT) if str(resolved).startswith(str(ROOT)) else resolved
                errors.append(f"{md_file.relative_to(ROOT)}: reference '{ref_path}' → {rel} not found")
        except Exception as e:
            errors.append(f"{md_file.relative_to(ROOT)}: scan error: {e}")

    if errors:
        result = make_result(
            gate_id=gate_id,
            validator="reference_integrity",
            status="fail",
            blocking=False,
            checked_files=checked_files[:50],
            errors=errors[:20],
            rule_refs=["docs/governance/openspec-harness-boundary.md"],
            metadata={"total_checked": len(checked_files), "total_errors": len(errors)},
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)

    result = make_result(
        gate_id=gate_id,
        validator="reference_integrity",
        status="pass",
        blocking=False,
        checked_files=checked_files[:50],
        rule_refs=["docs/governance/ openspec-harness-boundary.md"],
        metadata={"total_checked": len(checked_files)},
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
