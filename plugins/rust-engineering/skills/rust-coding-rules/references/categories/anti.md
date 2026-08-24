# Anti-patterns

Prefix: `anti-` · 15 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when the named anti-pattern exists in a real path and obscures ownership, errors, iteration, abstraction, or measured performance.
- Defer when the alleged smell is required by the contract or the replacement would add more complexity or alter behavior.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`anti-clone-excessive`](../rules/anti-clone-excessive.md) | `alias` | `rust-ownership` | Don't clone when borrowing works |
| [`anti-collect-intermediate`](../rules/anti-collect-intermediate.md) | `alias` | `rust-performance` | Don't collect intermediate iterators |
| [`anti-empty-catch`](../rules/anti-empty-catch.md) | `canonical` | `rust-idioms` | Don't silently ignore errors |
| [`anti-expect-lazy`](../rules/anti-expect-lazy.md) | `alias` | `rust-errors` | Don't use expect for recoverable errors |
| [`anti-format-hot-path`](../rules/anti-format-hot-path.md) | `alias` | `rust-performance` | Don't use format! in hot paths |
| [`anti-index-over-iter`](../rules/anti-index-over-iter.md) | `alias` | `rust-performance` | Don't use indexing when iterators work |
| [`anti-lock-across-await`](../rules/anti-lock-across-await.md) | `alias` | `rust-concurrency` | Don't hold locks across await points |
| [`anti-over-abstraction`](../rules/anti-over-abstraction.md) | `canonical` | `rust-idioms` | Don't over-abstract with excessive generics |
| [`anti-panic-expected`](../rules/anti-panic-expected.md) | `alias` | `rust-errors` | Don't panic on expected or recoverable errors |
| [`anti-premature-optimize`](../rules/anti-premature-optimize.md) | `alias` | `rust-performance` | Don't optimize before profiling |
| [`anti-string-for-str`](../rules/anti-string-for-str.md) | `alias` | `rust-ownership` | Don't accept &String when &str works |
| [`anti-stringly-typed`](../rules/anti-stringly-typed.md) | `alias` | `rust-traits` | Don't use strings where enums or newtypes would provide type safety |
| [`anti-type-erasure`](../rules/anti-type-erasure.md) | `alias` | `rust-traits` | Don't use Box<dyn Trait> when impl Trait works |
| [`anti-unwrap-abuse`](../rules/anti-unwrap-abuse.md) | `alias` | `rust-errors` | Don't use `.unwrap()` in production code |
| [`anti-vec-for-slice`](../rules/anti-vec-for-slice.md) | `alias` | `rust-ownership` | Don't accept &Vec<T> when &[T] works |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
