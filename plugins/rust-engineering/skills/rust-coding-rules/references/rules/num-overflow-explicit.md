# num-overflow-explicit

> Handle integer overflow explicitly: `checked_`/`saturating_`/`wrapping_`/`overflowing_`## Decision

Use this context-sensitive Rust decision when its premise is established: Handle integer overflow explicitly: `checked_`/`saturating_`/`wrapping_`/`overflowing_`.

## Apply When

Apply when range, overflow, narrowing, floating-point semantics, ordering, or a numeric invariant is part of the contract, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the selected behavior would silently change domain semantics or add a representation optimization without measured need. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. State the valid domain and choose checked, saturating, wrapping, overflowing, tolerant, or total-order behavior explicitly.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Stronger numeric types and checks prevent invalid states but can add conversion, API, storage, and compatibility costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Test minimum, maximum, zero, invalid conversion, NaN or infinity, and boundary behavior relevant to the domain.

## Why It Matters

Integer overflow panics in debug builds and silently wraps (two's complement) in release builds. Relying on either default behavior is a latent bug — the release build can produce wrong results without any diagnostic. Choosing an explicit variant makes intent unmistakable to both the compiler and future readers.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn add_score(current: u32, delta: u32) -> u32 {
    current + delta  // panics in debug, wraps silently in release
}

fn increment_counter(c: u8) -> u8 {
    c + 1  // wraps to 0 in release when c == 255
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// checked_add: returns None on overflow — propagate or handle the error
fn add_score(current: u32, delta: u32) -> Option<u32> {
    current.checked_add(delta)
}

// saturating_add: clamps at the type's upper bound (u8::MAX == 255)
fn increment_saturating(c: u8) -> u8 {
    c.saturating_add(1)
}

// wrapping_add: intentional modular (two's complement) arithmetic
fn wrapping_sequence(n: u8) -> u8 {
    n.wrapping_add(1)
}

// overflowing_add: returns (result, did_overflow) — useful for carry detection
fn add_with_carry(a: u32, b: u32) -> (u32, bool) {
    a.overflowing_add(b)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn checked_returns_none_on_overflow() {
        assert_eq!(add_score(u32::MAX, 1), None);
        assert_eq!(add_score(10, 5), Some(15));
    }

    #[test]
    fn saturating_clamps_at_max() {
        assert_eq!(increment_saturating(255), 255);
        assert_eq!(increment_saturating(10), 11);
    }

    #[test]
    fn wrapping_rolls_over() {
        assert_eq!(wrapping_sequence(255), 0);
    }

    #[test]
    fn overflowing_reports_carry() {
        assert_eq!(add_with_carry(u32::MAX, 1), (0, true));
        assert_eq!(add_with_carry(1, 2), (3, false));
    }
}
```

## Key Points

| Method family | Returns | Use when |
|---|---|---|
| `checked_*` | `Option<T>` | overflow is an error your caller must handle |
| `saturating_*` | `T` | clamping at the type's bounds is correct behavior |
| `wrapping_*` | `T` | modular arithmetic is intentional (e.g., checksums, ring buffers) |
| `overflowing_*` | `(T, bool)` | you need the result *and* know whether it overflowed |

These methods are available on all primitive integer types in the standard library (`u8` through `u128`, `i8` through `i128`, `usize`, `isize`). Equivalent sub/mul/div/shl/shr variants exist for every arithmetic operation.

## Related Rules
- [num-saturating-clamp](num-saturating-clamp.md) - bound values with `clamp` and saturating arithmetic
- [num-cast-try-from](num-cast-try-from.md) - avoid `as` for narrowing casts; prefer `TryFrom`
