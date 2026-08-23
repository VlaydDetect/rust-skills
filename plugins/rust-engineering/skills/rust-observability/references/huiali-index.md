# Huiali references for `rust-observability`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-ebpf`](../../rust-systems-networking/references/huiali/rust-ebpf.md) — supporting; Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.
- [`rust-middleware`](../../rust-architecture/references/huiali/rust-middleware.md) — supporting; Request pipelines, ordering, short-circuiting, context propagation, cancellation, retries, timeouts, and cross-cutting policy.
- [`rust-observability`](huiali/rust-observability.md) — primary; Structured events, spans, metrics, correlation, cardinality, redaction, sampling, and operational failure evidence.
- [`rust-performance`](../../rust-performance/references/huiali/rust-performance.md) — supporting; Baselines, profiling, allocation, cache behavior, batching, contention, latency distributions, throughput, and regression evidence.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
