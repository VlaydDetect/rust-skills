# Low-level references for `rust-dependencies`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`cargo-workflows`](../../rust-cargo-build/references/low-level/cargo-workflows.md) — supporting; Workspace, feature, build-script, lockfile, cache, CI, and Cargo tool workflows.
- [`rust-security`](../../rust-architecture/references/low-level/rust-security.md) — supporting; Threat boundaries, dependency advisories and policy, FFI, fuzzing, unsafe validation, supply-chain inputs, and release hardening.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.
