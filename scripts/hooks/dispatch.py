#!/usr/bin/env python3
"""
Hook Dispatcher — 统一校验调度器

职责：
- 加载 harness/hooks/registry.yaml 声明式注册表
- 按 event + path + phase 匹配应运行的 validator
- 执行 validator 并汇总结果
- 支持 dry-run、list、run-all 等模式

边界：
- 这是 Harness execution layer，不是 OpenSpec canonical policy。
- 不定义校验规则本身，只负责路由和执行。

用法:
    python scripts/hooks/dispatch.py --help
    python scripts/hooks/dispatch.py --list [--event EVENT]
    python scripts/hooks/dispatch.py --dry-run --event post_tool_use --files FILE1 FILE2
    python scripts/hooks/dispatch.py --run --event post_tool_use --files FILE1 FILE2
    python scripts/hooks/dispatch.py --run --event pre_commit --staged
    python scripts/hooks/dispatch.py --run --event manual --validator traceability --topic eip-4337
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# 常量与路径
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent.parent
REGISTRY_PATH = ROOT / "harness" / "hooks" / "registry.yaml"
VALIDATORS_DIR = SCRIPT_DIR / "validators"

# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


@dataclass
class ValidationResult:
    """单个 validator 的执行结果"""

    validator_id: str
    passed: bool
    severity: str  # "error" | "warning"
    duration_ms: int
    stdout: str
    stderr: str


@dataclass
class HookRule:
    """从 registry.yaml 解析出的单条规则"""

    id: str
    event: str
    phases: list[str]
    path_patterns: list[str]
    validator: str  # 相对于 VALIDATORS_DIR
    args_mode: str  # "files" | "one_per_file" | "none"
    severity: str
    blocking: bool
    timeout: int
    enabled: bool
    description: str


@dataclass
class DispatchReport:
    """调度报告"""

    event: str
    matched_rules: list[HookRule] = field(default_factory=list)
    results: list[ValidationResult] = field(default_factory=list)
    total_duration_ms: int = 0
    blocked: bool = False


# ---------------------------------------------------------------------------
# Registry 加载
# ---------------------------------------------------------------------------


def load_registry(path: Path = REGISTRY_PATH) -> list[HookRule]:
    """加载并解析 registry.yaml，返回 HookRule 列表"""
    import yaml

    if not path.exists():
        print(f"[dispatch] ERROR: registry not found at {path}", file=sys.stderr)
        sys.exit(1)

    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict) or "validators" not in data:
        print(f"[dispatch] ERROR: invalid registry format at {path}", file=sys.stderr)
        sys.exit(1)

    rules: list[HookRule] = []
    for entry in data["validators"]:
        rule = HookRule(
            id=entry["id"],
            event=entry.get("event", "manual"),
            phases=entry.get("phases", []),
            path_patterns=entry.get("path_patterns", []),
            validator=entry["validator"],
            args_mode=entry.get("args_mode", "files"),
            severity=entry.get("severity", "error"),
            blocking=entry.get("blocking", True),
            timeout=entry.get("timeout", 30),
            enabled=entry.get("enabled", True),
            description=entry.get("description", ""),
        )
        rules.append(rule)
    return rules


# ---------------------------------------------------------------------------
# 匹配逻辑
# ---------------------------------------------------------------------------


def match_paths(rule: HookRule, files: list[str]) -> list[str]:
    """如果规则的 path_patterns 命中 files 中的任意文件，返回命中的文件列表"""
    if not rule.path_patterns:
        # 无 path_patterns → 匹配所有文件（如 advisory 检查）
        return files if files else [""]
    matched = []
    for f in files:
        for pattern in rule.path_patterns:
            if fnmatch.fnmatch(f, pattern):
                matched.append(f)
                break
    return matched


def match_rules(
    rules: list[HookRule],
    event: str,
    files: list[str] | None = None,
    phase: str | None = None,
    validator_id: str | None = None,
) -> list[tuple[HookRule, list[str]]]:
    """
    返回匹配的规则及其对应的文件列表。
    返回 list of (rule, matched_files)。
    """
    result = []
    for rule in rules:
        if not rule.enabled:
            continue
        if validator_id and rule.id != validator_id:
            continue
        if rule.event != event:
            continue
        if phase and phase not in rule.phases:
            continue
        matched = match_paths(rule, files or [])
        if matched:
            result.append((rule, matched))
    return result


# ---------------------------------------------------------------------------
# 执行逻辑
# ---------------------------------------------------------------------------


def run_validator(
    rule: HookRule, files: list[str], extra_args: list[str] | None = None
) -> ValidationResult:
    """执行单个 validator，返回结果"""
    script = VALIDATORS_DIR / rule.validator
    if not script.exists():
        return ValidationResult(
            validator_id=rule.id,
            passed=False,
            severity=rule.severity,
            duration_ms=0,
            stdout="",
            stderr=f"validator script not found: {script}",
        )

    # 根据 args_mode 构建命令
    if rule.args_mode == "one_per_file":
        # 每个文件单独运行一次 validator
        all_passed = True
        combined_stdout = []
        combined_stderr = []
        total_ms = 0
        for f in files:
            cmd = [sys.executable, str(script), f] + (extra_args or [])
            start = time.monotonic()
            try:
                proc = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=rule.timeout
                )
                elapsed = int((time.monotonic() - start) * 1000)
                total_ms += elapsed
                combined_stdout.append(proc.stdout.strip())
                if proc.returncode != 0:
                    all_passed = False
                    combined_stderr.append(proc.stderr.strip())
            except subprocess.TimeoutExpired:
                all_passed = False
                combined_stderr.append(f"timeout after {rule.timeout}s")
        return ValidationResult(
            validator_id=rule.id,
            passed=all_passed,
            severity=rule.severity,
            duration_ms=total_ms,
            stdout="\n".join(combined_stdout),
            stderr="\n".join(combined_stderr),
        )
    elif rule.args_mode == "files":
        # 所有文件作为参数一次传入
        cmd = [sys.executable, str(script)] + files + (extra_args or [])
        start = time.monotonic()
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=rule.timeout
            )
            elapsed = int((time.monotonic() - start) * 1000)
            return ValidationResult(
                validator_id=rule.id,
                passed=proc.returncode == 0,
                severity=rule.severity,
                duration_ms=elapsed,
                stdout=proc.stdout.strip(),
                stderr=proc.stderr.strip(),
            )
        except subprocess.TimeoutExpired:
            return ValidationResult(
                validator_id=rule.id,
                passed=False,
                severity=rule.severity,
                duration_ms=rule.timeout * 1000,
                stdout="",
                stderr=f"timeout after {rule.timeout}s",
            )
    else:
        # args_mode == "none"，不传文件参数
        cmd = [sys.executable, str(script)] + (extra_args or [])
        start = time.monotonic()
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=rule.timeout
            )
            elapsed = int((time.monotonic() - start) * 1000)
            return ValidationResult(
                validator_id=rule.id,
                passed=proc.returncode == 0,
                severity=rule.severity,
                duration_ms=elapsed,
                stdout=proc.stdout.strip(),
                stderr=proc.stderr.strip(),
            )
        except subprocess.TimeoutExpired:
            return ValidationResult(
                validator_id=rule.id,
                passed=False,
                severity=rule.severity,
                duration_ms=rule.timeout * 1000,
                stdout="",
                stderr=f"timeout after {rule.timeout}s",
            )


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------


def print_report(report: DispatchReport, verbose: bool = False) -> bool:
    """打印调度报告，返回是否被 blocking error 阻止"""
    if not report.matched_rules:
        print(f"[dispatch] event={report.event}: no matching validators")
        return False

    print(f"[dispatch] event={report.event}: {len(report.matched_rules)} validator(s) matched")
    for rule in report.matched_rules:
        print(f"  - [{rule.id}] {rule.description} (severity={rule.severity}, blocking={rule.blocking})")

    print()
    blocked = False
    for r in report.results:
        status = "PASS" if r.passed else ("WARN" if r.severity == "warning" else "FAIL")
        icon = "✓" if r.passed else ("⚠" if r.severity == "warning" else "✗")
        print(f"  {icon} [{r.validator_id}] {status} ({r.duration_ms}ms)")
        if not r.passed and verbose:
            if r.stdout:
                for line in r.stdout.split("\n"):
                    print(f"      stdout: {line}")
            if r.stderr:
                for line in r.stderr.split("\n"):
                    print(f"      stderr: {line}")
        if not r.passed and r.severity == "error" and any(
            rule.blocking for rule in report.matched_rules if rule.id == r.validator_id
        ):
            blocked = True

    print(f"[dispatch] total: {report.total_duration_ms}ms, {len(report.results)} run, blocked={blocked}")
    return blocked


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Hook Dispatcher — 统一校验调度器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --list
  %(prog)s --list --event post_tool_use
  %(prog)s --dry-run --event post_tool_use --files path/to/file.md
  %(prog)s --run --event pre_commit --staged
  %(prog)s --run --event manual --validator traceability --extra-args '--topic eip-4337'
        """,
    )
    parser.add_argument(
        "--list",
        dest="list_only",
        action="store_true",
        help="列出所有已注册的 validator（可按 --event 过滤）",
    )
    parser.add_argument(
        "--event",
        type=str,
        default="post_tool_use",
        help="事件名：post_tool_use / pre_commit / manual (默认: post_tool_use)",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="文件路径列表（用于匹配 path_patterns）",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="自动获取 git staged 文件列表（等效于 --files $(git diff --cached --name-only)）",
    )
    parser.add_argument(
        "--phase",
        type=str,
        default=None,
        help="过滤特定 phase（request / plan / draft / artifact / review）",
    )
    parser.add_argument(
        "--validator",
        type=str,
        default=None,
        help="只运行指定 id 的 validator",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="执行匹配的 validator",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只展示匹配结果，不实际执行",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细的 validator 输出",
    )
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="以 JSON 格式输出结果",
    )
    parser.add_argument(
        "--extra-args",
        nargs="*",
        default=None,
        help="传递给 validator 的额外参数",
    )
    parser.add_argument(
        "--registry",
        type=str,
        default=None,
        help="覆盖 registry.yaml 路径",
    )
    return parser


def get_staged_files() -> list[str]:
    """获取 git staged 文件列表"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        return [f for f in result.stdout.strip().split("\n") if f]
    except Exception:
        return []


def main():
    parser = build_parser()
    args = parser.parse_args()

    registry_path = Path(args.registry) if args.registry else REGISTRY_PATH
    rules = load_registry(registry_path)

    # --list 模式
    if args.list_only:
        filtered = [r for r in rules if (not args.event or r.event == args.event)]
        if args.output_json:
            print(json.dumps([
                {
                    "id": r.id,
                    "event": r.event,
                    "phases": r.phases,
                    "path_patterns": r.path_patterns,
                    "validator": r.validator,
                    "severity": r.severity,
                    "blocking": r.blocking,
                    "enabled": r.enabled,
                    "description": r.description,
                }
                for r in filtered
            ], indent=2, ensure_ascii=False))
        else:
            print(f"Registered validators ({len(filtered)} for event='{args.event}'):")
            print()
            for r in filtered:
                status = "ON" if r.enabled else "OFF"
                print(f"  [{status:3s}] {r.id}")
                print(f"        event={r.event}, phases={r.phases}")
                print(f"        patterns={r.path_patterns}")
                print(f"        severity={r.severity}, blocking={r.blocking}, timeout={r.timeout}s")
                print(f"        validator={r.validator}")
                print(f"        {r.description}")
                print()
        return

    # 确定文件列表
    files = list(args.files) if args.files else []
    if args.staged:
        files = get_staged_files()
        if not files:
            print("[dispatch] no staged files")
            return

    # 匹配规则
    matched = match_rules(rules, args.event, files, args.phase, args.validator)

    # --dry-run 模式
    if args.dry_run:
        report = DispatchReport(event=args.event, matched_rules=[m[0] for m in matched])
        for rule, matched_files in matched:
            print(f"  MATCH [{rule.id}] files={matched_files}")
        if not matched:
            print(f"[dispatch] event={args.event}, files={files}: no matching validators")
        else:
            print(f"[dispatch] event={args.event}, files={files}: {len(matched)} validator(s) would run")
        return

    # --run 模式
    if args.run:
        report = DispatchReport(event=args.event, matched_rules=[m[0] for m in matched])
        extra = args.extra_args or []
        start_time = time.monotonic()
        for rule, matched_files in matched:
            result = run_validator(rule, matched_files, extra)
            report.results.append(result)
        report.total_duration_ms = int((time.monotonic() - start_time) * 1000)

        if args.output_json:
            print(json.dumps({
                "event": report.event,
                "total_duration_ms": report.total_duration_ms,
                "blocked": any(
                    not r.passed and r.severity == "error" and r.validator_id in {
                        rule.id for rule, _ in matched if rule.blocking
                    }
                    for r in report.results
                ),
                "results": [
                    {
                        "validator_id": r.validator_id,
                        "passed": r.passed,
                        "severity": r.severity,
                        "duration_ms": r.duration_ms,
                        "stdout": r.stdout,
                        "stderr": r.stderr,
                    }
                    for r in report.results
                ],
            }, indent=2, ensure_ascii=False))
        else:
            blocked = print_report(report, verbose=args.verbose)
            if blocked:
                sys.exit(1)
        return

    # 默认：打印帮助
    parser.print_help()


if __name__ == "__main__":
    main()
