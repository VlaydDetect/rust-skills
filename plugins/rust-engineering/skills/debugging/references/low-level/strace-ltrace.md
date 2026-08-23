# Low-level Strace Ltrace protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-observability`, `$rust-performance`.
- Retained scope: System-call and dynamic-library tracing, filtering, errno diagnosis, timing, attachment, seccomp investigation, and bounded capture.
- Baseline correction: Tracing can expose secrets, alter timing, require privilege, and generate large output. Scope PID, events, duration, and output handling before running.
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

- `strace Output Format` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `Diagnosing Common Issues` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `Binary won't start` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `File not found issues` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `Network issues` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `Permission issues` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `Memory issues (strace side)` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `strace -c Output Analysis` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `ltrace Filter Patterns` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `Combining strace + gdb` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `strace on Docker / Containers` — inspect when relevant; source `skills/profilers/strace-ltrace/references/strace-patterns.md`.
- `Basic strace usage` — inspect when relevant; source `skills/profilers/strace-ltrace/SKILL.md`.
- `Filter by syscall category` — inspect when relevant; source `skills/profilers/strace-ltrace/SKILL.md`.
- `Interpreting common errors` — inspect when relevant; source `skills/profilers/strace-ltrace/SKILL.md`.
- `Useful strace flags` — inspect when relevant; source `skills/profilers/strace-ltrace/SKILL.md`.
- `ltrace — library call tracing` — inspect when relevant; source `skills/profilers/strace-ltrace/SKILL.md`.
- `Practical diagnosis workflows` — inspect when relevant; source `skills/profilers/strace-ltrace/SKILL.md`.
- `seccomp filter debugging` — inspect when relevant; source `skills/profilers/strace-ltrace/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 20 unique source block bodies: 20 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`perf-security`](https://docs.kernel.org/admin-guide/perf-security.html) — perf privilege and data-exposure boundary; `kernel-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
