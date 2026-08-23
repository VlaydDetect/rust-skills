# Low-level Af Xdp protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-systems-networking`.
- Supporting profiles: `$rust-unsafe`, `$rust-performance`.
- Retained scope: UMEM ownership, fill/completion and RX/TX rings, XDP redirect, copy/zero-copy modes, queue binding, and packet lifecycle.
- Baseline correction: Kernel, libbpf/binding, NIC, driver, queue, privilege, and zero-copy support are required evidence. Preserve a bounded owner transition for every frame.
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

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Architecture overview` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.
- `UMEM and XSK socket creation` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.
- `Populate fill ring` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.
- `XDP redirect program` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.
- `RX processing loop` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.
- `Copy vs zero-copy` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.
- `libbpf xsk.h helpers` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.
- `Performance vs DPDK` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.
- `Production patterns` — inspect when relevant; source `skills/async-io/af-xdp/SKILL.md`.

## Failure modes and guardrails

- Zero-copy still has ownership, synchronization and cleanup transitions.
- Queue/core/NUMA constants are not portable.
- Crate compilation does not prove verifier, driver or device acceptance.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 10 unique source block bodies: 10 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; `current-beta`, reviewed 2026-08-23.
- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
