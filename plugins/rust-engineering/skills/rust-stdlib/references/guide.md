# Rust Standard Library Field Guide

This guide is the detailed policy for `rust-stdlib`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Std types encode useful guarantees: ordering, uniqueness, ownership, thread safety, error propagation, and platform representation.
- `Vec` is often the best default sequence because contiguous storage and iteration are simple; alternative collections need an operation-driven reason.
- Hash iteration order is not a stable serialization or user-visible ordering contract.
- Filesystem paths and environment or process strings may contain non-UTF-8 platform data.
- I/O APIs distinguish buffered versus unbuffered access, partial reads or writes, and interruption.
- Interior mutability types differ by thread model: `Cell` and `RefCell` are single-threaded; locks and atomics add synchronization semantics.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Ordered keyed iteration required | BTreeMap | Ordering is an explicit semantic guarantee |
| Fast lookup with no stable order | HashMap | Avoid paying for an unused ordering contract |
| Filesystem boundary | Path or OsStr | Preserves native representation |
| Elapsed timeout | Instant | Monotonic behavior matches duration measurement |
| Shared mutable state | Message passing, lock, or atomic by invariant | The data protocol determines the primitive |

## Common Failure Modes

- Adding a crate for functionality already covered safely by std under the repository MSRV.
- Converting paths to lossy UTF-8 and later treating the value as a round-trippable path.
- Depending on hash iteration order in tests, output, or serialization.
- Assuming `write` consumes the entire buffer or that every read fills it.
- Choosing atomics because they appear cheaper without a documented memory-ordering invariant.

## Required Evidence

- Required operations and semantics matched to the selected type or API.
- MSRV and platform availability for any less-established standard-library feature.
- Edge-case behavior for empty values, invalid input, numeric limits, partial I/O, and time changes as applicable.
- A benchmark only when the choice is performance-sensitive and alternatives are semantically valid.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-stdlib/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
