# Closures

Prefix: `closure-` · 5 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when callback capture, call multiplicity, mutation, lifetime, storage, or dispatch semantics control the interface.
- Defer when a named function or concrete operation is clearer, or boxing and static bounds add constraints with no real storage need.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Source decision |
|---|---|---|---|
| [`closure-disjoint-capture`](../rules/closure-disjoint-capture.md) | `adapted` | `rust-traits` | Capture only what you use; lean on edition-2021 disjoint closure captures |
| [`closure-fn-trait-bounds`](../rules/closure-fn-trait-bounds.md) | `adapted` | `rust-traits` | Require the least restrictive `Fn` trait a callback needs (`FnOnce` ⊇ `FnMut` ⊇ `Fn`) |
| [`closure-impl-fn-return`](../rules/closure-impl-fn-return.md) | `adapted` | `rust-traits` | Return closures as `impl Fn`/`FnMut`/`FnOnce`, not `Box<dyn Fn>` |
| [`closure-move-capture`](../rules/closure-move-capture.md) | `conditional` | `rust-traits` | Use `move` for closures that outlive the current scope; clone before `move` to keep the original |
| [`closure-static-vs-dyn`](../rules/closure-static-vs-dyn.md) | `adapted` | `rust-traits` | Accept `impl Fn` (generic) for hot callbacks; use `&dyn Fn`/`Box<dyn Fn>` to cut code size or to store them |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
