#!/usr/bin/env python3
"""
Hook Dispatcher v2 — Gate 调度器

职责：
- 加载 harness/gates/registry.yaml 获取 gate 定义
- 加载 scripts/hooks/validators/registry.yaml 获取 validator 脚本映射
- 构建 change context
- 根据 gate 选择 validators 并顺序执行
- 聚合 gate result 并写入 validation/*.json
- blocking gate fail 时 exit 2

用法:
    python scripts/hooks/dispatch.py --change openspec/changes/<id> --gate post_draft
    python scripts/hooks/dispatch.py --change openspec/changes/<id> --all
    python scripts/hooks/dispatch.py --event pre_publish --change openspec/changes/<id>
    python scripts/hooks/dispatch.py --event post_write --change openspec/changes/<id>
    python scripts/hooks/dispatch.py --change openspec/changes/<id> --gate post_draft --json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent.parent
DEFAULT_GATE_REGISTRY = ROOT / "harness" / "gates" / "registry.yaml"
DEFAULT_VALIDATOR_REGISTRY = SCRIPT_DIR / "validators" / "registry.yaml"

# ---------------------------------------------------------------------------
# 本地 lib
# ---------------------------------------------------------------------------

sys.path.insert(0, str(SCRIPT_DIR))

from lib.gate_result import make_result, aggregate_results
from lib.change_context import find_repo_root, find_change_dir, load_change_context
from lib.yaml_loader import load_yaml


# ---------------------------------------------------------------------------
# Registry 加载
# ---------------------------------------------------------------------------


def load_gate_registry(path: Path) -> dict[str, Any]:
    """加载 gate registry。"""
    if not path.exists():
        print(f"[dispatch] ERROR: gate registry not found at {path}", file=sys.stderr)
        sys.exit(1)
    return load_yaml(str(path))


def load_validator_registry(path: Path) -> dict[str, Any]:
    """加载 validator registry。"""
    if not path.exists():
        print(f"[dispatch] ERROR: validator registry not found at {path}", file=sys.stderr)
        sys.exit(1)
    return load_yaml(str(path))


# ---------------------------------------------------------------------------
# 事件 -> gate 映射
# ---------------------------------------------------------------------------

EVENT_GATE_MAP = {
    "post_write": ["post_request", "post_plan", "post_research", "post_draft", "post_review"],
    "stop": [],  # 汇总模式，不运行新检查
    "pre_publish": ["pre_publish"],
    "pre_commit": ["pre_commit"],  # pre-commit hook 专用，由 resolve_gates_from_event 处理
}

# 不属于研究 change 的路径前缀，预提交时应跳过
NON_CHANGE_PATH_PREFIXES = [
    "scripts/hooks/tests/fixtures/",
    "openspec/changes/archive/",
]


def _staged_files_involve_change() -> list[str]:
    """获取 staged 文件中属于 openspec/changes/ 的路径，排除 fixture/archive。"""
    try:
        proc = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=10,
        )
        files = [f for f in proc.stdout.strip().split("\n") if f.strip()]
    except Exception:
        return []
    # 过滤：只包含 openspec/changes/ 下的文件
    relevant = []
    for f in files:
        if f.startswith("openspec/changes/"):
            # 排除 test fixtures 和 archive
            if any(f.startswith(p) for p in NON_CHANGE_PATH_PREFIXES):
                continue
            relevant.append(f)
    return relevant


def _infer_gates_from_staged(staged: list[str], change_dir: str) -> list[str]:
    """从 staged 文件列表推断应运行的 gate。

    只根据当前 change_dir 内的文件推断，确保范围受控。
    """
    # 过滤出属于当前 change 的文件
    own_files = [f for f in staged if change_dir and f.startswith(change_dir + "/")]
    if not own_files:
        return []

    # 收集该 change 目录内存在的文件名
    own_basenames = {os.path.basename(f) for f in own_files}

    # 根据文件存在性推断最靠后的 gate
    if "publish.md" in own_basenames:
        return ["pre_publish"]
    if "review.md" in own_basenames:
        return ["post_review"]
    if "draft.md" in own_basenames:
        return ["post_draft"]
    if "plan.md" in own_basenames:
        return ["post_plan"]
    if "request.md" in own_basenames:
        return ["post_request"]
    # 如果 staged 中只有 sources/diagrams 等辅助文件
    return ["post_research"]


def resolve_gates_from_event(event: str, change_dir: str, gates: dict) -> list[str]:
    """根据 event 解析应运行的 gate 列表。"""
    if event == "stop":
        return []

    if event == "pre_publish":
        return ["pre_publish"]

    if event == "pre_commit":
        # 预提交：从 staged 文件推断涉及的 change，只运行该 change 对应的 gate
        staged = _staged_files_involve_change()
        if not staged:
            return []  # 没有研究相关文件，跳过所有 gate
        return _infer_gates_from_staged(staged, change_dir)

    if event == "post_write":
        # 根据 change 目录中的文件推断 gate
        gate_list = EVENT_GATE_MAP.get(event, [])
        # 简化：根据文件存在性推断最匹配的 gate
        if os.path.exists(os.path.join(change_dir, "publish.md")):
            return ["pre_publish", "post_review"]
        if os.path.exists(os.path.join(change_dir, "review.md")):
            return ["post_review"]
        if os.path.exists(os.path.join(change_dir, "draft.md")):
            return ["post_draft"]
        if os.path.exists(os.path.join(change_dir, "plan.md")):
            return ["post_plan"]
        if os.path.exists(os.path.join(change_dir, "request.md")):
            return ["post_request"]
        return gate_list

    # 默认：运行所有 non-publish gates
    return [g for g in gates if g != "post_publish"]


# ---------------------------------------------------------------------------
# Validator 执行
# ---------------------------------------------------------------------------


def run_validator(
    validator_name: str,
    validator_entry: dict,
    change_dir: str,
    gate_id: str,
    gate_config: dict,
    repo_root: str,
) -> dict[str, Any]:
    """执行单个 validator，返回 result dict。"""
    script = validator_entry.get("script", "")
    script_path = Path(repo_root) / script

    if not script_path.exists():
        return make_result(
            gate_id=gate_id,
            validator=validator_name,
            status="error",
            blocking=gate_config.get("blocking", True),
            errors=[f"validator script not found: {script}"],
            rule_refs=gate_config.get("rule_refs", []),
            metadata={"change_dir": change_dir, "repo_root": repo_root},
        )

    cmd = [sys.executable, str(script_path), change_dir, gate_id]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=repo_root,
        )
        # 尝试从 stdout 解析 JSON result
        for line in proc.stdout.strip().split("\n"):
            line = line.strip()
            if line.startswith("{"):
                try:
                    result = json.loads(line)
                    return result
                except json.JSONDecodeError:
                    pass

        # 如果无法解析 JSON，根据 exit code 构建 result
        status = "pass" if proc.returncode == 0 else "fail"
        return make_result(
            gate_id=gate_id,
            validator=validator_name,
            status=status,
            blocking=gate_config.get("blocking", True),
            checked_files=gate_config.get("files", {}).get("required", []),
            errors=[proc.stderr.strip()] if proc.stderr.strip() and proc.returncode != 0 else [],
            warnings=[proc.stdout.strip()] if proc.stdout.strip() else [],
            rule_refs=gate_config.get("rule_refs", []),
            metadata={"change_dir": change_dir, "repo_root": repo_root},
        )
    except subprocess.TimeoutExpired:
        return make_result(
            gate_id=gate_id,
            validator=validator_name,
            status="error",
            blocking=gate_config.get("blocking", True),
            errors=["validator timed out (60s)"],
            rule_refs=gate_config.get("rule_refs", []),
            metadata={"change_dir": change_dir, "repo_root": repo_root},
        )
    except Exception as e:
        return make_result(
            gate_id=gate_id,
            validator=validator_name,
            status="error",
            blocking=gate_config.get("blocking", True),
            errors=[str(e)],
            rule_refs=gate_config.get("rule_refs", []),
            metadata={"change_dir": change_dir, "repo_root": repo_root},
        )


# ---------------------------------------------------------------------------
# Gate 执行
# ---------------------------------------------------------------------------


def run_gate(
    gate_id: str,
    gate_config: dict,
    change_dir: str,
    validator_registry: dict,
    repo_root: str,
) -> dict[str, Any]:
    """运行单个 gate，返回聚合的 gate result。"""
    validators = gate_config.get("validators", [])
    blocking = gate_config.get("blocking", True)
    rule_refs = gate_config.get("rule_refs", [])
    required_files = gate_config.get("files", {}).get("required", [])

    validators_reg = validator_registry.get("validators", {})
    results = []

    for v_name in validators:
        v_entry = validators_reg.get(v_name)
        if not v_entry:
            results.append(make_result(
                gate_id=gate_id,
                validator=v_name,
                status="error" if blocking else "warn",
                blocking=blocking,
                errors=[f"validator '{v_name}' not found in validator registry"],
                rule_refs=rule_refs,
                metadata={"change_dir": change_dir, "repo_root": repo_root},
            ))
            continue

        result = run_validator(v_name, v_entry, change_dir, gate_id, gate_config, repo_root)
        results.append(result)

    # 聚合结果
    gate_result = aggregate_results(gate_id, blocking, results)

    # 确保 rule_refs 和 checked_files 完整
    if not gate_result.get("rule_refs"):
        gate_result["rule_refs"] = rule_refs
    if not gate_result.get("checked_files"):
        gate_result["checked_files"] = required_files

    return gate_result


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------


def write_gate_result(gate_result: dict, change_dir: str, gate_config: dict):
    """写入 gate result JSON。"""
    output_path = gate_config.get("output", {}).get("path", f"validation/{gate_result.get('gate_id', 'unknown')}.json")
    full_path = os.path.join(change_dir, output_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        json.dump(gate_result, f, indent=2, ensure_ascii=False)
    return full_path


def print_result(gate_result: dict, json_output: bool = False):
    """打印 gate result。"""
    if json_output:
        print(json.dumps(gate_result, indent=2, ensure_ascii=False))
        return

    status = gate_result.get("status", "unknown")
    gate_id = gate_result.get("gate_id", "unknown")
    icon = {"pass": "✓", "warn": "⚠", "fail": "✗", "error": "✗", "skip": "○"}.get(status, "?")

    print(f"[gate] {icon} {gate_id}: {status}")

    for err in gate_result.get("errors", []):
        print(f"  ERROR: {err}")
    for warn in gate_result.get("warnings", []):
        print(f"  WARN: {warn}")

    checked = gate_result.get("checked_files", [])
    if checked:
        print(f"  checked: {', '.join(checked)}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Hook Dispatcher v2 — Gate 调度器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --change openspec/changes/<id> --gate post_draft
  %(prog)s --change openspec/changes/<id> --all
  %(prog)s --event pre_publish --change openspec/changes/<id>
  %(prog)s --event post_write --change openspec/changes/<id>
  %(prog)s --change openspec/changes/<id> --gate post_draft --json
        """,
    )
    parser.add_argument(
        "--change",
        type=str,
        default=None,
        help="change 目录路径",
    )
    parser.add_argument(
        "--gate",
        type=str,
        default=None,
        help="运行指定 gate",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="运行所有适用 gates",
    )
    parser.add_argument(
        "--event",
        type=str,
        default=None,
        help="hook event: post_write / stop / pre_publish",
    )
    parser.add_argument(
        "--gate-registry",
        type=str,
        default=None,
        help="gate registry 路径",
    )
    parser.add_argument(
        "--validator-registry",
        type=str,
        default=None,
        help="validator registry 路径",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 格式输出",
    )
    parser.add_argument(
        "--list-gates",
        action="store_true",
        help="列出所有 gates",
    )
    # 向后兼容旧 CLI 接口
    parser.add_argument(
        "--run",
        action="store_true",
        help="[兼容] 执行匹配的 validator（旧接口）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="[兼容] 只展示匹配结果",
    )
    parser.add_argument(
        "--list",
        dest="list_only",
        action="store_true",
        help="[兼容] 列出 validator",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="[兼容] 文件路径列表",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="[兼容] 自动获取 git staged 文件",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="[兼容] 详细输出",
    )
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="[兼容] JSON 输出",
    )
    parser.add_argument(
        "--extra-args",
        nargs="*",
        default=None,
        help="[兼容] 额外参数",
    )
    parser.add_argument(
        "--registry",
        type=str,
        default=None,
        help="[兼容] 覆盖 registry 路径",
    )
    parser.add_argument(
        "--validator",
        type=str,
        default=None,
        help="[兼容] 只运行指定 validator",
    )
    parser.add_argument(
        "--phase",
        type=str,
        default=None,
        help="[兼容] 过滤 phase",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    gate_registry_path = Path(args.gate_registry) if args.gate_registry else DEFAULT_GATE_REGISTRY
    validator_registry_path = (
        Path(args.validator_registry) if args.validator_registry else DEFAULT_VALIDATOR_REGISTRY
    )

    gate_registry = load_gate_registry(gate_registry_path)
    validator_registry = load_validator_registry(validator_registry_path)
    gates = gate_registry.get("gates", {})

    # --list-gates 模式
    if args.list_gates:
        for gid, gconf in gates.items():
            blocking = gconf.get("blocking", False)
            artifact = gconf.get("artifact", "unknown")
            validators = gconf.get("validators", [])
            print(f"  {gid}: artifact={artifact}, blocking={blocking}, validators={validators}")
        return

    # --list 兼容模式
    if args.list_only:
        print("[dispatch] --list: use --list-gates instead")
        return

    # pre_commit 事件专用路径：只检查 staged 的研究文件
    if args.event == "pre_commit":
        staged = _staged_files_involve_change()
        if not staged:
            print("[dispatch] pre_commit: no staged research files, skipping")
            return
        # 从 staged 文件提取涉及的 change 目录
        changes_involved = set()
        for f in staged:
            cd = _infer_change_dir(f)
            if cd:
                changes_involved.add(cd)
        if not changes_involved:
            print("[dispatch] pre_commit: no valid change directory, skipping")
            return
        overall_blocked = False
        for cd in sorted(changes_involved):
            # 为每个涉及的 change 运行 gate
            gates_to_run = resolve_gates_from_event(args.event, cd, gates)
            if not gates_to_run:
                continue
            for gate_id in gates_to_run:
                gate_config = gates.get(gate_id)
                if not gate_config:
                    continue
                gate_result = run_gate(gate_id, gate_config, cd, validator_registry, repo_root)
                output_path = write_gate_result(gate_result, cd, gate_config)
                print_result(gate_result, args.json or args.output_json)
                status = gate_result.get("status", "unknown")
                if status in ("fail", "error") and gate_config.get("blocking", False):
                    overall_blocked = True
        if overall_blocked:
            print("[dispatch] blocking gate failed, exit 2")
            sys.exit(2)
        sys.exit(0)

    # 兼容模式：--run --event post_tool_use --files <path>
    # 当收到 --files 参数时，从文件路径推断 change_dir
    if args.files and not args.change:
        for f in args.files:
            if f and os.path.exists(f):
                inferred = _infer_change_dir(f)
                if inferred:
                    args.change = inferred
                    break
            elif f:
                # 文件可能还未创建，尝试从路径推断
                inferred = _infer_change_dir_from_path(f)
                if inferred:
                    args.change = inferred
                    break

    # 定位 change 目录
    change_dir = args.change
    if not change_dir:
        try:
            repo_root = find_repo_root()
            change_dir = find_change_dir(repo_root)
        except RuntimeError:
            # 如果无法定位 change，在 post_tool_use 事件中静默退出
            if args.event == "post_tool_use" or args.event == "post_write":
                print("[dispatch] no change directory found, skipping")
                return
            print("[dispatch] ERROR: cannot locate change directory, use --change", file=sys.stderr)
            sys.exit(1)

    if not change_dir or not os.path.isdir(change_dir):
        # 文件路径可能不在 change 目录中，跳过
        if args.event == "post_tool_use" or args.event == "post_write":
            print(f"[dispatch] not in a change directory, skipping")
            return
        print(f"[dispatch] ERROR: change directory not found: {change_dir}", file=sys.stderr)
        sys.exit(1)

    repo_root = find_repo_root(change_dir)

    # 根据 event 或 --gate/--all 解析 gates 列表
    gates_to_run = []

    if args.event:
        gates_to_run = resolve_gates_from_event(args.event, change_dir, gates)
    elif args.gate:
        gates_to_run = [args.gate]
    elif args.all:
        gates_to_run = list(gates.keys())
    else:
        # 默认：根据文件存在性推断
        gates_to_run = resolve_gates_from_event("post_write", change_dir, gates)

    if args.event == "stop":
        # stop 模式：汇总当前 change 的 validation/*.json
        validation_dir = os.path.join(change_dir, "validation")
        if os.path.isdir(validation_dir):
            results = []
            for fname in sorted(os.listdir(validation_dir)):
                if fname.endswith(".json"):
                    fpath = os.path.join(validation_dir, fname)
                    try:
                        data = json.loads(Path(fpath).read_text())
                        results.append(data)
                    except Exception:
                        results.append({"file": fname, "status": "error", "errors": ["failed to parse"]})

            if args.json or args.output_json:
                print(json.dumps({"event": "stop", "change_dir": change_dir, "results": results}, indent=2))
            else:
                print(f"[dispatch] stop: {len(results)} gate result(s) in {validation_dir}")
                for r in results:
                    status = r.get("status", "unknown")
                    gid = r.get("gate_id", r.get("file", "unknown"))
                    icon = {"pass": "✓", "warn": "⚠", "fail": "✗", "error": "✗", "skip": "○"}.get(status, "?")
                    print(f"  {icon} {gid}: {status}")
        else:
            print(f"[dispatch] stop: no validation results found in {change_dir}")
        return

    if not gates_to_run:
        print(f"[dispatch] no gates to run for change={change_dir}")
        return

    # 执行 gates
    overall_blocked = False
    for gate_id in gates_to_run:
        gate_config = gates.get(gate_id)
        if not gate_config:
            print(f"[dispatch] ERROR: gate '{gate_id}' not found in registry", file=sys.stderr)
            continue

        gate_result = run_gate(gate_id, gate_config, change_dir, validator_registry, repo_root)
        output_path = write_gate_result(gate_result, change_dir, gate_config)
        print_result(gate_result, args.json or args.output_json)

        status = gate_result.get("status", "unknown")
        if status in ("fail", "error") and gate_config.get("blocking", False):
            overall_blocked = True

    if overall_blocked:
        if not args.json and not args.output_json:
            print("[dispatch] blocking gate failed, exit 2")
        sys.exit(2)
    else:
        if not args.json and not args.output_json:
            print(f"[dispatch] all gates completed, change={change_dir}")
        sys.exit(0)


def _infer_change_dir(filepath: str) -> str | None:
    """从文件路径向上查找包含 change.yaml 的目录。"""
    d = Path(filepath).resolve().parent if os.path.isfile(filepath) else Path(filepath).resolve()
    while d != d.parent:
        if (d / "change.yaml").exists():
            return str(d)
        d = d.parent
    return None


def _infer_change_dir_from_path(filepath: str) -> str | None:
    """从未创建的文件路径推断 change 目录。"""
    if "openspec/changes/" in filepath:
        parts = filepath.split("openspec/changes/")
        if len(parts) > 1:
            repo_root = filepath.split("openspec/changes/")[0]
            change_part = parts[1]
            change_id = change_part.split("/")[0] if "/" in change_part else change_part
            candidate = os.path.join(repo_root, "openspec", "changes", change_id)
            if os.path.isdir(candidate):
                return candidate
    return None


if __name__ == "__main__":
    main()
