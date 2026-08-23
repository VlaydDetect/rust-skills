# Huiali references for `rust-concurrency`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-actor`](huiali/rust-actor.md) — primary; Actor ownership, bounded mailboxes, request-response, supervision, restart policy, lifecycle, and backpressure.
- [`rust-async`](huiali/rust-async.md) — primary; Future lifecycle, cancellation safety, structured tasks, backpressure, bounded streams, joins, selection, and blocking boundaries.
- [`rust-async-pattern`](huiali/rust-async-pattern.md) — primary; Async architecture choices, arenas, actors, owned snapshots, task topology, cancellation, and lifetime containment.
- [`rust-cache`](../../rust-architecture/references/huiali/rust-cache.md) — supporting; Cache ownership, key identity, freshness, invalidation, stampede control, capacity, failure behavior, and observability.
- [`rust-concurrency`](huiali/rust-concurrency.md) — primary; Send/Sync, shared-state and message-passing choices, atomics, lock scope, thread/task ownership, cancellation, and shutdown.
- [`rust-coroutine`](huiali/rust-coroutine.md) — primary; Stackless and stackful models, explicit state machines, suspension, scheduling, pinning, cancellation, and resource cleanup.
- [`rust-distributed`](../../rust-distributed-systems/references/huiali/rust-distributed.md) — supporting; Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.
- [`rust-embedded`](../../rust-architecture/references/huiali/rust-embedded.md) — supporting; no_std constraints, HAL ownership, interrupts, bounded memory, timing, peripherals, power, and deterministic cleanup.
- [`rust-middleware`](../../rust-architecture/references/huiali/rust-middleware.md) — supporting; Request pipelines, ordering, short-circuiting, context propagation, cancellation, retries, timeouts, and cross-cutting policy.
- [`rust-mutability`](../../rust-ownership/references/huiali/rust-mutability.md) — supporting; Exclusive mutation, reborrowing, interior mutability, aliasing, lock/borrow scope, and observable API effects.
- [`rust-ownership`](../../rust-ownership/references/huiali/rust-ownership.md) — supporting; Moves, borrows, reborrows, smart pointers, lifetime boundaries, clone decisions, and ownership-error diagnosis.
- [`rust-pin`](../../rust-pin/references/huiali/rust-pin.md) — supporting; Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.
- [`rust-resource`](../../rust-ownership/references/huiali/rust-resource.md) — supporting; RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
