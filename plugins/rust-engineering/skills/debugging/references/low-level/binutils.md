# Low-level Binutils protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-cargo-build`, `$rust-unsafe-ffi`.
- Retained scope: Archive, strip, objcopy, address translation, demangling, strings, headers, disassembly, and cross-tool selection.
- Baseline correction: Select tools by object format and target. Never strip or rewrite the only artifact; work from a copy and preserve build identity and separate symbols.
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

- `Table of Contents` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `ar — static archives` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `strip — remove symbols` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `objcopy — binary transformation` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `addr2line — address to source` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `strings — extract text` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `c++filt — demangle symbols` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `ranlib — archive index` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `Cross-binutils naming` — inspect when relevant; source `skills/binaries/binutils/references/cheatsheet.md`.
- `ar` — static library management` — inspect when relevant; source `skills/binaries/binutils/SKILL.md`.
- `strip` — remove debug info` — inspect when relevant; source `skills/binaries/binutils/SKILL.md`.
- `objcopy` — binary section manipulation` — inspect when relevant; source `skills/binaries/binutils/SKILL.md`.
- `addr2line` — address to source` — inspect when relevant; source `skills/binaries/binutils/SKILL.md`.
- `c++filt` — demangle C++ symbols` — inspect when relevant; source `skills/binaries/binutils/SKILL.md`.
- `strings` — extract printable strings` — inspect when relevant; source `skills/binaries/binutils/SKILL.md`.
- `readelf` and `objdump` quick reference` — inspect when relevant; source `skills/binaries/binutils/SKILL.md`.
- `Cross-binutils` — inspect when relevant; source `skills/binaries/binutils/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 17 unique source block bodies: 17 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
