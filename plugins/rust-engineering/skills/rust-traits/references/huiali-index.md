# Huiali references for `rust-traits`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-const`](../../rust-stable/references/huiali/rust-const.md) — supporting; Const evaluation, const fn, const generics, compile-time constraints, static data, and supported-toolchain limits.
- [`rust-lifetime-complex`](../../rust-ownership/references/huiali/rust-lifetime-complex.md) — supporting; Lifetime diagnosis, variance, HRTBs, GATs, reborrowing, returned borrows, trait objects, and async lifetime boundaries.
- [`rust-linear-type`](../../rust-ownership/references/huiali/rust-linear-type.md) — supporting; Affine resource semantics, exactly-once transitions, typestate, non-cloneable capabilities, RAII, and leak versus double-use analysis.
- [`rust-type-driven`](huiali/rust-type-driven.md) — primary; Newtypes, typestate, sealed states, capability types, trait bounds, associated types, and invalid-state elimination.
- [`rust-zero-cost`](../../rust-performance/references/huiali/rust-zero-cost.md) — supporting; Static versus dynamic dispatch, monomorphization, iterators, abstraction boundaries, code size, allocation, and measured runtime cost.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
