# Rust Optimization Decision Guide

## Start With a Decision, Not a Technique

Specify the unit of useful work, service or library boundary, representative distribution, primary metric, secondary budgets, and correctness oracle. Separate an observed regression from a new optimization opportunity. An unexplained failure starts with `debugging`; missing attribution or an invalid comparison starts with `rust-profiling`.

Produce a short hypothesis record:

| Field | Question |
|---|---|
| Evidence | Which absolute cost, call path, queue, or resource explains the current limit? |
| Mechanism | What work, indirection, serialization, or generated instruction would change? |
| Constraint | Which property makes this legal, where is it enforced, and can it change? |
| Prediction | Which metric should move, and what result would disprove the explanation? |
| Cost | What might worsen: memory, construction, updates, tails, startup, build, portability, or maintenance? |
| Acceptance | What effect is useful, which regressions are unacceptable, and what uncertainty remains? |

Do not impose a large form on a one-line change. Record only the facts that control the decision. Missing evidence should select an experiment, not a speculative implementation.

## Rank Candidate Changes

| Evidence | Candidate | Check before choosing | Disconfirming result |
|---|---|---|---|
| Repeated work dominates | Remove, precompute, or batch work | Input stability, invalidation, memory and latency budgets | Work moves to another frequent path or tails regress |
| Expensive search or traversal | Change algorithm, index, or traversal direction | Size distribution, key space, misses, ordering, update mix | Representative operations do not improve |
| Allocations or dependent loads dominate | Simplify ownership or representation, reuse a buffer | Lifetime, growth, address stability, peak retention | Allocation count falls but working set or elapsed cost rises |
| Shared state serializes progress | Narrow ownership/critical section, clone small cursors, partition state | Consistency, contention, cancellation, skew | Parallelism increases but bandwidth or queueing dominates |
| Instruction or branch bottleneck remains | Reshape a loop, specialize, vectorize, or evaluate PGO | Actual codegen, target fleet, code size and dispatch | Larger code or dispatch costs erase the local gain |

Use rough upper bounds to avoid low-value work. If a serial operation accounts for fraction `f` of elapsed work and becomes `s` times faster, `1 / ((1 - f) + f / s)` is an upper-bound model only under those serial assumptions. Sampled CPU share is not automatically `f`; overlapping I/O, contention, saturation, and queueing require a critical-path or resource model.

## Preserve the Full Contract

Read callers, constructors, mutation paths, tests, and persistence or wire boundaries. An observed small collection is not a maximum-size guarantee. A trusted internal key does not prove every future caller is trusted. An implementation's current layout is not a stable ABI or serialization format.

Prefer a private representation change behind the existing API when possible. Changes to public signatures, durable bytes, address stability, iteration order, floating-point results, or failure behavior need their owning profile and explicit compatibility treatment. Never hide a semantic relaxation inside a performance patch.

## Generated Code and Unsafe

Inspect the same target, concrete generic instantiation, features, profile, and flags as the measured artifact. Check the caller when inlining or LTO changes the final body; a standalone function's assembly can be misleading. Confirm the hot bounds-check or dispatch path exists before removing it.

For unchecked indexing, prove the full index range against the exact slice, including empty inputs, integer overflow, and all mutation paths. Validate untrusted dimensions before the unsafe block. A safe wrapper must enforce its contract in release builds; an unsafe API must document all caller obligations. Mutable references also require non-overlap and aliasing reasoning. Do not execute an invalid unsafe call as a negative test: test that the safe boundary rejects it.

The existing [golden fixture](../../rust-performance/examples/golden/) compares a safe iterator with a validated unchecked loop using defined wrapping arithmetic. It demonstrates a local proof and parity tests, not an established speedup. `rust-unsafe` remains authoritative for soundness and [Miri/sanitizer coverage](../../rust-unsafe/references/low-level/rust-sanitizers-miri.md).

## Finish the Experiment

Use [benchmark analysis](../../rust-profiling/references/benchmark-analysis.md) for comparable estimates and uncertainty. Recheck end-to-end behavior, stage costs, construction/destruction, memory, and relevant neighboring inputs. Keep raw evidence and the artifact identity. A local speedup with no established system benefit is a local result; an inconclusive or unjustifiably complex candidate should be rejected without manufacturing a positive conclusion.
