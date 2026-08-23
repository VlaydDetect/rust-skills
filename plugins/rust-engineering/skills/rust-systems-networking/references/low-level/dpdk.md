# Low-level Dpdk protocol

<!-- low-level-source-family: dpdk; source=skills/async-io/dpdk/SKILL.md; sha256=4786f104619ba02f57671537ceadf8bc59d65b68b3aedc871b8f5213fdbacf2a; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/async-io/dpdk/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-systems-networking`.
- Supporting profiles: `$rust-unsafe`, `$rust-performance`.
- Retained scope: EAL, huge pages, PMDs, mempools/mbufs, RX/TX bursts, rings, RSS, NUMA, affinity, and pipeline topology.
- Baseline correction: Merge only concepts not already owned by the Huiali protocol. Binding APIs, device arguments, huge pages, queue counts, and core maps are target-specific and require exact evidence.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- kernel/NIC/driver/CPU/NUMA.
- privileges and deployment.
- resolved binding/library version.
- queue/ring/buffer topology.
- overload, shutdown and cleanup.

## Decision protocol

1. Select the kernel-verifier, AF_XDP, or DPDK execution model before applying rules.
2. Draw every buffer/frame/map/event ownership transition through receive, queue, drop, transmit and detach.
3. Record ring capacities, queue/core placement, batching and backpressure/drop behavior.
4. Prove FFI layout, alignment, lifetime and thread-affinity at the binding boundary.
5. Measure on the real target; classify host-only or hardware-free examples as fragments.

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Huge pages setup` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.
- `EAL initialization` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.
- `Port configuration and PMD` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.
- `RX/TX burst loop` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.
- `rte_ring for inter-core queues` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.
- `RSS configuration` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.
- `testpmd validation` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.
- `QEMU virtio testing` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.
- `Pipeline vs run-to-completion` — inspect when relevant; source `skills/async-io/dpdk/SKILL.md`.

## Failure modes and guardrails

- Zero-copy still has ownership, synchronization and cleanup transitions.
- Queue/core/NUMA constants are not portable.
- Crate compilation does not prove verifier, driver or device acceptance.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 11 unique source block bodies: 8 `fragment`, 3 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; `current-beta`, reviewed 2026-08-23.
- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
