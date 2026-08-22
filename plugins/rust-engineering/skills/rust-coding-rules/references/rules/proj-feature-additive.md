# proj-feature-additive

> Design Cargo features to be strictly additive

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-cargo-build; supporters=`rust-api-design`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Design Cargo features to be strictly additive.

## Apply When

Apply when a demonstrated module, crate, visibility, target, feature, MSRV, or build-script boundary needs clearer ownership, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the change is driven only by file size or speculative reuse and would add package, public API, build, or migration cost. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Map current owners and public paths, choose the cheapest boundary that enforces responsibility, and plan all callers and configurations.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Stronger boundaries improve ownership and isolation while adding navigation, build graph, feature, release, and migration overhead.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `serde`) must already be accepted by the project or be approved before addition.

## Verification

Inspect cargo metadata and public paths, then compile affected packages, features, targets, docs, tests, and generated boundaries.

## Why It Matters

Cargo unifies features across the dependency graph: if any crate in the build enables a feature, every consumer of that crate gets it. A feature that removes or changes existing behavior will break crates that depend on the baseline behavior the moment a third dependency enables it. Features must only add capability — new trait impls, additional dependencies, optional integrations — never subtract. Mutually exclusive features are an anti-pattern in the Cargo model.

## Bad

```toml
[features]
# "no_std" disables std — enabling it REMOVES behavior
no_std = []

[dependencies]
# and somewhere in lib.rs:
# #[cfg(not(feature = "no_std"))]
# use std::collections::HashMap;
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// lib.rs — toggling off std via a feature is non-additive
#[cfg(not(feature = "no_std"))]
use std::vec::Vec;

#[cfg(feature = "no_std")]
use alloc::vec::Vec;
```

## Good

```toml
[features]
# "std" ADDS std support; no_std is the baseline
default = ["std"]
std = []

# Optional integrations — purely additive
serde = ["dep:serde"]
tokio = ["dep:tokio"]

[dependencies]
serde = { version = "1", optional = true }
tokio = { version = "1", optional = true }
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// lib.rs — std is opt-in, no_std is the default baseline
#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(feature = "std")]
use std::vec::Vec;

#[cfg(not(feature = "std"))]
use alloc::vec::Vec;
```

## Rules for Additive Features

- A feature may add new items, trait impls, or dependencies — never gate-away existing ones.
- If you ship a `no_std` crate, make `std` a feature in `default`, not the other way around.
- Mutually exclusive features (e.g. `backend-a` vs `backend-b`) cannot be enforced by Cargo; emit a compile-time error via `compile_error!` if both are set, and document the limitation clearly.
- Use `dep:` syntax (`dep:serde`) to keep optional dependency names out of the feature namespace.

## Related Rules
- [api-serde-optional](api-serde-optional.md) - gate Serialize/Deserialize behind a feature flag
- [proj-workspace-deps](proj-workspace-deps.md) - use workspace dependency inheritance
- [lint-cfg-check](lint-cfg-check.md) - catch feature-gate typos with unexpected_cfgs
