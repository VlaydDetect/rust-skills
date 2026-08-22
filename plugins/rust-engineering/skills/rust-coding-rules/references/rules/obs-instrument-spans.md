# obs-instrument-spans

> Use `#[tracing::instrument]` and spans to attach context to async tasks and requests

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-observability; supporters=`rust-errors`, `rust-performance`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `#[tracing::instrument]` and spans to attach context to async tasks and requests.

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

A span groups all events emitted during a logical operation (an HTTP request, a database call, a background job) and attaches structured context to every event within it. Without spans, log lines from concurrent async tasks interleave with no way to correlate them. The `#[tracing::instrument]` attribute creates a span automatically from the function's arguments as fields. There is one critical async pitfall: holding a span *entry guard* (`let _g = span.enter()`) across an `.await` point attaches the span to the wrong task when the executor resumes on a different thread — use `.instrument(span)` on the future instead.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use tracing::{info, span, Level};

// BAD: holding an entry guard across .await corrupts span context
async fn fetch_user(user_id: u64) -> Result<String, String> {
    let span = span!(Level::INFO, "fetch_user", user_id);
    let _guard = span.enter(); // guard held here...

    let result = some_async_db_call(user_id).await; // ...across this await — wrong!
    info!("fetched user");
    result
}

async fn some_async_db_call(_id: u64) -> Result<String, String> {
    Ok("alice".to_string())
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tracing::{info, instrument, Instrument, info_span};

// GOOD: #[instrument] handles async correctly; skip large/sensitive args
#[instrument(skip(db), fields(user.id = user_id))]
async fn fetch_user(user_id: u64, db: &DbPool) -> Result<String, DbError> {
    info!("fetching user from database");
    let user = db.query_user(user_id).await?;
    info!(username = %user.name, "user fetched");
    Ok(user.name)
}

// GOOD: manual span + .instrument() for dynamic span names
async fn process_job(job_id: &str) {
    let span = info_span!("process_job", job.id = job_id);
    async move {
        info!("job started");
        do_work().await;
        info!("job complete");
    }
    .instrument(span)
    .await;
}

async fn do_work() {}

// Placeholder types for the example
struct DbPool;
#[derive(Debug)] struct DbUser { name: String }
#[derive(Debug)] struct DbError;

impl DbPool {
    async fn query_user(&self, _id: u64) -> Result<DbUser, DbError> {
        Ok(DbUser { name: "alice".to_string() })
    }
}
```

## Key Points

- **`#[instrument]`** is the preferred way to instrument async functions — it wraps the whole future in `.instrument(span)` under the hood.
- Use `skip(arg)` or `skip_all` to exclude large types (e.g., database pools, byte buffers) and sensitive values from auto-captured fields.
- Use `fields(key = value)` inside `#[instrument]` to add or rename fields beyond the auto-captured args.
- For manual spans, always attach with `.instrument(span).await`, never hold a guard across `.await`.
- Spans nest automatically: entering a child span inside a parent records the parent's context in traces, enabling waterfall views in tools like Jaeger or Tempo.

## Related Rules
- [obs-structured-fields](obs-structured-fields.md) - structured fields within span events
- [obs-no-sensitive-data](obs-no-sensitive-data.md) - use `skip` to prevent secrets leaking into spans
- [async-no-lock-await](async-no-lock-await.md) - same problem pattern: do not hold guards across `.await`
