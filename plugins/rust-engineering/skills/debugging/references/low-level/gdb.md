# Low-level Gdb protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-cargo-build`, `$rust-verify`.
- Retained scope: GDB startup, breakpoints, watchpoints, state and thread inspection, reverse and remote debugging, scripting, and common symbol failures.
- Baseline correction: Use repository and toolchain-provided Rust helpers when present. Do not edit global gdbinit, start remote servers, or assume command support without user authorization and local evidence.
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

- `Table of Contents` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Startup` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Execution control` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Breakpoints & watchpoints` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Inspection` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Stack` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Memory` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Threads` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Reverse debugging` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `Display formats` — inspect when relevant; source `skills/debuggers/gdb/references/cheatsheet.md`.
- `GDB Python API basics` — inspect when relevant; source `skills/debuggers/gdb/references/scripting.md`.
- `Custom pretty-printer` — inspect when relevant; source `skills/debuggers/gdb/references/scripting.md`.
- `STL pretty-printers (libstdc++)` — inspect when relevant; source `skills/debuggers/gdb/references/scripting.md`.
- `Breakpoint commands` — inspect when relevant; source `skills/debuggers/gdb/references/scripting.md`.
- `Convenience variables` — inspect when relevant; source `skills/debuggers/gdb/references/scripting.md`.
- `Useful define aliases` — inspect when relevant; source `skills/debuggers/gdb/references/scripting.md`.
- `Prerequisite: compile with debug info` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.
- `Start GDB` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.
- `Essential commands` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.
- `Breakpoints and watchpoints` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.
- `Inspect state` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.
- `Multi-thread debugging` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.
- `Reverse debugging (record/replay)` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.
- `Remote debugging with gdbserver` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.
- `GDB init file (~/.gdbinit)` — inspect when relevant; source `skills/debuggers/gdb/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 24 unique source block bodies: 23 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
