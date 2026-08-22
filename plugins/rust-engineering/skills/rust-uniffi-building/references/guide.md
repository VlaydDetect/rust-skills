# Rust UniFFI Building Field Guide

This guide is the detailed policy for `rust-uniffi-building`. It synthesizes the full-stack UniFFI-building skill and its UDL, proc-macro, type, error, callback, async, build, packaging, and testing references; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- UniFFI maps a constrained interface model to Rust scaffolding and target-language bindings through UDL or proc-macro metadata.
- Records are value data, enums represent closed variants, objects carry identity and lifetime, callbacks reverse control, and errors cross as declared outcomes.
- Foreign runtimes differ in nullability, integer ranges, thread confinement, garbage collection, exceptions, async scheduling, and naming conventions.
- Generated source is an artifact; the committed Rust interface, UDL or attributes, configuration, and generation command are its source of truth.
- Binary packaging must align library names, architectures, symbols, search paths, and target-language package layout.
- Only foreign-side tests prove that generated APIs compile, load, translate values, and release resources in the consumer environment.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Simple value transfer | Record or enum | Maps predictably across languages |
| Stateful service | UniFFI object | Identity and lifecycle are explicit |
| Foreign implementation called by Rust | Callback interface | Reverse control needs a declared contract |
| Rust-specific generic API | Boundary facade DTO or object | UniFFI should not expose Rust type-system machinery |
| Existing UDL project | Preserve mode unless migration is justified | Mixing generation styles adds cognitive and build cost |

## Common Failure Modes

- Designing the interface only from Rust and discovering awkward or unsupported target-language shapes later.
- Treating generated bindings as the source of truth and hand-editing them.
- Omitting callback lifetime or async cancellation behavior.
- Testing only Rust scaffolding and never compiling a target-language consumer.
- Changing generated names or enum or error shapes without cross-language migration analysis.

## Required Evidence

- Pinned UniFFI mode and tooling policy, interface source, generation command, and packaging layout.
- A language-neutral contract for values, objects, errors, callbacks, async, threading, and lifecycle.
- Foreign-language compile and runtime tests on each supported platform or an explicit unavailable matrix.
- Round-trip, error, callback, cancellation, repeated cleanup, and package-loading evidence.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-uniffi-building/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
