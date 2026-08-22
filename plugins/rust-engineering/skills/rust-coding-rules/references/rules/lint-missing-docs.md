# lint-missing-docs

> Warn on missing documentation for public items

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-style-clippy; supporters=`rust-stable`, `rust-cargo-build`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Warn on missing documentation for public items.

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

## Trade-offs

Stricter lint policy catches defects earlier but increases toolchain churn, exception maintenance, and migration work.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Run the configured format and Clippy gate with exact packages, targets, features, and toolchain; separate baseline failures.

## Why It Matters

The `missing_docs` lint ensures all public API items are documented. For libraries, documentation IS the user interface. Missing docs mean users can't understand your API without reading source code.

## Configuration

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Configuration illustration -->
```rust
// In lib.rs
#![warn(missing_docs)]
```

Or in `Cargo.toml`:

```toml
[lints.rust]
missing_docs = "warn"
```

For strict enforcement:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Configuration illustration -->
```rust
#![deny(missing_docs)]
```

## What It Catches

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the What It Catches illustration -->
```rust
#![warn(missing_docs)]

pub struct User {  // WARN: missing documentation for a struct
    pub name: String,  // WARN: missing documentation for a field
    pub age: u32,      // WARN: missing documentation for a field
}

pub fn process() { }  // WARN: missing documentation for a function

pub trait Handler {  // WARN: missing documentation for a trait
    fn handle(&self);  // WARN: missing documentation for a method
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#![warn(missing_docs)]

//! User management module.

/// Represents a registered user in the system.
pub struct User {
    /// The user's display name.
    pub name: String,
    /// The user's age in years.
    pub age: u32,
}

/// Processes pending user requests.
///
/// # Examples
///
/// ```
/// process();
/// ```
pub fn process() { }

/// Handler trait for request processing.
pub trait Handler {
    /// Handle an incoming request.
    fn handle(&self);
}
```

## Private Items

`missing_docs` only applies to `pub` items. Private items don't trigger warnings:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Private Items illustration -->
```rust
#![warn(missing_docs)]

struct Internal { }  // No warning - private

pub struct Public { }  // WARN - public, needs docs
```

## Allow for Specific Items

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Allow for Specific Items illustration -->
```rust
#![warn(missing_docs)]

/// Documented module.
pub mod api {
    /// Documented struct.
    pub struct Config { }
    
    #[allow(missing_docs)]
    pub mod internal {
        // Internal API, docs not required
        pub struct Helper { }
    }
}
```

## Gradual Adoption

For existing codebases, start with `warn` and fix incrementally:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Gradual Adoption illustration -->
```rust
// Phase 1: Warn, fix critical items
#![warn(missing_docs)]

// Phase 2: After cleanup, deny
#![deny(missing_docs)]
```

## Combining with doc Attributes

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Combining with doc Attributes illustration -->
```rust
#![warn(missing_docs)]
#![warn(rustdoc::broken_intra_doc_links)]
#![warn(rustdoc::private_intra_doc_links)]
```

## Workspace Configuration

```toml
# In workspace Cargo.toml
[workspace.lints.rust]
missing_docs = "warn"

# Member crates inherit
[lints]
workspace = true
```

## What to Document

| Item | Doc Focus |
|------|-----------|
| Structs | Purpose, usage example |
| Struct fields | What it represents |
| Enums | When to use each variant |
| Functions | What it does, params, return |
| Traits | Contract and expectations |
| Modules | What the module provides |

## Related Rules
- [doc-all-public](./doc-all-public.md) - Documentation patterns
- [lint-unsafe-doc](./lint-unsafe-doc.md) - Unsafe documentation
- [doc-examples-section](./doc-examples-section.md) - Adding examples
