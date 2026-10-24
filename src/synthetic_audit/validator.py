"""Validation and deterministic report generation."""

from __future__ import annotations

import math
from typing import Any, Iterable

from .contract import AuditReport, EvidenceRecord, ValidationError

ALLOWED_STATUSES = {"pass", "warning", "fail"}
CONTRACT_VERSION = "1.0"


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValidationError(f"{label} must be a finite number")
    return float(value)


def _validate_record(record: EvidenceRecord) -> dict[str, Any]:
    if not all(isinstance(value, str) and value for value in (record.subject_id, record.dataset_id, record.snapshot_hash)):
        raise ValidationError("subject_id, dataset_id, and snapshot_hash must be non-empty strings")
    if record.synthetic_data is not True:
        raise ValidationError("synthetic_data must be true in this public demo")

    seen_evidence: set[str] = set()
    results = []
    for check in record.checks:
        for key in ("check_id", "status", "expected", "observed", "tolerance", "evidence_refs"):
            if key not in check:
                raise ValidationError(f"{record.subject_id}: check missing {key}")
        check_id = check["check_id"]
        status = check["status"]
        if not isinstance(check_id, str) or not check_id:
            raise ValidationError(f"{record.subject_id}: check_id must be non-empty")
        if status not in ALLOWED_STATUSES:
            raise ValidationError(f"{record.subject_id}/{check_id}: invalid status {status!r}")
        expected = _number(check["expected"], "expected")
        observed = _number(check["observed"], "observed")
        tolerance = _number(check["tolerance"], "tolerance")
        if tolerance < 0:
            raise ValidationError(f"{record.subject_id}/{check_id}: tolerance must be non-negative")
        refs = check["evidence_refs"]
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref for ref in refs):
            raise ValidationError(f"{record.subject_id}/{check_id}: evidence_refs must be non-empty strings")
        if len(refs) != len(set(refs)):
            raise ValidationError(f"duplicate evidence references: {record.subject_id}/{check_id}")
        duplicates = seen_evidence.intersection(refs)
        if duplicates:
            raise ValidationError(f"duplicate evidence references: {', '.join(sorted(duplicates))}")
        seen_evidence.update(refs)

        delta = round(observed - expected, 10)
        if status == "pass" and abs(delta) > tolerance:
            raise ValidationError(f"{record.subject_id}/{check_id}: pass exceeds tolerance")
        results.append(
            {
                "check_id": check_id,
                "status": status,
                "expected": expected,
                "observed": observed,
                "delta": delta,
                "tolerance": tolerance,
                "evidence_refs": sorted(refs),
                "reason": check.get("reason", ""),
            }
        )
    return {
        "subject_id": record.subject_id,
        "dataset_id": record.dataset_id,
        "snapshot_hash": record.snapshot_hash,
        "synthetic_data": True,
        "checks": sorted(results, key=lambda result: result["check_id"]),
    }


def validate_records(raw_records: Iterable[dict[str, Any]]) -> AuditReport:
    records = [_validate_record(EvidenceRecord.from_dict(raw)) for raw in raw_records]
    subjects = [record["subject_id"] for record in records]
    if len(subjects) != len(set(subjects)):
        raise ValidationError("duplicate subject_id")
    return AuditReport(CONTRACT_VERSION, tuple(sorted(records, key=lambda record: record["subject_id"])))
