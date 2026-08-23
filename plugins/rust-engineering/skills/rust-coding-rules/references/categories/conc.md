# Concurrency

Prefix: `conc-` · 4 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when correctness or liveness spans threads, tasks, locks, channels, atomics, ordering, or shutdown.
- Defer when one owner and sequential execution satisfy the workload, or the proposed parallelism has no measured benefit.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`conc-atomic-ordering`](../rules/conc-atomic-ordering.md) | `conditional` | `rust-concurrency` | Use the weakest correct memory `Ordering` for every atomic operation |
| [`conc-rayon-par-iter`](../rules/conc-rayon-par-iter.md) | `conditional` | `rust-concurrency` | Use rayon's `par_iter()` for CPU-bound data parallelism |
| [`conc-scoped-threads`](../rules/conc-scoped-threads.md) | `conditional` | `rust-concurrency` | Use `std::thread::scope` to borrow stack data across threads |
| [`conc-thread-local`](../rules/conc-thread-local.md) | `canonical` | `rust-concurrency` | Prefer `thread_local!` with `Cell`/`RefCell` over `static mut` |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
