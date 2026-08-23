# Rust Machine Learning Field Guide

Research baseline: **2026-08-23**. Re-run `rust-research` for current framework releases, operator and backend support, native ABI requirements, model-format advisories, and maintenance state before adoption.

## Core Model Contract

ML correctness is pipeline parity, not merely loading the same weight file. Version and hash the full contract:

- model architecture, weight format and hash, tokenizer or feature vocabulary, labels, and domain metadata;
- input decoding, resizing, normalization, tokenization, truncation, padding, masks, and special tokens;
- tensor names, ranks, dynamic dimensions, dtype, layout, contiguous requirements, device, and precision;
- evaluation versus training mode, random seeds, sampling parameters, state or cache initialization, and numerical tolerances;
- output decoding, thresholding, ranking, non-maximum suppression, detokenization, and domain postprocessing.

Validate rank, each dimension, dtype, finite/range policy, layout, and device before execution. A tensor conversion that succeeds can still transpose channels, reinterpret labels, or broadcast the wrong dimension and yield plausible output. Keep golden fixtures from a trusted reference implementation and compare the final domain output as well as selected intermediate tensors.

## Framework Selection Matrix

| Framework | Prefer when | Verify before choosing |
|---|---|---|
| [`linfa`](https://docs.rs/linfa/latest/linfa/) | Classical ML with an `ndarray`-oriented Rust API | Exact algorithm maturity, numerical behavior, preprocessing, and maintenance |
| [SmartCore](https://github.com/smartcorelib/smartcore) | A required classical algorithm or matrix/backend option is stronger there | Algorithm-specific quality, serialization, ndarray interop, and release support |
| [`tch-rs`](https://github.com/LaurentMazare/tch-rs) | LibTorch/PyTorch compatibility and operator coverage dominate | Exact LibTorch ABI/version, C++ runtime, CUDA match, packaging, and thread behavior |
| [Candle](https://github.com/huggingface/candle) | Rust-centric inference or training with CPU, CUDA, Metal, or Hugging Face model code | Model implementation parity, backend operators, quantization, and target support |
| [Burn](https://burn.dev/docs/burn/) | Backend-generic Rust training or inference is a real requirement | Explicit backend, supported ops, serialization, compile and feature cost, deployment maturity |
| [`tensor-rs`](https://docs.rs/tensor-rs/latest/tensor_rs/) | Only after a niche capability and maintained version are demonstrated | Age, ownership, algorithm coverage, docs, safety, and alternatives; never default by name alone |

`linfa` and SmartCore serve classical ML rather than being interchangeable general deep-learning frameworks. Compare the exact algorithm, missing-value and categorical handling, numerical convergence, model persistence, and test evidence. A uniform trait surface does not prove equivalent results.

Choose `tch-rs` when compatibility with a specific PyTorch or LibTorch environment justifies its native dependency. Pin the supported LibTorch version and CPU or CUDA build, C++ ABI, target runtime libraries, download or vendoring policy, and packaging for every platform. Exercise deployment on a clean machine; a developer’s existing Python or CUDA installation is not a release dependency strategy.

Candle favors a relatively small Rust implementation and Hugging Face ecosystem examples, but model ports remain code that must match the source architecture and tokenizer. Burn offers backend-generic abstractions; choose one concrete production backend and test it rather than assuming generic code behaves identically everywhere. Disable unused features to control compile time and binary/native dependency surface, but do not optimize the feature graph before the model works.

Treat `tensor-rs` as experimental or niche until `rust-crate-discovery` produces current evidence. A crate name resembling a mature ecosystem is not evidence of operator coverage, training support, performance, or maintenance.

## Training and Evaluation

Separate data splits, preprocessing fit, training, validation, and held-out evaluation. Prevent leakage by fitting normalization, vocabulary, imputation, and feature selection only on training data. Record dataset identity and license, split method, seed, shuffle and sampler behavior, optimizer and schedule, loss, metrics, stopping criteria, checkpoint format, and resumability.

Reproducibility has levels. Exact bitwise results may be unavailable across devices or parallel kernels; define the required statistical or tolerance contract. Match train/eval mode for dropout and normalization, control seeds where supported, and log nondeterministic operations. Compare accuracy or task quality separately from systems benchmarks so a faster backend cannot hide a regression.

Quantization, mixed precision, reduced accumulation, and fused kernels need representative task-level evaluation, including rare classes, long sequences, extreme values, and calibration data. Validate NaN/Inf behavior and avoid silently saturating or truncating tensors.

## Model Assets and Loading

Prefer formats designed for tensor assets, with explicit names, shapes, dtypes, lengths, and bounded parsing. Treat pickle-like or executable object formats as untrusted code and do not load them from untrusted sources. Verify model and tokenizer hashes before activation, cap file and tensor sizes before allocation, use checked shape products, and reject duplicate or unexpected tensors according to policy.

Make model activation atomic: fully load and validate a candidate, warm it if required, then swap the serving handle. Keep the previous known-good model until the new one passes readiness. Bound simultaneous reload memory and define cancellation and cleanup after a failed load.

## Serving and Backpressure

Serving adds queueing, batching, concurrency, warmup, model reload, cancellation, memory pressure, and telemetry beyond the model call. Set maximum queue length, batch size, batching wait, input size, concurrent executions, output size, and total deadline. Reject or shed overload predictably rather than converting it into unbounded memory.

Batch only compatible shapes or define padding and attention-mask semantics. Measure throughput and latency distributions across batch sizes and real traffic skew; larger batches can increase tail latency and resident memory. Propagate request cancellation to queued work, but decide whether an already submitted device batch can be canceled or only have its result discarded.

Warmup should execute representative shapes and required compilation paths, not mutate model state or leak user data. Report readiness only after weights, tokenizer, device, and warmup are valid. Expose queue time, preprocessing, model execution, postprocessing, batch size, device, errors, fallbacks, and memory without logging sensitive raw inputs.

## Device and Data Hand-offs

`rust-data` owns host array shape, strides, columnar preparation, and batching semantics. `rust-gpu` owns adapter limits, host-device layout, transfers, kernels, synchronization, compilation, and device loss. The ML profile keeps model placement and precision requirements but must not collapse device mechanics into a generic “use GPU” instruction.

CPU and GPU implementations need reference parity on representative fixtures. Include transfer and compilation time in end-to-end benchmarks and define CPU fallback behavior for unavailable devices, unsupported operators, out-of-memory, or device loss. Fallback must not silently change precision or model version.

## Required Evidence

- Model, tokenizer, preprocessing, labels, formats, hashes, framework and native dependency versions, device, precision, and input/output schemas.
- Golden reference parity with stated tensor and task-level tolerances.
- Accuracy or quality tests separate from latency, throughput, startup, and memory measurements.
- Invalid and oversized input, unsupported operator, corrupt asset, cancellation, overload, reload, device loss, and fallback behavior.
- Clean-machine packaging evidence for native libraries and model assets.

## Completion Contract

State the selected framework and backend, the model contract, materially rejected alternatives, unproved assumptions, and the smallest verification that remains. Stable releases are the default. Pin alpha or RC dependencies exactly only when they provide a required capability, and record the upgrade risk.

## Primary Sources

- [Linfa documentation](https://docs.rs/linfa/latest/linfa/) and [SmartCore source](https://github.com/smartcorelib/smartcore)
- [tch-rs source](https://github.com/LaurentMazare/tch-rs), [Candle source](https://github.com/huggingface/candle), and [Burn documentation](https://burn.dev/docs/burn/)
- [`tensor-rs` documentation](https://docs.rs/tensor-rs/latest/tensor_rs/)

## Design protocol map

- [Rust ML constraints and pipeline choices](./domain-constraints.md)

Use this branch for tensor shape and dtype invariants, device placement, preprocessing parity, model lifecycle, batching, inference, and serving. Verify current backend and crate facts through `rust-research`; Design protocol version examples are not a dependency recommendation.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-gpu`](../../rust-gpu/references/gpu.md) — supporting; Device capabilities, memory hierarchy, transfer cost, alignment, coalescing, batching, synchronization, and measurement.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
