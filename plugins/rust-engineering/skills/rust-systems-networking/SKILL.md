---
name: rust-systems-networking
description: Design and review Rust eBPF and DPDK execution environments, including verifier-safe programs, maps and kernel ABI, packet buffer ownership, mempools, queues, bursts, RSS, NUMA placement, affinity, and bounded zero-copy lifecycles.
---

# Rust Systems Networking

Own execution-environment constraints for kernel eBPF and userspace packet pipelines. Route to the eBPF or DPDK branch; do not blend their memory and failure models.

## Use This Skill When

- An eBPF program, XDP path, probe, map, verifier rejection, kernel/user ABI, or attachment lifecycle is involved.
- A DPDK pipeline uses mempools, mbufs, RX/TX queues, bursts, RSS, huge pages, NUMA placement, or CPU affinity.
- Zero-copy or line-rate claims depend on explicit buffer ownership and hardware topology.

## Workflow

1. Select the environment: verifier-governed kernel program or polled userspace packet pipeline.
2. Record kernel/driver/NIC/CPU/NUMA, target architecture, privileges, attachment, deployment, and resolved binding versions.
3. Draw the packet or event resource lifecycle from allocation/receipt through every handoff, queue, drop, transmit, detach, and shutdown path.
4. Define bounded work, queue capacity, overload/drop behavior, CPU placement, and ABI/layout constraints.
5. Isolate unsafe and foreign calls; prove ownership, aliasing, alignment, and thread-affinity requirements.
6. Verify on the real target when available and label hardware- or dependency-specific source snippets as fragments otherwise.

## Decision Rules

- eBPF acceptance is controlled by the kernel verifier and program-type rules; ordinary Rust compilation is not sufficient evidence.
- Verify Aya or another binding against the exact resolved version; source examples do not establish current API syntax.
- An mbuf has one lifecycle owner at a time even when payload data is shared or externally referenced.
- Queue/core/NUMA placement is a hardware decision, not a portable constant.
- Burst size trades latency, cache behavior, and throughput; measure on representative traffic.
- Zero-copy does not mean zero ownership transitions, synchronization, cache misses, or cleanup obligations.

## Boundaries and Hand-offs

- `rust-observability` owns telemetry semantics; this profile owns eBPF probe constraints and attachment lifecycle.
- `rust-unsafe` owns pointer, FFI, and layout proofs; `rust-performance` owns measured optimization.
- `rust-architecture` owns the wider service boundary and deployment contract.
- Use `rust-research` for exact Aya, DPDK, binding, kernel, and device facts.

## Detailed Reference

Read [Systems Networking field guide](references/guide.md), then load only the conditional [`rust-ebpf`](references/huiali/rust-ebpf.md) or [`rust-dpdk`](references/huiali/rust-dpdk.md) Huiali protocol.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.

## Low-level protocols

For source-derived debugging, profiling, build, sanitizer, cross-target, ABI, async-internal, security, or hardware detail relevant to this profile, read the [Low-level integration index](references/low-level-index.md) and load only the matching family. Apply its official-evidence and command-safety gate before execution.
