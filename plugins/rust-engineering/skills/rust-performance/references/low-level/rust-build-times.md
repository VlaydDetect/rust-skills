# Low-level Rust Build Times protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-cargo-build`, `$rust-research`.
- Retained scope: Clean and incremental build measurement, Cargo timings, invalidation, monomorphization, caching, codegen backends, and linking.
- Baseline correction: Derive report and artifact locations from Cargo metadata. Cranelift, linker swaps, crate splitting, cache services, and profile changes are experiments, never universal speedups.
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

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Diagnose with cargo-timings` — inspect when relevant; source `skills/rust/rust-build-times/SKILL.md`.
- `sccache — compilation caching for Rust` — inspect when relevant; source `skills/rust/rust-build-times/SKILL.md`.
- `Cranelift codegen backend` — inspect when relevant; source `skills/rust/rust-build-times/SKILL.md`.
- `Workspace splitting for parallelism` — inspect when relevant; source `skills/rust/rust-build-times/SKILL.md`.
- `LTO configuration` — inspect when relevant; source `skills/rust/rust-build-times/SKILL.md`.
- `Fast linkers` — inspect when relevant; source `skills/rust/rust-build-times/SKILL.md`.
- `Other quick wins` — inspect when relevant; source `skills/rust/rust-build-times/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 10 unique source block bodies: 4 `fragment`, 6 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-timings`](https://doc.rust-lang.org/stable/cargo/reference/timings.html) — Cargo timings output and interpretation; `stable`, reviewed 2026-08-23.
- [`cargo-metadata`](https://doc.rust-lang.org/nightly/cargo/commands/cargo-metadata.html) — Machine-readable workspace, target directory, and resolved packages; `stable-format-v1`, reviewed 2026-08-23.
- [`cargo-build-cache`](https://doc.rust-lang.org/cargo/reference/build-cache.html) — Cargo target/build directories and artifact layout; `stable`, reviewed 2026-08-23.
- [`cargo-build-performance`](https://doc.rust-lang.org/cargo/guide/build-performance.html) — Measured Rust build-performance guidance; `stable`, reviewed 2026-08-23.
- [`cargo-unstable`](https://doc.rust-lang.org/cargo/reference/unstable.html) — Cargo unstable feature gates including codegen backends; `nightly`, reviewed 2026-08-23.
- [`sccache-rust`](https://github.com/mozilla/sccache/blob/main/docs/Rust.md) — Rust compiler-wrapper caching and limitations; `resolved-version`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
