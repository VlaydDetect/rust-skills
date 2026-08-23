# Low-level references for `rust-observability`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`ebpf-rust`](../../rust-systems-networking/references/low-level/ebpf-rust.md) — supporting; Kernel/user split, verifier constraints, program and map types, BTF/CO-RE, attachment, event transport, and load-failure diagnosis.
- [`rust-debugging`](../../debugging/references/low-level/rust-debugging.md) — supporting; Debug-profile selection, Rust-aware GDB/LLDB, backtraces, panics, structured instrumentation, and async task inspection.
- [`strace-ltrace`](../../debugging/references/low-level/strace-ltrace.md) — supporting; System-call and dynamic-library tracing, filtering, errno diagnosis, timing, attachment, seccomp investigation, and bounded capture.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Topic names are references, not additional product skills.
