# proj-flat-small

> Keep small projects flat## Decision

Use this context-sensitive Rust decision when its premise is established: Keep small projects flat.

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

Over-organizing small projects adds navigation overhead without benefit. A project with 5-10 files doesn't need nested directories. Start flat, add structure only when complexity demands it.

## Bad

```
src/
├── core/
│   └── mod.rs           # Just re-exports
├── domain/
│   ├── mod.rs
│   └── models/
│       ├── mod.rs
│       └── user.rs      # 50 lines
├── infrastructure/
│   ├── mod.rs
│   └── database/
│       ├── mod.rs
│       └── connection.rs # 30 lines
├── application/
│   ├── mod.rs
│   └── services/
│       └── mod.rs       # Empty
└── main.rs
```

## Good

```
src/
├── main.rs
├── lib.rs
├── config.rs
├── database.rs
├── user.rs
└── error.rs
```

## When to Add Structure

| File Count | Structure |
|------------|-----------|
| < 10 files | Flat in `src/` |
| 10-20 files | Group by feature |
| 20+ files | Feature folders with submodules |

## Progressive Structuring

### Stage 1: Flat

```
src/
├── main.rs
├── config.rs
├── user.rs
└── database.rs
```

### Stage 2: Logical Groups

```
src/
├── main.rs
├── config.rs
├── user.rs
├── order.rs        # Getting bigger
├── order_item.rs   # Related to order
└── database.rs
```

### Stage 3: Feature Folders

```
src/
├── main.rs
├── config.rs
├── user.rs
├── order/          # Now complex enough
│   ├── mod.rs
│   ├── model.rs
│   └── item.rs
└── database.rs
```

## Signs You Need More Structure

- Files exceed 300-500 lines
- Related files are hard to identify
- You're adding `_` prefixes for grouping (`user_model.rs`, `user_service.rs`)
- New team members get lost
- Same concepts repeated in file names

## Signs of Over-Structure

- Folders with 1-2 files
- `mod.rs` files that only re-export
- Deep nesting for simple concepts
- More lines in module declarations than code

## Example: CLI Tool

```
src/
├── main.rs         # Argument parsing, entry point
├── commands.rs     # CLI subcommands
├── config.rs       # Configuration loading
└── output.rs       # Formatting, printing
```

Not:

```
src/
├── cli/
│   └── commands/
│       └── mod.rs
├── config/
│   └── mod.rs
└── presentation/
    └── output/
        └── mod.rs
```

## Related Rules
- [proj-mod-by-feature](./proj-mod-by-feature.md) - Feature organization
- [proj-lib-main-split](./proj-lib-main-split.md) - Lib/main separation
- [proj-mod-rs-dir](./proj-mod-rs-dir.md) - Multi-file modules
