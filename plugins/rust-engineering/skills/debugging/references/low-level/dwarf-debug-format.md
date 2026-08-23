# Low-level Dwarf Debug Format protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$debugging`.
- Supporting profiles: `$rust-cargo-build`, `$rust-performance`.
- Retained scope: DWARF sections and DIEs, line and unwind data, split DWARF, debuginfod, LTO interactions, stripping, and separate symbols.
- Baseline correction: DWARF version, section names, split-debug layout, and tool support vary by target and linker. Match symbols by build identity instead of assumed filenames.
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

- `DWARF sections overview` — inspect when relevant; source `skills/debuggers/dwarf-debug-format/SKILL.md`.
- `Inspecting DWARF with dwarfdump` — inspect when relevant; source `skills/debuggers/dwarf-debug-format/SKILL.md`.
- `Reading DWARF DIE structure` — inspect when relevant; source `skills/debuggers/dwarf-debug-format/SKILL.md`.
- `Split DWARF (.dwo files)` — inspect when relevant; source `skills/debuggers/dwarf-debug-format/SKILL.md`.
- `debuginfod — remote debug symbol server` — inspect when relevant; source `skills/debuggers/dwarf-debug-format/SKILL.md`.
- `LTO and DWARF` — inspect when relevant; source `skills/debuggers/dwarf-debug-format/SKILL.md`.
- `Stripping and separate debug files` — inspect when relevant; source `skills/debuggers/dwarf-debug-format/SKILL.md`.

## Failure modes and guardrails

- Debuggers can evaluate code and change process state.
- Optimized source lines and variables are not a faithful execution transcript.
- Tracing, cores and memory inspection may expose secrets.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 7 unique source block bodies: 5 `fragment`, 2 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; `stable`, reviewed 2026-08-23.
- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
