# num-saturating-clamp

> Bound values with `clamp` and saturating arithmetic## Decision

Use this context-sensitive Rust decision when its premise is established: Bound values with `clamp` and saturating arithmetic.

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

Constraining a numeric value to a range is a common operation, but hand-rolled `if`/`min`/`max` chains are verbose and easy to get wrong (especially when combining signed and unsigned types). `Ord::clamp(min, max)` expresses the intent in a single call and is available on all types that implement `Ord` (all integer primitives, and `f32`/`f64` via their own `clamp` since Rust 1.50). When you additionally want arithmetic that stops at the type's limits rather than panicking or wrapping, combine `clamp` with `saturating_*` methods.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn apply_damage(health: i32, damage: i32) -> i32 {
    let result = health - damage;
    if result < 0 { 0 } else { result }  // verbose, easy to mis-order
}

fn clamp_volume(vol: u8, min: u8, max: u8) -> u8 {
    if vol < min {
        min
    } else if vol > max {
        max
    } else {
        vol
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
fn apply_damage(health: i32, damage: i32) -> i32 {
    // saturating_sub stops at i32::MIN — then clamp ensures non-negative
    health.saturating_sub(damage).clamp(0, i32::MAX)
}

fn clamp_volume(vol: u8, min: u8, max: u8) -> u8 {
    vol.clamp(min, max)
}

// integer clamp: any Ord type
fn clamp_score(score: i64) -> i64 {
    score.clamp(0, 100)
}

// float clamp: available on f32/f64 since Rust 1.50
fn normalize_alpha(a: f32) -> f32 {
    a.clamp(0.0, 1.0)  // NaN propagates: NaN.clamp(0.0, 1.0) == NaN
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn damage_does_not_go_below_zero() {
        assert_eq!(apply_damage(10, 5), 5);
        assert_eq!(apply_damage(3, 100), 0);
    }

    #[test]
    fn volume_is_bounded() {
        assert_eq!(clamp_volume(50, 10, 90), 50);
        assert_eq!(clamp_volume(5, 10, 90), 10);
        assert_eq!(clamp_volume(200, 10, 90), 90);
    }

    #[test]
    fn score_is_clamped() {
        assert_eq!(clamp_score(-10), 0);
        assert_eq!(clamp_score(150), 100);
        assert_eq!(clamp_score(75), 75);
    }

    #[test]
    fn float_nan_propagates_through_clamp() {
        assert!(f32::NAN.clamp(0.0, 1.0).is_nan());
    }
}
```

## Key Points

- **`clamp` panics if `min > max`** — this is a programming error and is caught in debug builds. If `min`/`max` come from user input, validate their order first.
- **`f32`/`f64` `clamp`** propagates `NaN`: if `self` is `NaN`, the result is `NaN`. If `min` or `max` is `NaN`, the result is unspecified. Filter `NaN` before calling `clamp` on untrusted floats.
- **Saturating vs. clamping**: `saturating_*` applies to a single arithmetic operation and stops at the type's absolute limits (`i32::MIN`/`i32::MAX`). `clamp` applies to the final value and accepts arbitrary bounds. They compose well, as shown in `apply_damage`.
- The standard library docs for `clamp` are at `std::cmp::Ord::clamp` and `f32::clamp`.

## Related Rules
- [num-overflow-explicit](num-overflow-explicit.md) - handle overflow with `checked_`/`saturating_`/`wrapping_`/`overflowing_`
- [num-cast-try-from](num-cast-try-from.md) - avoid `as` for narrowing casts; prefer `TryFrom`
