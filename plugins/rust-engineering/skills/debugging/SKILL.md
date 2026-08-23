---
name: debugging
description: Diagnose Rust compile, test, runtime, async, concurrency, unsafe, performance, and integration failures by reproducing and shrinking the real cause. Use for unexplained failures; do not guess a patch before the failure model is established.
---

# Rust Debugging

Own causal diagnosis from symptom to minimal, evidence-backed failure mechanism. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A compiler diagnostic, failing test, panic, hang, race, leak, crash, or inconsistent behavior needs explanation.
- The apparent fix failed repeatedly or the symptom moves between layers.
- A bug is environment-, target-, feature-, timing-, or input-dependent.

## Workflow

1. Capture the exact symptom, expected behavior, command, input, toolchain, target, features, environment, and earliest known good state.
2. Reproduce with the narrowest existing command and preserve the complete diagnostic chain, including causes and backtrace when relevant.
3. Form one falsifiable hypothesis at a time, then choose an observation that distinguishes it from alternatives.
4. Shrink the reproducer across input, feature set, package, thread count, module, and commit boundary without changing the behavior under study.
5. Use targeted instrumentation, differential runs, bisecting, Miri, loom, sanitizers, or profiles only when the failure class justifies them.
6. State root cause, triggering conditions, why competing hypotheses failed, and the regression evidence a fix must add.

## Decision Rules

- Read the first causally relevant compiler error before downstream cascades.
- After three unsuccessful variants of the same fix, stop and redesign the diagnostic question.
- Do not change optimization level, timing, or input and then claim the original failure is fixed.
- Separate deterministic logic errors from races, deadlocks, resource exhaustion, and environmental failures.
- Instrument boundaries and invariants, not every line; excess logging can hide timing bugs.
- For unsafe failures, minimize safe code first and use Miri or sanitizers within their documented coverage.
- For async hangs, inspect cancellation, pending futures, lock scope, bounded queues, and runtime shutdown.
- A plausible explanation is not root cause until it predicts and reproduces the observed behavior.

## Boundaries and Hand-offs

- `rust-errors` owns error API design; debugging owns why a particular failure occurred.
- `rust-performance` owns measured optimization after correctness and the bottleneck are established.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Debugging field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
