# Optimizing a System Across Components

## Map Useful Work Through the System

Follow one representative operation from arrival to completion. Record stages, concurrency, queues, ownership transfers, materialization, copies, allocations, I/O, and synchronization. Use correlation or timeline evidence when stages overlap. The hottest CPU function can be off the latency-critical path, and the critical path can run through a different thread or process.

Build a compact cost ledger: absolute stage cost, execution frequency, useful throughput, queued/in-flight work, bytes transferred, retained/peak memory, and evidence quality. Do not add overlapping CPU and I/O durations as if they were serial elapsed time. Normalize CPU or bytes by completed useful work as well as recording utilization.

## Find the Limiting Resource

| Observation | Distinguishing experiment | Candidate direction |
|---|---|---|
| One core saturates while workers wait | Per-thread CPU plus ready/wait and queue traces | Shared ownership, serial stage, load distribution |
| CPU falls but latency stays high | Follow wakeups, I/O completion and dependencies | Waiting, scheduling, timers, remote service |
| More workers stop improving throughput | Sweep concurrency and inspect memory/lock/I/O counters | Bandwidth, contention, false sharing, oversubscription |
| Allocation reduction raises RSS or tails | Observe lifetimes, peak retention and fragmentation | Oversized pooling, batching or cache retention |
| Offloading improves a small case but loses at scale | Measure transfer rate, copies, topology and queue depth | A new shared transport or networking core saturates |

Validate the load generator first: achieved versus offered rate, client CPU/network, pending operations, timeout/drop counts, and latency measured from intended arrival. A closed-loop client can hide saturation by issuing fewer requests while the service stalls. A fixed amount of completed work alone cannot establish an offered-load tail-latency improvement.

## Coordinate Changes Without Losing Causality

Keep one end-to-end objective and common workload across the phases. Local benchmarks answer stage questions; the system experiment judges the outcome. Consider eliminating duplicate validation, serialization, intermediate materialization or copies across a boundary only after proving that boundary's obligations still hold.

Start with one explanatory variable where practical. A hypothesis may require a coordinated producer/consumer or representation change; preserve intermediate variants or ablations that isolate useful contributions. Do not attribute the final speedup to one local optimization if several stages, dependencies or configurations changed.

Batching trades per-item overhead for queueing and memory. Sharding trades synchronization for skew, duplication and cross-shard operations. Caching trades recomputation for invalidation, retention and contention. Offloading trades local work for transfer, completion and synchronization overhead. Evaluate both latency and throughput at representative load, including overload and recovery when relevant.

## Re-profile After Each Accepted Phase

Repeat the critical-path and saturation analysis after a successful change. A former secondary stage can become dominant; spending the remaining effort on the old bottleneck can have little value. Inspect adjacent inputs, cold start, update paths and rare variants before accepting a broad improvement.

Use `rust-workflow` to split changes when the `3/6/10` routing circuit breakers are crossed. The invariant ledger and common performance budget survive the split; each phase gets a fresh owner and acceptance evidence. Do not split an atomic representation change in a way that temporarily violates correctness.

## Completion Record

State useful-work metrics before/after, uncertainty, resource costs, functional verification, current bottleneck, deployment/fleet assumptions, and unmeasured scenarios. A controlled rollout, A/B or rollback check may strengthen causal evidence when such deployment work is already authorized. A library microbenchmark alone never establishes a production fleet saving or service percentile.
