# Performance Patterns

Prefix: `perf-` · 13 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a controlled benchmark or profile identifies the operation and the proposed pattern preserves the correctness contract.
- Defer when the change is based on source aesthetics, a synthetic non-representative workload, or an unapproved faster-but-weaker primitive.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`perf-ahash`](../rules/perf-ahash.md) | `conditional` | `rust-performance` | Use a faster hasher (`ahash` / `FxHashMap`) when DoS resistance is not needed |
| [`perf-black-box-bench`](../rules/perf-black-box-bench.md) | `conditional` | `rust-performance` | Use black_box in benchmarks |
| [`perf-chain-avoid`](../rules/perf-chain-avoid.md) | `conditional` | `rust-performance` | Avoid chain in hot loops |
| [`perf-collect-into`](../rules/perf-collect-into.md) | `conditional` | `rust-performance` | Use collect_into for reusing containers |
| [`perf-collect-once`](../rules/perf-collect-once.md) | `conditional` | `rust-performance` | Don't collect intermediate iterators |
| [`perf-drain-reuse`](../rules/perf-drain-reuse.md) | `conditional` | `rust-performance` | Use drain to reuse allocations |
| [`perf-entry-api`](../rules/perf-entry-api.md) | `conditional` | `rust-performance` | Use entry API for map insert-or-update |
| [`perf-extend-batch`](../rules/perf-extend-batch.md) | `conditional` | `rust-performance` | Use extend for batch insertions |
| [`perf-io-buffering`](../rules/perf-io-buffering.md) | `conditional` | `rust-performance` | Wrap `Read`/`Write` in `BufReader`/`BufWriter` for many small operations |
| [`perf-iter-lazy`](../rules/perf-iter-lazy.md) | `conditional` | `rust-performance` | Keep iterators lazy, collect only when needed |
| [`perf-iter-over-index`](../rules/perf-iter-over-index.md) | `conditional` | `rust-performance` | Prefer iterators over manual indexing |
| [`perf-profile-first`](../rules/perf-profile-first.md) | `conditional` | `rust-performance` | Profile before optimizing |
| [`perf-release-profile`](../rules/perf-release-profile.md) | `conditional` | `rust-performance` | Optimize release profile settings |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
