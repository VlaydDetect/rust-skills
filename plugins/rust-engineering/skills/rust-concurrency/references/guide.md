# Rust Concurrency Field Guide

This guide is the detailed policy for `rust-concurrency`. It synthesizes the merged craft and full-stack concurrency skills covering threads, async, patterns, channels, locks, atomics, and testing; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

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
