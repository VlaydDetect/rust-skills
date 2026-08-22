# proj-pub-super-parent

> Use pub(super) for parent-only visibility

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-module-layout; supporters=`rust-workspace`, `rust-cargo-build`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use pub(super) for parent-only visibility.

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

`pub(super)` exposes items only to the immediate parent module. This is useful for helper functions and types that submodules share but shouldn't be visible to the rest of the crate.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// src/parser/mod.rs
pub mod lexer;
pub mod ast;

// src/parser/lexer.rs
pub fn internal_helper() {  // Visible to entire crate!
    // Helper only needed by lexer and ast
}

pub(crate) struct Token {  // Visible to entire crate
    // Only parser submodules need this
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// src/parser/mod.rs
pub mod lexer;
pub mod ast;

// Shared types for parser submodules only
pub(super) struct Token {
    pub(super) kind: TokenKind,
    pub(super) span: Span,
}

pub(super) fn shared_helper() -> Token {
    // Only visible in parser/*
}

// src/parser/lexer.rs
use super::{Token, shared_helper};

pub fn lex(input: &str) -> Vec<Token> {
    shared_helper();
    // ...
}

// src/parser/ast.rs
use super::Token;

pub fn parse(tokens: Vec<Token>) -> Ast {
    // ...
}
```

## Visibility Hierarchy

```
src/
├── lib.rs           # crate root
├── parser/
│   ├── mod.rs       # pub(super) items visible here
│   ├── lexer.rs     # can use pub(super) from mod.rs
│   └── ast.rs       # can use pub(super) from mod.rs
└── codegen.rs       # CANNOT see pub(super) parser items
```

## Pattern: Layered Visibility

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Layered Visibility illustration -->
```rust
// src/database/mod.rs
mod connection;
mod query;
mod pool;

// Only this module's children can see
pub(super) struct RawConnection { /* ... */ }

// Entire crate can see
pub(crate) struct Pool { /* ... */ }

// Everyone can see
pub struct Database { /* ... */ }
```

## Pattern: Test Helpers

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Test Helpers illustration -->
```rust
// src/parser/mod.rs
mod lexer;
mod ast;

#[cfg(test)]
mod tests {
    use super::*;
    
    // Test helper visible only to parser module's tests
    pub(super) fn make_test_token() -> Token {
        Token { kind: TokenKind::Test, span: Span::dummy() }
    }
}

// src/parser/lexer.rs
#[cfg(test)]
mod tests {
    use super::super::tests::make_test_token;
    // ...
}
```

## Comparison

| Visibility | Scope | Use Case |
|------------|-------|----------|
| `pub` | Everywhere | Public API |
| `pub(crate)` | Crate-wide | Internal shared utilities |
| `pub(super)` | Parent module | Submodule helpers |
| `pub(in path)` | Specific path | Precise control |
| (private) | Current module | Implementation details |

## When to Use pub(super)

- Helper functions shared between sibling modules
- Types used by submodules but not the rest of crate
- Implementation details of a module group
- Test utilities for a module tree

## Related Rules
- [proj-pub-crate-internal](./proj-pub-crate-internal.md) - Crate visibility
- [proj-pub-use-reexport](./proj-pub-use-reexport.md) - Re-export patterns
- [proj-mod-by-feature](./proj-mod-by-feature.md) - Feature organization
