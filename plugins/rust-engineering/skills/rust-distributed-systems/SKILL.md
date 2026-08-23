---
name: rust-distributed-systems
description: Design Rust systems across process or node failure boundaries, including consistency, idempotency, retry budgets, leases, versioned contracts, deduplication, saga and outbox coordination, consensus models, and two-phase commit trade-offs.
---

# Rust Distributed Systems

Own cross-node failure and consistency decisions. Keep delivery semantics, time, identity, retries, storage, and recovery explicit before selecting implementation mechanisms.

## Use This Skill When

- A request, command, event, job, or transaction crosses process or node boundaries.
- Retries can duplicate work, responses can be lost, messages can reorder, clocks can drift, or a coordinator can fail.
- Consistency, leases, leader election, saga/outbox, consensus, or two-phase commit is under discussion.

## Workflow

1. Define the operation, authoritative state, identities, invariants, and observable success.
2. Enumerate partial failures at every send, persist, apply, acknowledge, publish, and retry boundary.
3. Choose consistency and delivery semantics from product requirements, not protocol prestige.
4. Define idempotency key scope, deduplication persistence/expiry, retry classification, backoff, jitter, attempt and elapsed budgets.
5. Version wire and event contracts; specify compatibility, ordering, replay, and migration behavior.
6. Select coordination components from mature implementations, then test failure, recovery, duplicate, stale, and split-brain scenarios.

## Decision Rules

- A timeout means the outcome is unknown, not necessarily failed.
- At-least-once delivery requires idempotent effects or durable deduplication at the effect boundary.
- Retry budgets include attempts, elapsed time, backoff, jitter, per-attempt timeout, and cancellation/deadline propagation.
- Leases depend on bounded timing assumptions and fencing; an expired lease holder may still be alive.
- An outbox closes a local persist/publish gap only when relay, ordering, deduplication, and retention are defined.
- Do not write Raft, consensus, or two-phase commit from scratch for production merely because a model is easy to sketch.

## Boundaries and Hand-offs

- `rust-architecture` owns service and storage boundaries; this profile owns cross-node failure and consistency.
- `rust-concurrency` owns in-process tasks, queues, and cancellation.
- `rust-errors` owns error taxonomy and public error contracts; this profile classifies retryability and uncertainty.
- `rust-observability` supports correlation and recovery evidence; `rust-research` verifies selected components.

## Detailed Reference

Read [Distributed Systems field guide](references/guide.md) before adding retries or coordination. Load the [`rust-distributed` Huiali protocol](references/huiali/rust-distributed.md) for detailed source algorithms and classified fragments.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
