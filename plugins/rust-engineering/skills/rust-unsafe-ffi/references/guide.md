# Rust Unsafe FFI Field Guide

This guide is the detailed policy for `rust-unsafe-ffi`. It synthesizes the full-stack unsafe-FFI skill and craft FFI guidance, separated from internal unsafe and UniFFI ownership; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- An FFI boundary is an unsafe parser for foreign memory, values, lifecycle, and concurrency assumptions.
- Opaque handles usually evolve more safely than exposing Rust layout, vtables, collections, or allocator-owned fields.
- ABI stability covers calling convention, symbol, layout, size, alignment, enum representation, ownership, errors, and target data model.
- Foreign code can pass invalid pointers and values even if generated headers imply otherwise; exported safe wrappers must validate what can be validated.
- Panic, exception, and error systems do not automatically interoperate and need an explicit translation layer.
- Generated bindings reduce repetitive declarations but do not prove lifecycle, threading, or semantic compatibility.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Complex evolving Rust object | Opaque handle | Hides layout and allocator details |
| Small stable value record | repr(C) DTO with fixed fields | Direct transfer is manageable with version policy |
| Borrowed byte buffer | Pointer, length, call-scoped lifetime | Encoding and ownership remain explicit |
| Owned output buffer | Creator-specific free function | Prevents allocator mismatch |
| Cross-runtime callback | Function pointer plus context and deregistration protocol | Lifecycle and thread semantics are explicit |

## Common Failure Modes

- Creating a Rust slice from a foreign pointer before validating length, null, alignment, and lifetime.
- Exposing `String`, `Vec`, trait objects, or `repr(Rust)` values directly through C ABI.
- Allowing panic or foreign exception to cross an unsupported boundary.
- Leaving ownership implicit so both sides free or neither side frees memory.
- Testing only Rust declarations without compiling and running a real foreign caller.

## Required Evidence

- A language-neutral ABI document covering symbols, types, layout, ownership, strings, errors, callbacks, threading, and versioning.
- Safety arguments for every foreign-to-Rust pointer or value conversion.
- Foreign-side integration tests for every supported target and repeated lifecycle operations.
- Header or binding generation reproducibility and panic, allocator, invalid-input, and shutdown tests.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-unsafe-ffi/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
