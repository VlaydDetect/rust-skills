# Low-level Rust Security protocol

<!-- low-level-source-family: rust-security; source=skills/rust/rust-security/SKILL.md; sha256=48dcd633d20b5ae4a97abac8fc325c0bdd404df4a4df69e44c931f3cb9a3737d; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/rust-security/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-architecture`.
- Supporting profiles: `$rust-dependencies`, `$rust-unsafe`.
- Retained scope: Threat boundaries, dependency advisories and policy, FFI, fuzzing, unsafe validation, supply-chain inputs, and release hardening.
- Baseline correction: Split security ownership across architecture, dependencies, unsafe/FFI, testing, and verification. Advisory and license policies are project decisions, not copied allow/deny lists.
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

- `cargo-audit — vulnerability scanning` — inspect when relevant; source `skills/rust/rust-security/SKILL.md`.
- `cargo-deny — policy enforcement` — inspect when relevant; source `skills/rust/rust-security/SKILL.md`.
- `RUSTSEC advisory database` — inspect when relevant; source `skills/rust/rust-security/SKILL.md`.
- `Memory-safe FFI patterns` — inspect when relevant; source `skills/rust/rust-security/SKILL.md`.
- `Fuzzing for security bugs` — inspect when relevant; source `skills/rust/rust-security/SKILL.md`.
- `Miri for soundness` — inspect when relevant; source `skills/rust/rust-security/SKILL.md`.
- `Supply chain hardening` — inspect when relevant; source `skills/rust/rust-security/SKILL.md`.

## Failure modes and guardrails

- no_std does not imply no allocation or bare metal.
- A copied security allow/deny list is not a threat model.
- Hardware and deployment assumptions must remain configurable and evidenced.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 11 unique source block bodies: 4 `fragment`, 7 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-audit`](https://github.com/rustsec/rustsec/blob/main/cargo-audit/README.md) — RustSec advisory scanning; `resolved-version`, reviewed 2026-08-23.
- [`cargo-deny`](https://github.com/EmbarkStudios/cargo-deny) — Dependency license, advisory, source, and ban policy; `resolved-version`, reviewed 2026-08-23.
- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; `nightly-version-sensitive`, reviewed 2026-08-23.
- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
