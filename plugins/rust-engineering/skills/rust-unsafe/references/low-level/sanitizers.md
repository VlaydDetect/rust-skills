# Low-level Sanitizers protocol

<!-- low-level-source-family: sanitizers; source=skills/runtimes/sanitizers/SKILL.md; sha256=86c1d69d8cc0b4272a2ec744cac374a8779fc26b8fb89acba405128890b5967d; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/runtimes/sanitizers/SKILL.md` and 2 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-unsafe`.
- Supporting profiles: `$rust-verify`, `$rust-unsafe-ffi`.
- Retained scope: ASan, TSan, MSan, hardware-assisted modes, suppression and report concepts, and native dependency instrumentation.
- Baseline correction: The source is primarily C/C++. For Rust, use only modes and targets documented by rustc; reject UBSan-as-Rust instructions and do not combine flags by analogy.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- unsafe operation and safe caller contract.
- target and toolchain.
- executed input/schedule.
- FFI/native coverage.
- remaining manual invariants.

## Decision protocol

1. Write provenance, alignment, initialization, validity, aliasing, lifetime, layout, thread, panic and drop obligations.
2. Select Miri for supported MIR execution or a documented rustc sanitizer for a supported target and failure class.
3. Use the repository-pinned nightly when present; otherwise report the required evidence as unavailable instead of installing.
4. Minimize the reproducer and interpret the first causally relevant diagnostic.
5. Record what the run did not cover and keep the local safety proof authoritative.

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Quick reference table` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `Compiler flags` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `Required alongside sanitizer flags` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `Recovery control` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `Individual UBSan checks` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `ASan-specific options` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `Runtime options (environment variables)` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `ASAN_OPTIONS` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `UBSAN_OPTIONS` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `TSAN_OPTIONS` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `LSAN_OPTIONS` — inspect when relevant; source `skills/runtimes/sanitizers/references/flags.md`.
- `ASan report types` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `heap-buffer-overflow` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `use-after-free` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `stack-buffer-overflow` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `double-free` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `UBSan report types` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `signed-integer-overflow` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `null pointer dereference` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `shift exponent too large` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `misaligned access` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `TSan report types` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `data race` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `lock order inversion (deadlock risk)` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `LSan report` — inspect when relevant; source `skills/runtimes/sanitizers/references/reports.md`.
- `Decision tree: which sanitizer?` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `AddressSanitizer (ASan)` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `UndefinedBehaviorSanitizer (UBSan)` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `ThreadSanitizer (TSan)` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `MemorySanitizer (MSan)` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `ASan + UBSan combined` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `Suppressions` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `CMake integration` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `CI integration` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `HWASan (Hardware-Assisted AddressSanitizer)` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `MemTagSanitizer (ARM MTE)` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `GWP-ASan (production sampling)` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.
- `KASAN for kernel modules` — inspect when relevant; source `skills/runtimes/sanitizers/SKILL.md`.

## Failure modes and guardrails

- Miri explores concrete executions, not all inputs or schedules.
- Sanitizer support is mode- and target-specific and normally nightly.
- C/C++ UBSan recipes are not a Rust sanitizer mode.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 33 unique source block bodies: 32 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
