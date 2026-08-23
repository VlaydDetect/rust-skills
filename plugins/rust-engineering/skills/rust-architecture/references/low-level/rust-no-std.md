# Low-level Rust No Std protocol

<!-- low-level-source-family: rust-no-std; source=skills/rust/rust-no-std/SKILL.md; sha256=41f4c5d8561ce5059d814f91f94a42ea5012aa6c904aee5293d66b0d45c78f5f; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/rust-no-std/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-architecture`.
- Supporting profiles: `$rust-cargo-build`, `$rust-unsafe`.
- Retained scope: core/alloc/std capability boundaries, allocator and panic ownership, portable libraries, target configuration, and host-side testing.
- Baseline correction: Do not infer absence of allocation, a panic strategy, allocator, HAL, executor, or target layout merely from no_std. Separate library portability from final binary runtime requirements.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- deployment and trust boundary.
- target capabilities.
- resource and failure budget.
- external effects and supply inputs.
- required portability and maintenance policy.

## Decision protocol

1. Start from the threat, resource, platform or portability constraint rather than a named tool.
2. Separate domain policy from build, target, telemetry, security and hardware adapters.
3. Identify unavailable std/platform capabilities and assign explicit owners for allocation, panic, time, I/O and cleanup.
4. Route dependency policy, unsafe proof, fuzzing and artifact hardening to their existing owners.
5. Prove one target-specific vertical slice and document what host-only evidence cannot establish.

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `no_std crate structure` — inspect when relevant; source `skills/rust/rust-no-std/SKILL.md`.
- `core vs alloc vs std` — inspect when relevant; source `skills/rust/rust-no-std/SKILL.md`.
- `Custom global allocator` — inspect when relevant; source `skills/rust/rust-no-std/SKILL.md`.
- `Panic handler` — inspect when relevant; source `skills/rust/rust-no-std/SKILL.md`.
- `Writing portable no_std libraries` — inspect when relevant; source `skills/rust/rust-no-std/SKILL.md`.
- `Testing no_std on host` — inspect when relevant; source `skills/rust/rust-no-std/SKILL.md`.

## Failure modes and guardrails

- no_std does not imply no allocation or bare metal.
- A copied security allow/deny list is not a threat model.
- Hardware and deployment assumptions must remain configurable and evidenced.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 12 unique source block bodies: 12 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; `current-beta`, reviewed 2026-08-23.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
