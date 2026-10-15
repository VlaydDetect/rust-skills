# Low-level Windows Vendor and OS Profiling Protocol

> Focused decision protocol; examples are evidence, not automatic product policy.

## Routing and Scope

- Primary owner: `$rust-profiling`.
- Supporting profiles: `$rust-platforms` for Windows capability/effects and `$rust-research` for installed-version and CPU support.
- Canonical cross-platform routing lives in [Rust profiling](./rust-profiling.md).
- Retained scope: Intel VTune, AMD uProf, WPR/WPA, hotspots, microarchitecture, cache/memory access, bandwidth, scheduler, wakeups, waits, and I/O.

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

## Decision Matrix

| Question | Prefer |
|---|---|
| Intel CPU hotspots, cache misses, pipeline, memory access, bandwidth | already installed Intel VTune |
| AMD CPU hotspots, cache/branch/IPC/memory counters | already installed AMD uProf |
| Vendor profiler absent | WPR + WPA when Windows Performance Toolkit is already available |
| Thread repeatedly wakes, waits, or migrates | WPR + WPA |
| Latency greatly exceeds measured CPU work | WPR + WPA critical-path, scheduler, timer, and I/O analysis |
| Portable application call stacks | samply or cargo-flamegraph before escalating |

Vendor tooling owns PMU semantics for its supported processor/version. Detect the actual CPU and installed program; do not install a profiler, driver, symbol package, or Windows ADK automatically.

## Workflow

1. Reproduce the representative workload using the same `profiling` build and retain PDBs.
2. Start with hotspots or a hypothesis-specific vendor analysis, not every counter at once.
3. Record CPU model, tool/version, collection mode, driver/privilege state, symbols, profile/features, affinity, and workload.
4. Check sampling/counter coverage, unsupported events, multiplexing, and process/system scope.
5. If CPU analysis cannot explain the wall-clock gap, capture bounded ETW evidence with WPR and inspect WPA context switches, ready/wait/running time, timers, DPC/ISR, I/O, and wakeups.
6. Verify the resulting optimization with Criterion or the representative end-to-end benchmark.

## VTune Capture and Interpretation

Resolve the executable from the exact Cargo build, retain its PDB/debug identity, and check symbol diagnostics before attributing source lines. Select the application phase, process/threads and comparable useful work; do not include setup accidentally in one capture only.

Start with Hotspots (`vtune -collect hotspots -result-dir <result> -- <exact-executable> <args>` on versions supporting that syntax). Check the installed `vtune -help collect` before selecting knobs. User-mode sampling and hardware event sampling have different privileges, overhead and coverage. Do not treat a failed hardware collection as proof that software sampling or the program is broken.

Inspect absolute CPU time, elapsed time, per-thread utilization, self/inclusive cost and call stacks. CPU time sums across threads and can exceed elapsed time. A larger sample share after another stage improves does not prove this function slowed down. Use Microarchitecture Exploration (`uarch-exploration`) or Memory Access (`memory-access`) only for an actual front-end, branch, memory/NUMA or bandwidth hypothesis. Select CPU-supported events and inspect multiplexing, skid, missing stacks and frequency effects before diagnosing a stall from one ratio.

## WPR Recording and WPA Analysis

WPR records ETW; WPA analyzes the resulting ETL. Inspect `wpr -profiles` and the installed command help, select the minimum profiles/providers/stacks required by the symptom, and bound the recording interval and storage. Check for an existing recording first. Do not cancel another session to make a capture start; handle a conflict with the recording's owner.

For CPU attribution use CPU Usage (Sampled). For scheduling causality use CPU Usage (Precise), which derives intervals from context-switch and ready events. Distinguish Running, Ready (runnable but unscheduled), and Waiting (not runnable). Follow the readying thread, I/O completion, timers and application correlation along the request's critical path. Waiting on an idle worker is not automatically a bottleneck.

Check trace diagnostics, lost events, buffer limitations and symbol/stack completeness. Missing events are a coverage gap rather than evidence that work did not occur. Record capture overhead and keep the uninstrumented benchmark separate. Compare before/after absolute work and latency, not just pivot-table percentages. The [interpretation guide](../../../rust-profiling/references/profile-interpretation.md) owns shared counter, heap and timeline reasoning.

## Guardrails

- WPR writes ETL data and WPA is a GUI analysis tool; collection may require elevated/system effects and can capture sensitive system/application activity. Confirm scope, storage, duration, and authorization.
- WPA can cover part of a vendor-profiler investigation but is a less direct PMU workflow. Prefer it for OS/scheduler/I/O causality or as the installed fallback.
- Never infer AMD results from Intel event names or vice versa, and never turn a vendor threshold into universal policy.
- Missing tool, unsupported CPU, absent PDB, insufficient privilege, or unavailable ETW provider is `SKIP`, not permission to change the host.

## Evidence Gate

Reviewed 2026-10-15.

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [Intel VTune](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html)
- [AMD uProf release and support notes](https://docs.amd.com/r/en-US/63856-uProf-release-notes)
- [Windows Performance Recorder](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder)
- [Windows Performance Analyzer](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer)
- [CPU Usage Sampled and Precise](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/cpu-analysis)
- [VTune collection types and knobs](https://www.intel.com/content/www/us/en/docs/vtune-profiler/user-guide/2025-4/collect.html)

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
