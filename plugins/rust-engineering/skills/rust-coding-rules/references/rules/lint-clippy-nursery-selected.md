# lint-clippy-nursery-selected

> Enable high-value `clippy::nursery` lints selectively, not the whole group

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-style-clippy; supporters=`rust-stable`, `rust-cargo-build`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Enable high-value `clippy::nursery` lints selectively, not the whole group.

## Apply When

Apply when the repository needs a scoped formatting, lint, warning-level, cfg, or CI policy under its actual toolchain, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a broad lint group or automatic fix would change API, MSRV, semantics, generated code, or unrelated dirty files. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Reproduce the exact lint, classify it, fix semantic causes individually, and use the narrowest documented allow for intentional exceptions.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Stricter lint policy catches defects earlier but increases toolchain churn, exception maintenance, and migration work.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Run the configured format and Clippy gate with exact packages, targets, features, and toolchain; separate baseline failures.

## Why It Matters

The `clippy::nursery` group contains lints that are correct and useful but still being refined — their suggestions may be noisy or have edge cases that haven't been polished yet. Enabling the entire group (`#![warn(clippy::nursery)]`) floods you with false positives and creates churn as nursery lints graduate or change. Cherry-picking individual lints gives you the signal without the noise. Several nursery lints are especially valuable: `significant_drop_tightening` catches lock guards held across `.await` or longer than necessary, `redundant_clone` flags clones that could be moves, and `use_self` keeps type names DRY inside impl blocks.

## Bad

```toml
# Cargo.toml — enables every nursery lint, including noisy ones
[lints.clippy]
nursery = "warn"
```

## Good

```toml
# Cargo.toml — selectively enable high-value nursery lints
[lints.clippy]
# Catches lock/guard held longer than necessary (overlaps with async issues)
significant_drop_tightening = "warn"
# Flags .clone() calls that could be avoided by moving
redundant_clone = "warn"
# Replace TypeName with Self inside impl blocks
use_self = "warn"
# Avoid redundant else after a diverging if
redundant_else = "warn"
# Prefer or_default() over or(Default::default())
or_fun_call = "warn"
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// significant_drop_tightening example — lint fires here:
fn process(state: &Mutex<Vec<u32>>) -> usize {
    let guard = state.lock().unwrap();
    let len = guard.len();
    drop(guard);          // lint suggests dropping earlier, before the return
    expensive_work();
    len
}

// use_self example — lint fires here:
impl MyStruct {
    fn new() -> MyStruct {   // should be -> Self
        MyStruct { value: 0 }
    }
}

// Correct:
impl MyStruct {
    fn new() -> Self {
        Self { value: 0 }
    }
}
```

## Suggested Starter Set

| Lint | What it catches |
|------|----------------|
| `significant_drop_tightening` | Guards/locks held longer than needed |
| `redundant_clone` | `.clone()` where a move suffices |
| `use_self` | Type name repeated inside `impl` block |
| `redundant_else` | `else` after diverging `if` branch |
| `or_fun_call` | `or(Default::default())` → `or_default()` |

Start with this set. Add more only after reviewing what they flag in your codebase.

## Related Rules
- [lint-pedantic-selective](lint-pedantic-selective.md) - same strategy for clippy::pedantic
- [lint-warn-perf](lint-warn-perf.md) - enable the performance lint group
- [anti-lock-across-await](anti-lock-across-await.md) - don't hold locks across `.await`
