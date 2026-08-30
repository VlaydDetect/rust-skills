---
name: rust-platforms
description: Engineer Rust program behavior across Unix and Windows APIs, resource lifecycles, target capabilities, and global allocator choices. Use for OS-specific runtime behavior; use Nix skills for environments, packaging, and NixOS instead.
---

# Rust Platform Engineering

Own the behavior of a Rust program at Unix and Windows boundaries. Start with portable `std`, then a safe platform crate, and use the smallest raw binding only when the contract requires it.

## Use This Skill When

- Code opens file descriptors or native handles, uses signals, process APIs, Win32, COM, WinRT, or target-specific capabilities.
- A Unix implementation must distinguish POSIX, Linux, BSD, or macOS behavior.
- A Windows implementation must choose between `windows`, `windows-sys`, or focused generated bindings.
- A binary needs evidence for `tikv-jemallocator`, `mimalloc`, or the system allocator.
- A composition root already using mimalloc needs build-time and runtime policy for `mimalloc-pprof` heap captures on Windows or Unix.

## Workflow

1. Record supported targets, minimum OS versions, runtime capability requirements, and the exact resource lifecycle.
2. Try `std`; otherwise choose a safe focused crate and enable only the target features used.
3. Define ownership, borrowing, duplication, inheritance, cancellation, thread affinity, and the one correct close operation for every native resource.
4. Model partial I/O, interruption, would-block behavior, callbacks, encoding, and native error capture explicitly.
5. Keep target-specific code behind narrow modules and compile-check every supported target configuration.
6. Change the global allocator only at the binary or composition root and only after representative measurement.

## Decision Rules

- Unix is not synonymous with Linux; verify each API on every supported target.
- Prefer `OwnedFd` and `BorrowedFd` over integer descriptors, and typed RAII wrappers over unowned Windows handles.
- Acquire close-on-exec atomically where available; retrofitting it can race with concurrent process creation.
- Retry only operations whose documented interruption semantics permit it; never blindly retry `close`.
- Read Windows last-error state immediately after the failing call, before another call can overwrite it.
- Do not impose a global allocator from a reusable library or assume an allocator improves every workload.
- Keep allocator profiling at the composition root; distinguish sampled heap, exact allocation tracking, runtime-off overhead, platform symbols, and sanitizer/FFI compatibility.

## Boundaries and Hand-offs

- `nix-flakes`, `nix-dev-env`, `nix-packaging`, and `nixos` own environments, packaging, and NixOS configuration.
- `rust-unsafe-ffi` owns foreign ABI proofs and allocator pairing across ownership boundaries.
- `rust-cargo-build` owns target configuration and native linking; `rust-performance` owns benchmark design.
- Use `rust-research` whenever an API, crate version, target matrix, or word such as “latest” matters.

## Detailed Reference

Read [Rust platforms field guide](references/guide.md) before introducing raw OS bindings, changing native resource ownership, or selecting a global allocator.
