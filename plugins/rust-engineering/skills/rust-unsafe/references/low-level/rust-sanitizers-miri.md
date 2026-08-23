# Low-level Rust Sanitizers Miri protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-unsafe`.
- Supporting profiles: `$rust-verify`, `$debugging`.
- Retained scope: Miri and Rust sanitizer selection, execution scope, report interpretation, unsafe-code validation, and residual proof obligations.
- Baseline correction: Rust does not expose an `undefined` sanitizer mode. Miri interprets concrete executions and neither Miri nor a sanitizer proves soundness across all inputs, targets, optimizations, FFI, or schedules.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- unsafe operation and safe caller contract.
- target and toolchain.
- executed input/schedule.
- FFI/native coverage.
- remaining manual invariants.

## Decision protocol

1. Write provenance, alignment, initialization, validity, aliasing, lifetime, layout, thread, panic and drop obligations.
2. Select Miri for supported MIR execution or a documented rustc sanitizer for a supported target and failure class.
3. Use the repository-pinned nightly when present; otherwise report the required evidence as unavailable instead of installing.
4. Minimize the reproducer and interpret the first causally relevant diagnostic.
5. Record what the run did not cover and keep the local safety proof authoritative.

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Undefined Behaviour Caught by Miri` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/references/miri-ub-patterns.md`.
- `Pointer provenance violations` — inspect when relevant and verify against the project toolchain and current Miri documentation.
- `Transmutation errors` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/references/miri-ub-patterns.md`.
- `Stacked Borrows violations` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/references/miri-ub-patterns.md`.
- `Uninitialized memory` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/references/miri-ub-patterns.md`.
- `Lifetime extension` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/references/miri-ub-patterns.md`.
- `MIRIFLAGS Quick Reference` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/references/miri-ub-patterns.md`.
- `Miri Limitations` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/references/miri-ub-patterns.md`.
- `Sanitizer Comparison for Rust` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/references/miri-ub-patterns.md`.
- `Sanitizers in Rust (nightly required)` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/SKILL.md`.
- `Stable sanitizer workaround` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/SKILL.md`.
- `Interpreting ASan output in Rust` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/SKILL.md`.
- `Miri — interpreter for undefined behaviour` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/SKILL.md`.
- `What Miri detects` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/SKILL.md`.
- `ThreadSanitizer for Rust` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/SKILL.md`.
- `Miri configuration via MIRIFLAGS` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/SKILL.md`.
- `CI integration` — inspect when relevant; source `skills/rust/rust-sanitizers-miri/SKILL.md`.

## Failure modes and guardrails

- Miri explores concrete executions, not all inputs or schedules.
- Sanitizer support is mode- and target-specific and normally nightly.
- C/C++ UBSan recipes are not a Rust sanitizer mode.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 15 unique source block bodies: 11 `fragment`, 4 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-23.
- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; `nightly-version-sensitive`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
