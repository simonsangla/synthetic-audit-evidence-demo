# Source lineage and reuse boundary

This demo was derived from a real analytics need represented by the public
[`dbt-revenue-variance-demo`](https://github.com/simonsangla/dbt-revenue-variance-demo):
make expected-versus-observed variance evidence reproducible and reviewable.

The demo intentionally keeps only the portable contract idea. It does not copy
the source repository's project, seeds, generated site, warehouse profile, or
runtime integration. All values in this repository are newly authored synthetic
fixtures.

## Adapter boundary

A consuming private application should map its own already-computed results to
the contract at its boundary. Raw rows, private identifiers, credentials, and
source-system exports stay in that private application. This repository must
never receive reverse-synchronized evidence from a private consumer.
