# Huiali references for `rust-api-design`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-auth`](../../rust-architecture/references/huiali/rust-auth.md) — supporting; Authentication and authorization boundaries, credential lifecycle, expiry, revocation, audit, secret handling, and failure taxonomy.
- [`rust-error`](../../rust-errors/references/huiali/rust-error.md) — supporting; Result propagation, error boundaries, context, recoverability, domain errors, panic policy, and source chains.
- [`rust-error-advanced`](../../rust-errors/references/huiali/rust-error-advanced.md) — supporting; Layered error composition, stable public variants, context, aggregation, retry classification, and async/concurrent failures.
- [`rust-lifetime-complex`](../../rust-ownership/references/huiali/rust-lifetime-complex.md) — supporting; Lifetime diagnosis, variance, HRTBs, GATs, reborrowing, returned borrows, trait objects, and async lifetime boundaries.
- [`rust-macro`](../../rust-macros/references/huiali/rust-macro.md) — supporting; macro_rules!, derive, attribute and function-like procedural macros, token handling, hygiene, diagnostics, expansion, and compile-time tests.
- [`rust-mutability`](../../rust-ownership/references/huiali/rust-mutability.md) — supporting; Exclusive mutation, reborrowing, interior mutability, aliasing, lock/borrow scope, and observable API effects.
- [`rust-ownership`](../../rust-ownership/references/huiali/rust-ownership.md) — supporting; Moves, borrows, reborrows, smart pointers, lifetime boundaries, clone decisions, and ownership-error diagnosis.
- [`rust-type-driven`](../../rust-traits/references/huiali/rust-type-driven.md) — supporting; Newtypes, typestate, sealed states, capability types, trait bounds, associated types, and invalid-state elimination.
- [`rust-web`](../../rust-architecture/references/huiali/rust-web.md) — supporting; HTTP boundaries, extraction, validation, state ownership, cancellation, response contracts, graceful shutdown, and framework isolation.
- [`rust-xacml`](../../rust-architecture/references/huiali/rust-xacml.md) — supporting; Policy decision and enforcement boundaries, attribute modelling, combining algorithms, obligations, versioning, and auditability.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
