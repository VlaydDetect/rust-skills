# conc-rayon-par-iter

> Use rayon's `par_iter()` for CPU-bound data parallelism## Decision

Consider this rule only after its prerequisites are satisfied: Use rayon's `par_iter()` for CPU-bound data parallelism.

## Apply When

Apply when correctness or liveness spans threads, tasks, locks, channels, atomics, ordering, or shutdown, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when one owner and sequential execution satisfy the workload, or the proposed parallelism has no measured benefit. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Write the state machine, owners, capacities, lock order, memory ordering, failure, cancellation, and join policy.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Parallelism may improve throughput while increasing contention, scheduling variance, state-space, and shutdown complexity.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `rayon`) must already be accepted by the project or be approved before addition.
- Runtime, task ownership, cancellation, capacity, blocking, and shutdown behavior must be known.

## Verification

Use deterministic protocol tests and add loom, stress, or benchmarks only for the schedules or throughput they can demonstrate.

## Why It Matters

Rayon's work-stealing scheduler parallelizes data-parallel workloads with an API nearly identical to standard iterators — often a one-word change from `.iter()` to `.par_iter()` yields near-linear speedup across cores. It automatically balances load across threads, handles chunking, and composes with the full iterator adapter chain. For IO-bound concurrency, use async instead; rayon is strictly for CPU-bound computation.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// single-threaded — wastes available cores on a CPU-bound workload
fn sum_squares(data: &[f64]) -> f64 {
    data.iter().map(|x| x * x).sum()
}

fn normalize(data: &mut [f64]) {
    let max = data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    data.iter_mut().for_each(|x| *x /= max);
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use rayon::prelude::*;

fn sum_squares(data: &[f64]) -> f64 {
    data.par_iter().map(|x| x * x).sum()
}

fn normalize(data: &mut [f64]) {
    let max = data.par_iter().cloned().reduce(|| f64::NEG_INFINITY, f64::max);
    data.par_iter_mut().for_each(|x| *x /= max);
}

fn keep_positive(data: &[f64]) -> Vec<f64> {
    data.par_iter().copied().filter(|&x| x > 0.0).collect()
}

fn sort_large(data: &mut [f64]) {
    // parallel unstable sort — faster than std sort for large slices
    data.par_sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
}
```

## Key Points

| Concern | Guidance |
|---------|----------|
| Import | `use rayon::prelude::*;` enables `.par_iter()` on slices and most collections |
| IO-bound work | Use async (`tokio`, `async-std`), not rayon — rayon threads block |
| Small collections | Sequential is often faster due to thread-spawn overhead; profile first |
| Minimum chunk size | Rayon's `with_min_len()` / `with_max_len()` tune granularity |
| Shared state | Use `Mutex` or atomic operations; rayon does not prevent data races |

## When to Use

- Processing large arrays, slices, or collections (image pixels, number crunching, parsing batches)
- CPU-bound transformations: map, filter, fold, sort
- When the per-element work is non-trivial (at least a few hundred nanoseconds)

## Related Rules
- [conc-scoped-threads](conc-scoped-threads.md) - borrow stack data across short-lived threads
- [perf-iter-over-index](perf-iter-over-index.md) - prefer iterators over manual indexing
- [async-spawn-blocking](async-spawn-blocking.md) - offload CPU work from async runtimes
