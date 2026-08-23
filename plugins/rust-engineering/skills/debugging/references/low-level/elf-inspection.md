# Low-level Elf Inspection protocol

<!-- low-level-source-family: elf-inspection; source=skills/binaries/elf-inspection/SKILL.md; sha256=a4bb93e063002724a3dff98f4d91fad57b36782a378d77fd613ec0beee55ce1b; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/binaries/elf-inspection/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-unsafe-ffi`, `$rust-performance`.
- Retained scope: ELF identity, sections, symbols, dynamic dependencies, disassembly, hardening properties, size, and build IDs.
- Baseline correction: Do not use ldd on an untrusted binary. Tool output and section conventions are ELF-specific; dispatch Mach-O and PE artifacts to appropriate native tools.
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

- `Quick reference` — inspect when relevant; source `skills/binaries/elf-inspection/references/cheatsheet.md`.
- `nm symbol types` — inspect when relevant; source `skills/binaries/elf-inspection/references/cheatsheet.md`.
- `readelf sections` — inspect when relevant; source `skills/binaries/elf-inspection/references/cheatsheet.md`.
- `Hardening checks` — inspect when relevant; source `skills/binaries/elf-inspection/references/cheatsheet.md`.
- `Shared library SONAME` — inspect when relevant; source `skills/binaries/elf-inspection/references/cheatsheet.md`.
- `Quick overview: `file` and `size` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.
- `Dynamic dependencies: `ldd` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.
- `Symbols: `nm` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.
- `Sections: `readelf` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.
- `Disassembly and source: `objdump` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.
- `Binary hardening check` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.
- `Section size analysis (binary bloat)` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.
- `Build ID` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.
- `Common diagnosis flows` — inspect when relevant; source `skills/binaries/elf-inspection/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 13 unique source block bodies: 12 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
