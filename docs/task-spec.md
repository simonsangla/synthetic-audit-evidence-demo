# Task specification: deterministic audit evidence contract

## Objective

Extend this existing synthetic repository so a private analytics application can adapt its own
already-computed results into a stable, auditable JSON evidence report without exporting private rows.

## Done when

- The contract is versioned and documented.
- The validator rejects missing provenance, duplicate evidence references, invalid numeric values, and
  contradictory status/delta combinations.
- The report is deterministic across input order.
- Golden output and adversarial fixtures cover pass, warning, fail, and invalid-input paths.
- A private adapter example is documented without using private data or integrations.
- All offline checks pass.

## Natural multi-turn work

1. Inspect the current contract and identify ambiguous semantics.
2. Decide and document status, tolerance, provenance, and ordering rules.
3. Implement the smallest compatible validator/report change.
4. Add negative and adversarial fixtures.
5. Verify deterministic output, review the diff, and document the private adapter boundary.

## Non-goals

- No Lsante code, patient data, Firebase, authentication, Snowflake, Cortex, deployment, or network
  runtime.
- No compliance claim.
- No generic data-quality platform.
- No raw source-row export.
