# Low-level Core Dumps protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-cargo-build`, `$rust-verify`.
- Retained scope: Core/minidump acquisition, build identity, symbols, debugger loading, thread triage, and missing-symbol recovery.
- Baseline correction: Core generation paths, retention, privilege, systemd integration, and symbol servers are host policy. Never change them automatically; first locate an existing dump and matching binary.
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

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Table of Contents` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `Enable core dumps` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `Core pattern configuration` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `systemd / coredumpctl` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `Analyse with GDB` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `Analyse with LLDB` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `debuginfod for symbols` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `Non-interactive triage` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `macOS cores` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `Stripping and symbol management` — inspect when relevant; source `skills/debuggers/core-dumps/references/cheatsheet.md`.
- `Enable core dumps (Linux)` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.
- `systemd/coredumpctl (modern Linux)` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.
- `Enable core dumps (macOS)` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.
- `Analyse a core with GDB` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.
- `Analyse a core with LLDB` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.
- `Missing symbols: debuginfod` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.
- `Missing symbols: manual approach` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.
- `Strip binaries and keep symbols` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.
- `Quick triage from core without full debug session` — inspect when relevant; source `skills/debuggers/core-dumps/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 18 unique source block bodies: 11 `fragment`, 7 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-build-cache`](https://doc.rust-lang.org/cargo/reference/build-cache.html) — Cargo target/build directories and artifact layout; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
