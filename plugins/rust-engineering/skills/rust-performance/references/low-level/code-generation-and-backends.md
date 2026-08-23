# Low-level Code Generation And Backends protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-cargo-build`, `$rust-research`.
- Retained scope: Compiler pipeline, LLVM lowering, target triples, calling-convention lowering, backend selection, and new-target feasibility.
- Baseline correction: LLVM utilities and target-backend authoring are not Cargo workflows. Cranelift and alternative backends remain toolchain- and target-gated experiments.
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

- `Backend pipeline (LLVM)` — inspect when relevant; source `skills/compiler-internals/code-generation-and-backends/SKILL.md`.
- `llc usage` — inspect when relevant; source `skills/compiler-internals/code-generation-and-backends/SKILL.md`.
- `TableGen patterns (conceptual)` — inspect when relevant; source `skills/compiler-internals/code-generation-and-backends/SKILL.md`.
- `Calling convention lowering` — inspect when relevant; source `skills/compiler-internals/code-generation-and-backends/SKILL.md`.
- `Target triple` — inspect when relevant; source `skills/compiler-internals/code-generation-and-backends/SKILL.md`.
- `Adding a target (outline)` — inspect when relevant; source `skills/compiler-internals/code-generation-and-backends/SKILL.md`.
- `Agent usage` — inspect when relevant; source `skills/compiler-internals/code-generation-and-backends/SKILL.md`.

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
- [`cargo-unstable`](https://doc.rust-lang.org/cargo/reference/unstable.html) — Cargo unstable feature gates including codegen backends; `nightly`, reviewed 2026-08-23.
- [`cargo-build-performance`](https://doc.rust-lang.org/cargo/guide/build-performance.html) — Measured Rust build-performance guidance; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
