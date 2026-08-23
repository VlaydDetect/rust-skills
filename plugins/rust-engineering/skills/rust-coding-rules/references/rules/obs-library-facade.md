# obs-library-facade

> Libraries emit through the tracing/log facade and never install a subscriber## Decision

Consider this rule only after its prerequisites are satisfied: Libraries emit through the tracing/log facade and never install a subscriber.

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
- External crates referenced by the source (`serde`, `tracing-subscriber`, `tracing`, `log`) must already be accepted by the project or be approved before addition.

## Verification

Test contractual fields and redaction, exercise async parentage and retries, and measure disabled and enabled overhead when material.

## Why It Matters

Installing a global subscriber or logger is a one-time, process-wide operation. If a library calls `tracing_subscriber::fmt::init()` or `env_logger::init()`, it silently conflicts with any other library or the application binary that does the same — the second call panics or is silently ignored, and the caller loses all control over log format, destination, and level filtering. Libraries must only *emit* events and spans; the binary that owns `main` decides how to handle them. This is the same contract as `log` has always enforced and `tracing` carries forward.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// In a library crate: mylib/src/lib.rs
use tracing::info;

pub fn connect(url: &str) {
    // BAD: library installs a subscriber — conflicts with the application
    tracing_subscriber::fmt::init();
    info!(url, "connecting");
}
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Also bad: using env_logger in a library
pub fn init_logging() {
    env_logger::init(); // steals the global logger from the application
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// In a library crate: mylib/src/lib.rs
use tracing::info;

pub fn connect(url: &str) {
    // Good: just emit; the application owns subscriber setup
    info!(url, "connecting");
}
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// In the binary: src/main.rs
fn main() {
    // The application initializes once, with full control
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    mylib::connect("postgres://localhost/app");
}
```

## Key Points

- **Library `Cargo.toml`**: depend on `tracing = "0.1"` only. Do **not** add `tracing-subscriber` or `env_logger` as non-`dev` dependencies.
- **Binary `Cargo.toml`**: add `tracing-subscriber = { version = "0.3", features = ["env-filter"] }` for the subscriber.
- If you need a subscriber in library tests, add it to `[dev-dependencies]` and call it inside `#[test]` functions using `tracing_subscriber::fmt::try_init()` (the `try_` variant does not panic on re-init).
- The `log` crate follows the same rule: libraries call `log::info!(...)`; applications call `env_logger::init()` or bridge via `tracing_log::LogTracer`.

```toml
# library Cargo.toml
[dependencies]
tracing = "0.1"

[dev-dependencies]
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

## Related Rules
- [obs-tracing-over-log](obs-tracing-over-log.md) - why to use `tracing` over `println!` or bare `log`
- [obs-levels-filter](obs-levels-filter.md) - configure level filtering with `EnvFilter` in the binary
- [api-serde-optional](api-serde-optional.md) - pattern for gating heavy dependencies behind feature flags
