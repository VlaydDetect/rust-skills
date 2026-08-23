# Low-level Pgo protocol

<!-- low-level-source-family: pgo; source=skills/compilers/pgo/SKILL.md; sha256=f9ca19583809996dcd5977e82346c71a0a39ce921dc2ba8dc5cbd58dfc664d1a; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/compilers/pgo/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-cargo-build`, `$rust-research`.
- Retained scope: Instrumentation or sample profile collection, workload representativeness, profile merge/use, post-link optimization, and impact verification.
- Baseline correction: Source commands are compiler-specific. Rust PGO and BOLT require current rustc/LLVM guidance, matching binaries, representative profiles, and before/after correctness and performance evidence.
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

- `GCC Profile Data Formats` — inspect when relevant; source `skills/compilers/pgo/references/pgo-workflow.md`.
- `Clang Profile Data Formats` — inspect when relevant; source `skills/compilers/pgo/references/pgo-workflow.md`.
- `llvm-profdata Commands` — inspect when relevant; source `skills/compilers/pgo/references/pgo-workflow.md`.
- `Context-Sensitive PGO (CS-PGO) Workflow` — inspect when relevant; source `skills/compilers/pgo/references/pgo-workflow.md`.
- `Workload Representativeness` — inspect when relevant; source `skills/compilers/pgo/references/pgo-workflow.md`.
- `BOLT Configuration Reference` — inspect when relevant; source `skills/compilers/pgo/references/pgo-workflow.md`.
- `Benchmarking Template` — inspect when relevant; source `skills/compilers/pgo/references/pgo-workflow.md`.
- `When to use PGO` — inspect when relevant; source `skills/compilers/pgo/SKILL.md`.
- `GCC PGO workflow` — inspect when relevant; source `skills/compilers/pgo/SKILL.md`.
- `Clang PGO workflow (IR-based, preferred)` — inspect when relevant; source `skills/compilers/pgo/SKILL.md`.
- `Clang SamplePGO (sampling, no instrumentation)` — inspect when relevant; source `skills/compilers/pgo/SKILL.md`.
- `CMake integration` — inspect when relevant; source `skills/compilers/pgo/SKILL.md`.
- `BOLT (post-link binary optimisation)` — inspect when relevant; source `skills/compilers/pgo/SKILL.md`.
- `Verifying PGO impact` — inspect when relevant; source `skills/compilers/pgo/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 12 unique source block bodies: 12 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`cargo-build-performance`](https://doc.rust-lang.org/cargo/guide/build-performance.html) — Measured Rust build-performance guidance; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
