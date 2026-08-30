# Rust Platforms Field Guide

Research baseline: **2026-08-23**. Re-run `rust-research` before relying on current crate versions, target support, operating-system behavior, or any claim described as latest.

## Start With the Platform Contract

List the supported target triples and minimum OS releases, then separate compile-time availability from runtime capability. A successful `cfg` only proves what was compiled; older kernels, optional Windows components, sandbox policies, and container restrictions can still reject a call. Prefer this selection ladder:

1. portable `std` API;
2. safe, focused platform crate;
3. the smallest typed or raw binding around a reviewed unsafe adapter.

Keep platform branches behind narrow modules with a platform-neutral application contract. Compile-check every supported target, but also run behavior tests on representative systems: cross-compilation cannot validate permissions, signals, handle inheritance, COM apartments, filesystem semantics, or runtime API availability.

## Unix: POSIX Is a Family, Not a Linux Alias

Classify every dependency on OS behavior as POSIX-like, Linux-specific, BSD-specific, or macOS-specific. The [`nix` crate](https://docs.rs/nix/latest/nix/) exposes APIs by Cargo feature and target; enable only the modules used and confirm each item is available on every target in the product matrix. Do not make a Linux-only syscall appear portable by hiding it behind `cfg(unix)`.

Use [`OwnedFd`](https://doc.rust-lang.org/std/os/fd/struct.OwnedFd.html) to transfer ownership and `BorrowedFd` to express a scoped borrow. Raw integers belong only at the syscall boundary. State whether duplication creates a new owner, whether descriptors may cross `exec`, and which task or thread may close them.

- Acquire `CLOEXEC` atomically during open, accept, pipe, or duplication when the OS offers it. Setting it later can race with another thread spawning a process.
- Reads and writes can complete partially. Advance by the returned byte count, handle zero according to the API, and keep protocol framing above the byte stream.
- `EAGAIN` or `EWOULDBLOCK` means the operation would block under the selected mode; integrate readiness and cancellation rather than spin.
- Handle `EINTR` per syscall documentation. Some operations may have made progress, timeouts may need recomputation, and wrappers may already retry.
- Never blindly retry `close` after an interruption. On common systems the descriptor number may already be released and reused, so a retry can close an unrelated resource.

Signals and `fork` sharply reduce what is safe. A signal handler may call only async-signal-safe operations and must not allocate, lock ordinary mutexes, format strings, or touch most runtime state. In a multithreaded child after `fork`, call only the platform-approved async-signal-safe path until `exec` or `_exit`; inherited locks may be permanently owned by vanished threads. Prefer spawn facilities that avoid a user-space post-fork phase.

## Windows: Typed APIs and Exact Lifecycles

Prefer the focused crates now documented by the [`windows-rs` project](https://github.com/microsoft/windows-rs), or `windows` when its typed Win32, COM, or WinRT projections fit the existing project. Use `windows-sys` only when raw ABI control, low-level compatibility, or compile-surface constraints are demonstrated. For a very narrow API surface, evaluate project-specific bindings generated with `windows-bindgen`. Enable only the required API-family features.

Call Unicode `W` APIs and define an embedded-NUL policy before encoding Rust text to UTF-16. A trailing terminator is often required but is not part of Rust string content. Preserve path meaning: normalization, verbatim paths, drive-relative paths, and case behavior are separate product decisions.

Every native result needs its exact sentinel and destructor:

- distinguish `NULL`, `INVALID_HANDLE_VALUE`, zero-sized success values, and valid pseudo-handles according to the called function;
- wrap each owned handle in RAII with the matching close routine; `CloseHandle`, registry close, socket close, COM release, and local-memory free are not interchangeable;
- capture [`GetLastError`](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror) immediately when the API contract says it is meaningful, before logging or cleanup calls overwrite thread-local state;
- preserve HRESULT information and distinguish success-with-status from failure.

Initialize COM with an explicit apartment model and balance initialization. Treat interface and callback use as apartment- and thread-affine unless the API proves otherwise. Callback state must outlive every possible invocation; define unregister, cancellation, reentrancy, panic containment, and shutdown ordering. Keep unwinding out of foreign callbacks.

Compile-time SDK presence does not guarantee runtime support. Use documented version checks, dynamic lookup, or capability APIs when supporting older Windows releases, and define a tested fallback or an actionable error.

## Global Allocator Policy

A reusable library must not select a process-global allocator for its consumer. Only the binary or composition root may make that choice, guarded for supported targets. New Unix investigations may evaluate [`tikv-jemallocator`](https://github.com/tikv/jemallocator), the maintained successor naming for legacy `jemallocator`; treat the old crate as migration context, not a new default. [`mimalloc`](https://docs.rs/mimalloc/latest/mimalloc/) is available on Windows and Unix, but remains a benchmark candidate rather than an automatic recommendation.

Compare against the system allocator on representative workloads and deployments. Measure median and tail latency, throughput, peak and steady RSS, fragmentation after churn, startup, binary size, idle retention, and behavior across the actual target matrix. Warm caches and synthetic allocation loops are insufficient evidence for an application-wide switch.

An alternative allocator adds operational constraints:

- memory allocated on one side of an FFI boundary must be freed by the paired allocator or an exported matching destructor;
- sanitizer, heap profiler, crash-dump, preload, and platform-debugging workflows may need the system allocator or special integration;
- static and dynamic runtime choices can create multiple heaps in one process;
- secure or guarded modes trade memory and CPU for hardening, so benchmark the enabled production configuration;
- allocator-specific tuning is process policy and must stay out of public library APIs.

### Heap Profiler Integration

[`mimalloc-pprof`](https://github.com/zackees/mimalloc-pprof) is a Windows-first sampled live-heap profiler that also supports Linux and macOS. Use it only when the composition root already selects its mimalloc implementation or when a separate allocator comparison authorizes the change.

- Resolve the current crate feature contract. Versions with compile-out support can use `default-features = false` to remove sampled pprof hooks while retaining the allocator/no-op profiler API; an application feature such as `heap-profiling` should map to the real resolved capability rather than inventing an upstream feature name.
- In an instrumented build, capture remains runtime-controlled through the resolved `prof::start`/`prof::stop` API or `MIMALLOC_PROF` environment contract. Runtime-off hooks can still add allocation-path overhead, so measure the disabled path and compile hooks out when runtime activation is not worth it.
- The profile is sampled live heap, not every allocation. Dump while allocations of interest remain live. Linux/macOS stacks require frame pointers in relevant code; Windows x64 needs matching PDB/unwind information.
- Never link the vendored Rust allocator and a second CMake mimalloc implementation into one process.

Use crate [`dhat`](https://docs.rs/dhat/latest/dhat/) for a bounded investigation that must account for every allocation observed by its wrapping global allocator. Gate it at the binary/test root, expect substantial overhead, isolate exact-count tests from global/test-harness noise, and do not claim memory-access tracking.

Profiler selection and commands remain owned by [`rust-performance`](../../rust-performance/references/low-level/rust-profiling.md); this section owns only allocator placement and platform constraints.

## Review and Verification

Require resource-lifecycle tests for success, early return, cancellation, callback teardown, process inheritance, and double-close prevention. Compile all target-specific modules, exercise runtime capability fallback, and run platform-native tests. For allocator changes, preserve the benchmark command, workload corpus, target details, and before/after results so the decision can be reversed when workloads or runtimes change.

## Primary Sources

- [`nix` documentation](https://docs.rs/nix/latest/nix/) and Rust [`std::os::fd`](https://doc.rust-lang.org/stable/std/os/fd/index.html)
- [windows-rs source and crate guidance](https://github.com/microsoft/windows-rs) and [Windows error handling](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
- [`tikv-jemallocator` source](https://github.com/tikv/jemallocator), [`mimalloc` crate documentation](https://docs.rs/mimalloc/latest/mimalloc/), [`mimalloc-pprof`](https://github.com/zackees/mimalloc-pprof), and [`dhat`](https://docs.rs/dhat/latest/dhat/)
