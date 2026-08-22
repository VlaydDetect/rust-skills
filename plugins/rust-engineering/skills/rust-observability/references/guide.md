# Rust Observability Field Guide

This guide is the detailed policy for `rust-observability`. It synthesizes the full-stack observability skill and its tracing, metrics, logging, correlation, testing, and overhead references; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- Logs describe events, traces relate operations causally, and metrics aggregate numeric behavior over time; they complement rather than replace one another.
- A span should represent an operation with meaningful start, end, fields, parentage, outcome, and duration.
- Async tasks can lose current span context when spawned unless instrumentation or propagation is explicit.
- Retries create multiple attempts for one logical operation and should expose both attempt and final outcome without double-counting.
- Cardinality and event volume are correctness constraints for operational cost and query usability.
- Testing observability focuses on stable event contracts, field safety, and boundary placement—not exact prose unless required.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Individual failure investigation | Structured log or error report | Carries context for one occurrence |
| Cross-boundary request path | Trace and spans | Represents causal timing and nested operations |
| Rate, latency, saturation, errors | Metrics | Aggregate trends support alerting and capacity |
| Unbounded identifier | Log or sampled trace field, not metric label | Protects metric cardinality |
| Propagated internal error | Record once at outcome owner | Avoids duplicate events |

## Common Failure Modes

- Logging full request or response bodies by default and leaking secrets or personal data.
- Using high-cardinality values as metric labels.
- Creating a span for every helper and obscuring meaningful operation hierarchy.
- Logging errors at creation, wrapping, propagation, and top level.
- Assuming tracing context automatically follows every spawned async task or thread.

## Required Evidence

- Operational questions mapped to specific events, spans, metrics, fields, units, and owners.
- A redaction and cardinality review for every externally controlled field.
- Async parentage, retry, cancellation, queue, and shutdown behavior demonstrated where relevant.
- Subscriber or exporter setup, filter and sampling assumptions, and measured hot-path overhead when material.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-observability/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
