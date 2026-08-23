# Huiali references for `rust-unsafe`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-dpdk`](../../rust-systems-networking/references/huiali/rust-dpdk.md) — supporting; Mempools, mbuf ownership, queues, burst processing, RSS, NUMA placement, affinity, and bounded packet-resource lifecycles.
- [`rust-ebpf`](../../rust-systems-networking/references/huiali/rust-ebpf.md) — supporting; Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.
- [`rust-embedded`](../../rust-architecture/references/huiali/rust-embedded.md) — supporting; no_std constraints, HAL ownership, interrupts, bounded memory, timing, peripherals, power, and deterministic cleanup.
- [`rust-ffi`](../../rust-unsafe-ffi/references/huiali/rust-ffi.md) — supporting; ABI layout, ownership transfer, allocator pairing, strings, callbacks, panic containment, handles, and foreign-thread behavior.
- [`rust-pin`](../../rust-pin/references/huiali/rust-pin.md) — supporting; Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.
- [`rust-unsafe`](huiali/rust-unsafe.md) — primary; Unsafe preconditions, aliasing, initialization, layout, provenance, Send/Sync, panic safety, and safe-abstraction review.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
