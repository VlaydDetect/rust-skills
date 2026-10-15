---
name: rust-performance
description: Route Rust performance work through the compatible performance entrypoint. Clarify the metric and choose rust-profiling for measurements, rust-optimization for confirmed bottlenecks, or debugging for unexplained failures; retain existing reference paths.
---

# Rust Performance

Preserve the public performance entrypoint and its reference paths. Resolve the actual decision to a focused owner rather than duplicating experiment, optimization, or soundness policy here.

## Workflow

1. Clarify useful work, the metric, correctness contract, representative workload, and available evidence.
2. Select the current decision using the table below and read that skill's entrypoint.
3. Hand off the bounded result; do not also retain `rust-performance` as an owner/helper for the same decision.
4. Any repository mutation enters `rust-workflow`; verification closes through `rust-verify`.

## Decision Routing

| Current decision | Owner |
|---|---|
| Unexplained regression, contradictory output, crash, hang, or non-reproducible failure | [debugging](../debugging/SKILL.md) |
| Design/audit a benchmark, interpret a capture, locate a limiting resource, measure build time or size | [rust-profiling](../rust-profiling/SKILL.md) |
| Choose a change from an established bottleneck and evaluate system trade-offs | [rust-optimization](../rust-optimization/SKILL.md) |
| Prove unsafe preconditions or interpret Miri/sanitizer evidence | [rust-unsafe](../rust-unsafe/SKILL.md) |

For a mixed task, route by phase with one owner per decision unit. Existing domain owners still control data architecture, concurrency semantics, durable formats and Cargo configuration. Profiling supplies measurements; optimization does not silently relax those contracts.

## Compatibility and References

- Read the [compatibility guide](references/guide.md) for the retained reference map and compiling fixture.
- The [benchmark implementation guide](references/performance-optimization-guide.md) and [tool matrix](references/low-level/rust-profiling.md) remain at their existing paths.
- The [low-level index](references/low-level-index.md) routes to the relevant tool or hardware family. Load only the matching family.
- Existing `$rust-performance` invocations remain valid; new automatic routes select the specific skill. Tool absence does not authorize installation or host-policy changes.
