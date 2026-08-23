# Low-level Branch Prediction And Speculation protocol

<!-- low-level-source-family: branch-prediction-and-speculation; source=skills/computer-architecture/branch-prediction-and-speculation/SKILL.md; sha256=0bae80935a364246723f06e8b4a88f8f8a3598eefd0c2723518f0ad0ed69822b; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/computer-architecture/branch-prediction-and-speculation/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-architecture`, `$rust-research`.
- Retained scope: Predictability, branch layout, misprediction measurement, speculation, and side-channel constraints.
- Baseline correction: Compiler hints and branchless rewrites are conditional. Security-sensitive constant-time behavior and runtime performance require separate, target-specific evidence.
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

- `Branch predictor basics` — inspect when relevant; source `skills/computer-architecture/branch-prediction-and-speculation/SKILL.md`.
- `Performance patterns` — inspect when relevant; source `skills/computer-architecture/branch-prediction-and-speculation/SKILL.md`.
- `Compiler hints (use sparingly)` — inspect when relevant; source `skills/computer-architecture/branch-prediction-and-speculation/SKILL.md`.
- `Speculative execution and side channels` — inspect when relevant; source `skills/computer-architecture/branch-prediction-and-speculation/SKILL.md`.
- `Measurement` — inspect when relevant; source `skills/computer-architecture/branch-prediction-and-speculation/SKILL.md`.
- `Agent usage` — inspect when relevant; source `skills/computer-architecture/branch-prediction-and-speculation/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 6 unique source block bodies: 6 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.
- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
