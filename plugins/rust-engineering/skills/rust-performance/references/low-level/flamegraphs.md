# Low-level Flamegraphs Protocol

> Focused decision protocol; examples are evidence, not automatic product policy.

## Routing and Scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-cargo-build` for symbols/profile selection and `$debugging` for unexplained capture failures.
- Canonical tool selection lives in [Rust profiling](./rust-profiling.md).
- Retained scope: sampled stack capture, flamegraph interpretation, cross-platform backends, differential views, and follow-up measurement.

## Required context

- metric and correctness contract.
- representative workload and data.
- target/profile/features/toolchain.
- hardware, kernel and load controls.
- baseline distribution and retained raw evidence.

## Decision protocol

1. Classify CPU, allocation, I/O, contention, binary-size, or build-time cost before choosing a tool.
2. Capture a comparable baseline and preserve raw samples, counters, reports, or build timings.
3. Use one profiler or counter set to locate a bottleneck; treat attribution as a hypothesis with tool limitations.
4. Change one variable and rerun the same workload and correctness checks.
5. Reject noise-level wins and report unmeasured targets, cold/warm state, tail behavior, and new complexity.

## Backend Choice

| Need | Prefer |
|---|---|
| Cross-platform interactive call tree/timeline | installed `samply` |
| Cross-platform SVG flamegraph from Cargo target | installed `cargo-flamegraph` |
| Unix in-process Criterion capture | `pprof-rs` with `criterion` and `flamegraph` |
| Linux PMU event sampling | `perf record`, optionally rendered as a flamegraph |

Build the selected workload with the project `profiling` profile and retain symbols. Use `cargo flamegraph --profile profiling` only after verifying the installed CLI. Samply may open a browser and local source/symbol server; cargo-flamegraph `--open` does the same kind of GUI effect. Both require authorization when executed.

## Interpretation

- Width is the proportion of captured samples containing the frame, not elapsed wall-clock time.
- The x-axis normally has no time ordering, and color normally has no cost meaning.
- Missing frames can come from sampling frequency, inlining, unwind data, stripped symbols, frame-pointer gaps, blocked/off-CPU time, or backend limitations.
- A wide caller can aggregate many children; inspect stacks and source before naming the optimization target.
- Preserve raw samples when the backend permits and compare equivalent workloads for differential views.
- Turn the suspected call path into a Criterion or representative end-to-end comparison. Never claim a speedup from the flamegraph alone.

## Guardrails

- Do not install a backend, enable DTrace, lower `perf_event_paranoid`, elevate privilege, open a viewer, or upload a profile automatically.
- Linux, macOS, and Windows backends expose different events and stack behavior; cross-platform support is not capability parity.
- Record tool/version, backend, sampling mode/frequency, profile/features/flags, symbols, workload, output, and residual blind spots.

## Evidence Gate

Reviewed 2026-08-30.

- [samply](https://github.com/mstange/samply)
- [cargo-flamegraph](https://github.com/flamegraph-rs/flamegraph)
- [pprof-rs](https://github.com/tikv/pprof-rs)
- [perf record](https://man7.org/linux/man-pages/man1/perf-record.1.html)
- [perf security](https://docs.kernel.org/admin-guide/perf-security.html)

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.