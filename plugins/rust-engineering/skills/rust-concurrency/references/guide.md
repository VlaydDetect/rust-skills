# Rust Concurrency Field Guide

This guide is the detailed policy for `rust-concurrency`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Concurrency correctness includes safety, ordering, at-most or at-least-once effects, cancellation, shutdown, fairness, and resource bounds.
- Threads suit blocking or CPU work with OS scheduling; async suits many suspended I/O operations when the dependency stack supports it.
- Channels encode ownership transfer and buffering; capacity determines backpressure and failure behavior.
- Locks serialize access to an invariant and create ordering constraints that can deadlock when acquisition order is inconsistent.
- Structured concurrency ties child lifetime and failure to an owner instead of detaching unobserved work.
- Loom explores modeled schedules for supported primitives; stress tests find some timing failures but are not exhaustive proofs.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| One owner, many commands | Bounded channel to owner task | Avoids shared mutation and defines backpressure |
| Small shared invariant | Mutex or RwLock by measured access pattern | The lock makes atomicity explicit |
| Single numeric state machine | Atomic only with ordering proof | Lock-free complexity must remain contained |
| Blocking CPU work in async app | Dedicated blocking pool or threads | Avoids starving executor workers |
| Fire-and-forget proposal | Owned task with shutdown and result policy | Detached failures and leaks are otherwise invisible |

## Common Failure Modes

- Holding a std mutex guard across `.await` or blocking an async runtime worker.
- Using an unbounded channel as implicit load shedding.
- Spawning tasks whose errors, panics, and shutdown are never observed.
- Adding `Arc<Mutex<_>>` around a poorly defined state machine instead of assigning ownership.
- Choosing relaxed atomics without a complete happens-before argument.

## Required Evidence

- A task or thread topology and state-ownership diagram with capacities and lifecycle owners.
- Explicit invariants, lock order, message ordering, cancellation, overload, and shutdown contracts.
- Tests for close, cancel, timeout, partial failure, producer overload, and clean join or drain behavior.
- Loom, stress, sanitizer, or benchmark evidence only where applicable, with stated model and coverage limits.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-concurrency/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.

## Design protocol map

- [Concurrency decision model](./concurrency-overview.md)
- [Concurrency comparison](./concurrency-comparison.md)
- [Thread patterns](./concurrency-thread-patterns.md)
- [Async patterns](./concurrency-async-patterns.md)
- [Common concurrency failures](./concurrency-common-errors.md)

Load only the relevant branch: threads, async tasks, locks, channels, atomics, or failure diagnosis. Select standard-library, runtime, crossbeam, or parking_lot facilities from topology, cancellation, backpressure, poisoning, fairness, MSRV, and dependency policy; the examples are alternatives, not defaults.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-actor`](./actor.md) — primary; Actor ownership, bounded mailboxes, request-response, supervision, restart policy, lifecycle, and backpressure.
- [`rust-async`](./async.md) — primary; Future lifecycle, cancellation safety, structured tasks, backpressure, bounded streams, joins, selection, and blocking boundaries.
- [`rust-async-pattern`](./async-pattern.md) — primary; Async architecture choices, arenas, actors, owned snapshots, task topology, cancellation, and lifetime containment.
- [`rust-cache`](../../rust-architecture/references/domains/cache.md) — supporting; Cache ownership, key identity, freshness, invalidation, stampede control, capacity, failure behavior, and observability.
- [`rust-concurrency`](./concurrency.md) — primary; Send/Sync, shared-state and message-passing choices, atomics, lock scope, thread/task ownership, cancellation, and shutdown.
- [`rust-coroutine`](./coroutine.md) — primary; Stackless and stackful models, explicit state machines, suspension, scheduling, pinning, cancellation, and resource cleanup.
- [`rust-distributed`](../../rust-distributed-systems/references/distributed.md) — supporting; Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.
- [`rust-embedded`](../../rust-architecture/references/domains/embedded-runtime.md) — supporting; no_std constraints, HAL ownership, interrupts, bounded memory, timing, peripherals, power, and deterministic cleanup.
- [`rust-middleware`](../../rust-architecture/references/domains/middleware.md) — supporting; Request pipelines, ordering, short-circuiting, context propagation, cancellation, retries, timeouts, and cross-cutting policy.
- [`rust-mutability`](../../rust-ownership/references/mutability.md) — supporting; Exclusive mutation, reborrowing, interior mutability, aliasing, lock/borrow scope, and observable API effects.
- [`rust-ownership`](../../rust-ownership/references/ownership.md) — supporting; Moves, borrows, reborrows, smart pointers, lifetime boundaries, clone decisions, and ownership-error diagnosis.
- [`rust-pin`](../../rust-pin/references/pin.md) — supporting; Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.
- [`rust-resource`](../../rust-ownership/references/resource.md) — supporting; RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
