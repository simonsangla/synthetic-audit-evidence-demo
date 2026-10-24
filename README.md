# Synthetic Audit Evidence Demo

Small, public, synthetic reference implementation for a deterministic audit/evidence contract.

The project turns expected-versus-observed checks into a stable JSON report with explicit provenance,
reconciliation deltas, and a status of `pass`, `warning`, or `fail`. It is deliberately domain-neutral:
the fixtures contain no patient, client, production, Firebase, Snowflake, or authentication data.

## Why this exists

The contract is a portable seam for analytics and operations applications. A private project can map
its own results into this shape without exporting source rows or private identifiers. The public demo
proves the contract, validator, deterministic ordering, and negative cases offline.

## Run

```bash
python3 -m unittest discover -s tests -v
python3 -m synthetic_audit.cli fixtures/evidence.json --output /tmp/audit-report.json
python3 -m synthetic_audit.cli fixtures/evidence.json --check fixtures/expected-report.json
```

No third-party packages or network access are required. `PYTHONPATH=src` is set by the test command
below through `tests/__init__.py`; for direct CLI use, run from the repository root with:

```bash
PYTHONPATH=src python3 -m synthetic_audit.cli fixtures/evidence.json --check fixtures/expected-report.json
```

## Contract

Each evidence record includes:

- a stable `subject_id` and `dataset_id`;
- a fixture `snapshot_hash`;
- checks with expected and observed values;
- a reconciliation delta and tolerance;
- evidence references;
- explicit `synthetic_data: true` metadata;
- deterministic status and failure reason.

The validator rejects missing provenance, duplicate evidence references, invalid statuses, and
non-finite numeric values. Reports are sorted by `subject_id` and check id before serialization.

## Private adapter pattern

Keep private source rows and identifiers inside the private project. A private adapter should map its
already-computed results into this contract, calculate hashes locally, run the validator, and export
only the report if that is permitted. Do not reverse-sync private evidence into this repository.

## Scope boundary

This is not a compliance framework, a healthcare model, a data-quality guarantee, or a replacement for
source-system controls. Green output means only that the supplied evidence satisfies this contract.
