# API Design

Prefix: `api-` · 17 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a public or independently evolving caller contract needs an ownership, construction, extension, or compatibility decision.
- Defer when the abstraction has only one local use or would expose implementation and dependency details without caller value.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`api-builder-must-use`](../rules/api-builder-must-use.md) | `canonical` | `rust-api-design` | Mark builder methods with `#[must_use]` to prevent silent drops |
| [`api-builder-pattern`](../rules/api-builder-pattern.md) | `conditional` | `rust-api-design` | Use Builder pattern for complex construction |
| [`api-common-traits`](../rules/api-common-traits.md) | `conditional` | `rust-api-design` | Implement standard traits (Debug, Clone, PartialEq, etc.) for public types |
| [`api-default-impl`](../rules/api-default-impl.md) | `canonical` | `rust-api-design` | Implement `Default` for types with sensible default values |
| [`api-extension-trait`](../rules/api-extension-trait.md) | `conditional` | `rust-api-design` | Use extension traits to add methods to external types |
| [`api-from-not-into`](../rules/api-from-not-into.md) | `canonical` | `rust-api-design` | Implement `From<T>`, not `Into<U>` - From gives you Into for free |
| [`api-impl-asref`](../rules/api-impl-asref.md) | `canonical` | `rust-api-design` | Use `AsRef<T>` when you only need to borrow the inner data |
| [`api-impl-fromiterator`](../rules/api-impl-fromiterator.md) | `canonical` | `rust-api-design` | Implement `FromIterator` and `Extend` for collection types, and `IntoIterator` for all three reference forms |
| [`api-impl-into`](../rules/api-impl-into.md) | `canonical` | `rust-api-design` | Accept `impl Into<T>` for flexible APIs, implement `From<T>` for conversions |
| [`api-must-use`](../rules/api-must-use.md) | `conditional` | `rust-api-design` | Mark types and functions with `#[must_use]` when ignoring results is likely a bug |
| [`api-newtype-safety`](../rules/api-newtype-safety.md) | `conditional` | `rust-api-design` | Use newtypes to prevent mixing semantically different values |
| [`api-non-exhaustive`](../rules/api-non-exhaustive.md) | `conditional` | `rust-api-design` | Use `#[non_exhaustive]` on public enums and structs for forward compatibility |
| [`api-operator-overload`](../rules/api-operator-overload.md) | `canonical` | `rust-api-design` | Overload operators only when the semantics are natural and unsurprising |
| [`api-parse-dont-validate`](../rules/api-parse-dont-validate.md) | `conditional` | `rust-api-design` | Parse into validated types at boundaries |
| [`api-sealed-trait`](../rules/api-sealed-trait.md) | `conditional` | `rust-api-design` | Use sealed traits to prevent external implementations while allowing use |
| [`api-serde-optional`](../rules/api-serde-optional.md) | `conditional` | `rust-api-design` | Make serde a feature flag, not a hard dependency for library crates |
| [`api-typestate`](../rules/api-typestate.md) | `conditional` | `rust-api-design` | Use typestate pattern to encode state machine invariants in the type system |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
