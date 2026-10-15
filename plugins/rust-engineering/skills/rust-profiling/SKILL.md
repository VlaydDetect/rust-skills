---
name: rust-profiling
description: Design and interpret Rust benchmarks, CPU and heap profiles, counters, traces, code-size and build-time measurements. Use for Criterion, VTune, perf, WPR/WPA, or ambiguous performance evidence; use rust-optimization to choose changes and debugging for unexplained failures.
---

# Rust Profiling

Own measurement validity and resource attribution. A profile explains where to investigate; a comparable experiment determines whether a change helped.

## Workflow

1. Define useful work, the metric and correctness oracle, workload distribution, baseline, useful-effect threshold, and secondary budgets.
2. Inspect the actual target, toolchain, features, profile, flags, allocator, runtime and machine. Preserve exact binaries, symbols, raw outputs and invocation details.
3. Audit the harness before interpreting a result: work elimination, timing boundary, input state, units, dependencies, warmup, load generator, and comparable build identities.
4. Select the smallest supported tool that distinguishes the resource hypotheses. Check symbols, scope, lost events/stacks, sampling coverage and instrumentation overhead before trusting attribution.
5. Interpret absolute costs and uncertainty, not only percentages or significance. Request one discriminating follow-up if the evidence cannot choose between explanations.
6. Return an evidence record and a bounded bottleneck hypothesis to `rust-optimization`, or a reproducer to `debugging`. State invalid, inconclusive and unavailable evidence explicitly.

## Decision Rules

- Use Criterion by default for maintained microbenchmarks; preserve an existing adequate harness. Divan remains a small exploratory alternative. Service percentiles need a representative end-to-end harness.
- Separate independent-operation throughput from dependency-chain latency and warm-cache cost from startup or cold-working-set cost.
- `black_box` is a best-effort compiler barrier, not a guarantee that the benchmark models the product. Inspect generated code when the result is implausible.
- CPU time, elapsed time, ready/wait time, sampled heap, exact allocation counts, peak heap and RSS answer different questions.
- Changing sample proportions does not establish an absolute improvement. Sampling and counters have target-specific coverage and uncertainty.
- Do not install tools, change host policy, or enable broader tracing merely because a profiler is missing. Use existing authorization; missing capability is `SKIP` with the evidence gap.

## References and Ownership

- Read the [profiling guide](references/guide.md), then [benchmark analysis](references/benchmark-analysis.md) or [profile interpretation](references/profile-interpretation.md).
- The existing [tool matrix](../rust-performance/references/low-level/rust-profiling.md) and [Windows protocol](../rust-performance/references/low-level/intel-vtune-amd-uprof.md) retain their public paths and supply conditional tool procedures.
- `rust-optimization` owns candidate selection; `debugging` owns unexplained failures; `rust-unsafe` owns Miri/sanitizer interpretation and soundness.
- `rust-cargo-build` owns effective build configuration, and `rust-observability` owns application span/metric semantics. Add instrumentation through `rust-workflow` when source changes are needed.
- `rust-performance` is the compatibility entrypoint. Resolve it to the actual decision owner instead of occupying a second role for the same measurement.
- `rust-verify` executes the selected evidence matrix; passing structural eval validation is not a behavioral model evaluation or hardware measurement.
