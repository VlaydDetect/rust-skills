# Rust Machine Learning Field Guide

This guide is the detailed policy for `rust-ml`. It synthesizes the craft Rust ML framework and serving guides combined with full-stack crate, performance, observability, and FFI disciplines; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- ML correctness is pipeline parity: input decoding, preprocessing, tensor construction, model execution, and postprocessing must all match the validated reference.
- Inference runtimes and native bindings differ in operator coverage, graph optimization, device backends, model formats, and packaging.
- Tensor layout and dtype errors can produce plausible but wrong outputs, making golden fixtures and shape checks essential.
- Serving adds queueing, batching, warmup, model reload, concurrency, cancellation, memory pressure, and telemetry beyond the model call.
- Reproducibility needs model and tokenizer hashes, code and dependency versions, seeds, device, precision, and representative data.
- Accuracy, latency, throughput, memory, binary size, startup, and portability are separate metrics with trade-offs.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Portable inference model | Evaluate format runtime by operator and target support | Model extension alone does not ensure execution |
| Rust-native training | Framework with autograd and device needs | Training requirements differ from inference deployment |
| Low-volume request | Direct or small batch inference | Avoids queue latency and complexity |
| High-throughput service | Bounded dynamic batching | Balances utilization with latency limits |
| Edge or embedded target | Size and operator constrained runtime | Memory, native deps, and target support dominate |

## Common Failure Modes

- Loading the same model but using different tokenization, normalization, labels, or output decoding.
- Silently converting tensor shapes or dtypes and accepting plausible output.
- Choosing a GPU framework without deployment driver, architecture, or fallback validation.
- Benchmarking only model execution while ignoring preprocessing, transfers, queueing, and postprocessing.
- Serving unbounded batches or queues and turning load into memory exhaustion.

## Required Evidence

- Model, tokenizer, preprocessing, labels, formats, hashes, versions, device, precision, and input or output schemas.
- Golden parity fixtures against a trusted reference with defined tolerances and task metrics.
- End-to-end latency, throughput, memory, startup, and accuracy results under representative batching and concurrency.
- Unsupported operator, invalid input, device loss, cancellation, overload, and fallback behavior.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
