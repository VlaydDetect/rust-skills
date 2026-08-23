# Rust GPU Field Guide

## Execution Brief

Capture device/API support, dependency version, workload dimensions, input/output layout, precision, latency and throughput targets, memory ceiling, portability, failure handling, and CPU fallback. Treat unknown hardware facts as unknowns rather than filling them with common defaults.

## Memory Map

For every resource record host owner, device owner, allocation location, alignment, stride, format, access flags, upload/readback path, reuse policy, and synchronization state. Include padding in structs and matrices. Prefer fewer large, reusable transfers when evidence supports batching, but bound the additional latency and resident memory.

## Dispatch Review

- Prove bounds for every invocation and tail element.
- Match work decomposition to the actual algorithm before tuning group dimensions.
- Distinguish intra-group barriers, queue ordering, host/device fences, and device-wide waits.
- Avoid read-after-write and reuse races across command submissions.
- Surface compilation, validation, out-of-memory, device-loss, timeout, and unsupported-feature errors.

## Measurement Ladder

1. Establish a correct CPU/reference result and representative inputs.
2. Measure end-to-end wall time and warmup behavior.
3. Separate conversion, upload, queue wait, execution, download, and validation.
4. Vary batch size and input shape while recording latency distributions and memory.
5. Compare against the real fallback, not a deliberately weak baseline.

## Required Evidence

- Capability query or deployment contract for the target.
- Exact resolved backend/crate version when API details matter.
- Byte-layout tests or explicit serialization for host/device structures.
- Correctness comparisons with stated tolerances.
- Measurements that include transfer and synchronization costs.

## Compiling Example

The dependency-free fixture in `../examples/golden/` plans batch size from explicit transfer, memory, and latency budgets. It models the decision without pretending to execute on absent hardware.

