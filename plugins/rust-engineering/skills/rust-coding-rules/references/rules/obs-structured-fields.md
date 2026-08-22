# obs-structured-fields

> Record structured key-value fields, not values interpolated into the message string

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-observability; supporters=`rust-errors`, `rust-performance`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Record structured key-value fields, not values interpolated into the message string.

## Apply When

Apply when a known operational question needs logs, spans, metrics, correlation, error reports, or redaction at an owning boundary, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the signal has no consumer, duplicates propagated errors, exposes sensitive data, or creates unbounded cardinality or unmeasured hot-path cost. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Map the operational question to a signal, stable fields, owner, level, parentage, cardinality, redaction, and sampling policy.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Telemetry improves diagnosis while consuming CPU, allocation, storage, privacy budget, and operator attention.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tracing`) must already be accepted by the project or be approved before addition.

## Verification

Test contractual fields and redaction, exercise async parentage and retries, and measure disabled and enabled overhead when material.

## Why It Matters

When values are interpolated directly into the message string (e.g., `"processed 42 items for user 7 in 120ms"`), they become opaque text. Log aggregators (Loki, Elasticsearch, OpenTelemetry) cannot filter on `items = 42` or group by `user.id` because those values no longer exist as discrete fields. Structured fields keep data machine-parseable, filterable, and chart-able without regex post-processing. `tracing` supports three field sigils: `%expr` for `Display`, `?expr` for `Debug`, and bare `field = value` for typed primitives — the message string should only contain a stable, human-readable description.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use tracing::info;

fn process_batch(user_id: u64, items: usize, elapsed_ms: u64) {
    // Values buried in the message string — unqueryable in aggregators
    info!("processed {} items for user {} in {}ms", items, user_id, elapsed_ms);
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tracing::info;

fn process_batch(user_id: u64, items: usize, elapsed_ms: u64) {
    // Structured: each value is a discrete, queryable field
    info!(
        user.id = user_id,
        items,
        elapsed_ms,
        "batch processed"
    );
}

#[derive(Debug)]
struct Request {
    path: String,
    method: String,
}

fn handle_request(req: &Request, status: u16) {
    // %req uses Display; ?req uses Debug; status is a primitive
    info!(
        request = ?req,   // Debug format for the whole struct
        status,
        "request complete"
    );
}
```

## Field Sigil Reference

| Syntax | Trait used | When to use |
|---|---|---|
| `field = value` | native (primitive) | integers, bools, floats |
| `field = %expr` | `Display` | strings, IDs, URLs, types with clean `Display` |
| `field = ?expr` | `Debug` | structs, enums, vecs — for diagnostics |
| `field` (shorthand) | same as `field = field` | when name matches variable |

## Key Points

- Keep the message string short, stable, and human-readable. It should make sense *without* the fields.
- Prefer `%` over `?` for values that have a clean `Display` (e.g., `%id`, `%path`) — JSON backends quote Debug output inconsistently.
- Use namespaced field names like `user.id`, `http.status`, `db.query` when aligning to OpenTelemetry semantic conventions.
- Avoid placing the same data in both the message and a field (redundant and noisy).

## Related Rules
- [obs-tracing-over-log](obs-tracing-over-log.md) - foundational setup for `tracing`
- [obs-no-sensitive-data](obs-no-sensitive-data.md) - never put secrets or PII in structured fields
- [obs-error-chain](obs-error-chain.md) - log errors as structured fields with full source chain

## Verified Rulebook Example

<!-- rust-example: fixture; dependencies: tracing -->
```rust
fn main() {
    let user_id = 42_u64;
    tracing::info!(user_id, operation = "load", "request completed");
}
```
