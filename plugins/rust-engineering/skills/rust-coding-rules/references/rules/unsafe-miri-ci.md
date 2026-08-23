# unsafe-miri-ci

> Run targeted Miri coverage when the repository pins a compatible nightly and the exercised code is supported by Miri.
## Decision

Consider this rule only after its prerequisites are satisfied: add targeted Miri coverage for unsafe or otherwise validity-sensitive execution paths that Miri can model.

## Apply When

Apply when an unsafe operation or safe wrapper needs an explicit validity, aliasing, initialization, layout, thread, panic, or drop proof, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a safe standard-library or already accepted crate abstraction enforces the same invariant. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. List every unsafe precondition, prove each from adjacent checks or types, and minimize the operation and caller obligations.
4. Select supported tests or binaries, record Miri's platform and FFI limits, and vary seeds only when concurrency scheduling matters.
5. Run the repository-pinned command without installing or switching toolchains implicitly, then keep the manual safety proof and other platform evidence explicit.

## Trade-offs

Unsafe may unlock an ABI or measured optimization, but creates a permanent universal soundness proof obligation.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `serde`, `criterion`) must already be accepted by the project or be approved before addition.
- Supported targets, layout or ABI contract, panic policy, and safety invariants must be explicit.

## Verification

Audit every constructor and destruction path, compile relevant targets, and run focused tests plus Miri or sanitizers where applicable.

## Why It Matters

Miri is an interpreter for Rust MIR that detects several classes of undefined behavior along the concrete executions it explores, including invalid memory accesses, uninitialized reads, some provenance or aliasing violations, and data races in supported executions. Sanitizers, fuzzers, platform integration tests, static reasoning, and review cover different failure classes.

Miri can expose failures missed by ordinary tests, but a passing run is not unconditional evidence: it does not enumerate all inputs or schedules, model every platform API or FFI call, or reproduce optimized native execution. The local operation-by-operation safety proof remains authoritative.

## Bad

```yaml
# CI assumes an ordinary test run proves unsafe soundness.
- name: Test
  run: cargo test --all-features
```

## Good

```yaml
# Prerequisite: rust-toolchain.toml already pins a nightly with the Miri component.
- name: Run the supported unsafe-core subset under Miri
  run: cargo miri test -p unsafe-core raw_buffer_regressions
```

## Key Points

- **Nightly component**: use the project's pinned nightly and current Miri documentation. Tool availability is a prerequisite, not permission to install or switch it.
- **Execution scope**: select tests that exercise the actual invariant. Record skipped platform, I/O, FFI, or dependency paths.
- **Flags are version-sensitive**: do not copy provenance, aliasing-model, isolation, seed, or leak flags from this rule. Confirm them against the pinned Miri version.
- **Concurrency is sampled**: seeds may explore additional schedules, but a finite set cannot prove race freedom.
- **Prioritization is contextual**: unsafe boundaries are high-value targets. A safe-only crate can still trigger a defect in dependencies or unsafe internals, so absence of local `unsafe` is not proof of zero benefit.

## When It's Acceptable to Skip

- The relevant code path depends on unsupported platform APIs, FFI, or another Miri limitation; use native integration evidence and keep the manual proof.
- The pinned toolchain lacks Miri; report `SKIP` rather than changing the toolchain implicitly.
- A broad suite is impractical; retain a targeted subset that reaches the invariant and state the residual coverage gap.

## Related Rules
- [unsafe-maybeuninit](unsafe-maybeuninit.md) - use `MaybeUninit<T>` for uninitialized memory
- [unsafe-safety-comment](unsafe-safety-comment.md) - document every unsafe block
- [test-criterion-bench](test-criterion-bench.md) - use criterion for benchmarking (separate from Miri)
