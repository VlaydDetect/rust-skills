# Conversions

Prefix: `conv-` · 3 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a conversion has stable ownership, validation, loss, or error semantics worth expressing through standard traits.
- Defer when the conversion is ambiguous, lossy without an explicit name, or broad generic acceptance would hide cost or meaning.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`conv-asmut-mutable`](../rules/conv-asmut-mutable.md) | `canonical` | `rust-api-design` | Accept `impl AsMut<T>` for flexible mutable borrowed inputs instead of concrete mutable references |
| [`conv-fromstr-parsing`](../rules/conv-fromstr-parsing.md) | `conditional` | `rust-api-design` | Implement `FromStr` to enable `str::parse` for string-to-type conversions |
| [`conv-tryfrom-fallible`](../rules/conv-tryfrom-fallible.md) | `canonical` | `rust-api-design` | Implement `TryFrom` for fallible conversions instead of ad-hoc conversion functions |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
