"""Typed, dependency-free representation of the public evidence contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ValidationError(ValueError):
    """Raised when an evidence record violates the contract."""


@dataclass(frozen=True)
class EvidenceRecord:
    subject_id: str
    dataset_id: str
    snapshot_hash: str
    synthetic_data: bool
    checks: tuple[dict[str, Any], ...]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "EvidenceRecord":
        required = ("subject_id", "dataset_id", "snapshot_hash", "synthetic_data", "checks")
        missing = [key for key in required if key not in raw]
        if missing:
            raise ValidationError(f"missing required fields: {', '.join(missing)}")
        if not isinstance(raw["checks"], list) or not raw["checks"]:
            raise ValidationError("checks must be a non-empty list")
        return cls(
            subject_id=raw["subject_id"],
            dataset_id=raw["dataset_id"],
            snapshot_hash=raw["snapshot_hash"],
            synthetic_data=raw["synthetic_data"],
            checks=tuple(raw["checks"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "dataset_id": self.dataset_id,
            "snapshot_hash": self.snapshot_hash,
            "synthetic_data": self.synthetic_data,
            "checks": list(self.checks),
        }


@dataclass(frozen=True)
class AuditReport:
    version: str
    records: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {"contract_version": self.version, "records": list(self.records)}
