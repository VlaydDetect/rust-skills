# api-serde-optional

> Make serde a feature flag, not a hard dependency for library crates

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-traits`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Make serde a feature flag, not a hard dependency for library crates.

## Apply When

Apply when a public or independently evolving caller contract needs an ownership, construction, extension, or compatibility decision, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the abstraction has only one local use or would expose implementation and dependency details without caller value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Write representative caller examples, minimize public surface, and review ownership, errors, extension rights, and compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

More flexibility can improve call sites while increasing inference, monomorphization, compatibility, and maintenance obligations.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`serde_json`, `serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile downstream-style examples and check docs, public paths, feature behavior, and the declared compatibility baseline.

## Why It Matters

Not all users of your library need serialization. Making serde a required dependency adds compile time and binary size for everyone. Feature flags let users opt-in to serde support only when needed, following Rust's philosophy of zero-cost abstractions and minimal dependencies.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Cargo.toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }

// lib.rs
use serde::{Serialize, Deserialize};

// Every user pays for serde, even if they don't need it
#[derive(Serialize, Deserialize)]
pub struct Config {
    pub name: String,
    pub value: i32,
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Cargo.toml
[dependencies]
serde = { version = "1.0", features = ["derive"], optional = true }

[features]
default = []
serde = ["dep:serde"]

// lib.rs
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Config {
    pub name: String,
    pub value: i32,
}

// Users opt-in:
// my_crate = { version = "1.0", features = ["serde"] }
```

## Macro Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Macro Pattern illustration -->
```rust
// Reusable macro for serde derives
#[cfg(feature = "serde")]
macro_rules! impl_serde {
    ($($t:ty),*) => {
        $(
            impl serde::Serialize for $t {
                // ...
            }
            impl<'de> serde::Deserialize<'de> for $t {
                // ...
            }
        )*
    };
}

#[cfg(not(feature = "serde"))]
macro_rules! impl_serde {
    ($($t:ty),*) => {};
}

// Or use cfg_attr for derived impls
#[derive(Debug, Clone)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Point {
    pub x: f64,
    pub y: f64,
}
```

## Feature Documentation

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Feature Documentation illustration -->
```rust
// lib.rs

//! # Features
//!
//! - `serde`: Enables `Serialize` and `Deserialize` implementations for all types.
//!
//! # Example with serde
//!
//! ```toml
//! [dependencies]
//! my_crate = { version = "1.0", features = ["serde"] }
//! ```

#![cfg_attr(docsrs, feature(doc_cfg))]

/// A configuration type.
/// 
/// When the `serde` feature is enabled, this type implements
/// `Serialize` and `Deserialize`.
#[derive(Debug, Clone)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(docsrs, doc(cfg(feature = "serde")))]
pub struct Config {
    pub name: String,
}
```

## Multiple Optional Dependencies

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Multiple Optional Dependencies illustration -->
```rust
// Cargo.toml
[dependencies]
serde = { version = "1.0", features = ["derive"], optional = true }
rkyv = { version = "0.7", optional = true }
borsh = { version = "0.10", optional = true }

[features]
default = []
serde = ["dep:serde"]
rkyv = ["dep:rkyv"]
borsh = ["dep:borsh"]

// lib.rs
#[derive(Debug, Clone)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "rkyv", derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize))]
#[cfg_attr(feature = "borsh", derive(borsh::BorshSerialize, borsh::BorshDeserialize))]
pub struct Message {
    pub id: u64,
    pub content: String,
}
```

## Testing with Features

```bash
# Test without serde
cargo test

# Test with serde
cargo test --features serde

# Test all feature combinations
cargo test --all-features
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Testing with Features illustration -->
```rust
// Test serde round-trip when feature enabled
#[cfg(feature = "serde")]
#[test]
fn test_serde_roundtrip() {
    let config = Config { name: "test".into() };
    let json = serde_json::to_string(&config).unwrap();
    let parsed: Config = serde_json::from_str(&json).unwrap();
    assert_eq!(config, parsed);
}
```

## When to Make Serde Required

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Make Serde Required illustration -->
```rust
// ✅ Required: Library is about serialization
// (e.g., json-schema, config-file parser)
[dependencies]
serde = "1.0"

// ✅ Required: Domain heavily uses serde
// (e.g., API client, data format library)

// ❌ Optional: General-purpose utility library
// ❌ Optional: Math/algorithm library
// ❌ Optional: Most libraries!
```

## Related Rules
- [proj-lib-main-split](./proj-lib-main-split.md) - Library structure
- [api-common-traits](./api-common-traits.md) - Core trait implementations
- [lint-deny-correctness](./lint-deny-correctness.md) - Feature testing
- [serde-try-from-validate](./serde-try-from-validate.md) - Validate while deserializing
- [serde-rename-all](./serde-rename-all.md) - Match external naming conventions
