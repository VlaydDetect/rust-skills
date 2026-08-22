# doc-module-inner

> Use `//!` for module-level documentation

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-documentation; supporters=`rust-api-design`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `//!` for module-level documentation.

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
- External crates referenced by the source (`serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Run rustdoc links and doctests under intended features and inspect that examples include their actual prerequisites.

## Why It Matters

Inner doc comments (`//!`) document the module itself, not the next item. They appear at the top of module files and describe the module's purpose, contents, and usage patterns. This helps users understand what a module provides before diving into individual items.

Module docs are the first thing users see in `cargo doc` when navigating to a module.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// This module handles authentication
// It provides JWT and session-based auth

mod auth;

pub use auth::*;
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// auth.rs
/// Authentication utilities  // Wrong: this documents nothing useful
use std::collections::HashMap;

pub struct Session { /* ... */ }
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
//! Authentication and authorization utilities.
//!
//! This module provides multiple authentication strategies:
//!
//! - [`JwtAuth`] - JSON Web Token based authentication
//! - [`SessionAuth`] - Cookie-based session authentication
//! - [`ApiKeyAuth`] - API key authentication for services
//!
//! # Examples
//!
//! ```
//! use my_crate::auth::{JwtAuth, Authenticator};
//!
//! let auth = JwtAuth::new("secret-key");
//! let token = auth.generate_token(&user)?;
//! ```
//!
//! # Feature Flags
//!
//! - `jwt` - Enables JWT authentication (enabled by default)
//! - `sessions` - Enables session-based authentication

use std::collections::HashMap;

pub struct Session { /* ... */ }
```

## Where to Use Inner Docs

| Location | Purpose |
|----------|---------|
| `lib.rs` | Crate-level documentation (appears on crate root) |
| `mod.rs` | Module documentation for directory modules |
| `module.rs` | Module documentation for single-file modules |

## Crate Root Example

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Crate Root Example illustration -->
```rust
//! # My Awesome Crate
//!
//! `my_crate` provides utilities for handling complex workflows.
//!
//! ## Quick Start
//!
//! ```rust
//! use my_crate::prelude::*;
//!
//! let workflow = Workflow::builder()
//!     .add_step(Step::new("fetch"))
//!     .add_step(Step::new("process"))
//!     .build();
//! ```
//!
//! ## Modules
//!
//! - [`workflow`] - Core workflow engine
//! - [`steps`] - Built-in workflow steps
//! - [`prelude`] - Common imports
//!
//! ## Feature Flags
//!
//! | Feature | Description |
//! |---------|-------------|
//! | `async` | Async workflow execution |
//! | `serde` | Serialization support |

pub mod workflow;
pub mod steps;
pub mod prelude;
```

## Key Sections for Module Docs

1. **Brief description** - One-line summary
2. **Overview** - What the module provides
3. **Examples** - How to use it
4. **Feature flags** - Optional functionality
5. **See Also** - Related modules

## Related Rules
- [doc-all-public](./doc-all-public.md) - Documenting public items
- [doc-examples-section](./doc-examples-section.md) - Adding examples
- [doc-cargo-metadata](./doc-cargo-metadata.md) - Crate metadata
