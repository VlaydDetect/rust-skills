# Performance Measurement and Optimization Map

This retained entrypoint separates measurement from change selection. `rust-performance` routes older invocations to the current decision owner.

## Select the Decision

- For an unexplained regression or wrong behavior, start with [debugging](../../debugging/SKILL.md).
- For an invalid/missing baseline, unclear resource cost, benchmark statistics or trace interpretation, use [rust-profiling](../../rust-profiling/SKILL.md).
- For a confirmed limiting resource and a behavior-preserving change, use [rust-optimization](../../rust-optimization/SKILL.md).
- For unsafe operations, retain [rust-unsafe](../../rust-unsafe/SKILL.md) as the soundness authority.

## Detailed Protocols

- [Benchmark design and analysis](../../rust-profiling/references/benchmark-analysis.md)
- [Profile interpretation](../../rust-profiling/references/profile-interpretation.md)
- [Data and workload contracts](../../rust-optimization/references/data-and-workload-contracts.md)
- [System optimization](../../rust-optimization/references/system-optimization.md)
- [Criterion timing loops and commands](performance-optimization-guide.md)
- [Tool selection](low-level/rust-profiling.md)

All repository changes enter `rust-workflow`; one decision has one owner. A profiler does not establish a speedup, and a local speedup does not establish an end-to-end improvement.
