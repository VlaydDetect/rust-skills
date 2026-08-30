# Low-level Hardware Counters Protocol

> Focused decision protocol; examples are evidence, not automatic product policy.

## Routing and Scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-platforms` for OS/hardware availability and `$rust-research` for resolved tool/event semantics.
- Canonical platform routing lives in [Rust profiling](./rust-profiling.md).
- Retained scope: cache misses, branches, instructions, cycles, IPC/CPI, bandwidth, PMU event selection, multiplexing, attribution, and limitations.

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

## Platform Decision

- **Linux:** use an already installed `perf`. Discover event names with the installed `perf list`; use `perf stat` for aggregate ratios and `perf record`/`report`/`annotate` when source or instruction attribution is needed.
- **Windows on Intel CPU:** prefer an already installed Intel VTune configuration for hotspots, microarchitecture, memory access, cache, and bandwidth.
- **Windows on AMD CPU:** prefer an already installed AMD uProf configuration supported by that CPU/OS.
- **Windows scheduler/I/O question or missing vendor profiler:** use WPR + WPA for ETW context switches, ready/wait/running time, timers, wakeups, and I/O. It is not the primary PMU microbenchmark path.
- **macOS/BSD:** do not prescribe Linux `perf` behind `cfg(unix)`. Use a supported native backend or report the requested PMU evidence as `SKIP`.

## Measurement Contract

1. Name the hypothesis: cache level, branch behavior, front/back-end stalls, bandwidth, false sharing, or another concrete mechanism.
2. Record CPU model/microcode, OS/kernel, tool version, event names/raw encodings, workload, affinity, profile, features, and run controls.
3. Check unsupported events, multiplexing/scaling, skid, counter width, privilege, virtualization, and frequency/power effects.
4. Prefer ratios tied to the hypothesis and report raw counts plus elapsed/work units.
5. Repeat the same workload and use generated code or source attribution before changing the implementation.

There is no universal “bad cache-miss rate,” IPC target, or branch threshold. A lower miss count can still accompany slower code when instructions, work, or runtime conditions differ.

## Guardrails

- Do not install vendor tools/drivers, change host security, elevate privilege, or assume a counter name from another CPU.
- Do not compare Intel and AMD events as if they were identical.
- Do not use WPR/WPA capture as a replacement for Criterion or an end-to-end before/after benchmark.

## Evidence Gate

Reviewed 2026-08-30.

- [perf record](https://man7.org/linux/man-pages/man1/perf-record.1.html)
- [perf security](https://docs.kernel.org/admin-guide/perf-security.html)
- [Intel VTune](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html)
- [AMD uProf](https://docs.amd.com/r/en-US/63856-uProf-release-notes)
- [Windows Performance Recorder](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder)
- [Windows Performance Analyzer](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer)

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.