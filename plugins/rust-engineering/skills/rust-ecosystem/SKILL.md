---
name: rust-ecosystem
description: Choose broad Rust project shape, library classes, toolchain components, targets, and ecosystem conventions before a specific crate decision. Use for bootstrap, solution-class guidance, or high-level integration orientation.
---

# Rust Ecosystem

Own broad project bootstrap and solution-class selection before detailed crate evaluation. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A new Rust project or subsystem needs a practical starting shape, target, runtime class, or library category.
- The user asks how the Rust ecosystem approaches a broad domain such as CLI, web, embedded, async, parsing, or services.
- Build, target, library, and crate-extraction choices need an initial map before detailed ownership is assigned.

## Workflow

1. Clarify product type, deployment target, library versus application status, MSRV, no-std, async, native integration, and operational constraints.
2. Choose the simplest standard project shape and std capability that can satisfy current requirements.
3. Identify ecosystem categories and already-adopted project conventions without prematurely selecting a new crate.
4. Map high-risk choices such as async runtime, serialization format, web framework, native toolchain, embedded target, or plugin ABI to dedicated evaluation.
5. Sketch package, target, configuration, and validation topology only to the depth needed for the first vertical slice.
6. Route specific adoption to `rust-crate-discovery` and ongoing build, workspace, or dependency policy to their owner profiles.

## Decision Rules

- Start with a binary or library package and add workspace structure only for present boundaries.
- Choose an async runtime only when workloads and dependencies require async I/O; synchronous code is a valid default.
- Avoid framework-driven architecture before domain and deployment constraints are known.
- Account for no-std, WASM, embedded, mobile, cross compilation, and native libraries as first-class target constraints.
- Use existing repository libraries and patterns before adding parallel ecosystem choices.
- A CLI, service, library, proc macro, build tool, and embedded firmware have different error, configuration, and release conventions.
- Extract a crate when ownership, reuse, target, unsafe, compilation, or release isolation is real—not as speculative reuse.
- Do not present current crate popularity or maintenance as fact without current authorized research.

## Boundaries and Hand-offs

- `rust-crate-discovery` owns evidence-based selection among actual candidates.
- `rust-architecture`, `rust-workspace`, and `rust-cargo-build` own detailed design after the broad project class is clear.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Ecosystem field guide](references/guide.md) before making a consequential design choice. Use the [Actionbook ecosystem protocol](references/actionbook-index.md) for detailed integration questions, then verify effective dependencies through Cargo metadata. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
