---
name: rust-optimization
description: Choose and validate Rust optimizations from a confirmed bottleneck, workload properties, and preserved contracts. Use for algorithms, representations, component pipelines, generated code, or PGO; use rust-profiling for measurement and debugging for unexplained failures.
---

# Rust Optimization

Own the choice of a change and its system-level trade-offs. A measured hot function is a starting point: the objective is the user-visible metric under the actual workload.

## Workflow

1. Record the target metric, representative workload, comparable baseline, minimum worthwhile effect, and permitted regressions. Ask for missing product trade-offs before choosing a risky change.
2. Map the critical path, resource saturation, queues, copies, allocations, synchronization, and component boundaries. Ask `rust-profiling` for the smallest measurement that separates competing explanations.
3. Build an invariant ledger: property, evidence, enforcing constructor or mutation path, scope, and failure behavior. Distinguish observed distributions from guarantees.
4. Rank hypotheses by plausible system benefit, confidence, experiment cost, and semantic risk. Prefer removing work or simplifying an algorithm before lower-level tuning when evidence supports it.
5. Test the smallest coherent hypothesis, preserving useful intermediate variants when several components must change together. Any repository mutation enters `rust-workflow`; this skill does not bypass its single-writer or routing contract.
6. Verify behavior and the original metric, inspect new costs and neighboring workloads, and profile again for a migrated bottleneck. Keep, reject, or report an inconclusive result explicitly.

## Decision Rules

- Never infer a win from fewer lines, fewer clones, lower asymptotic complexity, or a library's unrelated benchmark.
- Preserve ordering, errors, panic behavior, cancellation, resource bounds, numerical policy, security, supported targets, and public compatibility unless their change is explicitly authorized.
- A fixed length can justify `Box<[T]>`; it does not imply immutable elements, stable addresses across conversion, or a guaranteed RSS reduction.
- Use an end-to-end budget for multi-component changes. Avoid optimizing only the largest sampled frame when waits, copies, or another saturated component controls completion.
- Compiler flags, allocators, parallelism, caches, SIMD, PGO, and unsafe are candidates with costs, not global defaults.
- No universal percentage establishes success. Set a useful-effect threshold from the task and interpret uncertainty before increasing complexity.

## Unsafe Optimization Gate

First compare safe forms and inspect the optimized artifact: the compiler may already remove bounds checks or vectorize the loop. If a relevant cost remains, `rust-unsafe` owns the operation-by-operation proof, including every path that can invalidate the invariant. `debug_assert!`, successful tests, and a faster benchmark do not establish safety. Measure native optimized code separately from Miri or sanitizer runs.

## References and Hand-offs

- Read the [decision guide](references/guide.md), then [data and workload contracts](references/data-and-workload-contracts.md) or [system optimization](references/system-optimization.md) for the current hypothesis.
- `rust-profiling` owns experiment validity and interpretation; `debugging` owns unexplained symptoms or incorrect results.
- `rust-data` owns access-pattern-driven data architecture; `rust-concurrency` owns synchronization and cancellation; `rust-cargo-build` owns effective compiler/linker configuration. Keep one owner per distinct decision.
- Use the existing [PGO/BOLT protocol](../rust-performance/references/low-level/pgo.md) only when feedback-directed optimization is a plausible candidate.
- Select at most nine relevant rules from the [performance](../rust-coding-rules/references/categories/perf.md), [optimization](../rust-coding-rules/references/categories/opt.md), and [memory](../rust-coding-rules/references/categories/mem.md) indexes after routing. Rules do not replace measurements.
