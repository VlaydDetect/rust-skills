# Rust Data Engineering Field Guide

Research baseline: **2026-08-23**. Re-run `rust-research` for current crate versions, feature flags, execution-plan behavior, and optimizer guarantees before implementing version-sensitive advice.

## Begin With Transformations

Describe the operations before choosing the representation: scans, point lookups, joins, filters, updates, neighborhood queries, reductions, and serialization. Record cardinality, skew, field access frequency, mutation rate, stable-identity needs, batching window, cache and memory ceiling, and which stages dominate measured time.

Data-oriented programming matches layout and processing order to those facts. It is not synonymous with one container or with removing domain types. Start with ordinary structures, split hot and cold fields when their access diverges, and consider:

- **AoS** when operations usually consume most fields of one item together;
- **SoA** when loops scan a few fields across many items or vectorized kernels require contiguous lanes;
- **AoSoA** when fixed blocks improve SIMD or device transfer without making the whole dataset columnar;
- stable IDs or generation-checked handles when physical rows move, rather than exposing indices as durable identity.

Batch transformations where it reduces dispatch and synchronization, but bound queue latency and memory. Benchmark representative distributions and full pipeline conversions; a faster inner loop can lose to transposition, compaction, or materialization.

## ECS Is a Workload Choice

Use an ECS when many heterogeneous entities repeatedly flow through systems selected by component sets. A conventional object or table model is usually simpler for static records, request/response services, or a small number of homogeneous collections.

For [Bevy ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) and [`hecs`](https://docs.rs/hecs/latest/hecs/), map the component combinations and structural-change rate before implementation. Archetype count grows with observed component combinations; optional queries, marker components, and highly dynamic bundles can create broad scans or archetype explosion. Archetypes usually persist after creation, so churn can leave many small tables.

Choose storage from access patterns. Table storage favors dense iteration but moving an entity between component sets can copy or relocate rows. Sparse-set storage reduces some structural-change costs and suits uncommon markers, but adds indirection and can slow iteration. Measure the actual queries rather than turning this into a global component rule.

Structural commands are commonly deferred. Document when queued spawns, inserts, removals, and despawns become visible, and do not read a same-frame mutation as though it were immediate. Scheduling parallelism is constrained by declared mutable and immutable component access; broad queries and hidden interior mutation reduce safe concurrency. Change-detection flags describe framework observation semantics, not necessarily semantic difference, and their scan cost can still be proportional to candidates. Do not rely on entity iteration order unless explicitly sorted. Never persist raw entity IDs, archetype positions, component layout, or runtime change ticks as the storage schema.

## Polars: Optimize the Plan, Not the Fluent Syntax

Prefer [lazy scans and expressions](https://docs.pola.rs/user-guide/concepts/lazy-api/) for query-shaped work. Apply projections and predicates before joins and materialization, call `collect` at a deliberate boundary, and inspect the optimized plan to confirm predicate and projection pushdown. An expression that looks lazy can still block streaming or force materialization; validate the actual engine and version behavior under representative data.

Define null and floating-point NaN semantics separately. Pin time zones and daylight-saving handling, categorical dictionaries, sort stability, join cardinality, and integer overflow behavior. Avoid row-wise UDFs when an expression exists because they obscure optimization and often serialize execution. Control nested parallelism: Polars already uses a thread pool, so combining it with outer Rayon or request-level fan-out can oversubscribe cores and inflate memory.

Test whether the chosen streaming path spills or falls back to resident memory. Track input bytes, peak RSS, output rows, partition skew, and time to first and last batch, not just operator duration.

## ndarray and nalgebra: Layout Is Part of the Boundary

With [`ndarray`](https://docs.rs/ndarray/latest/ndarray/), record shape, axis meaning, strides, ownership, and broadcasting. Views can be sliced, reversed, transposed, broadcast, or otherwise non-contiguous; never pass `as_ptr()` plus a guessed length to BLAS, C, GPU, or file output without proving layout. Iterate using APIs that respect strides. Copy to a declared contiguous order only at a boundary that requires it, and measure that copy.

Validate broadcasting explicitly because compatible shapes can still express the wrong domain operation. Empty axes, zero-sized arrays, negative strides, aliasing rules for mutable views, and reshape failures deserve tests. Keep dimension types static where they materially prove an invariant and dynamic where runtime data truly controls shape.

For [`nalgebra`](https://nalgebra.rs/docs/user_guide/vectors_and_matrices/), choose static versus dynamic dimensions deliberately and remember its conventional column-major storage. Define vector orientation, handedness, multiplication order, coordinate spaces, angle units, and row/column-major expectations at graphics, FFI, serialization, or shader boundaries. A transposed mathematical convention can produce plausible but wrong transforms.

## Arrow and DataFusion: Columnar Ownership and Execution

An Arrow [`RecordBatch`](https://docs.rs/arrow/latest/arrow/record_batch/struct.RecordBatch.html) couples a schema with equal-length column arrays. Preserve field order, data types, nullability, metadata, and logical versus physical representation. Understand null bitmaps, variable-length offset width, dictionary identity, chunk boundaries, and zero-copy slices. A small slice can retain the large parent buffers; compact or rechunk only when retained memory is measured and material.

At ingestion boundaries, validate array lengths, offsets, child ranges, dictionary keys, and schema compatibility. Do not assume a foreign Arrow producer follows the same extension metadata or timestamp convention. Choose batch size from operator amortization, cache behavior, latency, and memory rather than a fixed folklore number.

For [DataFusion](https://datafusion.apache.org/user-guide/introduction.html), inspect logical and physical plans with `EXPLAIN`. Confirm partition pruning, predicate and projection pushdown, join strategy, repartitioning, statistics quality, sort requirements, and UDF placement. Declare UDF volatility correctly; claiming deterministic or immutable behavior can enable invalid rewrites or caching.

Configure and observe the memory pool. Operators such as joins, sorts, aggregations, and windows can exceed memory unless bounded and spill-capable, while not every allocation is necessarily tracked by the pool. Verify spill paths, temporary-disk capacity and cleanup, cancellation, skewed partitions, and backpressure between producers and consumers. Statistics can be missing or stale, so test plans on representative data rather than trusting estimates alone.

## Verification Contract

Keep semantic tests separate from performance evidence. Cover empty and singleton inputs, null/NaN combinations, extreme dimensions, skew, duplicate keys, invalid offsets, structural ECS churn, nondeterministic ordering, cancellation, and memory pressure. For optimizations, preserve the workload generator, input distribution, hardware, thread count, plan output, peak memory, and before/after measurements.

## Primary Sources

- [Bevy ECS introduction](https://bevy.org/learn/quick-start/getting-started/ecs/) and [`hecs` documentation](https://docs.rs/hecs/latest/hecs/)
- [Polars Lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/)
- [`ndarray` documentation](https://docs.rs/ndarray/latest/ndarray/) and [nalgebra matrices guide](https://nalgebra.rs/docs/user_guide/vectors_and_matrices/)
- [Arrow `RecordBatch`](https://docs.rs/arrow/latest/arrow/record_batch/struct.RecordBatch.html) and [DataFusion user guide](https://datafusion.apache.org/user-guide/introduction.html)
