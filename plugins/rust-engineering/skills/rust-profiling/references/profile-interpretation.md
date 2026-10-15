# Interpreting Profiles and Traces

## Validate Attribution First

Identify the capture interval, process/threads, workload phase, useful work completed, collection mode, sampling period and dropped events or stacks. Confirm exact binary/debug identity and symbolization. Unresolved frames, failed unwinding, inlining and line-table drift are attribution limitations, not proof that the application executed the displayed source line most often.

| Observation | Interpretation | Next discriminating evidence |
|---|---|---|
| A flamegraph box is wide | Many included samples traverse that stack | Absolute CPU/work, self versus inclusive cost, caller and phase |
| A function's share rises after a change | Its relative fraction rose; absolute cost may have fallen | Same useful work, total CPU/time and absolute attribution |
| CPU time exceeds elapsed time | Threads can execute concurrently | Per-thread/core utilization and actual completion path |
| Elapsed time greatly exceeds CPU work | Waiting/ready time, external work or under-observed execution may dominate | Scheduler/I/O timeline, scope and stack quality |
| Many allocations but low live heap | Churn, not necessarily retained-memory pressure | Bytes/rate, lifetimes, allocator cost and peak memory |
| Live heap falls but RSS does not | Allocator/OS retention or other mappings may dominate | Working set, retained pages, size classes, mappings and phase |

Flamegraph x position is not elapsed chronology and color is usually not cost. Inclusive frames overlap; summing them double-counts work. Compare matching workloads and capture durations before using differential views. Samples describe observed execution, not every event or a direct speedup.

## Counters and Microarchitecture

Start from a mechanism: dependent loads, branch misses, bandwidth, front-end pressure, false sharing or compute throughput. Resolve available events for the exact CPU/kernel/tool, including hybrid core types. Normalize events by useful work and interpret IPC/cycles with frequency, utilization and stalls. More retired instructions can still reduce elapsed time.

Inspect event scope, privilege exclusions, multiplex time/scaling, sampling skid, lost events and stack completeness. A counter percentage alone cannot prove memory bandwidth saturation; compare achieved bandwidth, working-set behavior and the CPU's relevant limits. Do not convert CPU/vendor-specific warning thresholds into general Rust rules. Virtualization or permissions can make a desired event unavailable.

## VTune and Windows Performance Toolkit

Use the [Windows procedure](../../rust-performance/references/low-level/intel-vtune-amd-uprof.md). VTune Hotspots locates CPU work; use Microarchitecture Exploration or Memory Access only when the hypothesis needs their hardware data. Distinguish user-mode sampling from hardware event sampling and verify installed CPU/driver/privilege support. Retain the exact EXE/PDB and inspect symbol diagnostics.

WPR records ETW and WPA analyzes ETL. CPU Usage (Sampled) attributes sampled running activity. CPU Usage (Precise) uses context-switch/ready events to inspect Running, Ready and Waiting intervals. Follow the thread that readies a critical-path thread, I/O completions and relevant dependencies. An idle worker's long wait is not a problem unless the requested operation depends on it. A thread waiting on a lock and a runnable thread waiting for a CPU need different changes.

Use bounded captures around the reproduced symptom with the required providers/stacks. Check trace diagnostics, event loss, buffer limitations and capture overhead before explaining missing activity. Do not stop another user's recording or broaden system-wide tracing implicitly. Collection authority comes from the user/task; installation, elevation, external symbol downloads and trace upload remain separate effects.

## Heap and Timeline Evidence

Heaptrack or a wrapping allocation profiler observes allocations within its coverage; sampled live-heap profilers estimate live allocation populations. Neither automatically covers foreign/custom allocators or all process memory. Record profiler lifetime, sampling/stack configuration, allocator and excluded libraries. Compare equivalent phases and useful work; a snapshot taken after objects die cannot locate their earlier retained cost.

Tracy/application spans can connect stages, locks, queues and threads. Check nesting, clocks, correlation and disabled/enabled instrumentation overhead. Existing `tracing` semantics belong to `rust-observability`. Timeline coincidence is a hypothesis; validate a dependency with a focused perturbation or causal event chain.

## Limits and Handoff

State what was observed, what remains ambiguous, and the smallest useful next capture. Use `debugging` when an observation contradicts correctness or cannot be reproduced. Give `rust-optimization` the limiting resource, cost magnitude, workload conditions and a disconfirming prediction. Do not propose an allocator, lock-free structure or unchecked access merely because its corresponding tool appears in this guide.
