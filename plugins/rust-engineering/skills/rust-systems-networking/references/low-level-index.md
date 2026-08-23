# Low-level references for `rust-systems-networking`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`af-xdp`](low-level/af-xdp.md) — primary; UMEM ownership, fill/completion and RX/TX rings, XDP redirect, copy/zero-copy modes, queue binding, and packet lifecycle.
- [`dpdk`](low-level/dpdk.md) — primary; EAL, huge pages, PMDs, mempools/mbufs, RX/TX bursts, rings, RSS, NUMA, affinity, and pipeline topology.
- [`ebpf-rust`](low-level/ebpf-rust.md) — primary; Kernel/user split, verifier constraints, program and map types, BTF/CO-RE, attachment, event transport, and load-failure diagnosis.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.
