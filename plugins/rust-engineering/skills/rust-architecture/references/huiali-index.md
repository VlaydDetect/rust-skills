# Huiali references for `rust-architecture`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-actor`](../../rust-concurrency/references/huiali/rust-actor.md) — supporting; Actor ownership, bounded mailboxes, request-response, supervision, restart policy, lifecycle, and backpressure.
- [`rust-async-pattern`](../../rust-concurrency/references/huiali/rust-async-pattern.md) — supporting; Async architecture choices, arenas, actors, owned snapshots, task topology, cancellation, and lifetime containment.
- [`rust-auth`](huiali/rust-auth.md) — primary; Authentication and authorization boundaries, credential lifecycle, expiry, revocation, audit, secret handling, and failure taxonomy.
- [`rust-cache`](huiali/rust-cache.md) — primary; Cache ownership, key identity, freshness, invalidation, stampede control, capacity, failure behavior, and observability.
- [`rust-database`](huiali/rust-database.md) — primary; Persistence boundaries, transactions, consistency, schema evolution, query ownership, pooling, and error translation.
- [`rust-distributed`](../../rust-distributed-systems/references/huiali/rust-distributed.md) — supporting; Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.
- [`rust-embedded`](huiali/rust-embedded.md) — primary; no_std constraints, HAL ownership, interrupts, bounded memory, timing, peripherals, power, and deterministic cleanup.
- [`rust-error-advanced`](../../rust-errors/references/huiali/rust-error-advanced.md) — supporting; Layered error composition, stable public variants, context, aggregation, retry classification, and async/concurrent failures.
- [`rust-middleware`](huiali/rust-middleware.md) — primary; Request pipelines, ordering, short-circuiting, context propagation, cancellation, retries, timeouts, and cross-cutting policy.
- [`rust-web`](huiali/rust-web.md) — primary; HTTP boundaries, extraction, validation, state ownership, cancellation, response contracts, graceful shutdown, and framework isolation.
- [`rust-xacml`](huiali/rust-xacml.md) — primary; Policy decision and enforcement boundaries, attribute modelling, combining algorithms, obligations, versioning, and auditability.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
