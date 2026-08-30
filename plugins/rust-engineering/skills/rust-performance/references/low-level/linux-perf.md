# Low-level Linux Perf Protocol

> Focused decision protocol; examples are evidence, not automatic product policy.

## Routing and Scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-cargo-build` for symbols/frame flags and `$debugging` for capture failures.
- Retained scope: `perf list`, `stat`, `record`, `report`, `annotate`, stack collection, event selection, and failure diagnosis on Linux.
- Linux `perf` is not a portable Unix interface.

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

## Decision Protocol

1. Build the representative target with the workspace-owned `profiling` profile.
2. Resolve the actual artifact and installed perf version.
3. Use `perf list` to select events available for the concrete CPU/kernel.
4. Use `perf stat` for aggregate cycles, instructions, cache/branch events, or a hypothesis-specific group.
5. Use `perf record` plus `report`/`annotate` when call-path or instruction attribution is required.
6. Select frame-pointer, DWARF, or LBR call graphs from the binary, CPU, kernel, and installed perf capabilities; record the choice.
7. Repeat comparable runs and confirm any source change with Criterion or the representative end-to-end benchmark.

## Interpretation

- Event names and raw encodings vary by CPU; unsupported or silently substituted events invalidate the claim.
- Multiplexed events are scaled estimates. Record scheduling/coverage and avoid oversized groups.
- Sampling skid can attribute an event near rather than exactly at the causing instruction.
- Cache misses require level, access type, work unit, and denominator; raw counts alone do not identify a fix.
- Frame-pointer and DWARF stacks have different build and runtime costs. Use command-scoped `-C force-frame-pointers=yes` only when selected.

## Security and Effects

`perf_event_paranoid`, capabilities, kernel modules, tracepoints, system-wide capture, and root access are host security policy. Never lower, install, or elevate automatically. A denied event, absent perf binary, unsupported counter, or insufficient symbol/unwind data is `SKIP` or an authorization request.

## Evidence Gate

Reviewed 2026-08-30.

- [perf record](https://man7.org/linux/man-pages/man1/perf-record.1.html)
- [perf security](https://docs.kernel.org/admin-guide/perf-security.html)
- [rustc codegen options](https://doc.rust-lang.org/rustc/codegen-options/index.html)
- [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html)

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.