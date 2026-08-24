# Const and Compile Time

Prefix: `const-` · 4 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when compile-time evaluation or value parameterization enforces a useful invariant within the declared MSRV.
- Defer when the feature is unavailable at the MSRV or const complexity harms diagnostics and compile time without runtime value.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`const-block`](../rules/const-block.md) | `canonical` | `rust-stable` | Use inline `const { }` blocks for compile-time evaluation and assertions |
| [`const-fn`](../rules/const-fn.md) | `canonical` | `rust-stable` | Make functions `const fn` when they can run at compile time |
| [`const-generics`](../rules/const-generics.md) | `canonical` | `rust-stable` | Parameterize over values with const generics `<const N: usize>` |
| [`const-vs-static`](../rules/const-vs-static.md) | `canonical` | `rust-stable` | Use `const` for an inlined value and `static` for a single addressed instance |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
