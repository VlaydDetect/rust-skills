# Huiali references for `rust-performance`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-cache`](../../rust-architecture/references/huiali/rust-cache.md) — supporting; Cache ownership, key identity, freshness, invalidation, stampede control, capacity, failure behavior, and observability.
- [`rust-concurrency`](../../rust-concurrency/references/huiali/rust-concurrency.md) — supporting; Send/Sync, shared-state and message-passing choices, atomics, lock scope, thread/task ownership, cancellation, and shutdown.
- [`rust-const`](../../rust-stable/references/huiali/rust-const.md) — supporting; Const evaluation, const fn, const generics, compile-time constraints, static data, and supported-toolchain limits.
- [`rust-database`](../../rust-architecture/references/huiali/rust-database.md) — supporting; Persistence boundaries, transactions, consistency, schema evolution, query ownership, pooling, and error translation.
- [`rust-dpdk`](../../rust-systems-networking/references/huiali/rust-dpdk.md) — supporting; Mempools, mbuf ownership, queues, burst processing, RSS, NUMA placement, affinity, and bounded packet-resource lifecycles.
- [`rust-ebpf`](../../rust-systems-networking/references/huiali/rust-ebpf.md) — supporting; Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.
- [`rust-gpu`](../../rust-gpu/references/huiali/rust-gpu.md) — supporting; Device capabilities, memory hierarchy, transfer cost, alignment, coalescing, batching, synchronization, and measurement.
- [`rust-observability`](../../rust-observability/references/huiali/rust-observability.md) — supporting; Structured events, spans, metrics, correlation, cardinality, redaction, sampling, and operational failure evidence.
- [`rust-performance`](huiali/rust-performance.md) — primary; Baselines, profiling, allocation, cache behavior, batching, contention, latency distributions, throughput, and regression evidence.
- [`rust-zero-cost`](huiali/rust-zero-cost.md) — primary; Static versus dynamic dispatch, monomorphization, iterators, abstraction boundaries, code size, allocation, and measured runtime cost.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
