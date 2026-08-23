# Low-level Build Acceleration protocol

<!-- low-level-source-family: build-acceleration; source=skills/build-systems/build-acceleration/SKILL.md; sha256=b2dd7de62557f531e14028e0b9d65279b577d934f434d04d12208f3a56fdbfd7; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/build-systems/build-acceleration/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-cargo-build`, `$rust-research`.
- Retained scope: Bottleneck diagnosis, compiler caches, distributed compilation, debug information, invalidation, hit-rate analysis, and cache correctness.
- Baseline correction: For Rust, prefer the existing Cargo/sccache path. Cache credentials, remote backends, C/C++ PCH/unity, and distcc are conditional and never automatic product defaults.
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

- `Table of Contents` — inspect when relevant; source `skills/build-systems/build-acceleration/references/ccache-config.md`.
- `Configuration File Locations` — inspect when relevant; source `skills/build-systems/build-acceleration/references/ccache-config.md`.
- `Key Settings` — inspect when relevant; source `skills/build-systems/build-acceleration/references/ccache-config.md`.
- `CI / Shared Cache` — inspect when relevant; source `skills/build-systems/build-acceleration/references/ccache-config.md`.
- `Troubleshooting Hit Rate` — inspect when relevant; source `skills/build-systems/build-acceleration/references/ccache-config.md`.
- `Diagnose the bottleneck first` — inspect when relevant; source `skills/build-systems/build-acceleration/SKILL.md`.
- `ccache — compiler cache` — inspect when relevant; source `skills/build-systems/build-acceleration/SKILL.md`.
- `sccache — cloud-compatible cache (Rust, C/C++)` — inspect when relevant; source `skills/build-systems/build-acceleration/SKILL.md`.
- `Precompiled headers (PCH)` — inspect when relevant; source `skills/build-systems/build-acceleration/SKILL.md`.
- `Unity / jumbo builds` — inspect when relevant; source `skills/build-systems/build-acceleration/SKILL.md`.
- `split-DWARF — reduce link time` — inspect when relevant; source `skills/build-systems/build-acceleration/SKILL.md`.
- `distcc — distributed compilation` — inspect when relevant; source `skills/build-systems/build-acceleration/SKILL.md`.
- `Include pruning with IWYU` — inspect when relevant; source `skills/build-systems/build-acceleration/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 16 unique source block bodies: 12 `fragment`, 4 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-build-performance`](https://doc.rust-lang.org/cargo/guide/build-performance.html) — Measured Rust build-performance guidance; `stable`, reviewed 2026-08-23.
- [`cargo-build-cache`](https://doc.rust-lang.org/cargo/reference/build-cache.html) — Cargo target/build directories and artifact layout; `stable`, reviewed 2026-08-23.
- [`sccache-rust`](https://github.com/mozilla/sccache/blob/main/docs/Rust.md) — Rust compiler-wrapper caching and limitations; `resolved-version`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
