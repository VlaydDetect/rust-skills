# Low-level references for `rust-verify`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`cargo-workflows`](../../rust-cargo-build/references/low-level/cargo-workflows.md) — supporting; Workspace, feature, build-script, lockfile, cache, CI, and Cargo tool workflows.
- [`core-dumps`](../../debugging/references/low-level/core-dumps.md) — supporting; Core/minidump acquisition, build identity, symbols, debugger loading, thread triage, and missing-symbol recovery.
- [`fuzzing`](../../rust-testing/references/low-level/fuzzing.md) — supporting; Target design, corpus, dictionary, crash reproduction, minimization, sanitizer composition, structure-aware inputs, and bounded CI campaigns.
- [`gdb`](../../debugging/references/low-level/gdb.md) — supporting; GDB startup, breakpoints, watchpoints, state and thread inspection, reverse and remote debugging, scripting, and common symbol failures.
- [`lldb`](../../debugging/references/low-level/lldb.md) — supporting; LLDB startup, breakpoints, expressions, watchpoints, threads, Apple behavior, IDE integration, and scripting.
- [`rust-sanitizers-miri`](../../rust-unsafe/references/low-level/rust-sanitizers-miri.md) — supporting; Miri and Rust sanitizer selection, execution scope, report interpretation, unsafe-code validation, and residual proof obligations.
- [`rust-unsafe`](../../rust-unsafe/references/low-level/rust-unsafe.md) — supporting; Unsafe operations, raw pointers, traits, safe wrappers, transmute, UnsafeCell, provenance, aliasing, initialization, and drop.
- [`sanitizers`](../../rust-unsafe/references/low-level/sanitizers.md) — supporting; ASan, TSan, MSan, hardware-assisted modes, suppression and report concepts, and native dependency instrumentation.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Topic names are references, not additional product skills.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-testing`](../../rust-testing/references/testing.md) — supporting; Unit, integration, property, compile-fail, concurrency, fuzz and regression strategy with observable failure criteria.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
