# obs-error-chain

> Log errors with their full source chain, and log each error exactly once

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-observability; supporters=`rust-errors`, `rust-performance`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Log errors with their full source chain, and log each error exactly once.

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
- External crates referenced by the source (`anyhow`, `tracing`) must already be accepted by the project or be approved before addition.

## Verification

Test contractual fields and redaction, exercise async parentage and retries, and measure disabled and enabled overhead when material.

## Why It Matters

Logging only the top-level `Display` of an error silently drops the underlying cause chain — you see "request failed" but not *why*. The two common fixes are: use `?` format (`error = ?err`) to capture `Debug` output including the chain, or use `{:#}` on an `anyhow::Error` which formats the full cause chain. The second hazard is the log-and-return anti-pattern: logging the error at every propagation layer records the same failure multiple times with different amounts of context, polluting aggregators. Log once, at the boundary that *handles* the error; everywhere else, propagate with `?` and optionally add context.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use tracing::error;

async fn fetch_data(id: u64) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
    let data = read_from_db(id).await.map_err(|e| {
        error!("{}", e);  // BAD: drops source chain, logs too early
        e
    })?;
    Ok(data)
}

async fn handle(id: u64) -> Result<(), Box<dyn std::error::Error>> {
    let data = fetch_data(id).await.map_err(|e| {
        error!("{}", e);  // BAD: logged again at every layer
        e
    })?;
    process(data);
    Ok(())
}

async fn read_from_db(_id: u64) -> Result<Vec<u8>, std::io::Error> {
    Err(std::io::Error::other("connection refused"))
}
fn process(_data: Vec<u8>) {}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use anyhow::{Context, Result};
use tracing::{error, instrument, warn};

// Propagate with context; do NOT log here
#[instrument]
async fn read_from_db(id: u64) -> Result<Vec<u8>> {
    inner_db_call(id)
        .await
        .with_context(|| format!("failed to read record {id} from database"))
    // No logging — just add context and propagate
}

// Also just propagates
#[instrument]
async fn fetch_data(id: u64) -> Result<Vec<u8>> {
    read_from_db(id).await.context("fetch_data failed")
}

// The handler boundary: this is where the error is HANDLED, so log it once
#[instrument]
async fn handle_request(id: u64) -> Result<(), String> {
    match fetch_data(id).await {
        Ok(data) => {
            process(data);
            Ok(())
        }
        Err(err) => {
            // {:#} on anyhow::Error prints the full cause chain
            error!(error = %format!("{err:#}"), "request failed");
            Err("internal error".to_string())
        }
    }
}

async fn inner_db_call(_id: u64) -> Result<Vec<u8>> {
    Err(anyhow::anyhow!("connection refused"))
}
fn process(_data: Vec<u8>) {}
```

## Key Points

- **`error = ?err`**: uses `Debug` — prints the error and its `source()` chain for types that implement it.
- **`format!("{err:#}")`** or `%format!(...)`: `anyhow::Error`'s alternate Display walks the full chain with `: ` separators.
- **Propagate, don't log**: use `?` and `.context()` / `.with_context()` at intermediate layers; log at the single handling boundary.
- If you *must* log at a non-handling layer (e.g., background task that discards the error), use `warn!` not `error!` to signal it was absorbed.
- The `tracing-error` crate provides `SpanTrace` to capture the span context at the error site and attach it to the error type.

## Related Rules
- [err-context-chain](err-context-chain.md) - add context with `.context()` / `.with_context()`
- [err-source-chain](err-source-chain.md) - chain underlying errors with `#[source]`
- [anti-empty-catch](anti-empty-catch.md) - avoid silently swallowing errors
