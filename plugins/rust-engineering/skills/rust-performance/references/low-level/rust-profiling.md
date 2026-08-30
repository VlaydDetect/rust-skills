# Low-level Rust Profiling Protocol

> Focused decision protocol; examples are evidence, not automatic product policy.

## Routing and Retained Scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-cargo-build` for Cargo profiles and symbols, `$rust-platforms` for OS and global-allocator constraints, `$rust-observability` for `tracing` span semantics, and `$rust-unsafe`/`$rust-unsafe-ffi` for sanitizer evidence.
- Retained scope: Criterion and Divan, CPU sampling, flamegraphs, heap profiling, PMU counters, Tracy timelines, Windows ETW analysis, readable symbols, and comparable before/after evidence.
- Baseline correction: do not install tools, change host security, open a GUI/browser, upload a trace, start network discovery, assume artifact paths, or pin arbitrary versions without authorization. A profile selects a hypothesis; a comparable benchmark establishes improvement.

## Required Context

- metric, correctness contract, workload, and stopping condition;
- target, Cargo profile, features, toolchain, relevant flags, allocator, and symbol files;
- OS/kernel, CPU vendor/model, hardware class, power/thermal/load controls, and required privileges;
- exact installed tool/version and its process, output, GUI, browser, network, upload, driver, ETW, and host-configuration effects;
- baseline distribution and retained raw evidence.

## Decision protocol

1. Classify CPU, allocation, I/O, contention, binary-size, or build-time cost before choosing a tool.
2. Capture a comparable baseline and preserve raw samples, counters, reports, or build timings.
3. Use one profiler or counter set to locate a bottleneck; treat attribution as a hypothesis with tool limitations.
4. Change one variable and rerun the same workload and correctness checks.
5. Reject noise-level wins and report unmeasured targets, cold/warm state, tail behavior, and new complexity.

## Project-owned `profiling` Profile

Define custom profiles at the workspace root:

```toml
[profile.profiling]
inherits = "release"
debug = true
strip = "none"
```

Use `cargo build --profile profiling` or `cargo bench --profile profiling`. Resolve the artifact from effective Cargo metadata and the selected target/profile; do not hardcode `target/profiling` when the project changes target directories.

Do not add LTO, `panic = "abort"`, `codegen-units = 1`, target CPU flags, or an allocator to this profile. They change the workload and belong to separate measured experiments. Keep frame pointers command-scoped with `-C force-frame-pointers=yes` when the selected backend requires them, and record the flag. Do not place a profiling profile or rustflags in global Cargo configuration.

## Tool Selection Matrix

| Question | Primary path | Constraints and fallback |
|---|---|---|
| Maintained microbenchmark or regression evidence | Criterion | Use groups, representative inputs, throughput, setup isolation, baselines, and identical environments |
| Minimal local function benchmark | Divan | Exploratory only when Criterion baseline/profiler integration is not required |
| CPU stacks on Linux/macOS/Windows | Installed `samply` or `cargo-flamegraph` | Backends and on/off-CPU capabilities differ by OS; browser/GUI effects require approval |
| In-process CPU profiling on POSIX/Unix | `pprof-rs` | Criterion/flamegraph integration; signal/unwinding limits apply |
| Sampled live heap on Windows/Linux/macOS | `mimalloc-pprof` | Only when the binary already owns mimalloc or an allocator change is separately measured |
| Every Rust heap allocation in a bounded run | crate `dhat` | Global allocator, source changes, experimental/high overhead, no memory-access tracking |
| Frames, zones, locks, threads, GPU timeline | Tracy through `rust_tracy_client` | Conditional instrumentation, version/protocol match, possible local-network/source exposure |
| Cache misses and PMU events on Linux | installed `perf stat`/`perf record` | Select events from `perf list` for the exact CPU; never weaken host policy automatically |
| Cache misses and microarchitecture on Windows/Intel | installed Intel VTune | Verify supported CPU, driver/permissions, symbols, and selected analysis |
| Cache misses and microarchitecture on Windows/AMD | installed AMD uProf | Verify supported CPU/OS and the installed analysis configuration |
| Scheduler, wakeups, waits, I/O, unexplained latency on Windows | WPR capture plus WPA analysis | Heavy ETW path; use when vendor tools are absent or the question is OS-level causality |
| Unsafe, FFI, C/C++, custom allocator validity | rustc sanitizer plus matching native instrumentation | Explicit target/toolchain/runtime coverage; route interpretation to unsafe/FFI |

`samply` and `cargo-flamegraph` are cross-platform entry points, not capability equivalence claims. Linux `perf` is not a generic `cfg(unix)` tool: macOS and BSD need their available platform backend or an explicit `SKIP`.

## Criterion and `pprof-rs`

- Criterion `--profile-time <seconds>` repeats the benchmark without normal analysis or saving results. Use it for profiler capture, not for a benchmark comparison.
- A direct Criterion executable requires `--bench`. Resolve its path from Cargo output/metadata.
- `pprof-rs` features `criterion` and `flamegraph` provide Criterion hooks and SVG output. `Frames` and `frames_post_processor` are APIs, not a Cargo feature named `frames`.
- The optional `frame-pointer` feature selects frame-pointer unwinding and is nightly/build-std sensitive. It does not remove the need to compile relevant code with usable frame pointers.
- The default libunwind path and signal-driven sampling have safety and completeness limits; missed or truncated stacks remain tool limitations, not application facts.

## Cross-platform CPU Sampling

### `samply`

Build optimized code with debug information, then record the resolved artifact. Samply supports macOS, Linux, and Windows; current backends do not provide identical data. Windows/macOS can include off-CPU samples, while Linux sampling uses perf events.

`samply record` normally opens Firefox Profiler in a browser and starts a local symbol/source server. Data stays local until the user chooses upload, but browser launch, local serving, symbol-server network access, and upload are distinct effects that require approval. Never copy upstream `sudo` or `perf_event_paranoid` recipes into an automatic workflow.

### `cargo-flamegraph`

Use the installed version's `--profile profiling` support and select a package/target explicitly. Linux uses perf, macOS uses a platform backend, and Windows has a native backend with optional DTrace support. `--open`, privilege flags, and host-policy changes are never automatic.

A flamegraph's box width is sample proportion. The x-axis is not elapsed time and color is normally not cost. Preserve raw samples when possible and verify any optimization with Criterion or the representative end-to-end benchmark.

## Heap Profiling

### `mimalloc-pprof`

Use only at the binary/composition root and only when it is already the process allocator or a separately authorized, measured allocator experiment selects it. A reusable library must not impose it, and one process must not link two mimalloc implementations.

There are two independent controls:

1. **Build-time:** resolve the crate's current feature contract. Versions that expose compile-out support can use `default-features = false` to omit sampled pprof hooks while retaining the allocator/no-op profiler API; C/C++ builds use their resolved `MI_PPROF=OFF` contract. Map an application-owned feature such as `heap-profiling` to the resolved dependency capability rather than inventing a crate feature name.
2. **Runtime:** an instrumented build remains opt-in through the resolved `prof::start`/`prof::stop` API or `MIMALLOC_PROF` environment contract. Runtime-off hooks can still add per-allocation overhead, so compile them out when production throughput matters more than runtime activation.

The output is a sampled live-heap profile, not a record of every allocation. Dump while allocations of interest remain live. On Linux/macOS, keep frame pointers throughout the libraries whose stacks matter; on Windows x64 retain matching PDBs and unwind data.

### crate `dhat`

Use `dhat` for a short, focused, cross-platform run that must account for every allocation observed by its wrapping global allocator. Gate both the allocator and profiler with a project feature, run release-like code with debug information, and isolate allocation-count tests because the test harness and global state can perturb exact counts.

`dhat` is experimental and can slow the program substantially, especially where backtrace capture is expensive. It does not track memory reads/writes or allocations outside its profiler lifetime. It must not be enabled in ordinary production builds.

## Tracy Timeline

Use Tracy through `tracy-client`/`rust_tracy_client` for application zones, frames, locks, threads, memory events, plots, and GPU timelines. If the project already uses `tracing`, `tracing-tracy` is the narrow adapter; `rust-observability` still owns span names, fields, cardinality, and redaction.

Gate `tracy-client`, `tracing-tracy`, and `tracy-client-sys` with their resolved `enable` feature and a project capability. Match the client crates to the Tracy protocol version. Depending on configuration, discovery packets and captured source/assembly/trace data can be exposed to the local network, so capture and viewer/network effects require explicit approval.

## Cache Misses and Windows Escalation

- On Linux, start with `perf list`, then choose `perf stat` ratios or `perf record` sampling for the concrete cache/branch hypothesis. Event names, raw encodings, multiplexing, skid, and thresholds are CPU/kernel-specific.
- On Windows with an Intel CPU, prefer an already installed VTune for hotspots, microarchitecture, cache, bandwidth, and memory access. With an AMD CPU, prefer an already installed AMD uProf configuration. Do not install vendor tools or drivers automatically and do not infer results across CPU vendors.
- Use WPR + WPA when vendor tooling is absent or the question is “why does this thread keep waking?” / “why is latency 30 ms when CPU work is 4 ms?”. WPR records ETW events; WPA analyzes ETL timelines, context switches, ready/wait/running time, I/O, timers, and wakeups. This workflow complements rather than replaces the comparable benchmark.

## Sanitizer Branch

Unsafe Rust, FFI, C/C++, and custom allocators require a separate evidence path:

- select only sanitizer modes and targets documented by the current rustc;
- use an explicit `--target` so host build scripts and proc macros are not instrumented accidentally;
- use repository-pinned nightly and `build-std` when required;
- instrument C/C++ with the matching Clang sanitizer/runtime and use `external-clangrt` where the current Rust contract requires it;
- state every uninstrumented library, allocator, runtime, target, input, and schedule gap;
- do not recommend a Rust `undefined` sanitizer mode, which rustc does not expose.

See [Rust sanitizer and Miri protocol](../../../rust-unsafe/references/low-level/rust-sanitizers-miri.md) and [FFI policy](../../../rust-unsafe-ffi/references/guide.md).

## Failure Modes and Guardrails

- Comparing captures or benchmarks with different profiles, flags, features, allocators, targets, or workloads.
- Treating samples as exhaustive events, sampled heap as exact allocation history, or timeline correlation as causation without a focused check.
- Shipping always-on profiler hooks or network-capable instrumentation without measuring disabled-path cost and reviewing data exposure.
- Installing tools, opening viewers, uploading traces, adding symbol servers, enabling ETW, elevating privilege, or changing host configuration implicitly.
- Treating a missing tool, symbol file, hardware counter, nightly component, or target as a product regression instead of `SKIP`.

Record the exact command, tool version, target, scope, output location, effects, result, and residual risk.

## Evidence Gate

Reviewed 2026-08-30; re-check resolved versions before execution.

- [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html) — custom-profile inheritance, debug information, stripping, and workspace-root ownership.
- [Criterion](https://bheisler.github.io/criterion.rs/book/) and [profiling mode](https://bheisler.github.io/criterion.rs/book/user_guide/profiling.html) — benchmark methodology, hooks, and `--profile-time`.
- [Divan](https://docs.rs/divan/latest/divan/) — minimal harness, registration, inputs, and current MSRV.
- [pprof-rs](https://github.com/tikv/pprof-rs) — features, Criterion integration, frame processing, and unwinding limits.
- [samply](https://github.com/mstange/samply) — macOS/Linux/Windows backends, symbol requirements, browser/local-server behavior, and data handling.
- [cargo-flamegraph](https://github.com/flamegraph-rs/flamegraph) — cross-platform backends and resolved CLI surface.
- [mimalloc-pprof](https://github.com/zackees/mimalloc-pprof) — sampled heap, build/runtime gating, platforms, symbols, and disabled-path overhead.
- [dhat](https://docs.rs/dhat/latest/dhat/) — wrapping allocator, exact allocation accounting, feature gating, and limitations.
- [Tracy](https://github.com/wolfpld/tracy) and [Rust Tracy client](https://github.com/nagisa/rust_tracy_client) — timeline capabilities, adapter, protocol compatibility, conditional enablement, and network/data warning.
- [perf record](https://man7.org/linux/man-pages/man1/perf-record.1.html) and [perf security](https://docs.kernel.org/admin-guide/perf-security.html) — Linux PMU capture and privilege boundary.
- [Intel VTune](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html) and [AMD uProf](https://docs.amd.com/r/en-US/63856-uProf-release-notes) — vendor analysis and supported hardware/OS contracts.
- [Windows Performance Recorder](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder) and [Windows Performance Analyzer](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer) — ETW capture and ETL analysis.
- [rustc sanitizers](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — current modes, target matrix, `build-std`, and foreign-runtime integration.
