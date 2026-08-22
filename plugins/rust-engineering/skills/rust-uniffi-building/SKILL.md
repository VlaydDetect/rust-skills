---
name: rust-uniffi-building
description: Build and maintain UniFFI component interfaces, scaffolding, UDL or proc-macro exports, foreign-language bindings, packaging, async, callbacks, errors, and cross-language tests. Use for UniFFI-specific integration.
---

# Rust UniFFI Building

Own UniFFI interface definition, scaffolding, binding generation, packaging, and foreign-language validation. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A Rust library must expose APIs to Kotlin, Swift, Python, or other UniFFI-supported consumers.
- UDL, UniFFI proc macros, scaffolding generation, async exports, callbacks, records, enums, errors, or custom types are changing.
- Generated language packages fail to build, load, or preserve expected ownership and threading behavior.

## Workflow

1. Define target languages, UniFFI mode and version, supported platforms, packaging, async runtime, threading, and compatibility policy.
2. Design a language-neutral interface using supported records, enums, objects, errors, callbacks, and custom types; keep Rust-specific generics and lifetimes internal.
3. Choose UDL or proc-macro workflow according to repository convention and tool support, then make generation reproducible.
4. Translate domain types and errors at the boundary and document object ownership, callback lifetime, async cancellation, and thread affinity.
5. Build Rust artifacts and generated bindings for each target language through repository-native commands without checking in incidental build output.
6. Run foreign-language integration tests for construction, calls, errors, async, callbacks, cleanup, and package loading on supported targets.

## Decision Rules

- Expose a language-neutral contract rather than mirroring every internal Rust type or trait.
- UniFFI code generation reduces ABI boilerplate but does not remove lifecycle, threading, versioning, or semantic design obligations.
- Objects crossing the boundary need clear strong-reference and destruction behavior in each target language runtime.
- Callbacks must define invocation thread, lifetime, reentrancy, cancellation, and behavior during shutdown.
- Async exports need runtime integration, cancellation semantics, error mapping, and target-language task behavior.
- Error enums and messages should preserve actionable categories while avoiding private data leakage.
- Custom types require stable lowering and lifting rules plus round-trip tests.
- Generated bindings and packages must be reproducible from committed interface sources and pinned tooling policy.

## Boundaries and Hand-offs

- `rust-unsafe-ffi` owns the underlying ABI and unsafe validity concepts when generated layers are insufficient.
- `rust-api-design` owns the Rust-side public contract and `rust-semver` owns released cross-language compatibility decisions.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust UniFFI Building field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
