# Rust Traits and Type-Driven Design Field Guide

This guide is the detailed policy for `rust-traits`. It synthesizes the craft trait dispatch and type-driven design guides plus full-stack stable and API design guidance; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

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
