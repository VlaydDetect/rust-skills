# Rust GPU Field Guide

Research baseline: **2026-08-23**. Re-run `rust-research` for backend releases, adapter support, limits, shader toolchains, validation rules, and driver advisories before a version-sensitive change.

## Execution Brief

Capture target OS and architecture, GPU families, driver and API floor, deployment update control, workload dimensions and distribution, input and output layouts, numerical tolerance, latency and throughput targets, memory ceiling, portability, startup budget, cancellation, device-loss handling, and CPU fallback. Treat hardware facts not measured or queried as unknown.

Choose a backend from the deployment contract. `wgpu` provides a portable graphics and compute abstraction with backend-dependent capabilities. Vendor CUDA-family tooling can expose different operations and packaging requirements. Raw Vulkan, Metal, or Direct3D may be justified by an existing renderer or an unavailable abstraction, but they expand unsafe and synchronization surface. No backend is a universal default.

## rust-gpu Toolchain Boundary

[`rust-gpu`](https://github.com/Rust-GPU/rust-gpu) is an experimental Rust-to-SPIR-V compiler, not a stable general-purpose GPU runtime. Its releases are coupled to exact nightly compiler toolchains; the snapshot changelog showed an alpha line with a specifically pinned nightly. Isolate shaders in a dedicated workspace or package with its own toolchain file and dependency resolution so the application toolchain can remain stable.

Keep shader crates small and device-compatible. Do not assume ordinary Rust standard-library, allocation, panic, trait-object, recursion, or pointer behavior is available on SPIR-V. Validate produced modules with the relevant SPIR-V validator and the target backend. Preserve CPU parity fixtures for algorithm semantics and compile shaders in CI on the pinned toolchain. An alpha compiler upgrade is a deliberate migration with output validation, not a routine patch bump.

## wgpu Adapter and Device Contract

With [`wgpu`](https://docs.rs/wgpu/latest/wgpu/), enumerate adapters under the actual power and surface requirements, then inspect features, limits, downlevel capabilities, formats, and queue support. Request only features the application uses and limits no higher than required. Define a fallback or actionable startup failure when no adapter satisfies the contract.

Treat adapter selection and device creation as fallible. Capture uncaptured validation errors, out-of-memory behavior, device loss, and surface reconfiguration. Rebuild resources or exit cleanly according to product requirements; do not assume a device remains valid forever. Pipeline caches and compiled shader artifacts are backend-, driver-, adapter-, and version-sensitive: validate compatibility, tolerate rejection, and never make cache presence necessary for correctness.

## Host-Device Layout

For every buffer and texture record host owner, device owner, allocation location, element type, byte layout, alignment, stride, padding, format, usage flags, access direction, upload or readback path, reuse policy, and synchronization state. Rust `repr(Rust)` is not a device ABI. Use an explicitly compatible representation, checked conversion, and compile-time or byte-level layout tests.

Uniform, storage, copy, and dynamic-offset alignments can differ. Account for row-pitch and texture-copy alignment, matrix convention, bool and enum representation, padding bytes, and minimum binding sizes. Never cast arbitrary structs into bytes merely because the total size happens to match. Keep device bytes free of uninitialized padding when validation, hashing, or information exposure matters.

Prefer persistent reusable buffers and fewer transfers when measurements support batching, but bound resident memory and added latency. Staging belts, mapped buffers, and asynchronous readback have lifetimes: do not write while the device reads, reuse a range before completion, or drop callback state too early. Distinguish host mapping completion from GPU execution completion.

## Dispatch and Synchronization Review

- Prove bounds for every invocation, index calculation, and tail element with checked host-side sizes.
- Match work decomposition to the algorithm before tuning workgroup dimensions; query applicable limits.
- Define producer, consumer, access mode, visibility point, and lifetime for every dependency.
- Distinguish workgroup barriers, command ordering, queue submission, mapping callbacks, fences, and whole-device waits.
- Avoid read-after-write, write-after-read, and buffer-reuse races across submissions.
- Surface shader compilation, pipeline creation, validation, unsupported feature, timeout, out-of-memory, device-loss, and fallback errors.

GPU APIs can validate declared usage but cannot prove algorithmic synchronization inside a shader. Avoid unnecessary barriers and global waits, yet never remove synchronization from timing alone without a correctness model. Dispatch order can be deterministic while floating-point reductions are not bitwise deterministic.

## Measurement Ladder

1. Establish a correct CPU or trusted reference result on representative and adversarial shapes.
2. Measure cold and warm end-to-end wall time, including adapter or context setup and pipeline compilation.
3. Separate data conversion, upload, queue delay, execution, download, validation, and cache effects.
4. Vary batch size, workgroup shape, and input distribution while recording latency distributions and peak device and host memory.
5. Compare against the real production fallback, including its preprocessing and threading.
6. Repeat on the supported adapter and driver matrix, not only the development GPU.

Accept an optimization only when the complete pipeline improves under product constraints. A faster kernel can lose after transfers, format conversion, compilation, synchronization, or readback. Record warmup policy so benchmark-only priming is not mistaken for production latency.

## Required Evidence

- Capability query or deployment contract for each target class.
- Exact backend, crate, driver, shader compiler, and toolchain versions when APIs or generated code matter.
- Byte-layout and alignment tests for host-device structures.
- CPU or trusted-reference comparisons with tolerances, special values, empty and non-multiple work sizes.
- Device-loss, invalid-shader, capacity, cancellation, timeout, and fallback tests.
- Measurements that include transfer, compilation, synchronization, and memory costs.

## Compiling Example

The dependency-free fixture in `../examples/golden/` plans batch size from explicit transfer, memory, and latency budgets. It models the decision without pretending to execute on absent hardware.

## Primary Sources

- [`rust-gpu` source and release history](https://github.com/Rust-GPU/rust-gpu)
- [`wgpu` documentation](https://docs.rs/wgpu/latest/wgpu/)

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-gpu`](./gpu.md) — primary; Device capabilities, memory hierarchy, transfer cost, alignment, coalescing, batching, synchronization, and measurement.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
