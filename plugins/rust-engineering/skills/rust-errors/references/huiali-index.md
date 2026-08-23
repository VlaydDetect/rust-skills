# Huiali references for `rust-errors`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-actor`](../../rust-concurrency/references/huiali/rust-actor.md) — supporting; Actor ownership, bounded mailboxes, request-response, supervision, restart policy, lifecycle, and backpressure.
- [`rust-async`](../../rust-concurrency/references/huiali/rust-async.md) — supporting; Future lifecycle, cancellation safety, structured tasks, backpressure, bounded streams, joins, selection, and blocking boundaries.
- [`rust-auth`](../../rust-architecture/references/huiali/rust-auth.md) — supporting; Authentication and authorization boundaries, credential lifecycle, expiry, revocation, audit, secret handling, and failure taxonomy.
- [`rust-database`](../../rust-architecture/references/huiali/rust-database.md) — supporting; Persistence boundaries, transactions, consistency, schema evolution, query ownership, pooling, and error translation.
- [`rust-distributed`](../../rust-distributed-systems/references/huiali/rust-distributed.md) — supporting; Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.
- [`rust-error`](huiali/rust-error.md) — primary; Result propagation, error boundaries, context, recoverability, domain errors, panic policy, and source chains.
- [`rust-error-advanced`](huiali/rust-error-advanced.md) — primary; Layered error composition, stable public variants, context, aggregation, retry classification, and async/concurrent failures.
- [`rust-linear-type`](../../rust-ownership/references/huiali/rust-linear-type.md) — supporting; Affine resource semantics, exactly-once transitions, typestate, non-cloneable capabilities, RAII, and leak versus double-use analysis.
- [`rust-observability`](../../rust-observability/references/huiali/rust-observability.md) — supporting; Structured events, spans, metrics, correlation, cardinality, redaction, sampling, and operational failure evidence.
- [`rust-resource`](../../rust-ownership/references/huiali/rust-resource.md) — supporting; RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.
- [`rust-web`](../../rust-architecture/references/huiali/rust-web.md) — supporting; HTTP boundaries, extraction, validation, state ownership, cancellation, response contracts, graceful shutdown, and framework isolation.
- [`rust-xacml`](../../rust-architecture/references/huiali/rust-xacml.md) — supporting; Policy decision and enforcement boundaries, attribute modelling, combining algorithms, obligations, versioning, and auditability.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
