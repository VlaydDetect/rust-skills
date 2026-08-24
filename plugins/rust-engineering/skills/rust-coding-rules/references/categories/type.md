# Type Safety

Prefix: `type-` · 13 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a type can encode a real invariant, state, identity, representation, or output contract more reliably than convention.
- Defer when the extra type machinery does not eliminate a meaningful invalid state or would make a local operation harder to use.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`type-deref-coercion`](../rules/type-deref-coercion.md) | `canonical` | `rust-traits` | Implement `Deref`/`DerefMut` only for smart-pointer and transparent wrapper types |
| [`type-display-vs-debug`](../rules/type-display-vs-debug.md) | `conditional` | `rust-traits` | Use `Display` for user-facing output and `Debug` for diagnostics; never swap them |
| [`type-enum-states`](../rules/type-enum-states.md) | `conditional` | `rust-traits` | Use enums for mutually exclusive states |
| [`type-generic-bounds`](../rules/type-generic-bounds.md) | `canonical` | `rust-traits` | Add trait bounds only where needed, prefer where clauses for readability |
| [`type-never-diverge`](../rules/type-never-diverge.md) | `canonical` | `rust-traits` | Use `!` (never type) for functions that never return |
| [`type-newtype-ids`](../rules/type-newtype-ids.md) | `conditional` | `rust-traits` | Wrap IDs in newtypes: `UserId(u64)` |
| [`type-newtype-validated`](../rules/type-newtype-validated.md) | `conditional` | `rust-traits` | Use newtypes to enforce validation at construction time |
| [`type-no-stringly`](../rules/type-no-stringly.md) | `conditional` | `rust-traits` | Avoid stringly-typed APIs; use enums, newtypes, or validated types |
| [`type-numeric-fmt`](../rules/type-numeric-fmt.md) | `canonical` | `rust-traits` | Implement `LowerHex`, `UpperHex`, `Octal`, and `Binary` for numeric newtypes |
| [`type-option-nullable`](../rules/type-option-nullable.md) | `canonical` | `rust-traits` | Use `Option<T>` for values that might not exist |
| [`type-phantom-marker`](../rules/type-phantom-marker.md) | `canonical` | `rust-traits` | Use `PhantomData` to express type relationships without runtime cost |
| [`type-repr-transparent`](../rules/type-repr-transparent.md) | `canonical` | `rust-traits` | Use `#[repr(transparent)]` for newtypes in FFI contexts |
| [`type-result-fallible`](../rules/type-result-fallible.md) | `conditional` | `rust-traits` | Use `Result<T, E>` for operations that can fail |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
