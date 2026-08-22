# Rust Performance Field Guide

This guide is the detailed policy for `rust-performance`. It synthesizes the merged craft and full-stack performance skills covering benchmarking, profiling, optimization, build time, and regression control; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- Performance work is an experiment: controlled baseline, profile, hypothesis, change, comparison, and decision.
- Criterion or Divan can estimate distributions and noise for microbenchmarks, while end-to-end harnesses cover realistic integration costs.
- Profilers reveal where resources are spent; allocation counters, flame graphs, sampling, tracing, and compiler timing answer different questions.
- Data layout, access locality, allocation, copies, branch behavior, hashing, dispatch, and synchronization are common runtime levers.
- Cargo profiles control optimization, debug info, LTO, codegen units, panic strategy, and stripping with build-time and artifact trade-offs.
- A benchmark committed without an execution policy can rot; document when, where, and how regression thresholds are interpreted.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Unknown hotspot | Profile first | Optimizing guesses wastes complexity |
| Small pure function | Microbenchmark | Isolates algorithm and allocation cost |
| Service latency | End-to-end representative load | Queues, I/O, runtime, and contention dominate |
| Compile-time regression | Cargo timings and clean or incremental controls | Runtime profilers answer the wrong question |
| Unsafe optimization proposal | Safe baseline and measured threshold first | Soundness debt needs material value |

## Common Failure Modes

- Benchmarking debug builds or comparing different feature, target, hardware, or load conditions.
- Reporting one timing sample without variance, warmup, or noise analysis.
- Optimizing allocation or cloning that is not visible in the profile.
- Changing hash order, floating-point behavior, errors, or cancellation while claiming semantics are preserved.
- Committing complex caching, pooling, SIMD, or unsafe code for an unmeasured future load.

## Required Evidence

- Metric, workload, baseline, environment, toolchain, profile, features, target, and correctness oracle.
- Profile or counter evidence identifying the bottleneck and its share of cost.
- Repeated before-and-after results with variance and magnitude, not only a percentage.
- Functional equivalence checks, trade-offs, regression policy, and unmeasured deployment contexts.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-performance/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
