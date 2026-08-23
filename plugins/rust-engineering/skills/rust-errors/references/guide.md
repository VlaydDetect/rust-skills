# Rust Error Design Field Guide

This guide is the detailed policy for `rust-errors`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- An error taxonomy should correspond to caller actions such as retry, correct input, choose another resource, abort operation, or report a bug.
- `Result` propagates recoverable outcomes; `Option` is appropriate only when absence is the complete information callers need.
- Concrete enums work well for library contracts; context-oriented wrappers or erased reports work well at application composition boundaries.
- `From` conversions should be semantically lossless enough for their layer; overly broad conversions collapse distinct decisions.
- Error context should name the attempted operation and safe identifiers, not restate the lower-level message.
- Recovery includes compensation, fallback, retry, cancellation, and partial-success semantics, all of which need explicit ownership.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Public library boundary | Stable typed enum or structured type | Callers need matchable recovery categories |
| Application top level | Context-rich erased report | Composition matters more than downstream matching |
| Expected absence | Option | No additional cause or recovery category is needed |
| Invalid external input | Recoverable validation error | The caller can correct or reject the request |
| Impossible internal state | Invariant error or panic by policy | Distinguish bugs from routine operations |

## Common Failure Modes

- Using strings as the only error contract and forcing callers to parse display text.
- Logging an error at every propagation layer and producing duplicate noisy events.
- Hiding the original source or backtrace when adding high-level context.
- Retrying all errors, including invalid input, cancellation, permission denial, or non-idempotent operations.
- Publishing dependency error types and unintentionally coupling SemVer to that dependency.

## Required Evidence

- A failure taxonomy mapped to caller action, retryability, reporting, and redaction.
- Tests for important variants, causal chains, conversions, and negative recovery behavior.
- Public compatibility analysis for exported errors and non-exhaustive policy.
- A clear ownership boundary for logging so propagation does not duplicate telemetry.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Design protocol map

- [Error-handling decision model](./error-handling-overview.md)
- [Application versus library examples](./error-handling-library-vs-app.md)
- [Detailed error patterns](./error-handling-error-patterns.md)

Use these references to trace from a local `Result`, `Option`, panic, or propagation question to caller-visible recovery and domain semantics. Preserve source chains and context at boundaries. Do not turn `expect`, `unwrap`, `anyhow`, or `thiserror` into a universal preference.

## Domain recovery

- [Domain-error classification and recovery](./domain-error-overview.md)

Load this branch only when transient/permanent classification, retries, fallbacks, degradation, or user-visible codes are part of a confirmed product contract.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-actor`](../../rust-concurrency/references/actor.md) — supporting; Actor ownership, bounded mailboxes, request-response, supervision, restart policy, lifecycle, and backpressure.
- [`rust-async`](../../rust-concurrency/references/async.md) — supporting; Future lifecycle, cancellation safety, structured tasks, backpressure, bounded streams, joins, selection, and blocking boundaries.
- [`rust-auth`](../../rust-architecture/references/domains/auth.md) — supporting; Authentication and authorization boundaries, credential lifecycle, expiry, revocation, audit, secret handling, and failure taxonomy.
- [`rust-database`](../../rust-architecture/references/domains/database.md) — supporting; Persistence boundaries, transactions, consistency, schema evolution, query ownership, pooling, and error translation.
- [`rust-distributed`](../../rust-distributed-systems/references/distributed.md) — supporting; Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.
- [`rust-error`](./error.md) — primary; Result propagation, error boundaries, context, recoverability, domain errors, panic policy, and source chains.
- [`rust-error-advanced`](./error-advanced.md) — primary; Layered error composition, stable public variants, context, aggregation, retry classification, and async/concurrent failures.
- [`rust-linear-type`](../../rust-ownership/references/linear-type.md) — supporting; Affine resource semantics, exactly-once transitions, typestate, non-cloneable capabilities, RAII, and leak versus double-use analysis.
- [`rust-observability`](../../rust-observability/references/observability.md) — supporting; Structured events, spans, metrics, correlation, cardinality, redaction, sampling, and operational failure evidence.
- [`rust-resource`](../../rust-ownership/references/resource.md) — supporting; RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.
- [`rust-web`](../../rust-architecture/references/domains/web.md) — supporting; HTTP boundaries, extraction, validation, state ownership, cancellation, response contracts, graceful shutdown, and framework isolation.
- [`rust-xacml`](../../rust-architecture/references/domains/xacml.md) — supporting; Policy decision and enforcement boundaries, attribute modelling, combining algorithms, obligations, versioning, and auditability.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
