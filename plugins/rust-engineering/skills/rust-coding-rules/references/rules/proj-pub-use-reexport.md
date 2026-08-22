# proj-pub-use-reexport

> Use pub use for clean public API

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-module-layout; supporters=`rust-workspace`, `rust-cargo-build`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use pub use for clean public API.

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
- External crates referenced by the source (`serde`, `bytes`) must already be accepted by the project or be approved before addition.

## Verification

Inspect cargo metadata and public paths, then compile affected packages, features, targets, docs, tests, and generated boundaries.

## Why It Matters

`pub use` re-exports items from submodules at the current module level. This creates a flat, ergonomic public API while keeping internal organization flexible. Users import from one place; you can reorganize internals without breaking their code.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// lib.rs - Deep module paths exposed
pub mod error;
pub mod config;
pub mod client;
pub mod types;

// Users must write:
use my_crate::error::MyError;
use my_crate::config::Config;
use my_crate::client::http::HttpClient;
use my_crate::types::request::Request;
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// lib.rs - Flat public API
mod error;
mod config;
mod client;
mod types;

pub use error::MyError;
pub use config::Config;
pub use client::http::HttpClient;
pub use types::request::Request;

// Users write:
use my_crate::{Config, HttpClient, MyError, Request};
```

## Pattern: Selective Re-export

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Selective Re-export illustration -->
```rust
// src/lib.rs
mod internal;

// Only re-export what users need
pub use internal::{
    PublicStruct,
    PublicTrait,
    public_function,
};

// Keep implementation details hidden
// internal::helper_function is NOT exported
```

## Pattern: Rename on Re-export

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Rename on Re-export illustration -->
```rust
mod v1 {
    pub struct Client { /* old implementation */ }
}

mod v2 {
    pub struct Client { /* new implementation */ }
}

// Re-export with clear names
pub use v2::Client;
pub use v1::Client as LegacyClient;
```

## Pattern: Prelude Module

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Prelude Module illustration -->
```rust
// src/lib.rs
pub mod prelude {
    pub use crate::{
        Config,
        Client,
        Error,
        Request,
        Response,
    };
}

// Users can glob import common items
use my_crate::prelude::*;
```

## Pattern: Feature-Gated Re-exports

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Feature-Gated Re-exports illustration -->
```rust
// src/lib.rs
mod core;
mod serde_impl;
mod async_impl;

pub use core::*;

#[cfg(feature = "serde")]
pub use serde_impl::*;

#[cfg(feature = "async")]
pub use async_impl::*;
```

## Comparison: Module Structure vs Public API

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Comparison: Module Structure vs Public API illustration -->
```rust
// Internal structure (complex)
src/
├── transport/
│   ├── http/
│   │   └── client.rs    // HttpClient
│   └── grpc/
│       └── client.rs    // GrpcClient
├── auth/
│   └── token.rs         // Token
└── lib.rs

// Public API (flat)
pub use transport::http::client::HttpClient;
pub use transport::grpc::client::GrpcClient;
pub use auth::token::Token;

// Users see:
my_crate::HttpClient
my_crate::GrpcClient
my_crate::Token
```

## Re-export External Types

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Re-export External Types illustration -->
```rust
// Re-export dependencies users will need
pub use bytes::Bytes;
pub use http::{Method, StatusCode};

// Now users don't need to depend on these crates directly
```

## Glob Re-exports

Use sparingly:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Glob Re-exports illustration -->
```rust
// OK for internal modules
pub use internal::*;

// Careful with external crates - pollutes namespace
pub use serde::*;  // Usually too broad
```

## Related Rules
- [proj-prelude-module](./proj-prelude-module.md) - Prelude pattern
- [proj-pub-crate-internal](./proj-pub-crate-internal.md) - Internal visibility
- [api-non-exhaustive](./api-non-exhaustive.md) - API stability
