# Numeric and Arithmetic Safety

Prefix: `num-` · 5 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when range, overflow, narrowing, floating-point semantics, ordering, or a numeric invariant is part of the contract.
- Defer when the selected behavior would silently change domain semantics or add a representation optimization without measured need.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`num-cast-try-from`](../rules/num-cast-try-from.md) | `canonical` | `rust-idioms` | Avoid `as` for narrowing casts; use `From` for widening and `TryFrom` for narrowing |
| [`num-float-compare`](../rules/num-float-compare.md) | `canonical` | `rust-idioms` | Don't compare floats with `==`; use a tolerance, and `total_cmp` for ordering |
| [`num-nonzero`](../rules/num-nonzero.md) | `canonical` | `rust-idioms` | Use `NonZero*` types to forbid zero and unlock the niche optimization |
| [`num-overflow-explicit`](../rules/num-overflow-explicit.md) | `canonical` | `rust-idioms` | Handle integer overflow explicitly: `checked_`/`saturating_`/`wrapping_`/`overflowing_` |
| [`num-saturating-clamp`](../rules/num-saturating-clamp.md) | `canonical` | `rust-idioms` | Bound values with `clamp` and saturating arithmetic |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
