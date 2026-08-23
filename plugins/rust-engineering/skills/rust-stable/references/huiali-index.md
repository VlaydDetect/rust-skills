# Huiali references for `rust-stable`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-const`](huiali/rust-const.md) — primary; Const evaluation, const fn, const generics, compile-time constraints, static data, and supported-toolchain limits.
- [`rust-coroutine`](../../rust-concurrency/references/huiali/rust-coroutine.md) — supporting; Stackless and stackful models, explicit state machines, suspension, scheduling, pinning, cancellation, and resource cleanup.
- [`rust-learner`](../../rust-research/references/huiali/rust-learner.md) — supporting; Current-feature adoption, MSRV and Edition evidence, release-note research, feedback, and dependency-ordered practice.
- [`rust-type-driven`](../../rust-traits/references/huiali/rust-type-driven.md) — supporting; Newtypes, typestate, sealed states, capability types, trait bounds, associated types, and invalid-state elimination.
- [`rust-zero-cost`](../../rust-performance/references/huiali/rust-zero-cost.md) — supporting; Static versus dynamic dispatch, monomorphization, iterators, abstraction boundaries, code size, allocation, and measured runtime cost.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
