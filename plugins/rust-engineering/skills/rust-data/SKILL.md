---
name: rust-data
description: Design Rust data-oriented layouts, ECS workloads, multidimensional arrays, columnar processing, and query execution around measured access patterns. Use when data shape and traversal are primary; use database or ML skills for their domain semantics.
---

# Rust Data Engineering

Own data shape, access patterns, batching, and execution layout. Select structures from transformations and hot paths rather than from a preferred framework.

## Use This Skill When

- A workload needs an AoS, SoA, AoSoA, hot/cold split, stable IDs, or batch-oriented redesign.
- Bevy ECS or `hecs` storage, archetypes, scheduling, change detection, or structural mutation determine behavior.
- Rust code uses Polars, `ndarray`, `nalgebra`, Arrow, or DataFusion and layout or query planning matters.
- Columnar memory, null semantics, strides, dimensions, partitioning, spilling, or pushdown affect correctness or performance.

## Workflow

1. Write the transformations, cardinalities, mutation frequency, joins, scan patterns, latency targets, and memory ceiling.
2. Measure the current hot paths and identify which fields and rows are touched together.
3. Choose representation and batching from those access patterns; keep stable identity separate from physical location.
4. Make schema, nullability, dimensions, axes, strides, ordering, dictionary domains, and ownership explicit at boundaries.
5. Inspect ECS schedules or query plans before optimizing and test representative skew, nulls, empty inputs, and memory pressure.
6. Measure end-to-end behavior, including conversion, repartitioning, copies, spills, and retained buffers.

## Decision Rules

- Data-oriented design is a method for matching layout to access; it is not a requirement to convert every type to SoA.
- Introduce ECS for many heterogeneous entities and recurring systems, not as a universal application architecture.
- Runtime ECS component layout is not a stable persistence or network schema.
- An `ndarray` view need not be contiguous; a columnar slice can retain a much larger parent allocation.
- Prefer Polars lazy scans and expressions, then verify pushdown and streaming in the actual optimized plan.
- DataFusion performance claims require `EXPLAIN`, statistics, partitioning, batch sizing, memory-pool, and spill evidence.

## Boundaries and Hand-offs

- `rust-performance` owns general measurement after the data-specific access contract is defined.
- `rust-architecture` owns broader component boundaries; `rust-concurrency` owns synchronization and scheduling mechanisms.
- `rust-database` owns durable transactions and migrations; `rust-ml` owns model semantics; `rust-gpu` owns device execution.
- Use `rust-research` for version-specific APIs and optimizer behavior.

## Detailed Reference

Read [Rust data engineering field guide](references/guide.md) before an ECS, array-layout, columnar, or query-engine design change.
