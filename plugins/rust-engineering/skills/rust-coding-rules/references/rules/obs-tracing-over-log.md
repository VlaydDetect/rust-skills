# obs-tracing-over-log

> Use `tracing` for structured, span-aware diagnostics instead of `println!` or bare `log`## Decision

Consider this rule only after its prerequisites are satisfied: Use `tracing` for structured, span-aware diagnostics instead of `println!` or bare `log`.

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
- External crates referenced by the source (`tokio`, `tracing-subscriber`, `tracing`) must already be accepted by the project or be approved before addition.

## Verification

Test contractual fields and redaction, exercise async parentage and retries, and measure disabled and enabled overhead when material.

## Why It Matters

`println!` and `eprintln!` have no concept of log levels, targets, or structured data — they cannot be silenced, filtered, or parsed by observability pipelines. The `log` facade improves this but emits only flat strings and has no notion of spans. `tracing` records both *events* (point-in-time observations) and *spans* (contextual scopes that automatically follow execution across `.await` points and threads), with structured key-value fields, level filtering, and target routing. It is also interoperable with the `log` ecosystem via `tracing`'s `log` feature flag.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn handle_login(id: u64) {
    println!("user {} logged in", id);
    // No level, no structure, no filtering, goes to stdout unconditionally
}

fn main() {
    handle_login(42);
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tracing::info;

fn handle_login(id: u64) {
    // Structured field: user.id is queryable in JSON/OpenTelemetry backends
    info!(user.id = %id, "user logged in");
}

fn main() {
    // One-time subscriber init belongs in the binary, not in libraries
    tracing_subscriber::fmt::init();
    handle_login(42);
}
```

## Key Points

| Approach | Levels | Structured | Async-aware spans | `log` compat |
|---|---|---|---|---|
| `println!` | No | No | No | No |
| `log` facade | Yes | No | No | Yes |
| `tracing` | Yes | Yes | Yes | Yes (via feature) |

- Add to `Cargo.toml`: `tracing = "0.1"` for all crates; `tracing-subscriber = { version = "0.3", features = ["env-filter"] }` for binaries only.
- The `%expr` sigil uses `Display`; `?expr` uses `Debug`; bare `field = value` records typed primitives.
- `tracing` ships a `log` compatibility bridge: set `tracing-subscriber`'s `log` feature or call `tracing_log::LogTracer::init()` to capture existing `log`-emitting dependencies.

## Related Rules
- [obs-structured-fields](obs-structured-fields.md) - record key-value fields, not interpolated strings
- [obs-instrument-spans](obs-instrument-spans.md) - attach context to async tasks with spans
- [async-tokio-runtime](async-tokio-runtime.md) - production async runtime setup
