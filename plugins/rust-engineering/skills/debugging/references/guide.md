# Rust Debugging Field Guide

This guide is the detailed policy for `debugging`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- A debugging record needs symptom, context, reproducer, hypothesis, discriminating observation, and conclusion.
- Compiler diagnostics often cascade; fix or isolate the earliest primary error before interpreting later messages.
- Delta debugging removes dimensions while holding the failure predicate constant.
- Differential diagnosis compares good and bad builds, features, targets, inputs, or schedules.
- Concurrency tools explore schedules or memory rules, but no single tool proves absence of all races or undefined behavior.
- The best regression test fails for the root cause and stays stable when incidental implementation details change.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Borrow checker diagnostic | Minimize ownership and lifetime flow | Later type errors may be cascades |
| Intermittent async hang | Bound execution and inspect waits or cancellation | A timeout localizes liveness without treating it as correctness |
| Release-only crash | Compare codegen assumptions and unsafe paths | Optimization can expose UB or timing, not create valid semantics |
| Target-specific failure | Compare cfg, ABI, dependencies, and target data layout | Host success does not cover target contracts |
| Performance regression | Reproduce with the same benchmark environment | Uncontrolled baselines produce false causes |

## Common Failure Modes

- Editing several suspected causes at once and losing the discriminating experiment.
- Testing only the happy-path package while the failing CI job uses different features or targets.
- Treating a timeout, retry, clone, or larger buffer as a root-cause fix.
- Using logging that changes task scheduling and then declaring a race gone.
- Reducing the example until the original invariant or failure disappears.

## Required Evidence

- An exact reproduction command and observed output or a precise statement of why reproduction is unavailable.
- A minimized causal path with at least one hypothesis rejected by observation.
- Tool findings interpreted within tool limitations rather than as universal proof.
- A proposed regression check tied to the triggering condition and expected behavior.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-performance`](../../rust-performance/references/performance.md) — supporting; Baselines, profiling, allocation, cache behavior, batching, contention, latency distributions, throughput, and regression evidence.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
