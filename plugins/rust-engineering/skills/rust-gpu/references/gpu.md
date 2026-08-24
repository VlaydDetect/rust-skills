# Specialized Rust Gpu Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-gpu`.
- Supporting profiles when needed: `$rust-ml`, `$rust-performance`.
- Scope retained: Device capabilities, memory hierarchy, transfer cost, alignment, coalescing, batching, synchronization, and measurement.
- Baseline correction: Do not choose wgpu, CUDA, or another backend universally. Resolve the target, device capabilities, dependency version, data layout, and measurement plan first.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## GPU Memory Architecture

```
┌─────────────────────────────────────────┐
│              GPU memory                  │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐       │
│  │   Global    │  │   Shared    │       │
│  │   Memory    │  │   Memory    │       │
│  │  (VRAM)     │  │  (SMEM)     │       │
│  └─────────────┘  └─────────────┘       │
│                                         │
│  ┌─────────────┐  ┌─────────────┐       │
│  │  Constant   │  │   Local     │       │
│  │   Memory    │  │   Memory    │       │
│  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────┘
        ↓                    ↑
   CPU (over PCIe)      GPU compute units
```


## Memory-Type Comparison

| Memory type | Location | Latency | Size | Purpose |
|---------|------|------|------|------|
| Global | VRAM | High | Large | Input/output data |
| Shared | SMEM | Low | Small | Communication within a thread block |
| Constant | Cache | Medium | Medium | Read-only data |
| Local | Registers/VRAM | High | Small | Thread-private data |
| Register | SM | Lowest | Very small | Thread-private data |


## CUDA Memory Management (rust-cuda)<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use rust-cuda or cuda-sys
use cuda_sys::ffi::*;

// Allocate device memory
let mut d_ptr: *mut f32 = std::ptr::null_mut();
unsafe {
    cudaMalloc(&mut d_ptr as *mut *mut f32, size * std::mem::size_of::<f32>())
};

// Copy from host to device
unsafe {
    cudaMemcpy(
        d_ptr as *mut c_void,
        h_ptr as *const c_void,
        size * std::mem::size_of::<f32>(),
        cudaMemcpyHostToDevice
    );
};

// Copy from device to host
let mut h_result: Vec<f32> = vec![0.0; size];
unsafe {
    cudaMemcpy(
        h_result.as_mut_ptr() as *mut c_void,
        d_ptr as *const c_void,
        size * std::mem::size_of::<f32>(),
        cudaMemcpyDeviceToHost
    );
};

// Free device memory
unsafe {
    cudaFree(d_ptr as *mut c_void);
};
```


## Zero-Copy Memory<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Zero-copy: share memory between the host and device
let mut h_ptr: *mut f32 = std::ptr::null_mut();

// Allocate pinned (page-locked) memory with cudaMallocHost
unsafe {
    cudaMallocHost(&mut h_ptr as *mut *mut f32, size * std::mem::size_of::<f32>())
};

// The GPU can access pinned memory directly without a copy,
// but pinning increases system-memory pressure

// Copy asynchronously with cudaMemcpyAsync, overlapping transfer and computation
let stream: cudaStream_t = std::ptr::null_mut();
unsafe {
    cudaMemcpyAsync(
        d_ptr as *mut c_void,
        h_ptr as *const c_void,
        size * std::mem::size_of::<f32>(),
        cudaMemcpyHostToDevice,
        stream
    );
};

// Wait for synchronization
unsafe {
    cudaStreamSynchronize(stream);
};
```


## Unified Memory<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use unified memory so the CPU and GPU manage data migration automatically
let mut unified_ptr: *mut f32 = std::ptr::null_mut();

unsafe {
    // Allocate unified memory
    cudaMallocManaged(&mut unified_ptr as *mut *mut f32, size * std::mem::size_of::<f32>());
};

// CPU access
unsafe {
    for i in 0..size {
        *unified_ptr.add(i) = i as f32;
    }
};

// GPU access (automatically migrated to the device)
// Launch the CUDA kernel
launch_kernel(unified_ptr, size);

// CPU accesses the result (automatically migrated back to the host)
unsafe {
    println!("Result: {}", unified_ptr.add(0).read());
};

// Free the memory
unsafe {
    cudaFree(unified_ptr as *mut c_void);
};
```


## Coalesced Memory Access<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Coalesced-access pattern: optimize global-memory bandwidth
// ❌ Incorrect: non-coalesced access
__global__ void bad_access(float* data) {
    int idx = threadIdx.x + blockIdx.x * 32; // Strided access
    float value = data[idx * 32];  // Adjacent threads access values 32 * sizeof(float) apart
}

// ✅ Correct: coalesced access
__global__ void coalesced_access(float* data) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x; // Contiguous access
    float value = data[idx];  // All threads access contiguous values
}
```


## Using Shared Memory<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use shared memory to reduce global-memory accesses
__global__ void shared_memory_reduce(float* input, float* output) {
    __shared__ float sdata[256];  // 256 bytes of shared memory per block

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // Load from global memory into shared memory
    sdata[tid] = input[idx];
    __syncthreads();

    // Reduction
    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        __syncthreads();
    }

    // Write back the result
    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}
```


## Memory Alignment<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Memory-alignment optimization
const size_t ALIGNMENT = 256;  // 256-byte alignment

// Pointers returned by cudaMalloc are already aligned,
// but custom data structures require explicit alignment
struct alignas(256) AlignedData {
    float4 position;  // 16 bytes
    float4 normal;    // 16 bytes
    // ... automatically padded to 256 bytes
};

// Check alignment
assert(((uintptr_t)ptr % ALIGNMENT) == 0);
```


## Performance-Optimization Checklist

| Optimization | Checkpoint |
|-------|-------|
| Memory coalescing | Threads access contiguous memory |
| Shared memory | Reduce global-memory accesses |
| Memory alignment | Align to 256 bytes |
| Asynchronous operations | Overlap computation and transfer |
| Pinned memory | Use page-locked memory |
| Batching | Reduce kernel-launch overhead |


## Related Skills

```
rust-gpu
    │
    ├─► rust-performance → performance optimization
    ├─► rust-unsafe → low-level memory operations
    └─► rust-embedded → no_std devices
```
