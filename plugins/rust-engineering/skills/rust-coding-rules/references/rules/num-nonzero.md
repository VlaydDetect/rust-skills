# num-nonzero

> Use `NonZero*` types to forbid zero and unlock the niche optimization

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-idioms; supporters=`rust-stdlib`, `rust-stable`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use `NonZero*` types to forbid zero and unlock the niche optimization.

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

`NonZeroU32`, `NonZeroI64`, and their siblings (available for all integer primitives in `std::num`) make zero unrepresentable at the type level — you cannot construct one without going through `NonZeroU32::new(n)`, which returns `Option<NonZeroU32>`. This pushes the zero-check to the construction site and eliminates defensive zero-checks throughout the rest of the code. As a bonus, the compiler uses the zero bit-pattern as a *niche*, so `Option<NonZeroU32>` is exactly the same size as `u32` — no overhead for the `Option` tag.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// caller must remember never to pass 0, but nothing enforces it
fn divide(numerator: u32, denominator: u32) -> u32 {
    assert!(denominator != 0, "denominator must not be zero");
    numerator / denominator
}

// ID of 0 is "invalid" by convention — not enforced
struct Widget {
    id: u32,  // 0 means "not yet assigned" — stringly-typed convention
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::num::NonZeroU32;
use std::mem::size_of;

// zero is rejected at construction; division is always safe
fn divide(numerator: u32, denominator: NonZeroU32) -> u32 {
    numerator / denominator.get()
}

// ID is guaranteed non-zero; Option<WidgetId> is free
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct WidgetId(NonZeroU32);

impl WidgetId {
    /// Returns `None` if `id` is zero.
    pub fn new(id: u32) -> Option<Self> {
        NonZeroU32::new(id).map(WidgetId)
    }

    pub fn get(self) -> u32 {
        self.0.get()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::num::NonZeroU32;

    #[test]
    fn nonzero_new_returns_none_for_zero() {
        assert!(NonZeroU32::new(0).is_none());
        assert!(NonZeroU32::new(1).is_some());
    }

    #[test]
    fn option_nonzero_is_same_size_as_u32() {
        // niche optimization: no space overhead for Option
        assert_eq!(size_of::<Option<NonZeroU32>>(), size_of::<u32>());
        assert_eq!(size_of::<Option<NonZeroU32>>(), 4);
    }

    #[test]
    fn widget_id_rejects_zero() {
        assert!(WidgetId::new(0).is_none());
        let id = WidgetId::new(42).unwrap();
        assert_eq!(id.get(), 42);
    }

    #[test]
    fn divide_uses_nonzero_denominator() {
        let denom = NonZeroU32::new(3).unwrap();
        assert_eq!(divide(12, denom), 4);
    }
}
```

## Key Points

- All `NonZero*` types live in `std::num`: `NonZeroU8`, `NonZeroU16`, `NonZeroU32`, `NonZeroU64`, `NonZeroU128`, `NonZeroUsize`, and their signed counterparts.
- **Construction**: `NonZeroU32::new(n) -> Option<NonZeroU32>`. Use `NonZeroU32::new(n).expect("n must be non-zero")` only at well-verified program boundaries, not in production fallible paths.
- **Access**: `.get()` returns the inner primitive value.
- **Arithmetic**: `NonZeroU32` does not implement `Add`/`Sub` directly (the result could be zero). Extract with `.get()`, do arithmetic, and reconstruct with `NonZeroU32::new(result)?`.
- **Niche optimization** applies to `Option` and `Result`: the compiler stores the `None`/`Err` discriminant in the zero bit-pattern, so no extra word is needed. This also applies to custom newtypes that wrap `NonZero*`.

## Related Rules
- [type-newtype-ids](type-newtype-ids.md) - wrap IDs in newtypes for type-safe distinctions
- [mem-smaller-integers](mem-smaller-integers.md) - use the smallest integer type that fits
