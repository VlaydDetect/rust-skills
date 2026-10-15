# Specialized Rust Performance Routing

## Ownership

Use [rust-profiling](../../rust-profiling/SKILL.md) for benchmark design, CPU/heap attribution, counters, timelines, build time and binary-size evidence. Use [rust-optimization](../../rust-optimization/SKILL.md) to choose algorithms, representations, cross-component changes or compiler experiments from that evidence.

The `rust-performance` public entrypoint and this path remain compatible. Do not load it beside its resolved owner as another role for the same decision.

## Focused References

- [Profiling guide](../../rust-profiling/references/guide.md) selects the measurement layer and defines artifact identity.
- [Benchmark analysis](../../rust-profiling/references/benchmark-analysis.md) owns distributions, estimators, comparisons and load generation.
- [Optimization guide](../../rust-optimization/references/guide.md) owns hypotheses and trade-offs.
- [System optimization](../../rust-optimization/references/system-optimization.md) owns shared budgets and bottleneck migration.
- [Tool matrix](low-level/rust-profiling.md) preserves CPU, heap, Tracy and Windows procedures.
- [PGO/BOLT](low-level/pgo.md) covers training and evaluating feedback-directed builds.

`debugging` owns unexplained symptoms, `rust-unsafe` owns safety proofs, and `rust-verify` executes the selected checks. Respect the current project toolchain, target, features and explicit authorization across every handoff.
