# Low-level Intel Vtune Amd Uprof protocol

<!-- low-level-source-family: intel-vtune-amd-uprof; source=skills/profilers/intel-vtune-amd-uprof/SKILL.md; sha256=45ea01cb6c55202b16c53e7d8dd86a3a99be17237fbfc934168f121be7f4b3b2; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/profilers/intel-vtune-amd-uprof/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$debugging`, `$rust-research`.
- Retained scope: Vendor profiler selection, hotspots, microarchitecture, memory access, pipeline stalls, and roofline reasoning.
- Baseline correction: Availability, permissions, event semantics, and hardware support are vendor/version-specific. Do not install drivers or claim portability from a different CPU.
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

- `VTune setup (free Community Edition)` — inspect when relevant; source `skills/profilers/intel-vtune-amd-uprof/SKILL.md`.
- `Analysis types` — inspect when relevant; source `skills/profilers/intel-vtune-amd-uprof/SKILL.md`.
- `Hotspot analysis` — inspect when relevant; source `skills/profilers/intel-vtune-amd-uprof/SKILL.md`.
- `Microarchitecture exploration — pipeline stalls` — inspect when relevant; source `skills/profilers/intel-vtune-amd-uprof/SKILL.md`.
- `Memory access analysis` — inspect when relevant; source `skills/profilers/intel-vtune-amd-uprof/SKILL.md`.
- `AMD uProf — free alternative for AMD CPUs` — inspect when relevant; source `skills/profilers/intel-vtune-amd-uprof/SKILL.md`.
- `Roofline model` — inspect when relevant; source `skills/profilers/intel-vtune-amd-uprof/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 10 unique source block bodies: 10 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
