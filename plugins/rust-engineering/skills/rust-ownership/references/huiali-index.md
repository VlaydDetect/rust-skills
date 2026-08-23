# Huiali references for `rust-ownership`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-async`](../../rust-concurrency/references/huiali/rust-async.md) — supporting; Future lifecycle, cancellation safety, structured tasks, backpressure, bounded streams, joins, selection, and blocking boundaries.
- [`rust-async-pattern`](../../rust-concurrency/references/huiali/rust-async-pattern.md) — supporting; Async architecture choices, arenas, actors, owned snapshots, task topology, cancellation, and lifetime containment.
- [`rust-concurrency`](../../rust-concurrency/references/huiali/rust-concurrency.md) — supporting; Send/Sync, shared-state and message-passing choices, atomics, lock scope, thread/task ownership, cancellation, and shutdown.
- [`rust-ffi`](../../rust-unsafe-ffi/references/huiali/rust-ffi.md) — supporting; ABI layout, ownership transfer, allocator pairing, strings, callbacks, panic containment, handles, and foreign-thread behavior.
- [`rust-lifetime-complex`](huiali/rust-lifetime-complex.md) — primary; Lifetime diagnosis, variance, HRTBs, GATs, reborrowing, returned borrows, trait objects, and async lifetime boundaries.
- [`rust-linear-type`](huiali/rust-linear-type.md) — primary; Affine resource semantics, exactly-once transitions, typestate, non-cloneable capabilities, RAII, and leak versus double-use analysis.
- [`rust-mutability`](huiali/rust-mutability.md) — primary; Exclusive mutation, reborrowing, interior mutability, aliasing, lock/borrow scope, and observable API effects.
- [`rust-ownership`](huiali/rust-ownership.md) — primary; Moves, borrows, reborrows, smart pointers, lifetime boundaries, clone decisions, and ownership-error diagnosis.
- [`rust-pin`](../../rust-pin/references/huiali/rust-pin.md) — supporting; Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.
- [`rust-resource`](huiali/rust-resource.md) — primary; RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
