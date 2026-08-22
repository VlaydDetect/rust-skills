---
name: rust-testing
description: Design and write Rust unit, integration, doc, property, async, concurrency, fuzz, snapshot, mock, and end-to-end tests. Use when the primary task is test strategy or test implementation; use rust-verify to execute evidence after changes.
---

# Rust Testing

Own test architecture, case selection, fixtures, doubles, and regression design. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- New or changed behavior needs a regression test or a test strategy.
- Unit, integration, doc, property, fuzz, async, concurrency, snapshot, coverage, or mutation testing choices are needed.
- Tests are flaky, over-mocked, slow, brittle, or poorly aligned with public behavior.

## Workflow

1. Name the contract, failure mode, boundary, and cheapest test level that would fail for the defect or missing behavior.
2. Select representative success, boundary, invalid, error, lifecycle, and configuration cases without duplicating the same assertion at every layer.
3. Place unit tests near private deterministic logic, integration tests at public boundaries, and doc tests on caller-facing examples.
4. Use property, fuzz, schedule, snapshot, mock, or end-to-end techniques only for the risk they uniquely expose.
5. Make fixtures minimal and deterministic; isolate filesystem, clock, randomness, network, runtime, and global state through owned boundaries.
6. Prove the test catches the intended regression when practical, then hand exact commands and matrices to `rust-verify`.

## Decision Rules

- Test observable behavior and invariants rather than private call order unless the protocol itself is the contract.
- A regression test should fail before the fix for the right reason and pass after it.
- Prefer concrete fakes or in-memory adapters over broad mocking frameworks when they express the boundary.
- Property tests need meaningful generators, shrinking, and invariants; random inputs alone are not a property.
- Snapshots are appropriate for large intentional output, but review the semantic diff and normalize nondeterministic data.
- Async tests need bounded time, cancellation cleanup, and runtime compatibility without relying on arbitrary sleeps.
- Concurrency tests should encode invariants and use loom or controlled synchronization where possible rather than hoping for a race.
- Coverage and mutation scores guide missing cases but do not replace contract-based assertions.

## Boundaries and Hand-offs

- `rust-verify` owns selecting and running the post-change command matrix; this profile owns what tests should exist.
- `specs` owns normative acceptance behavior and `rust-performance` owns benchmark methodology.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Testing field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
