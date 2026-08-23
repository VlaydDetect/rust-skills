# Rust API Design Field Guide

This guide is the detailed policy for `rust-api-design`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- A Rust API contract includes syntax, types, ownership, errors, panics, blocking, ordering, complexity expectations, feature gates, auto traits, and supported targets.
- The smallest public surface preserves future implementation freedom and reduces SemVer obligations.
- Type-driven APIs can make invalid construction or state transitions unrepresentable, but excessive typestate harms error messages and ergonomics.
- Re-exports define downstream paths; moving source modules can remain compatible only when public paths are preserved.
- Generic and trait bounds are observable restrictions, while blanket impls and associated types affect downstream extension rights.
- Examples are API design tests because they reveal imports, inference, naming, error handling, and ownership at call sites.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Small fixed configuration | Direct constructor | Required values remain obvious |
| Many optional validated settings | Builder | Named staged configuration improves calls |
| Caller supplies transient data | Borrowed parameter | Avoids unnecessary ownership transfer |
| Open downstream implementation set | Public trait | Extension is part of the product contract |
| Closed internal implementation set | Enum or sealed trait | Preserves exhaustiveness and evolution control |

## Common Failure Modes

- Publishing internal storage, synchronization, or dependency types because they are convenient today.
- Adding lifetime parameters to broad caller surfaces when small owned boundary values would decouple usage.
- Treating a default trait method or new required bound as automatically non-breaking.
- Exposing public fields and later needing to validate or evolve construction.
- Designing only the success call and leaving errors, cancellation, cleanup, and repeated calls unspecified.

## Required Evidence

- Representative caller examples for core and edge behaviors.
- A public-surface inventory including re-exports, features, errors, traits, auto traits, and dependency types.
- Compatibility analysis against the latest released or declared baseline when one exists.
- Rustdoc and compile evidence under the declared MSRV, features, and target constraints.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-api-design/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-auth`](../../rust-architecture/references/domains/auth.md) — supporting; Authentication and authorization boundaries, credential lifecycle, expiry, revocation, audit, secret handling, and failure taxonomy.
- [`rust-error`](../../rust-errors/references/error.md) — supporting; Result propagation, error boundaries, context, recoverability, domain errors, panic policy, and source chains.
- [`rust-error-advanced`](../../rust-errors/references/error-advanced.md) — supporting; Layered error composition, stable public variants, context, aggregation, retry classification, and async/concurrent failures.
- [`rust-lifetime-complex`](../../rust-ownership/references/lifetime-complex.md) — supporting; Lifetime diagnosis, variance, HRTBs, GATs, reborrowing, returned borrows, trait objects, and async lifetime boundaries.
- [`rust-macro`](../../rust-macros/references/macro.md) — supporting; macro_rules!, derive, attribute and function-like procedural macros, token handling, hygiene, diagnostics, expansion, and compile-time tests.
- [`rust-mutability`](../../rust-ownership/references/mutability.md) — supporting; Exclusive mutation, reborrowing, interior mutability, aliasing, lock/borrow scope, and observable API effects.
- [`rust-ownership`](../../rust-ownership/references/ownership.md) — supporting; Moves, borrows, reborrows, smart pointers, lifetime boundaries, clone decisions, and ownership-error diagnosis.
- [`rust-type-driven`](../../rust-traits/references/type-driven.md) — supporting; Newtypes, typestate, sealed states, capability types, trait bounds, associated types, and invalid-state elimination.
- [`rust-web`](../../rust-architecture/references/domains/web.md) — supporting; HTTP boundaries, extraction, validation, state ownership, cancellation, response contracts, graceful shutdown, and framework isolation.
- [`rust-xacml`](../../rust-architecture/references/domains/xacml.md) — supporting; Policy decision and enforcement boundaries, attribute modelling, combining algorithms, obligations, versioning, and auditability.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
