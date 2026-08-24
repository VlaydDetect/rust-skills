# Observability

Prefix: `obs-` · 7 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a known operational question needs logs, spans, metrics, correlation, error reports, or redaction at an owning boundary.
- Defer when the signal has no consumer, duplicates propagated errors, exposes sensitive data, or creates unbounded cardinality or unmeasured hot-path cost.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`obs-error-chain`](../rules/obs-error-chain.md) | `conditional` | `rust-observability` | Log errors with their full source chain, and log each error exactly once |
| [`obs-instrument-spans`](../rules/obs-instrument-spans.md) | `conditional` | `rust-observability` | Use `#[tracing::instrument]` and spans to attach context to async tasks and requests |
| [`obs-levels-filter`](../rules/obs-levels-filter.md) | `conditional` | `rust-observability` | Use log levels meaningfully and filter with `EnvFilter` / `RUST_LOG` |
| [`obs-library-facade`](../rules/obs-library-facade.md) | `conditional` | `rust-observability` | Libraries emit through the tracing/log facade and never install a subscriber |
| [`obs-no-sensitive-data`](../rules/obs-no-sensitive-data.md) | `conditional` | `rust-observability` | Never log secrets or PII; redact or skip them |
| [`obs-structured-fields`](../rules/obs-structured-fields.md) | `conditional` | `rust-observability` | Record structured key-value fields, not values interpolated into the message string |
| [`obs-tracing-over-log`](../rules/obs-tracing-over-log.md) | `conditional` | `rust-observability` | Use `tracing` for structured, span-aware diagnostics instead of `println!` or bare `log` |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
