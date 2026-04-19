#!/usr/bin/env python3
"""
检查 knowledge/ 下长期 Markdown 的 frontmatter 格式。

按新目录模型校验：
- 校验长期 Markdown 是否有合法 frontmatter
- 按 object_type 校验必填字段
- 校验 research_depth 枚举
- 校验 synthesis_kind 是否为 comparison、evolution 或 taxonomy
- 校验 related_domains 是否都出现在 domains.yaml 中
- 拒绝已废弃字段：status, source_change, topic_slug, primary_domain, decision_space
- 校验路径结构是否符合 canonical 模型

用法:
    python scripts/general/check_frontmatter.py [knowledge/]
"""

import sys
from pathlib import Path
import yaml


# 枚举合法值
VALID_RESEARCH_DEPTH = {"deep", "focused", "light"}
VALID_SYNTHESIS_KIND = {"comparison", "evolution", "taxonomy"}
VALID_OBJECT_TYPES = {"primitive", "synthesis", "decision"}
DEPRECATED_FIELDS = {"status", "source_change", "topic_slug", "primary_domain", "decision_space"}


def load_domains(registry_path: Path) -> set:
    """从 domains.yaml 加载已注册的 domain_id 集合"""
    if not registry_path.exists():
        return set()
    content = yaml.safe_load(registry_path.read_text())
    if not content or "domains" not in content:
        return set()
    return {d["id"] for d in content["domains"] if isinstance(d, dict) and "id" in d}


def infer_object_type_from_path(file_path: Path, knowledge_root: Path):
    """从路径推断 object_type 和 domain_id"""
    try:
        rel = file_path.relative_to(knowledge_root)
    except ValueError:
        return None, None, None

    parts = rel.parts

    if len(parts) >= 4 and parts[0] == "analysis" and parts[1] == "primitives":
        # analysis/primitives/<domain_id>/<topic_slug>/artifact.md
        return "primitive", parts[2], parts[3]
    elif len(parts) >= 3 and parts[0] == "analysis" and parts[1] == "synthesis":
        # analysis/synthesis/<topic_slug>/artifact.md
        return "synthesis", None, parts[2]
    elif len(parts) >= 4 and parts[0] == "decisions":
        # decisions/<domain_id>/<topic_slug>/artifact.md 或 verdict.md
        return "decision", parts[1], parts[2]

    return None, None, None


def check_frontmatter(file_path: Path, knowledge_root: Path, domains: set) -> list:
    """检查单个 knowledge/ 文件的 frontmatter"""
    errors = []
    warnings = []

    content = file_path.read_text()
    if not content.startswith("---"):
        return [f"Missing frontmatter (should start with '---')"], []

    lines = content.split("\n")
    frontmatter_lines = []
    in_frontmatter = False
    closing_found = False

    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                closing_found = True
                break
        if in_frontmatter:
            frontmatter_lines.append(line)

    if not closing_found:
        return ["Unclosed frontmatter (missing closing '---')"], []

    try:
        fm = yaml.safe_load("\n".join(frontmatter_lines))
    except yaml.YAMLError as e:
        return [f"Invalid YAML in frontmatter: {e}"], []

    if fm is None:
        return ["Empty frontmatter"], []

    # 推断 object_type
    inferred_type, domain_id, topic_slug = infer_object_type_from_path(file_path, knowledge_root)

    # 检查 deprecated fields
    for field in DEPRECATED_FIELDS:
        if field in fm:
            errors.append(f"Deprecated field '{field}' found; remove it (derived from path or no longer used)")

    # verdict.md 极轻量 frontmatter 检查
    if file_path.name == "verdict.md":
        # verdict.md 只保留 updated_at
        allowed = {"updated_at"}
        extra = set(fm.keys()) - allowed
        if extra:
            warnings.append(f"verdict.md should only contain {allowed}; extra fields: {extra}")
        return errors, warnings

    # artifact.md 通用必填字段
    required_common = {"object_type", "title", "research_depth", "updated_at"}
    missing = required_common - set(fm.keys())
    if missing:
        errors.append(f"Missing required fields: {missing}")

    # 校验 object_type
    if "object_type" in fm:
        ot = fm["object_type"]
        if ot not in VALID_OBJECT_TYPES:
            errors.append(f"Invalid object_type '{ot}'; must be one of {VALID_OBJECT_TYPES}")
        if inferred_type and ot != inferred_type:
            errors.append(f"object_type '{ot}' does not match path-inferred type '{inferred_type}'")

    # 校验 research_depth
    if "research_depth" in fm:
        rd = fm["research_depth"]
        if rd not in VALID_RESEARCH_DEPTH:
            errors.append(f"Invalid research_depth '{rd}'; must be one of {VALID_RESEARCH_DEPTH}")

    # 校验 synthesis_kind (synthesis 必需)
    if inferred_type == "synthesis":
        if "synthesis_kind" not in fm:
            errors.append("Missing required field 'synthesis_kind' for synthesis type")
        elif fm["synthesis_kind"] not in VALID_SYNTHESIS_KIND:
            errors.append(f"Invalid synthesis_kind '{fm['synthesis_kind']}'; must be one of {VALID_SYNTHESIS_KIND}")

    # 校验 related_domains
    if "related_domains" in fm:
        rd = fm["related_domains"]
        if not isinstance(rd, list):
            errors.append("related_domains must be a list")
        elif domains:
            invalid = set(rd) - domains
            if invalid:
                errors.append(f"related_domains contains unregistered domains: {invalid}")

    # 校验 domain_id 是否已注册 (primitive/decision)
    if inferred_type in ("primitive", "decision") and domain_id and domains:
        if domain_id not in domains:
            errors.append(f"Unregistered domain_id '{domain_id}' in path; add to domains.yaml")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_frontmatter.py [knowledge/]")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Path not found: {target}")
        sys.exit(1)

    # 找到 knowledge root
    if target.name == "knowledge":
        knowledge_root = target
    elif target.parent.name == "knowledge":
        knowledge_root = target.parent
    else:
        # 尝试往上找
        knowledge_root = None
        for p in [target] + list(target.parents):
            if p.name == "knowledge":
                knowledge_root = p
                break
        if not knowledge_root:
            print("Could not find knowledge/ root from given path")
            sys.exit(1)

    registry_path = knowledge_root / "analysis" / "_registry" / "domains.yaml"
    domains = load_domains(registry_path)

    if not domains:
        print(f"Warning: domains.yaml not found or empty at {registry_path}")

    all_errors = []
    all_warnings = []

    # 只检查 artifact.md 和 verdict.md
    target_files = list(target.rglob("artifact.md")) + list(target.rglob("verdict.md"))
    if target.is_file() and target.name in ("artifact.md", "verdict.md"):
        target_files = [target]

    for md_file in target_files:
        errors, warnings = check_frontmatter(md_file, knowledge_root, domains)
        if errors:
            all_errors.append((md_file, errors))
        if warnings:
            all_warnings.append((md_file, warnings))

    exit_code = 0

    if all_warnings:
        print("Warnings:")
        for file_path, warns in all_warnings:
            print(f"  {file_path}:")
            for w in warns:
                print(f"    [warning] {w}")
        print()

    if all_errors:
        print(f"Found issues in {len(all_errors)} files:\n")
        for file_path, errs in all_errors:
            print(f"{file_path}:")
            for e in errs:
                print(f"  [error] {e}")
            print()
        exit_code = 1

    if not all_errors and not all_warnings:
        print("All frontmatter looks good!")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
