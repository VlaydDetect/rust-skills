# unsafe-miri-ci

> Run `cargo miri test` in CI for every crate that contains `unsafe` code.

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-unsafe; supporters=none; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Run `cargo miri test` in CI for every crate that contains `unsafe` code.

## Apply When

Apply when an unsafe operation or safe wrapper needs an explicit validity, aliasing, initialization, layout, thread, panic, or drop proof, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a safe standard-library or already accepted crate abstraction enforces the same invariant. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. List every unsafe precondition, prove each from adjacent checks or types, and minimize the operation and caller obligations.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Unsafe may unlock an ABI or measured optimization, but creates a permanent universal soundness proof obligation.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `serde`, `criterion`) must already be accepted by the project or be approved before addition.
- Supported targets, layout or ABI contract, panic policy, and safety invariants must be explicit.

## Verification

Audit every constructor and destruction path, compile relevant targets, and run focused tests plus Miri or sanitizers where applicable.

## Why It Matters

Miri is the only tool that *dynamically* detects undefined behavior in Rust programs at test time. It catches out-of-bounds memory accesses, use-after-free, reads of uninitialized memory, invalid pointer provenance, data races in `unsafe` multithreaded code, and violations of the Stacked Borrows / Tree Borrows aliasing models. The Rust standard library, tokio, serde, and many foundational crates all run Miri in CI before merging changes that touch unsafe code.

Static analysis and code review can miss subtle UB that only manifests at specific memory layouts; Miri's interpreted execution catches it unconditionally.

## Bad

```yaml
# CI that tests but never runs Miri — unsafe code ships unverified.
- name: Test
  run: cargo test --all-features
```

## Good

```yaml
# .github/workflows/miri.yml
name: Miri

on: [push, pull_request]

jobs:
  miri:
    name: Miri (nightly)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install nightly toolchain with Miri
        run: |
          rustup toolchain install nightly --component miri
          rustup override set nightly
          cargo miri setup

      - name: Run Miri
        env:
          MIRIFLAGS: "-Zmiri-strict-provenance"
        run: cargo miri test --all-features
```

## Key Points

- **Nightly only**: Miri requires a nightly toolchain. Pin a specific nightly date in `rust-toolchain.toml` if you need reproducible CI.
- **Slow**: Miri interprets rather than compiles, so test suites run 100–1000× slower than normal. Run Miri on a reduced set of tests or on a separate slower CI job if the full suite is prohibitive.
- **`MIRIFLAGS`**: `-Zmiri-strict-provenance` enables stricter pointer provenance checks, catching casts that violate the provenance model. Add `-Zmiri-tree-borrows` to opt into the newer Tree Borrows model.
- **Stacked Borrows**: Miri's default aliasing model. It catches violations of Rust's borrow rules at the pointer level — invaluable for raw-pointer and FFI code.
- **Setup command**: `cargo miri setup` pre-builds the Miri sysroot so the first test run is not cold. Run it once per CI cache key.
- Only crates with `unsafe` blocks need Miri coverage. Pure-safe crates gain nothing from it.

## When It's Acceptable to Skip

- Crates with zero `unsafe` code (safe-only crates get no benefit).
- Generated code or proc-macro output you do not control (audit the generator instead).
- Very large integration tests that make Miri impractical — run a targeted unit-test subset instead.

## Related Rules
- [unsafe-maybeuninit](unsafe-maybeuninit.md) - use `MaybeUninit<T>` for uninitialized memory
- [unsafe-safety-comment](unsafe-safety-comment.md) - document every unsafe block
- [test-criterion-bench](test-criterion-bench.md) - use criterion for benchmarking (separate from Miri)
