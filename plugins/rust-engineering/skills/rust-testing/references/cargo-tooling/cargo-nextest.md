# cargo-nextest: execution and isolation protocol
Use this reference when a project already uses nextest or explicitly needs its process-per-test runner, filtersets, profiles, groups, retries, timeouts, or reports. Ordinary test design remains in `$rust-testing`; command execution remains in `$rust-verify`.

## Evidence and precedence

1. Repository instructions, pinned toolchain, manifests, `.config/nextest.toml`, CI, task runner, and lockfile.
2. The installed `cargo nextest --version` and matching help output.
3. Current [running](https://nexte.st/docs/running/), [configuration](https://nexte.st/docs/configuration/reference/), and [coverage integration](https://nexte.st/docs/integrations/test-coverage/) documentation.
4. This protocol.

If nextest is absent, record `SKIP`. Do not install it, edit CI, fetch archives, or substitute a different test runner automatically.

## Execution model: what is and is not isolated

Nextest normally starts each test in a separate process. This improves crash containment and prevents in-process Rust globals from being shared between tests, but it is not complete isolation.

Tests may still contend through:

- the same filesystem paths and temporary-directory conventions;
- fixed TCP/UDP ports, databases, brokers, object stores, and other services;
- environment-controlled credentials, clocks, random sources, and host limits;
- inherited child processes and cleanup that outlives a test;
- shared caches, lockfiles, hardware devices, kernel state, and external rate limits.

Do not treat a pass under one schedule as evidence that a test is concurrency-safe. Give each test owned resources, unique namespaces, bounded cleanup, and explicit serialization when the resource cannot be partitioned.

## Selection protocol

1. Identify the exact Cargo package, target, feature set, target triple, ignored-test policy, and environment used by the failing or required gate.
2. Use `cargo nextest list` to inspect the selected inventory before a complex filter. Its machine-readable listing is distinct from run-event output.
3. Prefer nextest filter expressions for stable semantic selection. A bare substring argument is convenient for local diagnosis but can select more tests than intended.
4. Check the resolved expression grammar before using package, binary, test-kind, platform, dependency, or regex predicates; grammar and available predicates are tool-version contracts.
5. Keep the filter in project configuration or CI when it defines a lasting gate. Keep one-off diagnosis filters in the evidence record rather than silently changing policy.

<!-- command-contract: tool=cargo-nextest; channel=external; platform=project-host; effects=build-artifacts,process-execution; evidence=nextest-running,nextest-config -->
```bash
cargo nextest list --workspace --locked --offline
cargo nextest run --workspace --locked --offline -E '<reviewed-filter-expression>'
```

The example assumes those flags are supported by the resolved version and the needed registry/git data is cached. An offline cache miss is an environment limitation, not a reason to fetch implicitly.

## Profiles and concurrency

Keep shared policy in `.config/nextest.toml`. A named profile should express a real environment contract such as CI reporting or constrained local resources, not duplicate defaults without reason.

```toml
[profile.default]
retries = 0
test-threads = "num-cpus"
fail-fast = false
success-output = "never"
failure-output = "immediate-final"

[profile.ci]
retries = 0
fail-fast = false
slow-timeout = { period = "60s", terminate-after = 2 }

[profile.ci.junit]
path = "junit.xml"
```

Thread-count policy accepts a positive count, a supported negative offset from available CPUs, or the documented CPU-count value. Choose it from the test resource contract rather than maximizing parallelism blindly. Leave capacity for compilers, linkers, databases, containers, and CI sidecars.

The JUnit path is resolved within nextest's store/profile layout. A profile-local `junit.xml` is not necessarily at the workspace-relative path a source recipe assumes. Resolve the effective store directory before configuring upload or report consumers.

## Test groups and overrides

Use a test group when a known resource has bounded capacity. Name the resource, not a vague speed class.

```toml
[test-groups.database]
max-threads = 1

[[profile.default.overrides]]
filter = 'test(/database_/)'
test-group = 'database'
slow-timeout = { period = "90s", terminate-after = 2 }
```

Check override precedence and matching with the installed version. A serialized group protects only the nextest-scheduled tests assigned to it; it does not coordinate unrelated processes or another CI job using the same database.

Use platform overrides only for demonstrated target or host differences. Do not encode a slow machine as a universal OS property.

## Retries and flakes

Retries are a diagnostic and continuity tool, not a default cure.

- Start with zero unless the project explicitly owns a retry policy.
- Preserve and surface the initial failure, retry count, final outcome, and test identity.
- Quarantine or narrowly override a known flaky test; do not mask the whole suite.
- Set a removal condition and track the root cause: shared resource, clock, randomized seed, race, ordering, eventual consistency, or external service.
- A test that passes on retry is still flaky. CI reporting must not present it as an ordinary clean pass.
- Never retry destructive integration tests unless their reset/idempotency contract is proven.

When diagnosing, first reproduce with a stable seed/environment and constrained concurrency. A retry-only "fix" increases latency and hides evidence.

## Timeouts and termination

`slow-timeout` can report a slow test and terminate after repeated periods. Select values from observed test duration and cleanup requirements.

- Distinguish a slow warning from forced termination.
- Ensure SIGTERM/kill behavior is appropriate on the host and that child processes, containers, files, ports, and transactions are cleaned up.
- A timeout can truncate buffered output or leave external state. Preserve the nextest report and service logs.
- Do not use a larger timeout to bury a deadlock. Route unexplained hangs and lost wakeups to `$debugging` with `$rust-concurrency` support.

## Output contracts

Human terminal output, inventory JSON, experimental run-event streams, and JUnit are different interfaces.

- `cargo nextest list` owns inventory output; consumers must pin and validate its schema.
- Machine-readable run events use versioned experimental libtest-compatible formats in current nextest. Verify the installed format names and message-format version; do not assume generic Cargo JSON semantics.
- JUnit is profile-configured and written as a report artifact. Treat path, schema compatibility, retention, and upload as explicit CI contracts.
- Do not parse human output as a stable API.

Uploads and result publishing are network/external mutations and are never automatic in this plugin.

## Doctest gap

Nextest does not execute Rust doctests. If doctests are part of the repository contract, preserve a separate Cargo gate with the same relevant package and feature scope.

<!-- command-contract: tool=cargo; channel=project; platform=project-host; effects=build-artifacts,process-execution; evidence=nextest-running -->
```bash
cargo test --doc --workspace --locked --offline
```

Do not claim equivalence between the nextest suite and the doctest gate: compilation mode, harness, environment, and selected targets differ.

## Coverage hand-off

Nextest chooses and executes tests; coverage instrumentation and report semantics belong to [cargo-llvm-cov](cargo-llvm-cov.md). Keep three layers explicit:

1. `$rust-testing` defines which contracts and test populations matter.
2. The coverage tool supplies instrumentation and raw data.
3. Nextest supplies a runner for the supported non-doctest population.

Do not apply a retry-heavy profile to coverage silently: multiple executions can affect time and report interpretation even when coverage hits are merged.

## Diagnosis table

| Symptom | Inspect | Correct response |
|---|---|---|
| Test passes alone, fails in parallel | filesystem, ports, services, env, ordering | allocate unique resources or a bounded group; retain regression evidence |
| CI finds no tests | package/feature/target/filter expression and list output | compare selected inventory before changing runner |
| JUnit consumer finds no file | active profile and effective nextest store path | resolve actual report path; do not hardcode workspace `target` |
| Test killed as slow | period count, host signal behavior, child cleanup | distinguish deadlock from resource-starved slow execution |
| Retry produces green CI | initial failure and flaky status | surface flake, narrow retry, diagnose root cause |
| Doctest regression escaped | separate Cargo doctest gate | add the missing explicit gate |
| Parser rejects event output | resolved experimental format and schema version | update the consumer deliberately or use JUnit/listing contract |

## Verification record

For every retained nextest result record tool version, profile, package/target/features, filter expression, environment constraints, concurrency/groups, retry and timeout policy, exact command, report paths, exit status, failed/flaky tests, and the separate doctest outcome. This evidence lets `$rust-verify` reproduce the gate without owning the test strategy.
