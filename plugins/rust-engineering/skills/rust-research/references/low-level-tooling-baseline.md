# External Rust tooling baseline

> Product-owned command safety and evidence policy for low-level and reviewed Cargo-tool integrations. Reviewed 2026-08-30; project state always wins.

## Precedence

1. Explicit user contract and repository instructions.
2. Project `rust-toolchain*`, MSRV, Edition, Cargo manifests/config, lockfile, CI, target and resolved tool versions.
3. Current official Rust/Cargo documentation for language, compiler, target and Cargo behavior.
4. Exact tool-owner documentation for external profilers, caches, audit tools and runners.
5. This product baseline: Rust 1.98, Edition 2024 and resolver 3; never an implicit upgrade request.

## Command contract

Before running a command, record tool/version, stable/nightly/external/project channel, OS/target/hardware, required components, build/report/source/process/network/install/privilege/GUI/upload/config/lockfile effects, expected evidence, and stopping condition.

- Automatic and read-only workflows never install tools or components, fetch the network, update resolution, open GUIs, upload artifacts, use privilege, weaken host policy, edit global Cargo/debugger configuration, or mutate a lockfile.
- Use a project-pinned nightly when required. If unavailable, return `SKIP`; do not silently switch or install.
- Use an external tool only when already installed/resolved or after explicit authorization.
- Check the resolved tool's `--version` and matching `--help` before using a version-sensitive command. Tool-owner documentation owns external CLI syntax.
- An absent external tool is an explicit `SKIP`; installation needs separate authorization and never happens inside verification-only work.
- A useful external-tool recipe is not automatically a required local or CI baseline. Adopt it only through the project's own task and policy contract.
- Derive artifact locations from Cargo metadata and effective target/profile. Cargo's internal build-directory layout is not an API.
- Keep raw profiler/timing evidence and compare the same workload before and after one change.

## Corrected command semantics

- Cargo timing entrypoint: `cargo build --timings`; by default the current report is under the effective target directory at `cargo-timings/cargo-timing.html`.
- Resolve the effective directory with `cargo metadata --format-version 1 --locked --offline`; distinguish an offline cache miss from a project defect.
- Rust sanitizer flags are nightly and target-specific. A sanitizer mode named `undefined` is not supported by rustc.
- Miri executes MIR for selected tests or binaries; passing a run is not proof over all inputs, targets, FFI, optimizations or schedules.
- `rustup target add` provides the Rust standard library for a target, not its linker, sysroot, native libraries, emulator, device or runtime acceptance.
- perf frame-pointer, DWARF and LBR call graphs have different binary/CPU constraints; `perf_event_paranoid` is host security policy.
- cargo-flamegraph, Criterion, Divan, pprof-rs, samply, mimalloc-pprof, dhat, Tracy clients, vendor profilers, cargo-bloat, cargo-llvm-lines, and sccache are external tools whose exact commands belong to the resolved installed or project version, not Cargo itself.
- Criterion is the maintained-microbenchmark default for baselines and optimization claims. Divan is a minimal exploratory alternative; resolve its current MSRV and move to Criterion when baseline policy, Criterion analysis, or Criterion profiler hooks own the decision.
- A project profiling build uses a workspace-root custom profile that inherits `release`, retains debug information, and disables stripping. Do not place it in global Cargo configuration or silently add LTO, panic strategy, codegen-unit, target CPU, allocator, or global rustflags changes.
- Criterion `--profile-time` omits normal analysis/result saving. In pprof-rs, `criterion` and `flamegraph` are features, `Frames`/`frames_post_processor` are APIs, and `frame-pointer` is a separate nightly/build-std-sensitive feature.
- samply and cargo-flamegraph support Linux, macOS, and Windows through different backends. Samply normally opens a browser/local source server; cargo-flamegraph has explicit GUI/privilege options. These effects and any upload/symbol-server network access require authorization.
- mimalloc-pprof is sampled live-heap profiling for Windows, Linux, and macOS. Keep allocator selection at the composition root, distinguish build-time hook removal from runtime start/stop, measure runtime-off overhead, retain Unix frame pointers or Windows PDBs, and never link two mimalloc implementations.
- The `dhat` crate wraps the global allocator and observes every allocation in its active scope, but is experimental, source-intrusive, and potentially very slow. It does not instrument memory reads/writes.
- Tracy Rust clients and `tracing-tracy` must be conditionally enabled against a compatible protocol version. Discovery and trace/source/assembly data can be exposed on the local network.
- Linux cache/counter work uses the installed perf event set. Windows prefers installed VTune on Intel or AMD uProf on AMD; WPR/WPA is the heavier ETW fallback or the primary path for scheduler, wakeup, wait, timer, and I/O causality.
- Flamegraphs locate sampled CPU hypotheses. Criterion or another comparable benchmark measures the change. cargo-bloat does not support WASM and crate attribution is an estimate; cargo-llvm-lines counts unoptimized LLVM IR lines, not runtime cost.
- sccache is a compiler wrapper with cacheability limitations; remote credentials/backends and disabling incremental compilation are deployment decisions.
- Cranelift/Cargo codegen backend, linker changes, LTO, PGO, BOLT and target CPU features require exact toolchain/target support plus measurement.

## Reviewed Cargo-tool semantics

- **cargo-generate:** noninteractive mode only removes prompts. Generation still writes output and may initialize VCS, modify a parent workspace, fetch a remote template, overwrite files, or execute reviewed Rhai hooks. Prefer `cargo new` for plain crates; generate a pinned template into a fresh temporary directory, inspect it, then integrate the diff.
- **cargo-nextest:** process-per-test isolates Rust process memory and crashes, not shared files, ports, databases, services, devices, or child processes. Thread count, groups, retries, timeouts, filters, output schema, profile, and JUnit path are resolved-version/project policy. Retried passes remain flaky. Doctests require a separate Cargo gate.
- **cargo-llvm-cov:** coverage builds and executes instrumented code and writes raw/report artifacts; a normal run can clean tool-owned prior coverage state. For several formats, execute once with reporting deferred and render reports from the same data. Thresholds belong to the project; branch/doctest coverage remains pinned-nightly and version-sensitive. Browser opening and uploads are separate effects.
- **cargo-machete:** exit codes distinguish clean (`0`), findings (`1`), and processing error (`2`). Findings are heuristic candidates. Current false-positive policy belongs in package/workspace Cargo metadata with `ignored` or rename mappings. Metadata-assisted analysis can mutate `Cargo.lock`, so it is never an unconditional read-only scan.
- **Git worktree builds:** keep target/build state isolated by default. If supported by pinned Cargo, a templated `build.build-dir` with `{workspace-path-hash}` can preserve isolation under an external root. Use only an already configured sccache for cross-workspace compiler caching, and measure its limitations; one common writable target directory is not the default cache design.
- **Clippy:** lint levels and priorities belong in Cargo `[lints]`/`[workspace.lints]`; members inherit via `[lints] workspace = true`. `clippy.toml` holds only documented typed configuration keys. Group priority must be lower than individual overrides. Pedantic, nursery, cargo, and individual restriction lints are project choices, never blanket product defaults.

The Cargo tooling umbrella `rust-development` source contributes discovery pointers only: macro expansion routes to Cargo/research, audit/deny to dependency governance, Miri to unsafe/verify, fuzzing to testing, flamegraphs to performance, and cross-builds to Cargo/FFI/research. Its language, async, unsafe, WASI, embedded, crate-choice, and optimization recipes do not override the dedicated owners.

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
- [`cargo-generate-api`](https://docs.rs/cargo-generate/latest/cargo_generate/struct.GenerateArgs.html) — resolved cargo-generate argument semantics; authority `tool-owner`, channel `resolved-version`.
- [`cargo-generate-guide`](https://cargo-generate.github.io/cargo-generate/) — cargo-generate templates, variables, hooks, and CLI; authority `tool-owner`, channel `resolved-version`.
- [`cargo-llvm-lines`](https://github.com/dtolnay/cargo-llvm-lines) — Unoptimized LLVM IR line-count semantics; authority `tool-owner`, channel `resolved-version`.
- [`cargo-llvm-cov`](https://github.com/taiki-e/cargo-llvm-cov/blob/main/README.md) — cargo-llvm-cov instrumentation, reporting, and unstable modes; authority `tool-owner`, channel `resolved-version`.
- [`cargo-machete`](https://github.com/bnjbvr/cargo-machete) — cargo-machete scanning, Cargo metadata, and exit semantics; authority `tool-owner`, channel `resolved-version`.
- [`cargo-metadata`](https://doc.rust-lang.org/nightly/cargo/commands/cargo-metadata.html) — Machine-readable workspace, target directory, and resolved packages; authority `official-rust`, channel `stable-format-v1`.
- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; authority `official-rust`, channel `stable`.
- [`cargo-resolver`](https://doc.rust-lang.org/cargo/reference/resolver.html) — Dependency and feature resolution; authority `official-rust`, channel `stable`.
- [`cargo-timings`](https://doc.rust-lang.org/stable/cargo/reference/timings.html) — Cargo timings output and interpretation; authority `official-rust`, channel `stable`.
- [`cargo-unstable`](https://doc.rust-lang.org/cargo/reference/unstable.html) — Cargo unstable feature gates including codegen backends; authority `official-rust`, channel `nightly`.
- [`cargo-lints`](https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section) — Cargo lint levels, priorities, and workspace inheritance; authority `official-rust`, channel `stable`.
- [`clippy-catalog`](https://rust-lang.github.io/rust-clippy/) — toolchain-specific Clippy lint catalog; authority `official-rust-tool`, channel `toolchain-specific`.
- [`clippy-config`](https://doc.rust-lang.org/clippy/lint_configuration.html) — Clippy typed configuration keys; authority `official-rust-tool`, channel `toolchain-specific`.
- [`criterion`](https://bheisler.github.io/criterion.rs/book/) — Criterion benchmark methodology and APIs; authority `tool-owner`, channel `resolved-version`.
- [`criterion-profiling`](https://bheisler.github.io/criterion.rs/book/user_guide/profiling.html) — Criterion profiler hooks and `--profile-time` semantics; authority `tool-owner`, channel `resolved-version`.
- [`divan`](https://docs.rs/divan/latest/divan/) — Divan harness, benchmark registration, inputs, and current MSRV; authority `tool-owner`, channel `resolved-version`.
- [`pprof-rs`](https://github.com/tikv/pprof-rs) — CPU profiler features, Criterion integration, frame processing, and unwind limits; authority `tool-owner`, channel `resolved-version`.
- [`samply`](https://github.com/mstange/samply) — cross-platform sampling backends, symbols, browser/local-server behavior, and data handling; authority `tool-owner`, channel `resolved-version`.
- [`mimalloc-pprof`](https://github.com/zackees/mimalloc-pprof) — cross-platform sampled heap, allocator integration, build/runtime gating, and overhead; authority `tool-owner`, channel `resolved-version`.
- [`dhat`](https://docs.rs/dhat/latest/dhat/) — cross-platform wrapping allocator, exact allocation tracking, feature gating, and limitations; authority `tool-owner`, channel `resolved-version`.
- [`tracy`](https://github.com/wolfpld/tracy) — timeline, frame, lock, thread, memory, and GPU profiler; authority `tool-owner`, channel `resolved-version`.
- [`rust-tracy-client`](https://github.com/nagisa/rust_tracy_client) — Rust client crates, `tracing-tracy`, conditional enablement, protocol compatibility, and data-exposure warning; authority `tool-owner`, channel `resolved-version`.
- [`intel-vtune`](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html) — Intel CPU hotspots, microarchitecture, cache, and memory-access analysis; authority `tool-owner`, channel `installed-version`.
- [`amd-uprof`](https://docs.amd.com/r/en-US/63856-uProf-release-notes) — AMD uProf platform, processor, and analysis support; authority `tool-owner`, channel `installed-version`.
- [`windows-performance-recorder`](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder) — ETW capture and Windows Performance Toolkit effects; authority `official-platform`, channel `installed-version`.
- [`windows-performance-analyzer`](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer) — ETL timeline and system-event analysis; authority `official-platform`, channel `installed-version`.
- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; authority `official-tool-owner`, channel `nightly-version-sensitive`.
- [`git-worktree`](https://git-scm.com/docs/git-worktree.html) — linked worktree lifecycle and administration; authority `tool-owner`, channel `installed-git-specific`.
- [`nextest-config`](https://nexte.st/docs/configuration/reference/) — nextest profiles, groups, retries, threads, timeouts, and JUnit; authority `tool-owner`, channel `resolved-version`.
- [`nextest-coverage`](https://nexte.st/docs/integrations/test-coverage/) — nextest coverage integration; authority `tool-owner`, channel `resolved-version`.
- [`nextest-running`](https://nexte.st/docs/running/) — nextest execution, filtering, output, and doctest boundary; authority `tool-owner`, channel `resolved-version`.
- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; authority `official-tool-doc-mirror`, channel `installed-perf-specific`.
- [`perf-security`](https://docs.kernel.org/admin-guide/perf-security.html) — perf privilege and data-exposure boundary; authority `official-linux-kernel`, channel `kernel-specific`.
- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; authority `official-rust`, channel `nightly-target-specific`.
- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; authority `official-rust`, channel `toolchain-specific`.
- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; authority `official-rust`, channel `current-beta`.
- [`rustup-cross`](https://rust-lang.github.io/rustup/cross-compilation.html) — rustup cross-compilation responsibilities; authority `official-rust`, channel `current-rustup`.
- [`sccache-rust`](https://github.com/mozilla/sccache/blob/main/docs/Rust.md) — Rust compiler-wrapper caching and limitations; authority `tool-owner`, channel `resolved-version`.
