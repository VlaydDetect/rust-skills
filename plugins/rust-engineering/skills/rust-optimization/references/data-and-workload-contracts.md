# Data and Workload Contracts

## Build an Invariant Ledger

For each proposed simplification, record the property, its evidence, enforcing API, mutation paths, and scope. Classify it as an enforced invariant, an empirical distribution, or an assumption requiring confirmation. Include adversarial and rare inputs: an average of 60 entries does not establish a maximum of 60.

| Property to inspect | Possible simplification | Obligations and counterexample |
|---|---|---|
| Length stops changing after construction | `Vec<T>` to `Box<[T]>`, `String` to `Box<str>` | Elements may remain mutable. Audit growth/removal APIs, conversion cost, pointer escape, and caller compatibility. A reusable growing scratch buffer should usually stay growable. |
| Small ordered collections with a constrained key space | Flat sorted storage | Preserve sorted iteration, uniqueness and lookup semantics; include insertion/deletion shifts and large outliers. |
| Mostly failed lookups over a stable dictionary | Prefix rejection or specialized search | Measure miss position, string lengths, hits and updates. Early rejection does not establish logarithmic worst-case complexity. |
| Many separate allocations or repeated metadata | Contiguous storage, offsets, deduplication | Prove offset bounds/overflow, lifetime and identity semantics; include reconstruction and updates. |
| Rare large enum variants inflate frequent values | Box selected variants or revise representation | Measure discriminant, padding, niches, allocation size classes, frequencies and pointer chasing. Boxing can make common reads slower. |
| Shared immutable bytes but mutable reader cursors | Per-reader state over shared backing | Verify clone cost and underlying sharing; preserve synchronization where still required. Deep copies of large mutable data can reverse the trade-off. |
| Low-cost repeated computation with stable inputs | Cache or precompute | Define invalidation, lifetime, capacity and key equality; a lock or retained working set can cost more than recomputation. |

## Measure the Object Graph

Measure the containing type with `size_of`/`align_of` for the actual target, then account for heap objects, capacity slack, allocator rounding, references, and resident pages. Do not sum field sizes and assume that the enclosing object shrinks. Distinguish requested bytes, allocated bytes, live bytes, peak heap, and RSS.

`Vec::into_boxed_slice` discards excess capacity and may resize or relocate an allocation. Verify pointer requirements instead of promising a free conversion. Fixed-length storage saves capacity bookkeeping, but padding, zero-sized types, allocator behavior and the number of live objects determine the useful effect. Include build/freeze cost as well as steady-state reads; never compare a prebuilt candidate against a baseline that still pays construction.

Prefer documented representation guarantees. Narrow integer fields require a checked domain bound; field reordering must respect ABI and serialization constraints. Do not use `repr(packed)` as a generic memory fix: unaligned access and references introduce separate correctness obligations. Pointer tagging needs target, provenance, alignment and ownership proofs; an apparent unused address bit is not a portable guarantee.

## Compare Operations and Distributions

Characterize key cardinality, uniqueness, hit/miss ratios, key length, skew, mutation frequency, scan versus point access, and working-set size. Sweep relevant cache-size transitions without treating synthetic cache-friendly input as the production distribution. Include dependent searches for latency and independent searches for throughput when both matter.

For hashes, retain collision resistance required by the trust boundary. Faster hashing of known internal integers does not justify exposing an unprotected hasher to attacker-controlled strings. Preserve ordering, duplicate handling and deterministic output when replacing a container.

## Choose From Evidence

Use an algorithm or representation experiment to test a mechanism, then return to the whole-system scenario. Reject a candidate if converting, decoding, copying, updating or destroying the new representation consumes the expected gain. Consult `rust-data` for changed data architecture, `rust-ownership` for lifetime contracts, `rust-serialization` for durable/wire formats, and `rust-unsafe` only when an actual unsafe boundary is proposed. These are separate decisions, not reasons to load every profile together.
