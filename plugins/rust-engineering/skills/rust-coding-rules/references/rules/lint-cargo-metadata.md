# lint-cargo-metadata

> Enable clippy::cargo for published crates## Decision

Consider this rule only after its prerequisites are satisfied: Enable clippy::cargo for published crates.

## Apply When

Apply when the repository needs a scoped formatting, lint, warning-level, cfg, or CI policy under its actual toolchain, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a broad lint group or automatic fix would change API, MSRV, semantics, generated code, or unrelated dirty files. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Reproduce the exact lint, classify it, fix semantic causes individually, and use the narrowest documented allow for intentional exceptions.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Bad

Applying the headline as a universal rewrite without proving its premise, prerequisites, and caller-visible effects.

## Good

Apply the rule only to the demonstrated boundary, preserve the controlling contract, and retain evidence for the changed property.

## Trade-offs

Stricter lint policy catches defects earlier but increases toolchain churn, exception maintenance, and migration work.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `serde`, `syn`) must already be accepted by the project or be approved before addition.

## Verification

Run the configured format and Clippy gate with exact packages, targets, features, and toolchain; separate baseline failures.

## Why It Matters

The `clippy::cargo` lint group checks Cargo.toml for issues that affect publishing and dependency management. For crates intended for crates.io, these checks help ensure a professional, well-configured package.

## Configuration

```toml
# Cargo.toml
[lints.clippy]
cargo = "warn"
```

Or in code:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Configuration illustration -->
```rust
#![warn(clippy::cargo)]
```

## What It Catches

### Missing Metadata

```toml
# WARN: missing package.description
# WARN: missing package.license or package.license-file
# WARN: missing package.repository
[package]
name = "my-crate"
version = "0.1.0"
```

### Dependency Issues

```toml
# WARN: feature used but not defined
# WARN: dependency version not specified
[dependencies]
serde = "*"  # Bad: any version
tokio = { git = "..." }  # WARN for published crates
```

### Feature Issues

```toml
# WARN: negative_feature_names
[features]
no-std = []  # Should be: std = [] (opt-out vs opt-in)

# WARN: redundant_feature_names
[features]
default = ["feature-a"]
feature-a = []  # Feature name matches crate name
```

## Notable Lints

| Lint | Issue |
|------|-------|
| `cargo_common_metadata` | Missing description/license/repository |
| `multiple_crate_versions` | Same crate at different versions |
| `negative_feature_names` | Features like `no-std` instead of `std` |
| `redundant_feature_names` | Feature same as crate name |
| `wildcard_dependencies` | Using `*` for version |

## Complete Cargo.toml

```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2021"
rust-version = "1.70"

# Required for cargo lint satisfaction
description = "A short description of what this crate does"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/my-crate"

# Recommended
documentation = "https://docs.rs/my-crate"
readme = "README.md"
keywords = ["keyword1", "keyword2"]
categories = ["category-slug"]

[dependencies]
# Specific versions, not wildcards
serde = "1.0"
tokio = { version = "1.0", features = ["full"] }

[features]
default = ["std"]
std = []  # Opt-out, not no-std opt-in

[lints.clippy]
cargo = "warn"
```

## Multiple Crate Versions

```
# WARN: multiple versions of `syn` in dependency tree
# syn v1.0.109
# syn v2.0.48
```

Fix by updating dependencies or using `[patch]`:

```toml
[patch.crates-io]
old-dep = { git = "...", branch = "syn-2" }
```

## When to Disable

For internal/unpublished crates:

```toml
[lints.clippy]
cargo = "allow"  # Not publishing, metadata not needed
```

Or selectively:

```toml
[lints.clippy]
cargo = "warn"
multiple_crate_versions = "allow"  # Acceptable in this project
```

## Related Rules
- [doc-cargo-metadata](./doc-cargo-metadata.md) - Cargo.toml metadata
- [proj-workspace-deps](./proj-workspace-deps.md) - Workspace dependencies
- [lint-deny-correctness](./lint-deny-correctness.md) - Correctness lints
