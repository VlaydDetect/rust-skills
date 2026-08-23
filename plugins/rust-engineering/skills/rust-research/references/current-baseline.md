# Current Rust baseline

Snapshot date: **2026-08-22**. The current stable release is **Rust 1.98.0**, announced 2026-08-20 in the [official release post](https://blog.rust-lang.org/2026/08/20/Rust-1.98.0/) and [release index](https://blog.rust-lang.org/releases/).

This snapshot informs research; it is not a forced MSRV or migration target.

## Precedence

1. Explicit user and repository contract.
2. `rust-toolchain*`, `package.rust-version`, edition, resolver, CI, and supported targets.
3. Installed toolchain for local evidence.
4. Current stable only for greenfield work or explicit upstream research.

Do not add `rust-version` without a real compatibility commitment and CI evidence. Do not migrate an existing edition incidentally.

## Edition and resolver

Cargo currently creates new packages with Edition 2024 ([Edition Guide](https://doc.rust-lang.org/edition-guide/editions/creating-a-new-project.html)). Edition 2024 implies resolver 3 for packages, while a virtual workspace must set `resolver = "3"` explicitly ([resolver guide](https://doc.rust-lang.org/stable/edition-guide/rust-2024/cargo-resolver.html)). Preserve older editions when they are part of the project contract.

## Relevant Rust 1.98 capabilities

Use only when the project's MSRV permits them:

- `str::substr_range` and slice `subslice_range` for recovering validated ranges;
- `core::fmt::NumBuffer` and integer `format_into` as a standard-library candidate for allocation-free decimal formatting;
- atomic `from_mut`/slice conversion APIs where their aliasing contract is satisfied;
- `String` UTF-16 little/big-endian constructors;
- algebraic floating-point methods only when nondeterministic reassociation is acceptable and measured;
- the documented post-1.96 `ManuallyDrop<Box<_>>` move guarantee after explicit drop.

Verify every recommended stabilization against official release notes and record `min-rust`. Prefer an older compatible pattern when raising MSRV is not authorized.

## Cargo and Clippy

- Machine consumers pass `--format-version 1` to `cargo metadata` and tolerate added JSON fields and opaque identifiers.
- Read-only dependency discovery uses `--locked --offline`; failures remain explicit.
- Workspace-wide all-features checks are not universal because targets/features can be mutually exclusive.
- Preserve project lint configuration. Enable individual pedantic/nursery lints only with demonstrated value and documented exceptions; do not set `pedantic = "warn"` or `-D warnings` globally by default.

## Huiali modernization notes

- Pinning decisions use the current [`std::pin`](https://doc.rust-lang.org/std/pin/) contract. `Pin::new_unchecked`, `get_unchecked_mut`, and unsafe projection require a local proof of address stability, structural pinning, and destruction.
- The old `generators` and `generator_trait` feature names are not current guidance. The current nightly-only names are [`coroutines` and `coroutine_trait`](https://doc.rust-lang.org/beta/unstable-book/language-features/coroutines.html); prefer stable `Future`, streams, iterators, or explicit state machines unless nightly is an explicit project constraint.
- Procedural macros follow the Rust Reference's three forms: [function-like, derive, and attribute macros](https://doc.rust-lang.org/reference/procedural-macros.html). Generated-token hygiene and diagnostics are part of their public contract.
- Aya, GPU backends, DPDK bindings, runtimes, frameworks, and ecosystem crate APIs are version-sensitive. Query `cargo metadata` and exact-version official documentation before emitting dependency-specific code.
