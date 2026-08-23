# Low-level references for `rust-testing`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`fuzzing`](low-level/fuzzing.md) — primary; Target design, corpus, dictionary, crash reproduction, minimization, sanitizer composition, structure-aware inputs, and bounded CI campaigns.
- [`rust-unsafe`](../../rust-unsafe/references/low-level/rust-unsafe.md) — supporting; Unsafe operations, raw pointers, traits, safe wrappers, transmute, UnsafeCell, provenance, aliasing, initialization, and drop.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Topic names are references, not additional product skills.
