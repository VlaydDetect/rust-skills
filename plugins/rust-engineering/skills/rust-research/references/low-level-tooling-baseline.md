# Low-level tooling baseline

> Product-owned command safety and evidence policy for the low-level source integration. Reviewed 2026-08-23; project state always wins.

## Precedence

1. Explicit user contract and repository instructions.
2. Project `rust-toolchain*`, MSRV, Edition, Cargo manifests/config, lockfile, CI, target and resolved tool versions.
3. Current official Rust/Cargo documentation for language, compiler, target and Cargo behavior.
4. Exact tool-owner documentation for external profilers, caches, audit tools and runners.
5. This product baseline: Rust 1.98, Edition 2024 and resolver 3; never an implicit upgrade request.

## Command contract

Before running a command, record tool/version, stable/nightly/external channel, OS/target/hardware, required components, build/network/install/privilege/config/lockfile effects, expected evidence, and stopping condition.

- Automatic and read-only workflows never install tools or components, fetch the network, update resolution, use privilege, weaken host policy, or edit global Cargo/debugger configuration.
- Use a project-pinned nightly when required. If unavailable, return `SKIP`; do not silently switch or install.
- Use an external tool only when already installed/resolved or after explicit authorization.
- Derive artifact locations from Cargo metadata and effective target/profile. Cargo's internal build-directory layout is not an API.
- Keep raw profiler/timing evidence and compare the same workload before and after one change.

## Corrected command semantics

- Cargo timing entrypoint: `cargo build --timings`; by default the current report is under the effective target directory at `cargo-timings/cargo-timing.html`.
- Resolve the effective directory with `cargo metadata --format-version 1 --locked --offline`; distinguish an offline cache miss from a project defect.
- Rust sanitizer flags are nightly and target-specific. A sanitizer mode named `undefined` is not supported by rustc.
- Miri executes MIR for selected tests or binaries; passing a run is not proof over all inputs, targets, FFI, optimizations or schedules.
- `rustup target add` provides the Rust standard library for a target, not its linker, sysroot, native libraries, emulator, device or runtime acceptance.
- perf frame-pointer, DWARF and LBR call graphs have different binary/CPU constraints; `perf_event_paranoid` is host security policy.
- cargo-flamegraph, Criterion, cargo-bloat, cargo-llvm-lines, and sccache are external tools whose exact commands belong to the resolved installed version, not Cargo itself.
- Flamegraphs locate sampled CPU hypotheses. Criterion or another comparable benchmark measures the change. cargo-bloat does not support WASM and crate attribution is an estimate; cargo-llvm-lines counts unoptimized LLVM IR lines, not runtime cost.
- sccache is a compiler wrapper with cacheability limitations; remote credentials/backends and disabling incremental compilation are deployment decisions.
- Cranelift/Cargo codegen backend, linker changes, LTO, PGO, BOLT and target CPU features require exact toolchain/target support plus measurement.

## Evidence catalog

- [`async-future`](https://rust-lang.github.io/async-book/02_execution/02_future.html) — Future poll and wake contract; authority `official-rust`, channel `current`.
- [`async-pinning`](https://rust-lang.github.io/async-book/part-reference/pinning.html) — Pinning and async state-machine constraints; authority `official-rust`, channel `current`.
- [`cargo-audit`](https://github.com/rustsec/rustsec/blob/main/cargo-audit/README.md) — RustSec advisory scanning; authority `tool-owner`, channel `resolved-version`.
- [`cargo-bloat`](https://github.com/RazrFalcon/cargo-bloat) — cargo-bloat formats and attribution limits; authority `tool-owner`, channel `resolved-version`.
- [`cargo-build-cache`](https://doc.rust-lang.org/cargo/reference/build-cache.html) — Cargo target/build directories and artifact layout; authority `official-rust`, channel `stable`.
- [`cargo-build-performance`](https://doc.rust-lang.org/cargo/guide/build-performance.html) — Measured Rust build-performance guidance; authority `official-rust`, channel `stable`.
- [`cargo-build-scripts`](https://doc.rust-lang.org/cargo/reference/build-scripts.html) — Build-script inputs, outputs, directives, and host/target behavior; authority `official-rust`, channel `stable`.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; authority `official-rust`, channel `stable`.
- [`cargo-deny`](https://github.com/EmbarkStudios/cargo-deny) — Dependency license, advisory, source, and ban policy; authority `tool-owner`, channel `resolved-version`.
- [`cargo-flamegraph`](https://github.com/flamegraph-rs/flamegraph) — cargo-flamegraph backends and command surface; authority `tool-owner`, channel `resolved-version`.
- [`cargo-llvm-lines`](https://github.com/dtolnay/cargo-llvm-lines) — Unoptimized LLVM IR line-count semantics; authority `tool-owner`, channel `resolved-version`.
- [`cargo-metadata`](https://doc.rust-lang.org/nightly/cargo/commands/cargo-metadata.html) — Machine-readable workspace, target directory, and resolved packages; authority `official-rust`, channel `stable-format-v1`.
- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; authority `official-rust`, channel `stable`.
- [`cargo-resolver`](https://doc.rust-lang.org/cargo/reference/resolver.html) — Dependency and feature resolution; authority `official-rust`, channel `stable`.
- [`cargo-timings`](https://doc.rust-lang.org/stable/cargo/reference/timings.html) — Cargo timings output and interpretation; authority `official-rust`, channel `stable`.
- [`cargo-unstable`](https://doc.rust-lang.org/cargo/reference/unstable.html) — Cargo unstable feature gates including codegen backends; authority `official-rust`, channel `nightly`.
- [`criterion`](https://bheisler.github.io/criterion.rs/book/) — Criterion benchmark methodology and APIs; authority `tool-owner`, channel `resolved-version`.
- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; authority `official-tool-owner`, channel `nightly-version-sensitive`.
- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; authority `official-tool-doc-mirror`, channel `installed-perf-specific`.
- [`perf-security`](https://docs.kernel.org/admin-guide/perf-security.html) — perf privilege and data-exposure boundary; authority `official-linux-kernel`, channel `kernel-specific`.
- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; authority `official-rust`, channel `nightly-target-specific`.
- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; authority `official-rust`, channel `toolchain-specific`.
- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; authority `official-rust`, channel `current-beta`.
- [`rustup-cross`](https://rust-lang.github.io/rustup/cross-compilation.html) — rustup cross-compilation responsibilities; authority `official-rust`, channel `current-rustup`.
- [`sccache-rust`](https://github.com/mozilla/sccache/blob/main/docs/Rust.md) — Rust compiler-wrapper caching and limitations; authority `tool-owner`, channel `resolved-version`.
