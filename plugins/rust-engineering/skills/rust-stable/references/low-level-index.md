# Low-level references for `rust-stable`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`rust-cross`](../../rust-cargo-build/references/low-level/rust-cross.md) — supporting; Host/target separation, target support tiers, linker and runner configuration, native libraries, containers, emulators, and deployment validation.
- [`simd-intrinsics`](../../rust-performance/references/low-level/simd-intrinsics.md) — supporting; Auto-vectorization, runtime feature detection, x86 and ARM intrinsics, alignment, dispatch, scalar fallbacks, and generated assembly.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Topic names are references, not additional product skills.
