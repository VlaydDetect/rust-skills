# Huiali references for `rust-testing`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-macro`](../../rust-macros/references/huiali/rust-macro.md) — supporting; macro_rules!, derive, attribute and function-like procedural macros, token handling, hygiene, diagnostics, expansion, and compile-time tests.
- [`rust-testing`](huiali/rust-testing.md) — primary; Unit, integration, property, compile-fail, concurrency, fuzz and regression strategy with observable failure criteria.
- [`rust-unsafe`](../../rust-unsafe/references/huiali/rust-unsafe.md) — supporting; Unsafe preconditions, aliasing, initialization, layout, provenance, Send/Sync, panic safety, and safe-abstraction review.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
