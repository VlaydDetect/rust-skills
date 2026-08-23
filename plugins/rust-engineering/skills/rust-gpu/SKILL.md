---
name: rust-gpu
description: Design and diagnose Rust GPU execution, device capability selection, host-device memory movement, buffer layout, batching, synchronization, kernel or shader dispatch, and measured bottlenecks. Use when device execution changes correctness or performance.
---

# Rust GPU Engineering

Own device and memory execution contracts without assuming a backend. Keep device facts, data layout, synchronization, batching, and measurements explicit.

## Use This Skill When

- Rust code dispatches shaders or kernels, allocates device buffers, maps memory, or transfers data between host and device.
- Workgroup shape, occupancy, alignment, coalescing, synchronization, batching, or device loss controls behavior.
- A choice among graphics/compute APIs, CUDA-family tooling, portable GPU APIs, or CPU fallback needs current evidence.

## Workflow

1. Record target OS, GPU class, driver/API constraints, device capabilities, workload shapes, precision, and correctness tolerances.
2. Resolve the project's existing backend and exact dependency versions before using crate APIs.
3. Map every buffer's element type, byte layout, alignment, ownership, access direction, lifetime, and synchronization state.
4. Minimize transfers and dispatch overhead with measured batching; keep latency and memory ceilings explicit.
5. Validate shader/kernel bounds, work partitioning, barriers, queue ordering, device loss, and fallback behavior.
6. Measure end-to-end time, transfers, queue wait, execution, readback, memory, and correctness separately.

## Decision Rules

- Do not select `wgpu`, CUDA, Vulkan, OpenCL, or another backend universally.
- GPU acceleration is conditional on workload size, arithmetic intensity, transfer cost, supported operations, and deployment evidence.
- Rust type layout is not automatically a portable device ABI; define byte layout and alignment at the boundary.
- Coalescing and occupancy advice depends on the actual device and kernel; measure rather than copy fixed launch dimensions.
- Synchronization must name the producer, consumer, visibility point, and lifetime; avoid implicit whole-device waits.
- A faster kernel is not a faster pipeline if transfers, conversion, queueing, or readback dominate.

## Boundaries and Hand-offs

- `rust-ml` owns model and tensor semantics; this profile owns device execution and memory behavior.
- `rust-performance` owns benchmark design and bottleneck evidence after GPU-specific phases are separated.
- `rust-unsafe` owns host-side unsafe layout or pointer proofs.
- Use `rust-research` for exact backend/version APIs and `rust-workflow` for implementation.

## Detailed Reference

Read [Rust GPU field guide](references/guide.md) before selecting a backend or changing buffer layout. Load the [`rust-gpu` Huiali protocol](references/huiali/rust-gpu.md) only when its memory, batching, synchronization, or fragment examples match the task.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
