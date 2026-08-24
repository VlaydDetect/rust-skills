---
name: rust-concurrency
description: Design and debug Rust threads, async tasks, channels, locks, atomics, cancellation, backpressure, shutdown, Send and Sync, and concurrent state. Use when correctness or liveness spans execution contexts.
---

# Rust Concurrency

Own concurrent protocols, shared-state invariants, liveness, cancellation, and bounded execution. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- Threads, async tasks, executors, channels, locks, atomics, Send or Sync, cancellation, or shutdown are involved.
- The system can race, deadlock, hang, lose work, duplicate work, overload queues, or leak tasks.
- A synchronous versus async or message-passing versus shared-state decision controls the design.

## Workflow

1. Define the concurrency goal, state owner, task or thread topology, ordering, capacity, failure, cancellation, and shutdown semantics.
2. Choose synchronous, threaded, async, actor-like, channel, lock, or atomic mechanisms by workload and protocol rather than fashion.
3. Write invariants for shared data and lifecycle, including who starts, closes, drains, joins, retries, and reports failures.
4. Keep critical sections and borrow scopes narrow; never hold a blocking or incompatible lock across `.await`.
5. Bound queues, parallelism, retries, and time; define backpressure and overload behavior explicitly.
6. Test deterministic components, cancellation and shutdown paths, then use schedule exploration, stress, or loom where the primitive model supports it.

## Decision Rules

- `Send` permits ownership transfer and `Sync` permits shared references across threads; neither guarantees higher-level protocol correctness.
- Prefer ownership transfer or message passing when one component can own mutable state cleanly.
- A mutex protects an invariant, not merely a field; document which values must change together.
- Do not use unbounded channels where producers can outrun consumers under realistic failure or load.
- Cancellation can occur at suspension points and must not leave partial state, held permits, or orphan tasks.
- Every spawned task or thread needs an owner and an observation or join policy.
- Atomics require a written state machine and memory-ordering proof; use locks or channels when the protocol is not demonstrably simpler.
- Timeouts limit waiting but do not prove cancellation, cleanup, idempotency, or absence of deadlock.

## Rulebook Overlay

After task/thread ownership, bounds, cancellation, and shutdown are defined, select only relevant IDs from [`async-`](../rust-coding-rules/references/categories/async.md) or [`conc-`](../rust-coding-rules/references/categories/conc.md). Runtime or crate recommendations require existing adoption or approval.

## Boundaries and Hand-offs

- `rust-ownership` owns the underlying ownership and pointer graph; this profile owns cross-context coordination.
- `rust-observability` owns telemetry for task lifecycle and queues; `rust-performance` owns throughput or latency optimization.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Concurrency field guide](references/guide.md) before making a consequential design choice. Load only the needed branch of the [Design protocol concurrency protocol](./references/guide.md) for its detailed algorithms and examples. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Specialized Rust protocols

For additional topic detail, read the [Profile reference index](./references/guide.md) and load only the matching family reference.

## Low-level protocols

For low-level debugging, profiling, build, sanitizer, cross-target, ABI, async-internal, security, or hardware detail, read the [Low-level reference index](references/low-level-index.md) and load only the matching family. Apply its official-evidence and command-safety gate before execution.
