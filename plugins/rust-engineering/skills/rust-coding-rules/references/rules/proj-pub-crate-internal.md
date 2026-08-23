# proj-pub-crate-internal

> Use pub(crate) for internal APIs## Decision

Use this context-sensitive Rust decision when its premise is established: Use pub(crate) for internal APIs.

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

## Verification

Inspect cargo metadata and public paths, then compile affected packages, features, targets, docs, tests, and generated boundaries.

## Why It Matters

`pub(crate)` exposes items within the crate but hides them from external users. This creates clear boundaries between public API and internal implementation, preventing accidental breakage and reducing public API surface.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Everything public - users depend on internals
pub mod internal {
    pub struct InternalState {
        pub buffer: Vec<u8>,    // Implementation detail exposed
        pub dirty: bool,
    }
    
    pub fn process_internal(state: &mut InternalState) {
        // Users can call this, creating coupling
    }
}

pub struct Widget {
    pub state: internal::InternalState,  // Exposed!
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Internal module with crate visibility
pub(crate) mod internal {
    pub(crate) struct InternalState {
        pub(crate) buffer: Vec<u8>,
        pub(crate) dirty: bool,
    }
    
    pub(crate) fn process_internal(state: &mut InternalState) {
        // Only callable within crate
    }
}

pub struct Widget {
    state: internal::InternalState,  // Private field
}

impl Widget {
    pub fn new() -> Self {
        Self {
            state: internal::InternalState {
                buffer: Vec::new(),
                dirty: false,
            }
        }
    }
    
    pub fn do_something(&mut self) {
        internal::process_internal(&mut self.state);
    }
}
```

## Visibility Levels

| Visibility | Accessible From |
|------------|-----------------|
| `pub` | Everywhere |
| `pub(crate)` | Current crate only |
| `pub(super)` | Parent module only |
| `pub(in path)` | Specific module path |
| (private) | Current module only |

## Pattern: Internal Module

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Internal Module illustration -->
```rust
// src/lib.rs
mod internal;  // Private module
pub mod api;   // Public API

// src/internal.rs
pub(crate) struct Helper;
pub(crate) fn helper_function() -> Helper { Helper }

// src/api.rs
use crate::internal::{Helper, helper_function};

pub struct PublicType {
    helper: Helper,  // Uses internal type, but field is private
}
```

## Pattern: Test Visibility

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Test Visibility illustration -->
```rust
pub struct Parser {
    // Private implementation
    state: ParserState,
}

// Expose for testing but not public API
#[cfg(test)]
pub(crate) fn debug_state(&self) -> &ParserState {
    &self.state
}

// Or use a dedicated test helper
#[doc(hidden)]
pub mod __test_helpers {
    pub use super::ParserState;
}
```

## Pattern: Feature Module Internals

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Feature Module Internals illustration -->
```rust
// src/user/mod.rs
mod repository;  // Private
mod service;     // Private

pub use service::UserService;  // Only export the public API

// repository and service are pub(crate) internally
// so other modules in crate can use them if needed
```

## Benefits

| Approach | API Stability | Flexibility |
|----------|---------------|-------------|
| All `pub` | Any change breaks users | None |
| `pub(crate)` internals | Only `pub` items matter | Can refactor freely |
| Private | Maximum encapsulation | Limits crate flexibility |

## Related Rules
- [proj-pub-super-parent](./proj-pub-super-parent.md) - Parent-only visibility
- [proj-pub-use-reexport](./proj-pub-use-reexport.md) - Clean re-exports
- [api-non-exhaustive](./api-non-exhaustive.md) - Future-proof structs
