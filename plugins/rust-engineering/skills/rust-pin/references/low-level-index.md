# Low-level references for `rust-pin`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`rust-async-internals`](../../rust-concurrency/references/low-level/rust-async-internals.md) — supporting; Future polling, Waker replacement, task scheduling, pinning, cancellation, blocking boundaries, and async diagnostics.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.
