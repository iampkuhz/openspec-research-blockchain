#!/usr/bin/env python3
"""change_dedup — 检查重复 change 和 target path 一致性。

触发方式：post_plan
输入：change 目录路径
输出：若发现疑似重复 change 或 target path 不一致则 fail。
"""

import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from lib.gate_result import make_result
from lib.yaml_loader import load_yaml
from lib.markdown_utils import has_heading


# 合法 change ID 格式
CHANGE_ID_RE = re.compile(r"^(primitive|synthesis|decision)_[a-z0-9-]+_[a-z0-9-]+$")

# 从 change ID 提取 topic slug
TOPIC_RE = re.compile(r"^(?:primitive|synthesis|decision)_[a-z0-9-]+_([a-z0-9-]+)$")

# publish target 中的 topic 模式
PUBLISH_TOPIC_RE = re.compile(r"knowledge/analysis/(?:primitives|synthesis|source-notes)/[a-z0-9-]+/([a-z0-9-]+)/")


def extract_topic_from_id(change_id: str) -> str | None:
    m = TOPIC_RE.match(change_id)
    return m.group(1) if m else None


def extract_topics_from_publish_targets(change_yaml: dict) -> list[str]:
    topics = []
    for pt in change_yaml.get("publish_targets", []):
        if isinstance(pt, dict):
            to_path = pt.get("to", "")
            m = PUBLISH_TOPIC_RE.search(to_path)
            if m:
                topics.append(m.group(1))
    return topics


def extract_target_from_plan(plan_path: str) -> str | None:
    """从 plan.md 中提取目标 Knowledge 路径草案。"""
    if not os.path.exists(plan_path):
        return None
    content = Path(plan_path).read_text(encoding="utf-8")
    # 查找 knowledge/analysis/ 或 knowledge/decisions/ 路径
    m = re.search(r"(knowledge/(?:analysis|decisions)/[^\s\)]+)", content)
    return m.group(1) if m else None


def extract_target_from_request(request_path: str) -> str | None:
    """从 request.md 中提取预期产出路径。"""
    if not os.path.exists(request_path):
        return None
    content = Path(request_path).read_text(encoding="utf-8")
    m = re.search(r"(knowledge/(?:analysis|decisions)/[^\s\)]+)", content)
    return m.group(1) if m else None


def find_similar_active_changes(change_dir: str, topic_slug: str, task_type: str) -> list[str]:
    """查找同目录下疑似重复的 active change。"""
    changes_root = Path(change_dir).parent
    similar = []
    for d in sorted(changes_root.iterdir()):
        if not d.is_dir() or d.name == "archive" or d.name == Path(change_dir).name:
            continue
        change_yaml_path = d / "change.yaml"
        if not change_yaml_path.exists():
            continue
        try:
            data = load_yaml(str(change_yaml_path))
        except Exception:
            continue
        other_id = data.get("id", "")
        other_type = data.get("task_type", "")
        other_topic = extract_topic_from_id(other_id)

        # 同类型 + 同主题或近似主题
        if other_type == task_type and other_topic:
            if other_topic == topic_slug:
                similar.append(d.name)
            elif topic_slug in other_topic or other_topic in topic_slug:
                similar.append(f"{d.name} (近似主题: {other_topic})")
    return similar


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "post_plan"

    errors = []
    warnings = []
    checked = ["change.yaml", "plan.md", "request.md"]

    change_yaml_path = os.path.join(change_dir, "change.yaml")
    if not os.path.exists(change_yaml_path):
        result = make_result(
            gate_id=gate_id, validator="change_dedup", status="error", blocking=True,
            checked_files=checked, errors=["change.yaml not found"],
            rule_refs=["harness/rules/artifacts/plan-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    try:
        change_yaml = load_yaml(change_yaml_path)
    except Exception as e:
        result = make_result(
            gate_id=gate_id, validator="change_dedup", status="error", blocking=True,
            checked_files=checked, errors=[f"change.yaml 解析失败: {e}"],
            rule_refs=["harness/rules/artifacts/plan-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    change_id = change_yaml.get("id", "")
    task_type = change_yaml.get("task_type", "")
    topic_slug = extract_topic_from_id(change_id) or ""

    # 1. 检查 ID 格式
    if change_id and not CHANGE_ID_RE.match(change_id):
        # 只对新建 change 报错，历史 change 可以豁免
        if "_" in change_id or change_id.startswith(("primitive_", "synthesis_", "decision_")):
            warnings.append(f"change ID '{change_id}' 不推荐格式，建议: <task-type>_<domain-id>_<topic-slug>")

    # 2. 重复 change 检查
    if topic_slug and task_type:
        similar = find_similar_active_changes(change_dir, topic_slug, task_type)
        if similar:
            errors.append(f"发现疑似重复 change: {', '.join(similar)}")

    # 3. Target path 一致性检查
    plan_target = extract_target_from_plan(os.path.join(change_dir, "plan.md"))
    request_target = extract_target_from_request(os.path.join(change_dir, "request.md"))
    publish_targets = [pt.get("to", "") for pt in change_yaml.get("publish_targets", []) if isinstance(pt, dict)]

    all_targets = [t for t in [plan_target, request_target] + publish_targets if t]
    if len(all_targets) >= 2:
        unique_targets = set(all_targets)
        if len(unique_targets) > 1:
            errors.append(
                f"target path 不一致: request={request_target}, plan={plan_target}, "
                f"change.yaml publish_targets={publish_targets}"
            )

    # 4. publish target 格式检查
    for pt in publish_targets:
        if not pt.startswith("knowledge/"):
            errors.append(f"publish target '{pt}' 必须指向 knowledge/**")

    if errors:
        errors.insert(0, "change dedup / target path 检查失败")

    status = "fail" if errors else ("warn" if warnings else "pass")
    exit_code = 1 if status == "fail" else 0

    result = make_result(
        gate_id=gate_id,
        validator="change_dedup",
        status=status,
        blocking=True,
        checked_files=checked,
        errors=errors,
        warnings=warnings,
        rule_refs=["harness/rules/artifacts/plan-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
