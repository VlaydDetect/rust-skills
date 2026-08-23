# Low-level Rust Unsafe protocol

<!-- low-level-source-family: rust-unsafe; source=skills/rust/rust-unsafe/SKILL.md; sha256=96450d41663e02071ca414edbe89e1fd3b779139ce945726c48e665a838f934b; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/rust-unsafe/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-unsafe`.
- Supporting profiles: `$rust-testing`, `$rust-verify`.
- Retained scope: Unsafe operations, raw pointers, traits, safe wrappers, transmute, UnsafeCell, provenance, aliasing, initialization, and drop.
- Baseline correction: Each operation needs a local proof of its exact preconditions. Tool success supports but never replaces the proof, and unsafe is not a default optimization technique.
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

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `The Unsafe Contract` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Raw Pointer Patterns` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `NonNull — non-null raw pointer wrapper` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Pointer arithmetic` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Read/Write without creating references` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Safe Abstraction Patterns` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Invariant-based safety` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Pin and self-referential structs` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Transmute Safety Table` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Miri Testing for Unsafe` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `clippy for Unsafe` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `Stacked Borrows Rules (Miri model)` — inspect when relevant; source `skills/rust/rust-unsafe/references/unsafe-patterns.md`.
- `The five unsafe superpowers` — inspect when relevant; source `skills/rust/rust-unsafe/SKILL.md`.
- `Raw pointers` — inspect when relevant; source `skills/rust/rust-unsafe/SKILL.md`.
- `unsafe functions and traits` — inspect when relevant; source `skills/rust/rust-unsafe/SKILL.md`.
- `Safe abstractions over unsafe` — inspect when relevant; source `skills/rust/rust-unsafe/SKILL.md`.
- `transmute` — inspect when relevant; source `skills/rust/rust-unsafe/SKILL.md`.
- `UnsafeCell — interior mutability` — inspect when relevant; source `skills/rust/rust-unsafe/SKILL.md`.
- `Unsafe audit checklist` — inspect when relevant; source `skills/rust/rust-unsafe/SKILL.md`.
- `When to use unsafe` — inspect when relevant; source `skills/rust/rust-unsafe/SKILL.md`.

## Failure modes and guardrails

- Miri explores concrete executions, not all inputs or schedules.
- Sanitizer support is mode- and target-specific and normally nightly.
- C/C++ UBSan recipes are not a Rust sanitizer mode.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 16 unique source block bodies: 16 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; `nightly-version-sensitive`, reviewed 2026-08-23.
- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
