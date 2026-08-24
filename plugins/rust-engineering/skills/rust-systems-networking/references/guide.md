# Rust Systems Networking Field Guide

## eBPF Branch

Record program type, hook/attach point, kernel range, target architecture, verifier limits, helper availability, map ABI, event transport, privileges, load/attach/detach ownership, and userspace consumer behavior. Keep loops and memory access bounded and verifier-legible. Treat map keys and values as an explicit cross-boundary byte contract.

## DPDK Branch

Record EAL configuration, ports, queues, descriptors, mempool ownership, mbuf headroom/tailroom, offloads, RSS mapping, sockets, cores, huge pages, and shutdown order. Every RX result, clone, external buffer, enqueue, transmit completion, drop, and error path must end with exactly one valid ownership disposition.

## Lifecycle Questions

- Who owns a packet or event at this point?
- Can the next operation retain it, clone metadata, or transfer ownership?
- What returns the resource to its pool or detaches the kernel object on failure?
- Which CPU/queue may touch it, and which synchronization or affinity rule enforces that?
- What happens on a partial burst, full TX queue, consumer lag, attach failure, or shutdown?

## Verification

- Compile host and target halves separately where applicable.
- Validate struct size, alignment, endian interpretation, and generated/bindgen ABI against the target.
- Run verifier/load tests on the supported kernel; record rejection logs.
- Exercise partial-burst and cleanup paths without hardware through dependency-free models where possible.
- Benchmark only on stated NIC/CPU/NUMA/topology and traffic distributions.

## Compiling Example

The dependency-free fixture in `../examples/golden/` models bounded packet ownership through receive, process, transmit, retry, and recycle outcomes. It intentionally avoids claiming DPDK hardware execution.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-dpdk`](./dpdk.md) — primary; Mempools, mbuf ownership, queues, burst processing, RSS, NUMA placement, affinity, and bounded packet-resource lifecycles.
- [`rust-ebpf`](./ebpf.md) — primary; Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
