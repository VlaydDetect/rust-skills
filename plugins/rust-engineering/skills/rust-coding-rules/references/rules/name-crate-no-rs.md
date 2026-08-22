# name-crate-no-rs

> Don't suffix crate names with `-rs` or `-rust`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-style-clippy; supporters=`rust-api-design`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Don't suffix crate names with `-rs` or `-rust`.

## Apply When

Apply when an identifier is part of a Rust caller contract or repository convention and its name communicates cost, ownership, state, or behavior, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a rename would create compatibility churn without improving meaning or merely enforces taste already handled by tooling. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Classify the item and semantic operation, follow Rust convention and local vocabulary, then check public-path compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Conventional names improve discoverability but public renames can impose migration and deprecation costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile callers and docs, run configured naming lints, and perform compatibility analysis for public renames.

## Why It Matters

Adding `-rs` or `-rust` to crate names is redundant—you're already on crates.io, it's obviously Rust. These suffixes waste characters, clutter the namespace, and can make crate names harder to type. The Rust community discourages this pattern.

## Bad

```toml
# Cargo.toml
[package]
name = "json-parser-rs"    # Redundant -rs
name = "my-lib-rust"       # Redundant -rust
name = "http-client-rs"    # We know it's Rust
name = "rust-sqlite"       # rust- prefix equally bad
```

## Good

```toml
# Cargo.toml
[package]
name = "json-parser"
name = "my-lib"
name = "http-client"
name = "sqlite-wrapper"

# Real crate examples (no -rs):
# serde (not serde-rs)
# tokio (not tokio-rs)
# reqwest (not reqwest-rs)
# clap (not clap-rs)
```

## When Context Is Needed

```toml
# If you're porting a library from another language:
name = "python-ast"        # Describes what it's for, not what it's written in

# If you're providing bindings:
name = "openssl"           # The Rust crate IS the Rust interface

# Platform-specific:
name = "windows-sys"       # Platform, not language
```

## Repository Naming

```
# GitHub repos don't need -rs either
github.com/user/my-library      # Good
github.com/user/my-library-rs   # Unnecessary

# Though some do for disambiguation from other language versions
github.com/rust-lang/rust       # The rust repo itself uses "rust"
```

## Exceptions

```toml
# Rare cases where disambiguation matters:
# - If there's a widely-known non-Rust project with the same name
# - Official Rust project repositories (rust-lang org)

# But even then, consider alternatives:
name = "fancy-lib"           # Instead of fancy-rs
name = "better-json"         # Instead of json-rust
name = "my-serde-impl"       # Instead of serde-rs-fork
```

## Related Rules
- [proj-workspace-deps](./proj-workspace-deps.md) - Cargo configuration
- [doc-cargo-metadata](./doc-cargo-metadata.md) - Package metadata
- [name-funcs-snake](./name-funcs-snake.md) - Naming conventions
