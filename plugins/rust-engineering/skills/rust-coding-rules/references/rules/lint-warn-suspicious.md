# lint-warn-suspicious

> Enable clippy::suspicious for likely bugs

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-style-clippy; supporters=`rust-stable`, `rust-cargo-build`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Enable clippy::suspicious for likely bugs.

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

The `clippy::suspicious` lint group catches code patterns that are syntactically valid but almost always wrong. These are potential bugs that deserve investigation. Enabling this group as a warning helps catch mistakes early.

## Configuration

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Configuration illustration -->
```rust
// In lib.rs or main.rs
#![warn(clippy::suspicious)]
```

Or in `Cargo.toml`:

```toml
[lints.clippy]
suspicious = "warn"
```

Or in `clippy.toml`:

```toml
warn = ["clippy::suspicious"]
```

## What It Catches

### Suspicious Arithmetic

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Suspicious Arithmetic illustration -->
```rust
// WARN: Suspicious use of + in a << expression
let bits = 1 << 4 + 1;  // Probably meant (1 << 4) + 1 or 1 << (4 + 1)

// WARN: Suspicious use of | in a + expression
let value = x | 1 + y;  // Probably meant (x | 1) + y or x | (1 + y)
```

### Suspicious Comparisons

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Suspicious Comparisons illustration -->
```rust
// WARN: Almost swapped operands in a comparison
if 5 < x && x < 3 { }  // Impossible condition

// WARN: Suspicious assignment in a condition
if (x = 5) { }  // Probably meant x == 5
```

### Suspicious Method Calls

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Suspicious Method Calls illustration -->
```rust
// WARN: Suspicious map usage
let _: Vec<_> = vec.iter().map(|x| { 
    println!("{}", x);  // Side effect in map
    x
}).collect();  // Use for_each instead

// WARN: Suspicious string formatting
let s = format!("{}", format!("{}", x));  // Redundant nested format
```

### Suspicious Casts

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Suspicious Casts illustration -->
```rust
// WARN: Suspicious use of not on a bool
let inverted = !x as i32;  // Did you mean (!x) as i32 or !(x as i32)?

// WARN: Cast of float to int may lose precision
let n = 3.14_f64 as i32;  // May want .round() first
```

## Notable Lints in This Group

| Lint | Description |
|------|-------------|
| `suspicious_arithmetic_impl` | Unusual operator in arithmetic trait |
| `suspicious_assignment_formatting` | Looks like typo in assignment |
| `suspicious_else_formatting` | Else on wrong line |
| `suspicious_map` | Map with side effects |
| `suspicious_op_assign_impl` | Unusual op-assign implementation |
| `suspicious_splitn` | splitn that can't produce n parts |
| `suspicious_unary_op_formatting` | Confusing unary operator spacing |

## Example Catches

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Example Catches illustration -->
```rust
// Caught: Suspicious double negation
let value = --x;  // In Rust, this is -(-x), not pre-decrement

// Caught: Suspicious modulo
let remainder = x % 1;  // Always 0 for integers

// Caught: Suspicious else formatting
if condition {
    do_something();
}
else {  // Weird formatting, might be a mistake
    do_other();
}
```

## When to Allow

Rarely. If you need to suppress, document why:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Allow illustration -->
```rust
#[allow(clippy::suspicious_arithmetic_impl)]
impl Mul for Matrix {
    // Custom matrix multiplication using + for reduction step
    fn mul(self, rhs: Self) -> Self::Output {
        // ...
    }
}
```

## Related Rules
- [lint-deny-correctness](./lint-deny-correctness.md) - Deny definite bugs
- [lint-warn-style](./lint-warn-style.md) - Style warnings
- [lint-warn-complexity](./lint-warn-complexity.md) - Complexity warnings
