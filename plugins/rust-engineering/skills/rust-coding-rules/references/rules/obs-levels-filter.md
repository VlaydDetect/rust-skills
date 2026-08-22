# obs-levels-filter

> Use log levels meaningfully and filter with `EnvFilter` / `RUST_LOG`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-observability; supporters=`rust-errors`, `rust-performance`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use log levels meaningfully and filter with `EnvFilter` / `RUST_LOG`.

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
- External crates referenced by the source (`tracing-subscriber`, `tracing`, `bytes`) must already be accepted by the project or be approved before addition.

## Verification

Test contractual fields and redaction, exercise async parentage and retries, and measure disabled and enabled overhead when material.

## Why It Matters

Log levels exist to communicate urgency and to let operators tune verbosity without recompiling. Misusing them — emitting everything at `info!`, or leaving `debug!` output in hot paths in production — overwhelms aggregators and hides real signals. `tracing_subscriber::EnvFilter` reads the `RUST_LOG` environment variable and supports per-crate, per-target, and per-span directives, giving operators fine-grained control at runtime. For release builds, tracing's `max_level_*` Cargo features can compile out verbose levels entirely, eliminating even the call-site overhead.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use tracing::info;

fn handle_request(path: &str, body: &[u8]) {
    // BAD: debug-level detail emitted at info — always noisy in production
    info!(path, body_len = body.len(), raw = ?body, "handling request");
    info!("entered handle_request");         // trace-level lifecycle noise
    info!("about to parse body");            // also trace-level
    // ... actual logic ...
    info!("done handling request");
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tracing::{debug, error, info, instrument, trace, warn};

#[instrument(skip(body))]
fn handle_request(path: &str, body: &[u8]) {
    trace!("entered handler");                          // very verbose — trace
    debug!(body_len = body.len(), "parsing body");      // diagnostic — debug
    info!(path, "request received");                    // lifecycle — info

    match parse_body(body) {
        Ok(parsed) => {
            info!(items = parsed.len(), "request processed");
        }
        Err(e) if is_client_error(&e) => {
            warn!(error = ?e, "malformed request from client");   // recoverable — warn
        }
        Err(e) => {
            error!(error = ?e, "unexpected parse failure");       // needs attention — error
        }
    }
}

fn parse_body(_body: &[u8]) -> Result<Vec<u8>, String> { Ok(vec![]) }
fn is_client_error(_e: &str) -> bool { false }
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// In main: configure EnvFilter from RUST_LOG
fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,myapp=debug,hyper=warn".into()),
        )
        .init();
}
```

## Level Guidelines

| Level | Use for | Example |
|---|---|---|
| `error!` | Failures that need immediate attention | database connection lost |
| `warn!` | Recoverable anomalies, degraded state | retrying after timeout |
| `info!` | High-level lifecycle events | server started, request complete |
| `debug!` | Diagnostic detail for development | query parameters, cache status |
| `trace!` | Very verbose, per-iteration detail | loop counters, raw bytes |

## Key Points

- `RUST_LOG=info,mycrate=debug,hyper=warn` — comma-separated target=level pairs; the first token sets the global default.
- Compile out verbose levels in release with Cargo features: `tracing = { version = "0.1", features = ["max_level_debug", "release_max_level_info"] }`.
- Prefer `try_from_default_env()` with a fallback string over `from_default_env()` so the binary still starts when `RUST_LOG` is unset or malformed.

## Related Rules
- [obs-tracing-over-log](obs-tracing-over-log.md) - foundational `tracing` setup
- [obs-library-facade](obs-library-facade.md) - libraries emit events; binaries configure filtering
