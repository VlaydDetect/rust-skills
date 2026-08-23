# Huiali references for `rust-systems-networking`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-dpdk`](huiali/rust-dpdk.md) — primary; Mempools, mbuf ownership, queues, burst processing, RSS, NUMA placement, affinity, and bounded packet-resource lifecycles.
- [`rust-ebpf`](huiali/rust-ebpf.md) — primary; Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
