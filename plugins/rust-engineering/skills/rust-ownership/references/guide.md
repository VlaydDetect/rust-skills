# Rust Ownership Field Guide

This guide is the detailed policy for `rust-ownership`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Ownership determines who may drop a value; borrowing grants temporary access without transferring that responsibility.
- Mutable access must be exclusive for the duration used, while shared references forbid mutation except through sound interior-mutability mechanisms.
- Non-lexical lifetimes can end a borrow at last use, so control-flow reshaping often solves conflicts without extra allocation.
- Drop order is reverse declaration order within a scope and can affect locks, transactions, files, spans, and foreign resources.
- `Box` gives unique heap ownership, `Rc` shared single-thread ownership, `Arc` shared thread-safe ownership; neither reference-counted pointer alone makes inner mutation safe.
- Common diagnostics E0382, E0499, E0502, E0505, E0507, and E0597 point to different ownership-graph contradictions.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Caller retains data | Borrowed slice, str, or reference | Avoids transfer and allocation |
| Callee must retain independent data | Owned value | Borrow duration should not leak into unrelated callers |
| Single-thread shared graph | Rc with Cell or RefCell if needed | Matches non-Send topology with runtime borrow checks |
| Cross-thread shared graph | Arc plus lock or atomic invariant | Reference counting and mutation are separate concerns |
| Borrowed fast path with occasional edit | Cow | Makes conditional ownership explicit |

## Common Failure Modes

- Adding `'static` to satisfy the compiler when the data is not actually process-long or owned.
- Cloning every value at API boundaries and obscuring who owns state.
- Wrapping everything in `Arc<Mutex<_>>` without a concurrency protocol.
- Returning references to local temporaries or data protected by a dropped guard.
- Creating `Rc` or `Arc` cycles that keep resources alive indefinitely.

## Required Evidence

- An ownership and drop-order map for affected resources and references.
- The specific compiler rule or lifecycle invariant addressed by the chosen type.
- Tests or examples covering mutation, early return, error, cancellation, and cleanup paths as applicable.
- Allocation or contention measurements before selecting cloning or shared locking for performance reasons.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Design protocol map

Load only the branch that matches the controlling decision. These references preserve the source algorithms and examples; `rust-ownership` remains the owner and current project state overrides generic examples.

## Ownership and lifetimes

- [Core ownership questions](./ownership-overview.md)
- [Cross-language ownership comparison](./ownership-comparison.md)
- [Ownership best practices](./ownership-best-practices.md)
- [Compiler-error patterns](./ownership-common-errors.md)
- [Lifetime patterns](./ownership-lifetime-patterns.md)

Start here for moves, borrows, escaping references, lifetime relationships, or repeated clone-based fixes. Trace upward only when the local ownership graph exposes a design or domain mismatch.

## Resource topology

- [Resource-management protocol](./resource-overview.md)

Use this for `Box`, `Rc`, `Arc`, `Weak`, RAII, cycles, and drop ownership. Select from the actual single-thread, cross-thread, uniqueness, and lifecycle requirements.

## Mutability

- [Mutability protocol](./mutability-overview.md)

Use this for exclusive borrows, interior mutability, lock-backed mutation, and the question of whether mutation belongs at the current layer. No lock or cell type is a default independent of topology.

## Resource lifecycle

- [Lifecycle, guards, cleanup, and initialization](./lifecycle-overview.md)

Use this when acquisition, error, cancellation, shutdown, and drop paths must form one coherent resource protocol.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-async`](../../rust-concurrency/references/async.md) — supporting; Future lifecycle, cancellation safety, structured tasks, backpressure, bounded streams, joins, selection, and blocking boundaries.
- [`rust-async-pattern`](../../rust-concurrency/references/async-pattern.md) — supporting; Async architecture choices, arenas, actors, owned snapshots, task topology, cancellation, and lifetime containment.
- [`rust-concurrency`](../../rust-concurrency/references/concurrency.md) — supporting; Send/Sync, shared-state and message-passing choices, atomics, lock scope, thread/task ownership, cancellation, and shutdown.
- [`rust-ffi`](../../rust-unsafe-ffi/references/ffi-boundaries.md) — supporting; ABI layout, ownership transfer, allocator pairing, strings, callbacks, panic containment, handles, and foreign-thread behavior.
- [`rust-lifetime-complex`](./lifetime-complex.md) — primary; Lifetime diagnosis, variance, HRTBs, GATs, reborrowing, returned borrows, trait objects, and async lifetime boundaries.
- [`rust-linear-type`](./linear-type.md) — primary; Affine resource semantics, exactly-once transitions, typestate, non-cloneable capabilities, RAII, and leak versus double-use analysis.
- [`rust-mutability`](./mutability.md) — primary; Exclusive mutation, reborrowing, interior mutability, aliasing, lock/borrow scope, and observable API effects.
- [`rust-ownership`](./ownership.md) — primary; Moves, borrows, reborrows, smart pointers, lifetime boundaries, clone decisions, and ownership-error diagnosis.
- [`rust-pin`](../../rust-pin/references/pin.md) — supporting; Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.
- [`rust-resource`](./resource.md) — primary; RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
