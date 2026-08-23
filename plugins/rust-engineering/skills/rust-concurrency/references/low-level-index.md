# Low-level references for `rust-concurrency`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`concurrency-debugging`](../../debugging/references/low-level/concurrency-debugging.md) — supporting; Race, deadlock, lock-order, atomic-ordering, happens-before, and thread-state diagnosis.
- [`io-uring`](low-level/io-uring.md) — primary; Submission/completion ownership, operation lifetimes, registered resources, multishot operations, cancellation, zero-copy, and fallback I/O.
- [`memory-model`](low-level/memory-model.md) — primary; Atomic ordering, happens-before, release sequences, fences, publication, lock-free state machines, and common ordering failures.
- [`rust-async-internals`](low-level/rust-async-internals.md) — primary; Future polling, Waker replacement, task scheduling, pinning, cancellation, blocking boundaries, and async diagnostics.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Topic names are references, not additional product skills.
