#!/usr/bin/env python3
"""
Adapter: draft_diagram_contract validator.

The hook dispatcher passes a change directory, while the underlying research
validator expects draft.md. This adapter resolves the path and adds the
pipeline-level checks that plan-required formal diagrams are not silently
published as TODO placeholders.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent


FORMAL_DIAGRAM_PATTERNS = [
    re.compile(r"(需要|必须|必需|需调用|调用|requires?).*(diagram-agent|PlantUML|Architecture Diagram|Sequence Diagram|正式图表)", re.I),
    re.compile(r"(diagram-agent|PlantUML|Architecture Diagram|Sequence Diagram|正式图表).*(需要|必须|必需|required)", re.I),
]

NEGATED_OR_FALLBACK_PATTERN = re.compile(
    r"(不产出|不需要|无需|可选|后续|fallback|降级|Mermaid|ASCII|Markdown 表格|表格)",
    re.I,
)

TODO_PATTERN = re.compile(
    r"(\[TODO:\s*diag|TODO:\s*diagram|待补图|图表待补|diag-\d+.*TODO)",
    re.I,
)


def resolve_draft_path(arg: str) -> Path:
    path = Path(arg).expanduser()
    if path.is_dir():
        return path / "draft.md"
    return path


def plan_requires_formal_diagrams(change_dir: Path) -> bool:
    plan_path = change_dir / "plan.md"
    if not plan_path.exists():
        return False

    for line in plan_path.read_text(encoding="utf-8").splitlines():
        if NEGATED_OR_FALLBACK_PATTERN.search(line):
            continue
        if any(pattern.search(line) for pattern in FORMAL_DIAGRAM_PATTERNS):
            return True
    return False


def has_successful_diagram_package(change_dir: Path) -> bool:
    diagrams_dir = change_dir / "diagrams"
    if not diagrams_dir.exists():
        return False

    for validation_path in diagrams_dir.glob("*/validation.json"):
        try:
            data = json.loads(validation_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("final_status") == "success" and data.get("render_result") == "ok":
            return True
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: draft_diagram_contract.py <change-dir|draft.md>", file=sys.stderr)
        sys.exit(1)

    draft_path = resolve_draft_path(sys.argv[1]).resolve()
    change_dir = draft_path.parent

    if not draft_path.exists():
        print(f"draft.md 不存在：{draft_path}", file=sys.stderr)
        sys.exit(1)

    script = ROOT / "scripts" / "research" / "validate_draft_diagram_contract.py"
    result = subprocess.run(
        [sys.executable, str(script), str(draft_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        sys.exit(result.returncode)

    draft_text = draft_path.read_text(encoding="utf-8")
    if TODO_PATTERN.search(draft_text):
        print("draft.md 仍包含图表 TODO / diag 占位，阻塞 post_draft gate。", file=sys.stderr)
        sys.exit(1)

    formal_required = plan_requires_formal_diagrams(change_dir)
    if formal_required and "blocks=0" in result.stdout:
        print("plan.md 要求正式图表，但 draft.md 中没有 PlantUML block。", file=sys.stderr)
        sys.exit(1)

    if formal_required and not has_successful_diagram_package(change_dir):
        print("plan.md 要求正式图表，但 diagrams/ 中没有通过校验的 validation.json。", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
