# Low-level Fuzzing protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-testing`.
- Supporting profiles: `$rust-unsafe`, `$rust-verify`.
- Retained scope: Target design, corpus, dictionary, crash reproduction, minimization, sanitizer composition, structure-aware inputs, and bounded CI campaigns.
- Baseline correction: Use the project's existing fuzz harness and pinned tooling. Installation, long-running campaigns, corpus upload, OSS-Fuzz onboarding, and network actions require explicit authorization.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- input boundary and invariant.
- existing harness and engine version.
- corpus/dictionary/seeds.
- time and resource budget.
- crash artifact handling.

## Decision protocol

1. Choose a narrow target that converts bytes into a meaningful operation without hiding panics or hangs.
2. Seed valid structure, preserve and minimize crashes, and add each confirmed defect as a deterministic regression.
3. Compose sanitizers only where the current Rust/target documentation permits it.
4. Bound campaign time, memory, artifact retention and CI scope.
5. Treat coverage growth as guidance; assert the actual safety or behavior contract separately.

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Table of Contents` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `libFuzzer flags reference` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Common flags` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Corpus minimisation` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `AFL++ flags reference` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Core flags` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Multi-instance parallelism` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Status and output` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Writing good fuzz targets` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Anatomy of a libFuzzer target` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `What NOT to do in a fuzz target` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Custom mutator (libFuzzer)` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Corpus management` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Seeding the corpus` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Corpus minimisation (libFuzzer)` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Corpus deduplication (AFL++)` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Measure coverage of corpus` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Dictionary format` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Sanitizer combinations for fuzzing` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `CI integration patterns` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Short regression run (every PR)` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Long-running fuzzing (scheduled / nightly)` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `OSS-Fuzz integration` — inspect when relevant; source `skills/runtimes/fuzzing/references/targets.md`.
- `Write a fuzz target (libFuzzer)` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Build with libFuzzer` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Run libFuzzer` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Reproduce a crash` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `AFL++ setup` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `AFL++ with persistent mode (faster)` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Corpus management` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `CI integration` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Structure-aware fuzzing (libFuzzer)` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Atheris (Python fuzzing)` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Dataflow tracing` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `OSS-Fuzz integration` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Zig fuzz testing` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.
- `Dictionary files` — inspect when relevant; source `skills/runtimes/fuzzing/SKILL.md`.

## Failure modes and guardrails

- Random input without invariants produces weak signal.
- Fuzz engines, flags and corpus formats are version-specific.
- Long-running or uploaded campaigns require explicit authorization.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 34 unique source block bodies: 32 `fragment`, 2 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-23.
- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; `nightly-version-sensitive`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
