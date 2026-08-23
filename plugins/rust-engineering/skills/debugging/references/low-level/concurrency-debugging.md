# Low-level Concurrency Debugging protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-concurrency`, `$rust-unsafe`.
- Retained scope: Race, deadlock, lock-order, atomic-ordering, happens-before, and thread-state diagnosis.
- Baseline correction: A race detector covers executed schedules and supported code. Combine a minimized reproducer with protocol invariants; do not transplant C/C++ atomic examples into Rust without proving the Rust model.
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

- `ThreadSanitizer (TSan) — race detection` — inspect when relevant; source `skills/debuggers/concurrency-debugging/SKILL.md`.
- `Helgrind — lock-order and race detection` — inspect when relevant; source `skills/debuggers/concurrency-debugging/SKILL.md`.
- `Deadlock detection with GDB` — inspect when relevant; source `skills/debuggers/concurrency-debugging/SKILL.md`.
- `std::atomic misuse patterns` — inspect when relevant; source `skills/debuggers/concurrency-debugging/SKILL.md`.
- `Happens-before reasoning` — inspect when relevant; source `skills/debuggers/concurrency-debugging/SKILL.md`.
- `Rust concurrency — compile-time guarantees` — inspect when relevant; source `skills/debuggers/concurrency-debugging/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 8 unique source block bodies: 8 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-23.
- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; `nightly-version-sensitive`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
