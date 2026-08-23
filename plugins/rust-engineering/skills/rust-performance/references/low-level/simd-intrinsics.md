# Low-level Simd Intrinsics protocol

<!-- low-level-source-family: simd-intrinsics; source=skills/low-level-programming/simd-intrinsics/SKILL.md; sha256=bb64c77432fc9ec3a6d5dec3bcbeb10ef538ec7f3d3cc2a7a3a62eb8002affce; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/low-level-programming/simd-intrinsics/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-unsafe`, `$rust-stable`.
- Retained scope: Auto-vectorization, runtime feature detection, x86 and ARM intrinsics, alignment, dispatch, scalar fallbacks, and generated assembly.
- Baseline correction: Intrinsics require supported target features and local unsafe proofs. Never compile a baseline binary for target-cpu=native when it must run on different CPUs.
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

- `x86 Header Files` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/references/intel-intrinsics-guide.md`.
- `x86 Vector Types` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/references/intel-intrinsics-guide.md`.
- `SSE2 / AVX2 Float Intrinsics` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/references/intel-intrinsics-guide.md`.
- `AVX2 Integer Intrinsics (Common)` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/references/intel-intrinsics-guide.md`.
- `ARM NEON Types` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/references/intel-intrinsics-guide.md`.
- `NEON Load/Store/Arithmetic` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/references/intel-intrinsics-guide.md`.
- `Compiler Feature Guards` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/references/intel-intrinsics-guide.md`.
- `Online Resources` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/references/intel-intrinsics-guide.md`.
- `Check auto-vectorization` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/SKILL.md`.
- `Runtime CPU feature detection` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/SKILL.md`.
- `SSE2 / SSE4.2 intrinsics (x86)` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/SKILL.md`.
- `AVX2 intrinsics (x86)` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/SKILL.md`.
- `NEON intrinsics (ARM/AArch64)` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/SKILL.md`.
- `Choose auto-vectorization vs intrinsics` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/SKILL.md`.
- `Alignment and performance` — inspect when relevant; source `skills/low-level-programming/simd-intrinsics/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 11 unique source block bodies: 11 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; `current-beta`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
