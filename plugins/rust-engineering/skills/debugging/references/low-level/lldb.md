# Low-level Lldb protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-cargo-build`, `$rust-verify`.
- Retained scope: LLDB startup, breakpoints, expressions, watchpoints, threads, Apple behavior, IDE integration, and scripting.
- Baseline correction: LLDB command and Rust formatter availability depend on the installed distribution. Keep IDE and user-level configuration out of automatic workflows.
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

- `Table of Contents` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Process control` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Breakpoints` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Watchpoints` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Inspection` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Stack` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Memory` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Threads` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Signals` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Settings` — inspect when relevant; source `skills/debuggers/lldb/references/gdb-lldb-map.md`.
- `Start LLDB` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.
- `GDB → LLDB command map` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.
- `Breakpoints` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.
- `Inspect state` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.
- `Watchpoints` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.
- `Threads` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.
- `macOS / Apple specifics` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.
- `VS Code integration` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.
- `LLDB Python scripting` — inspect when relevant; source `skills/debuggers/lldb/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 8 unique source block bodies: 8 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
