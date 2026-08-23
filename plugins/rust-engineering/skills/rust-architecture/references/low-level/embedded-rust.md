# Low-level Embedded Rust protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-architecture`.
- Supporting profiles: `$rust-cargo-build`, `$rust-unsafe`.
- Retained scope: Target and memory layout, no_std entry/panic, flashing/debugging, compact telemetry, interrupts, concurrency models, and HAL ownership.
- Baseline correction: MCU, target, linker script, HAL/runtime versions, probe, panic path, clock and memory budget are required evidence. Do not install targets or tools automatically.
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

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Target Triples` — inspect when relevant; source `skills/embedded/embedded-rust/references/embedded-rust-targets.md`.
- `Installing Targets` — inspect when relevant; source `skills/embedded/embedded-rust/references/embedded-rust-targets.md`.
- `Common HAL Crates by MCU Family` — inspect when relevant; source `skills/embedded/embedded-rust/references/embedded-rust-targets.md`.
- `Memory Configuration` — inspect when relevant; source `skills/embedded/embedded-rust/references/embedded-rust-targets.md`.
- `probe-rs Chip Names` — inspect when relevant; source `skills/embedded/embedded-rust/references/embedded-rust-targets.md`.
- `Project setup` — inspect when relevant; source `skills/embedded/embedded-rust/SKILL.md`.
- `Minimal bare-metal program` — inspect when relevant; source `skills/embedded/embedded-rust/SKILL.md`.
- `probe-rs — flash and debug` — inspect when relevant; source `skills/embedded/embedded-rust/SKILL.md`.
- `defmt — efficient logging` — inspect when relevant; source `skills/embedded/embedded-rust/SKILL.md`.
- `RTIC — Real-Time Interrupt-driven Concurrency` — inspect when relevant; source `skills/embedded/embedded-rust/SKILL.md`.
- `Panic handlers` — inspect when relevant; source `skills/embedded/embedded-rust/SKILL.md`.

## Failure modes and guardrails

- no_std does not imply no allocation or bare metal.
- A copied security allow/deny list is not a threat model.
- Hardware and deployment assumptions must remain configurable and evidenced.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 13 unique source block bodies: 10 `fragment`, 3 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustup-cross`](https://rust-lang.github.io/rustup/cross-compilation.html) — rustup cross-compilation responsibilities; `current-rustup`, reviewed 2026-08-23.
- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; `current-beta`, reviewed 2026-08-23.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
