#!/usr/bin/env python3
"""gate_result — 统一 gate result 输出协议。

所有 validator 必须使用此模块生成结果，确保输出符合
harness/gates/schemas/gate-result.schema.json。
"""

from typing import Any


def make_result(
    gate_id: str,
    validator: str,
    status: str,
    blocking: bool,
    checked_files: list[str] | None = None,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
    rule_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建符合 gate-result.schema.json 的 result dict。"""
    return {
        "gate_id": gate_id,
        "validator": validator,
        "status": status,
        "blocking": blocking,
        "checked_files": checked_files or [],
        "errors": errors or [],
        "warnings": warnings or [],
        "rule_refs": rule_refs or [],
        "metadata": metadata or {},
    }


def aggregate_results(
    gate_id: str,
    blocking: bool,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """聚合多个 validator result 为单个 gate result。

    聚合规则：
    1. 任一 validator.blocking=true 且 status=error -> gate status error
    2. 任一 validator.blocking=true 且 status=fail -> gate status fail
    3. 任一 validator.blocking=false 且 status=fail/error -> 降级为 warn
    4. 任一 validator.blocking=true 且 status=warn -> gate status warn
    5. 全部 pass/skip -> pass，除非全部 skip 则 skip
    """
    if not results:
        return make_result(
            gate_id=gate_id,
            validator="aggregate",
            status="skip",
            blocking=blocking,
        )

    statuses = {r.get("status", "pass") for r in results}
    all_checked_files = []
    all_errors = []
    all_warnings = []
    all_rule_refs = set()

    for r in results:
        all_checked_files.extend(r.get("checked_files", []))
        all_errors.extend(r.get("errors", []))
        all_warnings.extend(r.get("warnings", []))
        all_rule_refs.update(r.get("rule_refs", []))

    # 确定聚合状态 — 尊重 per-validator blocking 意图
    # blocking=false 的 validator 的 fail/error 降级为 warn
    effective_statuses = set()
    for r in results:
        s = r.get("status", "pass")
        is_blocking = r.get("blocking", True)  # 默认 blocking=true（安全）
        if not is_blocking and s in ("fail", "error"):
            # 非阻断 validator 的问题降级为 advisory warning
            effective_statuses.add("warn")
            # 把原始错误移入 warnings
            for err in r.get("errors", []):
                all_warnings.append(f"[advisory] {err}")
            # 清空 errors 列表中该 validator 的贡献
            all_errors = [e for e in all_errors if e not in r.get("errors", [])]
        else:
            effective_statuses.add(s)

    if "error" in effective_statuses:
        status = "error"
    elif "fail" in effective_statuses:
        status = "fail"
    elif "warn" in effective_statuses:
        status = "warn"
    elif all(s in ("pass", "skip") for s in effective_statuses):
        if all(s == "skip" for s in effective_statuses):
            status = "skip"
        else:
            status = "pass"
    else:
        status = "pass"

    return make_result(
        gate_id=gate_id,
        validator="aggregate",
        status=status,
        blocking=blocking,
        checked_files=list(set(all_checked_files)),
        errors=all_errors,
        warnings=all_warnings,
        rule_refs=list(all_rule_refs),
        metadata={"aggregated_from": len(results)},
    )
