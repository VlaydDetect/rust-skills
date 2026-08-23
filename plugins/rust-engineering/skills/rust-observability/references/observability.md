# Specialized Rust Observability Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-observability`.
- Supporting profiles when needed: `$rust-errors`, `$rust-performance`.
- Scope retained: Structured events, spans, metrics, correlation, cardinality, redaction, sampling, and operational failure evidence.
- Baseline correction: Follow the project's telemetry stack and privacy boundary. Do not add a logging or tracing dependency, high-cardinality label, or global subscriber without a demonstrated contract.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

# Rust Observability Skill

## Core Question

**Which telemetry signals reduce mean time to detect and resolve production failures?**

## Signal Model

- Logs: contextual events and state snapshots.
- Traces: cross-service causal path and latency breakdown.
- Metrics: rate/error/duration + saturation and capacity.

Use all three intentionally, not interchangeably.

## Instrumentation Priorities

1. Request entry/exit and key business operations.
2. Downstream calls (DB, cache, RPC, queue).
3. Retry/timeouts and circuit-breaker transitions.
4. Queue depth and worker saturation.

## Logging Rules

- Structured logs only.
- No secrets/tokens/PII leakage.
- Stable field names for dashboards and alerts.

## Metrics Rules

- Keep label cardinality bounded.
- Prefer RED + USE style baseline metrics.
- Track queue/worker/resource saturation explicitly.

## Common Pitfalls

- High-cardinality labels (raw user/session IDs).
- Verbose debug logs on hot paths in production.
- Traces without propagated correlation context.
- Alert thresholds not aligned with SLOs.

## Review Checklist

- [ ] Critical path spans and error fields exist.
- [ ] Metrics cover latency/errors/saturation.
- [ ] Correlation IDs flow across service boundaries.
- [ ] Logging policy prevents sensitive data exposure.
- [ ] Alerts map to actionable runbooks.

## Verification Commands

```bash
cargo check
cargo test
cargo clippy
RUST_LOG=info cargo run
```

## Related Skills

- `rust-web`
- `rust-database`
- `rust-concurrency`
