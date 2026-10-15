# Benchmark Design and Analysis

## Audit the Work Before the Numbers

Define a correctness oracle outside the timed region, then confirm the benchmark performs the intended amount of useful work. Protect relevant inputs/outputs with `std::hint::black_box` when the project's MSRV supports it (stable since Rust 1.66); on an older toolchain use a compatible harness facility. A barrier is best effort: constant folding, loop-invariant work, unused results and unrealistic input predictability still require inspection.

Check setup, allocation, copying, parsing, validation, executor startup and destruction individually. Include a cost if it belongs to the product operation; exclude it only when measuring an explicitly narrower stage. Excluding input setup can still alter cache warmth. Use the existing [Criterion timing-loop guide](../../rust-performance/references/performance-optimization-guide.md) for `iter`, batching, destruction and async details.

Vary meaningful dimensions rather than only a random length: cardinality, hit/miss ratio and miss position, skew, boundary/error inputs, mutations, working set relative to caches, and concurrency. Repeatedly reading one hot key trains the branch predictor and cache. Deterministic representative input sets aid repeatability; sweep several meaningful sets so one seed does not choose the answer.

Independent operations often expose throughput or instruction-level parallelism. A dependency chain exposes latency. Do not label one as the other; inspect generated code if control speculation defeats the intended dependency. Verify throughput units against actual bytes/items completed, including batched iterations.

## Criterion Results

Use groups/IDs for the input matrix and throughput only when its units have product meaning. Preserve the harness version, sampling mode, warmup, sample count and measurement duration. Start with appropriate framework defaults; adjust them because pilot evidence shows inadequate precision or duration, not to produce a favorable answer.

Record the estimator used. In current Criterion, `Typical` uses slope when available and otherwise mean; verify the resolved version and sampling mode. Median, mean, slope and Typical are not interchangeable. Nor are the displayed absolute-time estimator and the baseline-change test necessarily the same statistic: read the matching report instead of reconstructing its change by dividing unrelated displayed bounds.

Keep raw sample/iteration data and point estimates with confidence intervals. An interval's midpoint is not the point estimate; averaging interval endpoints is not an aggregate estimator. Outlier labels describe observations, not permission to delete inconvenient samples. First investigate process load, warmup/drift, throttling, allocation state or distinct workload modes.

Statistical significance is not useful magnitude, and a non-significant result is not proof of equivalence. Set the minimum worthwhile effect and unacceptable regressions before evaluating candidates. Consider framework noise thresholds, measured run-to-run variation and uncertainty. Report inconclusive evidence when it cannot distinguish a useful improvement from noise or a harmful trade-off.

## Comparable Repeated Runs

Reject an unqualified comparison if the controlling toolchain, target, features, profile, flags, allocator, harness, inputs, runtime, hardware class or cache policy differs. A deliberate change to one of those is an experiment variable; measure it against a controlled baseline and keep other inputs fixed.

Interleave or randomize baseline/candidate order when drift can bias the outcome. Pair runs that share environment conditions. Separate within-run iteration samples from independent process/build/machine repetitions; thousands of iterations in one process do not establish reproducibility across runs. If using bootstrap, resample the actual independent units and preserve pairing/hierarchy (for example runs, then samples) justified by the design. Never treat confidence bounds as raw observations or invent paired measurements from unrelated runs.

Do not pool unrelated workloads into one median. Use per-scenario outcomes and predeclared workload weights when a product aggregate is required. State absolute and relative changes, uncertainty, adjacent regressions and unmeasured contexts. Avoid repeated testing until a favorable p-value appears; use a predefined run budget or a justified sequential method.

## Service and Concurrent Workloads

Measure offered and achieved rate, completed work, client saturation, concurrency, timeouts/errors and queue depth. For an open-loop latency objective, retain intended start time as well as actual send/completion time. Closed-loop latency can omit time when a slow service prevents new arrivals (coordinated omission). Use the harness's documented scheduling/correction semantics and disclose limitations; do not fabricate omitted samples after the fact.

Percentiles require request-level observations, a defined observation interval, enough tail observations, and treatment of errors/timeouts. A Criterion confidence interval over repeated batches is not a request p99. Cover relevant steady-state, startup, cold cache, overload, skew and mixed workloads proportionately. Confirm the client can drive the target before diagnosing a server throughput ceiling.

## Profiling Is a Separate Run

Criterion `--profile-time` repeats work without normal analysis/result saving. It locates costs and cannot supply the ordinary before/after baseline comparison. Direct Criterion executables need `--bench`; resolve the artifact rather than assuming a Cargo path. Keep native uninstrumented comparison runs separate from profiler, Miri, sanitizer and heavily instrumented heap runs.
