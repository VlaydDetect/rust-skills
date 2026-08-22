# doc-panics-section

> Include `# Panics` section for functions that can panic

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-documentation; supporters=`rust-api-design`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Include `# Panics` section for functions that can panic.

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
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Run rustdoc links and doctests under intended features and inspect that examples include their actual prerequisites.

## Why It Matters

Panics are exceptional conditions that crash the program (or unwind the stack). Users need to know when a function might panic so they can ensure preconditions are met or avoid the function in contexts where panics are unacceptable (e.g., `no_std`, embedded, FFI).

If a function can panic, document exactly when.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
/// Returns the element at the given index.
pub fn get(index: usize) -> &T {
    &self.data[index]  // Panics if out of bounds - not documented!
}

/// Divides two numbers.
pub fn divide(a: i32, b: i32) -> i32 {
    a / b  // Panics on division by zero - not documented!
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
/// Returns the element at the given index.
///
/// # Panics
///
/// Panics if `index` is out of bounds (i.e., `index >= self.len()`).
///
/// # Examples
///
/// ```
/// let v = vec![1, 2, 3];
/// assert_eq!(v.get(1), &2);
/// ```
pub fn get(&self, index: usize) -> &T {
    &self.data[index]
}

/// Divides two numbers.
///
/// # Panics
///
/// Panics if `divisor` is zero.
///
/// For a non-panicking version, use [`checked_divide`].
pub fn divide(dividend: i32, divisor: i32) -> i32 {
    dividend / divisor
}

/// Divides two numbers, returning `None` if the divisor is zero.
pub fn checked_divide(dividend: i32, divisor: i32) -> Option<i32> {
    if divisor == 0 {
        None
    } else {
        Some(dividend / divisor)
    }
}
```

## Common Panic Conditions

| Operation | Panic Condition |
|-----------|-----------------|
| Index access `[i]` | Index out of bounds |
| Division `/`, `%` | Division by zero |
| `.unwrap()` | `None` or `Err` value |
| `.expect()` | `None` or `Err` value |
| `slice::split_at(mid)` | `mid > len` |
| `Vec::remove(i)` | `i >= len` |
| Overflow (debug) | Integer overflow |

## Pattern: Panic vs Return Error

Document why you chose to panic vs return `Result`:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Panic vs Return Error illustration -->
```rust
/// Creates a new buffer with the given capacity.
///
/// # Panics
///
/// Panics if `capacity` is zero. A buffer must have at least
/// one byte of capacity.
///
/// This panics rather than returning an error because a zero-capacity
/// buffer represents a programming error, not a runtime condition.
pub fn new(capacity: usize) -> Self {
    assert!(capacity > 0, "capacity must be non-zero");
    // ...
}
```

## Pattern: Debug-Only Panics

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Debug-Only Panics illustration -->
```rust
/// Adds an item to the collection.
///
/// # Panics
///
/// In debug builds, panics if the collection is at capacity.
/// In release builds, this is a no-op when at capacity.
pub fn push(&mut self, item: T) {
    debug_assert!(self.len < self.capacity, "collection at capacity");
    // ...
}
```

## Provide Non-Panicking Alternatives

When documenting a panicking function, point to safe alternatives:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Provide Non-Panicking Alternatives illustration -->
```rust
/// # Panics
///
/// Panics if the index is out of bounds.
///
/// For a non-panicking version, use [`get`] which returns `Option<&T>`.
```

## Related Rules
- [doc-errors-section](./doc-errors-section.md) - Documenting errors
- [doc-safety-section](./doc-safety-section.md) - Documenting unsafe
- [err-result-over-panic](./err-result-over-panic.md) - Preferring Result
