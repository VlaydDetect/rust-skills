# Low-level Virtual Memory Paging And Tlb protocol

<!-- low-level-source-family: virtual-memory-paging-and-tlb; source=skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md; sha256=7cbb03f2e2e4084c76a9fd27760486199f1b82d37be5f370b2cd85ab0e7fcf5e; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-architecture`, `$rust-research`.
- Retained scope: Page translation, faults, TLB pressure, huge pages, mapping evidence, and embedded contrasts.
- Baseline correction: Page-table shape, page size, huge-page policy, counters, and kernel interfaces are target/OS facts. Do not request huge pages or host configuration automatically.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- metric and correctness contract.
- representative workload and data.
- target/profile/features/toolchain.
- hardware, kernel and load controls.
- baseline distribution and retained raw evidence.

## Decision protocol

1. Classify CPU, allocation, I/O, contention, binary-size, or build-time cost before choosing a tool.
2. Capture a comparable baseline and preserve raw samples, counters, reports, or build timings.
3. Use one profiler or counter set to locate a bottleneck; treat attribution as a hypothesis with tool limitations.
4. Change one variable and rerun the same workload and correctness checks.
5. Reject noise-level wins and report unmeasured targets, cold/warm state, tail behavior, and new complexity.

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Translation overview` — inspect when relevant; source `skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md`.
- `Page table (x86-64 4-level example)` — inspect when relevant; source `skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md`.
- `Page fault types (simplified)` — inspect when relevant; source `skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md`.
- `TLB pressure` — inspect when relevant; source `skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md`.
- `Embedded contrast (Cortex-M)` — inspect when relevant; source `skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md`.
- `Userspace inspection (Linux)` — inspect when relevant; source `skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md`.
- `Agent usage` — inspect when relevant; source `skills/computer-architecture/virtual-memory-paging-and-tlb/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 5 unique source block bodies: 5 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.
- [`perf-security`](https://docs.kernel.org/admin-guide/perf-security.html) — perf privilege and data-exposure boundary; `kernel-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
