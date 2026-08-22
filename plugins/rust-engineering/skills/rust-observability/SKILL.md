---
name: rust-observability
description: Design Rust logs, tracing spans, metrics, correlation, error reporting, redaction, cardinality, and async context. Use when runtime behavior must be diagnosable and operational signals need clear ownership.
---

# Rust Observability

Own operational telemetry contracts and placement at meaningful system boundaries. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- Code needs structured logs, tracing spans, metrics, correlation IDs, error reporting, or instrumentation policy.
- Async or distributed operations are difficult to follow across tasks and boundaries.
- Telemetry is duplicated, high-cardinality, secret-bearing, noisy, or insufficient for an operational question.

## Workflow

1. Name the operational questions, service objectives, failure boundaries, users, and privacy or cost constraints telemetry must support.
2. Choose logs for discrete records, spans for causal operations, metrics for aggregate trends, and error reports for actionable failures.
3. Define event names, fields, units, levels, correlation, span relationships, cardinality budgets, and redaction policy.
4. Instrument ownership boundaries and significant state transitions once; avoid logging the same propagated error at every layer.
5. Ensure async context follows spawned work deliberately and that cancellation, retries, queueing, and shutdown remain distinguishable.
6. Test field presence and redaction where contractual, measure overhead for hot paths, and document subscriber or exporter assumptions.

## Decision Rules

- Telemetry should answer a known question; an event without an operator or debugging use is noise.
- Use structured fields for machine queries and concise messages for humans; do not encode fields only in formatted strings.
- Never record secrets, credentials, authorization headers, private payloads, or sensitive identifiers without an explicit safe representation.
- Metric labels must have bounded cardinality; raw user, request, path, or error strings usually do not.
- Log errors at the layer that owns the outcome or user-visible consequence, not every `?` propagation.
- Span names and fields should be stable enough for dashboards while implementation detail stays replaceable.
- Sampling and filtering affect evidence; absence from telemetry is not always absence of behavior.
- Instrumentation on hot paths needs overhead measurement and disabled-path cost awareness.

## Boundaries and Hand-offs

- `rust-errors` owns failure types and recovery; this profile owns when those failures become telemetry.
- `rust-performance` owns optimizing telemetry overhead after it is measured.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Observability field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
