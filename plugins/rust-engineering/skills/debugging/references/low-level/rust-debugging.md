# Low-level Rust Debugging protocol

<!-- low-level-source-family: rust-debugging; source=skills/rust/rust-debugging/SKILL.md; sha256=2b42bc2d93aa069fc9a04ce7518459c7be126d92cf51f5ae7661c21490fd3440; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/rust-debugging/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-cargo-build`, `$rust-observability`.
- Retained scope: Debug-profile selection, Rust-aware GDB/LLDB, backtraces, panics, structured instrumentation, and async task inspection.
- Baseline correction: Use the actual Cargo profile and artifact path. Panic symbol names, pretty printers, tracing stacks, and async consoles are toolchain- or dependency-specific leads, not defaults.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- exact failing command and environment.
- matching executable, target and profile.
- build ID and symbols.
- input and process/thread state.
- debugger/tracer version and privilege boundary.

## Decision protocol

1. Reproduce and preserve the original failure before changing build settings.
2. Identify object format, optimization and symbol availability; match external symbols by build identity.
3. Choose the narrowest observation: backtrace, breakpoint/watchpoint, core, syscall trace, or thread snapshot.
4. Form one falsifiable hypothesis and collect only the state that distinguishes it.
5. Record debugger limitations caused by inlining, optimization, missing frames, unsupported format, or timing perturbation.

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `GDB Setup` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Automatic via rust-gdb` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Manual ~/.gdbinit setup` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `GDB Commands for Rust` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Types` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Breakpoints in Rust` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Thread debugging` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `LLDB Setup` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Automatic via rust-lldb` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Manual setup` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `LLDB Commands for Rust` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `VS Code / IDE Integration` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `CodeLLDB extension (recommended for Rust)` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Debugging #[no_std] Binaries` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Symbol Demangling` — inspect when relevant; source `skills/rust/rust-debugging/references/rust-gdb-pretty-printers.md`.
- `Build for debugging` — inspect when relevant; source `skills/rust/rust-debugging/SKILL.md`.
- `GDB with Rust pretty-printers` — inspect when relevant; source `skills/rust/rust-debugging/SKILL.md`.
- `LLDB with Rust pretty-printers` — inspect when relevant; source `skills/rust/rust-debugging/SKILL.md`.
- `Backtrace configuration` — inspect when relevant; source `skills/rust/rust-debugging/SKILL.md`.
- `Panic triage` — inspect when relevant; source `skills/rust/rust-debugging/SKILL.md`.
- `The dbg! macro` — inspect when relevant; source `skills/rust/rust-debugging/SKILL.md`.
- `Structured logging with tracing` — inspect when relevant; source `skills/rust/rust-debugging/SKILL.md`.
- `Async debugging with tokio-console` — inspect when relevant; source `skills/rust/rust-debugging/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 26 unique source block bodies: 22 `fragment`, 4 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; `stable`, reviewed 2026-08-23.
- [`cargo-metadata`](https://doc.rust-lang.org/nightly/cargo/commands/cargo-metadata.html) — Machine-readable workspace, target directory, and resolved packages; `stable-format-v1`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
