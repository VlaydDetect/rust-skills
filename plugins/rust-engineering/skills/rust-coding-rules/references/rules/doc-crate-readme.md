# doc-crate-readme

> Unify the README and crate root docs with `#![doc = include_str!("../README.md")]`## Decision

Use this context-sensitive Rust decision when its premise is established: Unify the README and crate root docs with `#![doc = include_str!("../README.md")]`.

## Apply When

Apply when a user-facing or safety-relevant Rust contract needs discoverable guarantees, examples, errors, panics, features, or migration guidance, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the prose would duplicate volatile implementation detail or claim behavior not established by current code and tests. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Identify the reader path and contract, write the smallest complete example, and link to one authoritative detailed explanation.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

More documentation improves discoverability but duplicated volatile detail drifts; executable examples cost maintenance but catch contract regressions.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Run rustdoc links and doctests under intended features and inspect that examples include their actual prerequisites.

## Why It Matters

Maintaining a `README.md` and a separate crate-level doc comment in `lib.rs` leads to inevitable drift: the README gets updated for GitHub/crates.io visitors while the rustdoc front page grows stale, or vice versa. The `include_str!` attribute macro (stable since Rust 1.54) makes the README the single source of truth for both surfaces. Set `readme = "README.md"` in `Cargo.toml` so crates.io also picks up the same file. The result: one file, three consistent rendering targets — GitHub, crates.io, and docs.rs.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// src/lib.rs — separate doc comment that will drift from README.md
//! # my-crate
//!
//! A library for doing things. (duplicate, will get out of date)
//!
//! ## Usage
//! ...

pub fn do_thing() {}
```

```toml
# Cargo.toml — readme field absent; crates.io shows nothing
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// src/lib.rs — README is the single source of truth
#![doc = include_str!("../README.md")]

pub fn do_thing() {}
```

```toml
# Cargo.toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"
readme = "README.md"          # crates.io landing page
documentation = "https://docs.rs/my-crate"
```

## Handling Non-Rust Code Blocks in README

When the README contains code blocks that are not valid Rust, rustdoc will try to compile them as doc-tests and fail. Fix this by tagging those blocks:

````markdown
```bash
cargo add my-crate
```

```text
output that should not be compiled
```

```rust,no_run
// example that should be shown but not executed
let x = long_running_operation();
```
````

For TOML or shell blocks already tagged with their language (` ```toml `, ` ```bash `), rustdoc ignores them automatically — no extra annotation needed.

## Related Rules
- [doc-module-inner](doc-module-inner.md) - use `//!` for module-level documentation
- [doc-cargo-metadata](doc-cargo-metadata.md) - fill Cargo.toml metadata fields
- [doc-all-public](doc-all-public.md) - document all public items with `///`
