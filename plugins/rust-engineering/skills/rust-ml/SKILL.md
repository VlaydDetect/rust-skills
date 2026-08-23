---
name: rust-ml
description: Design Rust machine-learning inference, training, tensor, preprocessing, model-format, device, batching, serving, and evaluation workflows. Use when ML-specific correctness and operational constraints control a Rust implementation.
---

# Rust Machine Learning

Own ML model integration and serving contracts in Rust, including data, device, performance, and reproducibility. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- Rust code loads or executes models, tensors, tokenizers, embeddings, preprocessing, training, or inference.
- A framework, model format, CPU or GPU backend, batching, quantization, or serving design needs selection.
- Predictions differ across languages or devices, or model performance and reproducibility need diagnosis.

## Workflow

1. Define task, model source and version, input and output schema, preprocessing, accuracy metric, latency or throughput target, device, memory, and deployment constraints.
2. Choose inference-only versus training scope and evaluate framework or runtime compatibility with model format, operators, target, licensing, and native dependencies.
3. Make tensor shape, dtype, layout, device placement, normalization, tokenization, batching, and postprocessing explicit at boundaries.
4. Build a minimal parity test against a trusted reference implementation and fixed fixtures before optimizing or serving.
5. Add model lifecycle, warmup, concurrency, backpressure, cancellation, observability, and resource limits for production serving.
6. Measure accuracy and systems performance independently, record environment and model hashes, and test fallback or unsupported-operator behavior.

## Decision Rules

- A model file alone is not a complete contract; preprocessing, tokenization, label mapping, postprocessing, and version are equally required.
- Validate tensor rank, dimensions, dtype, range, layout, and device before execution.
- Do not compare outputs across frameworks without matching evaluation mode, precision, random seeds, operators, and preprocessing.
- Batching improves throughput but can increase latency and memory; set capacity and wait limits.
- GPU use requires device availability, transfer cost, memory behavior, fallback, and native deployment evidence.
- Quantization and reduced precision need task-level accuracy evaluation, not only faster benchmarks.
- Keep untrusted model and input parsing within resource and format limits.
- Current framework recommendations require current primary-source research before substantial adoption.
- Choose `linfa`, `smartcore`, `tch-rs`, Candle, Burn, or another framework from the required algorithm, model ecosystem, backend, maturity, and deployment evidence rather than popularity.

## Boundaries and Hand-offs

- `rust-crate-discovery` owns current candidate evaluation for ML frameworks and runtimes.
- `rust-data` owns host data layout and columnar or array processing; `rust-gpu` owns device buffers, kernels, transfers, and synchronization.
- `rust-performance`, `rust-concurrency`, and `rust-observability` own their general mechanisms once ML-specific contracts are defined.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Machine Learning field guide](references/guide.md) before making a consequential design choice. Load the [Design protocol ML domain protocol](./references/guide.md) for its detailed domain questions, then verify backend and crate facts through `rust-research`. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Specialized Rust protocols

For additional topic detail, read the [Profile reference index](./references/guide.md) and load only the matching family reference.
