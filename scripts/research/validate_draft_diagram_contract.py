#!/usr/bin/env python3
"""校验 draft.md 中 PlantUML diagram 的 contract、一致性与来源证明。

本脚本只做 contract/provenance/hash 校验，不重新渲染 PlantUML。

用法:
    python3 scripts/research/validate_draft_diagram_contract.py <draft.md>

返回码:
    0 - 校验通过（包括没有 PlantUML blocks 的情况）
    1 - 校验失败（contract 缺失、validation 失败、hash 不匹配）
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
import hashlib


def sha256_text(text: str) -> str:
    """计算文本的 SHA256 哈希。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    """计算文件原始字节的 SHA256 哈希。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_plantuml_text(text: str) -> str:
    """统一换行并补齐结尾换行，避免 markdown block 与 .puml 文件因 EOF 差异误报。"""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if normalized and not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def parse_contract_comment(comment: str) -> dict[str, str] | None:
    """解析 contract comment，返回 dict 或 None（如果格式不正确）。

    期望格式:
    <!-- verified-diagram: package=./diagrams/<id>/validation.json puml=./diagrams/<id>/diagram.puml sha256=<hash> -->
    """
    pattern = r"<!--\s*verified-diagram:\s*package=([^\s]+)\s+puml=([^\s]+)\s+sha256=([a-fA-F0-9]{64})\s*-->"
    match = re.match(pattern, comment.strip())
    if not match:
        return None
    return {
        "package": match.group(1),
        "puml": match.group(2),
        "sha256": match.group(3).lower(),
    }


def extract_plantuml_blocks(content: str) -> list[tuple[str, str, int]]:
    """提取所有 plantuml code blocks。

    返回: list of (block_content, preceding_comment, block_start_line_no)
    """
    blocks = []
    lines = content.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        # 匹配 ```plantuml 开头
        if re.match(r"^```plantuml\s*$", line.strip()):
            block_start = i + 1  # 1-indexed line number
            block_lines = []
            i += 1
            # 收集 block 内容直到 ```
            while i < len(lines) and not lines[i].strip() == "```":
                block_lines.append(lines[i])
                i += 1

            block_content = normalize_plantuml_text("\n".join(block_lines))

            # 查找 preceding comment（紧邻的单行 HTML 注释）
            preceding_comment = ""
            if block_start >= 2:
                # 检查 block 前一行是否是 HTML 注释
                prev_line_idx = block_start - 2  # 转换为 0-indexed
                if prev_line_idx >= 0:
                    prev_line = lines[prev_line_idx]
                    if prev_line.strip().startswith("<!--") and "verified-diagram:" in prev_line:
                        preceding_comment = prev_line

            blocks.append((block_content, preceding_comment, block_start))
        i += 1

    return blocks


def validate_draft(draft_path: Path) -> tuple[bool, list[str]]:
    """验证 draft.md 中的所有 PlantUML diagram contracts。

    返回: (success, errors)
    """
    if not draft_path.exists():
        return False, [f"draft.md 不存在：{draft_path}"]

    content = draft_path.read_text(encoding="utf-8")
    blocks = extract_plantuml_blocks(content)

    if not blocks:
        # 没有 PlantUML blocks，返回成功
        return True, []

    errors = []
    change_dir = draft_path.parent

    for block_content, comment, line_no in blocks:
        # 检查是否有 contract comment
        if not comment:
            errors.append(
                f"line {line_no}: PlantUML block 缺少 contract comment。"
                f"必须在 block 前添加: <!-- verified-diagram: package=... puml=... sha256=... -->"
            )
            continue

        # 解析 contract comment
        contract = parse_contract_comment(comment)
        if not contract:
            errors.append(
                f"line {line_no}: contract comment 格式不正确。"
                f"期望格式：<!-- verified-diagram: package=./diagrams/<id>/validation.json puml=./diagrams/<id>/diagram.puml sha256=<sha256> -->"
            )
            continue

        # 验证 validation.json 存在
        validation_path = change_dir / contract["package"]
        if not validation_path.exists():
            errors.append(
                f"line {line_no}: validation.json 不存在：{contract['package']}"
            )
            continue

        # 验证 diagram.puml 存在
        puml_path = change_dir / contract["puml"]
        if not puml_path.exists():
            errors.append(
                f"line {line_no}: diagram.puml 不存在：{contract['puml']}"
            )
            continue

        # 读取并验证 validation.json
        try:
            validation_data = json.loads(validation_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"line {line_no}: validation.json 解析失败：{e}")
            continue

        # 验证 final_status=success
        if validation_data.get("final_status") != "success":
            errors.append(
                f"line {line_no}: validation.json 的 final_status 不是 success，当前为：{validation_data.get('final_status')}"
            )
            continue

        # 验证 render_result=ok
        if validation_data.get("render_result") != "ok":
            errors.append(
                f"line {line_no}: validation.json 的 render_result 不是 ok，当前为：{validation_data.get('render_result')}"
            )
            continue

        # 验证 comment / validation / diagram.puml 三者对同一源文件达成一致
        puml_file_sha256 = sha256_file(puml_path).lower()
        if puml_file_sha256 != contract["sha256"]:
            errors.append(
                f"line {line_no}: contract sha256 与 diagram.puml 文件不匹配。\n"
                f"  期望：{contract['sha256']}\n"
                f"  实际：{puml_file_sha256}"
            )
            continue

        # 验证 validation.json 中的 puml_sha256 与 contract 一致（防篡改校验）
        validation_puml_sha256 = validation_data.get("puml_sha256", "").lower()
        if validation_puml_sha256 != contract["sha256"]:
            errors.append(
                f"line {line_no}: contract sha256 与 validation.json 中的 puml_sha256 不匹配。\n"
                f"  contract: {contract['sha256']}\n"
                f"  validation.json: {validation_puml_sha256}"
            )
            continue

        # 验证 draft 中 block 内容与 diagram.puml 一致。
        puml_text = normalize_plantuml_text(puml_path.read_text(encoding="utf-8"))
        if block_content != puml_text:
            block_sha256 = sha256_text(block_content)
            canonical_sha256 = sha256_text(puml_text)
            errors.append(
                f"line {line_no}: PlantUML block 内容与 diagram.puml 不一致。\n"
                f"  block sha256: {block_sha256}\n"
                f"  diagram sha256: {canonical_sha256}\n"
                f"  这可能意味着 draft 中的 block 被手改了。"
            )
            continue

    return len(errors) == 0, errors


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：python3 scripts/research/validate_draft_diagram_contract.py <draft.md>", file=sys.stderr)
        return 1

    draft_path = Path(sys.argv[1]).expanduser().resolve()

    success, errors = validate_draft(draft_path)

    if not success:
        for error in errors:
            print(f"[错误] {error}", file=sys.stderr)
        return 1

    # 统计 blocks 数量用于报告
    content = draft_path.read_text(encoding="utf-8")
    blocks = extract_plantuml_blocks(content)
    block_count = len(blocks)

    if block_count == 0:
        print("blocks=0")
    else:
        print(f"blocks={block_count}")
        print("所有 PlantUML diagram contracts 校验通过。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
