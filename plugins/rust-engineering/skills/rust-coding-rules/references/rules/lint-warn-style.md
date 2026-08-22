# lint-warn-style

> Enable clippy::style for idiomatic code

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-style-clippy; supporters=`rust-stable`, `rust-cargo-build`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Enable clippy::style for idiomatic code.

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

## Good

Apply the rule only to the demonstrated boundary, preserve the controlling contract, and retain evidence for the changed property.

## Trade-offs

Stricter lint policy catches defects earlier but increases toolchain churn, exception maintenance, and migration work.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Run the configured format and Clippy gate with exact packages, targets, features, and toolchain; separate baseline failures.

## Why It Matters

The `clippy::style` lint group enforces idiomatic Rust patterns. While not bugs, style violations make code harder to read and maintain. Consistent style helps teams work together and makes code easier to review.

## Configuration

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Configuration illustration -->
```rust
// In lib.rs or main.rs
#![warn(clippy::style)]
```

Or in `Cargo.toml`:

```toml
[lints.clippy]
style = "warn"
```

## What It Catches

### Redundant Code

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Redundant Code illustration -->
```rust
// WARN: Redundant clone on Copy type
let x = 5;
let y = x.clone();  // Just use: let y = x;

// WARN: Redundant closure
iter.map(|x| foo(x))  // Just use: iter.map(foo)

// WARN: Redundant pattern matching
match result {
    Ok(x) => Ok(x),
    Err(e) => Err(e),
}  // Just return result
```

### Non-Idiomatic Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Non-Idiomatic Patterns illustration -->
```rust
// WARN: Should use if let
match option {
    Some(x) => do_something(x),
    None => {},
}
// Better: if let Some(x) = option { do_something(x) }

// WARN: Should use or_else
let value = if option.is_some() {
    option.unwrap()
} else {
    default()
};
// Better: option.unwrap_or_else(default)

// WARN: Collapsible if statements
if condition1 {
    if condition2 {
        do_something();
    }
}
// Better: if condition1 && condition2 { do_something() }
```

### Naming Issues

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Naming Issues illustration -->
```rust
// WARN: Function should not start with 'is_' returning non-bool
fn is_valid() -> i32 { 0 }  // Misleading name

// WARN: Method should not be named 'new' without returning Self
impl Foo {
    fn new() -> Bar { Bar }  // Confusing
}
```

## Notable Lints in This Group

| Lint | Better Pattern |
|------|---------------|
| `len_zero` | Use `is_empty()` instead of `len() == 0` |
| `redundant_field_names` | Use shorthand `{ x }` not `{ x: x }` |
| `unused_unit` | Remove `-> ()` and trailing `()` |
| `collapsible_if` | Combine nested ifs with `&&` |
| `single_match` | Use `if let` instead |
| `match_like_matches_macro` | Use `matches!()` macro |
| `needless_return` | Remove explicit `return` at end |
| `question_mark` | Use `?` instead of `match` |

## Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Examples illustration -->
```rust
// Before (style warnings)
fn process(data: Vec<i32>) -> Option<i32> {
    if data.len() == 0 {
        return None;
    }
    let first = match data.first() {
        Some(x) => x,
        None => return None,
    };
    return Some(*first);
}

// After (idiomatic)
fn process(data: Vec<i32>) -> Option<i32> {
    if data.is_empty() {
        return None;
    }
    let first = data.first()?;
    Some(*first)
}
```

## Selective Allowance

Some style lints may conflict with team preferences:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Selective Allowance illustration -->
```rust
// If your team prefers explicit returns
#[allow(clippy::needless_return)]
fn explicit_return() -> i32 {
    return 42;
}
```

## Related Rules
- [lint-warn-suspicious](./lint-warn-suspicious.md) - Suspicious patterns
- [lint-warn-complexity](./lint-warn-complexity.md) - Complexity warnings
- [lint-rustfmt-check](./lint-rustfmt-check.md) - Formatting checks
