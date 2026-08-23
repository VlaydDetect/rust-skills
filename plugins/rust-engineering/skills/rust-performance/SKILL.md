---
name: rust-performance
description: Measure and optimize Rust latency, throughput, allocations, cache behavior, binary size, build time, and resource use without changing semantics accidentally. Use when a performance target or regression has reproducible evidence.
---

# Rust Performance

Own performance diagnosis, experiment design, optimization, and regression evidence. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A benchmark, profile, production signal, or user requirement identifies a latency, throughput, memory, size, or build-time problem.
- An optimization proposal needs proof of bottleneck, magnitude, and semantic safety.
- Allocations, copying, hashing, layout, dispatch, synchronization, I/O, or compilation cost needs focused analysis.

## Workflow

1. Define the metric, workload, target, baseline, acceptable variance, correctness contract, and environment controls.
2. Reproduce with the same toolchain, profile, features, target, inputs, hardware or runner class, and thermal or load conditions.
3. Profile before editing to locate time, allocation, I/O, contention, code size, or compilation hotspots.
4. Form one optimization hypothesis and make the smallest change that tests it while preserving output and error behavior.
5. Compare distributions or repeated samples, inspect generated or profile evidence where needed, and reject noise-level wins.
6. Add a proportionate regression guard or documented benchmark, then report trade-offs and environments not measured.

## Decision Rules

- Correctness and public behavior remain constraints; faster wrong code is a regression.
- Use release-like profiles for runtime claims and representative incremental or clean builds for compile-time claims.
- Do not infer performance from source appearance, iterator versus loop style, or fewer lines.
- Measure allocations and copies before adding borrowing complexity, arenas, interning, or unsafe code.
- Choose collections and hashers by workload and security requirements, including collision behavior and ordering.
- Account for cold start, warm caches, tail latency, contention, batching, and I/O where the product cares about them.
- Unsafe or SIMD optimizations need target dispatch, fallback, invariant proof, and a material measured benefit.
- Compile-time improvements should identify monomorphization, macro, codegen-unit, dependency, linking, or proc-macro causes.

## Rulebook Overlay

After recording a comparable baseline and hotspot, select at most eight IDs from [`mem-`](../rust-coding-rules/references/categories/mem.md), [`opt-`](../rust-coding-rules/references/categories/opt.md), or [`perf-`](../rust-coding-rules/references/categories/perf.md). These indexes never supply a measurement or global optimization default.

## Boundaries and Hand-offs

- `debugging` owns causal diagnosis when the primary issue is incorrect or unexplained behavior.
- `rust-unsafe` owns soundness proof and `rust-testing` owns functional tests; performance does not relax either.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Performance field guide](references/guide.md) before making a consequential design choice. Load the relevant [Actionbook performance protocol](references/actionbook-index.md) branch for its detailed measurement and optimization algorithms. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
