# Traits and Generics

Prefix: `trait-` · 6 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when real implementations or callers need a behavioral abstraction, extension point, dispatch choice, or coherence solution.
- Defer when one concrete implementation or a closed enum expresses the current contract more directly.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`trait-associated-type-vs-generic`](../rules/trait-associated-type-vs-generic.md) | `canonical` | `rust-traits` | Use an associated type when each impl has exactly one output type; use a generic parameter when a type can implement the trait for many input types |
| [`trait-blanket-impl`](../rules/trait-blanket-impl.md) | `canonical` | `rust-traits` | Use a blanket impl `impl<T: Bound> Trait for T` to give behaviour to every type that satisfies a bound |
| [`trait-coherence-newtype`](../rules/trait-coherence-newtype.md) | `canonical` | `rust-traits` | Respect the orphan rule; wrap a foreign type in a newtype to implement a foreign trait on it |
| [`trait-default-methods`](../rules/trait-default-methods.md) | `canonical` | `rust-traits` | Define a trait in terms of a few required methods plus defaulted ones built on top of them |
| [`trait-dyn-vs-generic`](../rules/trait-dyn-vs-generic.md) | `conditional` | `rust-traits` | Choose static dispatch (generics / `impl Trait`) vs dynamic dispatch (`dyn Trait`) deliberately |
| [`trait-object-safety`](../rules/trait-object-safety.md) | `canonical` | `rust-traits` | Keep a trait dyn-compatible (object-safe) when you need `dyn Trait` |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
