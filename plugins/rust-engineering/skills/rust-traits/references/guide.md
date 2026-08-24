# Rust Traits and Type-Driven Design Field Guide

This guide is the detailed policy for `rust-traits`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- A trait is a behavioral contract, not merely a shared method name.
- Generic dispatch selects implementations at compile time; `dyn Trait` uses a vtable and requires an object-safe surface.
- Object safety is affected by `Self` use, generic methods, associated functions, and sized requirements.
- Coherence prevents ambiguous implementations across crates and makes blanket impl choices consequential.
- Newtypes create a local nominal type for invariants, implementations, and representation control.
- `PhantomData` communicates ownership, variance, drop-check, or auto-trait relationships and must match the real invariant.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| One known implementation | Concrete type or function | A trait adds indirection without present variation |
| Many compile-time implementations | Generic bound | Retains concrete types and optimization |
| Runtime plugin-like set | Trait object | Callers need heterogeneous values behind one interface |
| Closed variant set | Enum | Exhaustiveness and data-bearing variants are useful |
| External trait and type | Local newtype | Satisfies coherence while owning semantics |

## Common Failure Modes

- Creating one-method traits for every concrete helper without an actual boundary.
- Publishing blanket impls that prevent downstream implementations or overlap later.
- Returning trait objects without deciding ownership, lifetime, `Send`, or `Sync` requirements.
- Using typestate where a validated constructor and private fields express the invariant more simply.
- Adding `Clone + Send + Sync + 'static` bounds by habit and excluding valid implementations.

## Required Evidence

- At least two real implementations or a documented runtime or crate boundary that justifies abstraction.
- Dispatch, extension, object-safety, auto-trait, and compatibility decisions.
- Compile-pass and compile-fail examples for important bounds or state transitions.
- A public API review of blanket impls, associated types, sealing, and downstream implementation rights.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Design protocol map

Use these references after the API and ownership constraints are known. They preserve Design protocol's mechanical questions without treating every compile-time encoding as desirable.

## Zero-cost abstractions

- [Generics, dispatch, and monomorphization](./zero-cost-overview.md)

Use when choosing generics, `impl Trait`, trait objects, or manual specialization. Include code-size, compile-time, object-safety, and dynamic-dispatch costs in the decision.

## Type-driven design

- [Newtypes, typestate, markers, and sealed traits](./type-driven-overview.md)

Use when invalid states can be excluded at a stable boundary. Reject typestate or marker machinery when runtime validation is clearer or when state growth makes the API harder to use.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-const`](../../rust-stable/references/const.md) — supporting; Const evaluation, const fn, const generics, compile-time constraints, static data, and supported-toolchain limits.
- [`rust-lifetime-complex`](../../rust-ownership/references/lifetime-complex.md) — supporting; Lifetime diagnosis, variance, HRTBs, GATs, reborrowing, returned borrows, trait objects, and async lifetime boundaries.
- [`rust-linear-type`](../../rust-ownership/references/linear-type.md) — supporting; Affine resource semantics, exactly-once transitions, typestate, non-cloneable capabilities, RAII, and leak versus double-use analysis.
- [`rust-type-driven`](./type-driven.md) — primary; Newtypes, typestate, sealed states, capability types, trait bounds, associated types, and invalid-state elimination.
- [`rust-zero-cost`](../../rust-performance/references/zero-cost.md) — supporting; Static versus dynamic dispatch, monomorphization, iterators, abstraction boundaries, code size, allocation, and measured runtime cost.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
