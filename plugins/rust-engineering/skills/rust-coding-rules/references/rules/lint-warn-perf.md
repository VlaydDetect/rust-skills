# lint-warn-perf

> Enable clippy::perf for performance improvements## Decision

Use this context-sensitive Rust decision when its premise is established: Enable clippy::perf for performance improvements.

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

The `clippy::perf` lint group catches performance anti-patterns—inefficient allocations, unnecessary copies, suboptimal API usage. While not all performance issues are critical, avoiding obvious inefficiencies is good practice.

## Configuration

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Configuration illustration -->
```rust
// In lib.rs or main.rs
#![warn(clippy::perf)]
```

Or in `Cargo.toml`:

```toml
[lints.clippy]
perf = "warn"
```

## What It Catches

### Unnecessary Allocations

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Unnecessary Allocations illustration -->
```rust
// WARN: Unnecessary to_string before into
fn take_string(s: impl Into<String>) { }
take_string("hello".to_string());  // Just use: "hello"

// WARN: Box::new in return with deref coercion
fn make_trait() -> Box<dyn Trait> {
    Box::new(concrete)  // Could use Into
}

// WARN: Unnecessary vec! for iteration
for x in vec![1, 2, 3] { }  // Use array: [1, 2, 3]
```

### Inefficient Operations

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Inefficient Operations illustration -->
```rust
// WARN: Single-character string patterns
s.starts_with("x")  // Use char: 'x'
s.contains("a")     // Use char: 'a'

// WARN: iter().nth(0) instead of first()
iter.nth(0)  // Use: iter.first() or iter.next()

// WARN: Manual saturating arithmetic
if x > i32::MAX - y { i32::MAX } else { x + y }
// Use: x.saturating_add(y)
```

### Collection Inefficiencies

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Collection Inefficiencies illustration -->
```rust
// WARN: extend with a single element
vec.extend(std::iter::once(item));  // Use: vec.push(item)

// WARN: Inefficient to_vec
slice.iter().cloned().collect::<Vec<_>>()  // Use: slice.to_vec()

// WARN: Manual string concatenation
let s = format!("{}{}", a, b);  // When both are &str, use: a.to_owned() + b
```

## Notable Lints in This Group

| Lint | Improvement |
|------|-------------|
| `box_collection` | Use `Vec<T>` not `Box<Vec<T>>` |
| `iter_nth` | Use `.get(n)` or `.next()` |
| `large_enum_variant` | Box large variants |
| `manual_memcpy` | Use slice copy methods |
| `redundant_allocation` | Remove double boxing |
| `single_char_pattern` | Use `char` not `&str` |
| `slow_vector_initialization` | Use `vec![0; n]` |
| `unnecessary_to_owned` | Remove redundant `.to_owned()` |

## Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Examples illustration -->
```rust
// Before (perf warnings)
fn process(input: &str) -> String {
    let parts: Vec<_> = input.split(",").collect();
    let mut result = String::new();
    for part in parts.iter() {
        if part.starts_with(" ") {
            result = result + &part.trim().to_string();
        }
    }
    result
}

// After (optimized)
fn process(input: &str) -> String {
    input.split(',')
        .filter(|part| part.starts_with(' '))
        .map(str::trim)
        .collect()
}
```

## Allocation Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Allocation Patterns illustration -->
```rust
// Unnecessary allocation
let vec: Vec<i32> = vec![];  // Creates capacity
let vec: Vec<i32> = Vec::new();  // No allocation

// Pre-allocation
let mut vec = Vec::with_capacity(100);  // One allocation
for i in 0..100 {
    vec.push(i);  // No reallocation
}
```

## String Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the String Patterns illustration -->
```rust
// Slow: str pattern
s.contains("x");
s.find("y");

// Fast: char pattern
s.contains('x');
s.find('y');
```

## Related Rules
- [lint-warn-complexity](./lint-warn-complexity.md) - Complexity warnings
- [mem-with-capacity](./mem-with-capacity.md) - Pre-allocation
- [perf-profile-first](./perf-profile-first.md) - Profile before optimizing
