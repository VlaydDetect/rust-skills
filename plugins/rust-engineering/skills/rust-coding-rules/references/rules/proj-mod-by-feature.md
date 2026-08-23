# proj-mod-by-feature

> Organize modules by feature, not type## Decision

Use this context-sensitive Rust decision when its premise is established: Organize modules by feature, not type.

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

Feature-based organization keeps related code together, making navigation intuitive and changes localized. Type-based organization (all handlers in one folder, all models in another) scatters related code across the codebase, making features harder to understand and modify.

## Bad

```
src/
├── controllers/
│   ├── user_controller.rs
│   ├── order_controller.rs
│   └── product_controller.rs
├── models/
│   ├── user.rs
│   ├── order.rs
│   └── product.rs
├── services/
│   ├── user_service.rs
│   ├── order_service.rs
│   └── product_service.rs
└── repositories/
    ├── user_repository.rs
    ├── order_repository.rs
    └── product_repository.rs
```

## Good

```
src/
├── user/
│   ├── mod.rs           # Re-exports public items
│   ├── model.rs         # User struct, types
│   ├── repository.rs    # Database operations
│   ├── service.rs       # Business logic
│   └── handler.rs       # HTTP handlers
├── order/
│   ├── mod.rs
│   ├── model.rs
│   ├── repository.rs
│   ├── service.rs
│   └── handler.rs
├── product/
│   ├── mod.rs
│   ├── model.rs
│   ├── repository.rs
│   └── handler.rs
└── lib.rs
```

## Benefits

| Aspect | Type-Based | Feature-Based |
|--------|------------|---------------|
| Finding code | Search across folders | One folder per feature |
| Adding feature | Touch 4+ folders | Create one folder |
| Understanding feature | Jump between folders | Everything in one place |
| Deleting feature | Hunt through codebase | Delete one folder |
| Code ownership | Unclear | Clear feature owners |

## Module Structure

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Module Structure illustration -->
```rust
// src/user/mod.rs
mod model;
mod repository;
mod service;
mod handler;

// Re-export public API
pub use model::{User, UserId, CreateUserRequest};
pub use handler::router;
pub(crate) use service::UserService;
```

## Shared Code

```
src/
├── user/
├── order/
├── shared/              # Cross-cutting concerns
│   ├── mod.rs
│   ├── database.rs      # Connection pool
│   ├── error.rs         # Common error types
│   └── middleware.rs    # Auth, logging
└── lib.rs
```

## When to Flatten

Small modules don't need deep nesting:

```
src/
├── user/
│   ├── mod.rs           # Contains User struct + simple functions
│   └── repository.rs    # Only if complex enough
├── config.rs            # Simple enough for single file
└── lib.rs
```

## Hybrid Approach

For larger features, nest further by concern:

```
src/
├── billing/
│   ├── mod.rs
│   ├── invoice/
│   │   ├── mod.rs
│   │   ├── model.rs
│   │   └── service.rs
│   ├── payment/
│   │   ├── mod.rs
│   │   ├── model.rs
│   │   └── processor.rs
│   └── shared.rs
```

## Related Rules
- [proj-flat-small](./proj-flat-small.md) - Keep small projects flat
- [proj-pub-use-reexport](./proj-pub-use-reexport.md) - Clean public API
- [proj-lib-main-split](./proj-lib-main-split.md) - Lib/main separation
