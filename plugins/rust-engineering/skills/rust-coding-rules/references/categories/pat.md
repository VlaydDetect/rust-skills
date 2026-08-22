# Pattern Matching

Prefix: `pat-` · 5 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when pattern syntax can make state extraction, exhaustiveness, guards, or early return clearer without changing behavior.
- Defer when the syntax exceeds the declared MSRV or a catch-all would hide a meaningful future or current variant.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Source decision |
|---|---|---|---|
| [`pat-at-bindings`](../rules/pat-at-bindings.md) | `conditional` | `rust-idioms` | Use `@` bindings to capture a value while matching it against a pattern |
| [`pat-exhaustive-enum`](../rules/pat-exhaustive-enum.md) | `adapted` | `rust-idioms` | Match owned enums exhaustively; avoid catch-all `_` that hides new variants |
| [`pat-if-let-chains`](../rules/pat-if-let-chains.md) | `adapted` | `rust-idioms` | Use `if let` chains to combine pattern bindings and conditions |
| [`pat-let-else`](../rules/pat-let-else.md) | `conditional` | `rust-idioms` | Use `let ... else` for early-return pattern extraction |
| [`pat-matches-macro`](../rules/pat-matches-macro.md) | `adapted` | `rust-idioms` | Use `matches!()` for boolean pattern tests |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
