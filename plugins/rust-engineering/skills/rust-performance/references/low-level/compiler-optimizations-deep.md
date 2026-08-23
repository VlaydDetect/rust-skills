# Low-level Compiler Optimizations Deep protocol

<!-- low-level-source-family: compiler-optimizations-deep; source=skills/compiler-internals/compiler-optimizations-deep/SKILL.md; sha256=47b1a844dca5df7da36934b9ea9d9f62194aa42a66e10dba4b6d1a5352efc8c2; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/compiler-internals/compiler-optimizations-deep/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-cargo-build`, `$rust-research`.
- Retained scope: Optimization pipeline, vectorization diagnostics, register pressure, loop transforms, PGO, BOLT, and generated-code evidence.
- Baseline correction: Do not infer LLVM pass behavior or vectorization from source shape. Inspect the actual compiler output and benchmark the supported target.
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

- `Compiler pipeline map` — inspect when relevant; source `skills/compiler-internals/compiler-optimizations-deep/SKILL.md`.
- `Vectorization failure triage` — inspect when relevant; source `skills/compiler-internals/compiler-optimizations-deep/SKILL.md`.
- `Register allocation intuition` — inspect when relevant; source `skills/compiler-internals/compiler-optimizations-deep/SKILL.md`.
- `PGO workflow (Clang)` — inspect when relevant; source `skills/compiler-internals/compiler-optimizations-deep/SKILL.md`.
- `BOLT (post-link)` — inspect when relevant; source `skills/compiler-internals/compiler-optimizations-deep/SKILL.md`.
- `LICM example` — inspect when relevant; source `skills/compiler-internals/compiler-optimizations-deep/SKILL.md`.
- `Agent usage` — inspect when relevant; source `skills/compiler-internals/compiler-optimizations-deep/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 5 unique source block bodies: 5 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`cargo-build-performance`](https://doc.rust-lang.org/cargo/guide/build-performance.html) — Measured Rust build-performance guidance; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
