# cargo-llvm-cov: coverage evidence protocol
Use this reference when LLVM source-based coverage is already part of the project or the user explicitly asks to design coverage evidence. Coverage is a test adequacy signal, not a substitute for contract-based assertions.

## Ownership

- `$rust-testing` owns the covered behavior, test population, exclusions, and threshold policy.
- `$rust-verify` runs the already selected coverage command and records artifacts.
- `$rust-research` verifies the resolved cargo-llvm-cov, Rust, LLVM-tools, target, and unstable-feature contract.
- `$rust-performance` is not selected merely because a percentage is measured; it joins only for runtime or build-time cost analysis.

The tool-owner [README](https://github.com/taiki-e/cargo-llvm-cov/blob/main/README.md) owns current flags and supported combinations. Nextest integration follows [nextest's coverage guide](https://nexte.st/docs/integrations/test-coverage/).

## Prerequisites and effects

Before execution record:

1. Project toolchain and target, installed `cargo llvm-cov --version`, and matching help.
2. Availability of the required LLVM tools for that exact toolchain. Missing components or tools produce `SKIP`; the workflow does not install them.
3. Workspace/package/target/features and which tests, examples, binaries, integration tests, or doctests are in scope.
4. Runner choice (`cargo test`-style or nextest), runner profile, filters, retries, environment, and shared resources.
5. Effective Cargo target directory, intended report directory, retention, cleanup, and whether existing coverage data may be replaced.
6. Stable versus pinned-nightly status and target support for every requested mode.
7. Report consumers and network/upload boundaries. Generation is local; publication is a separate authorized action.

An ordinary coverage run builds instrumented artifacts, executes code, writes raw profiles/reports, and may clean part of its own previous coverage build state. It is not read-only even when source files are unchanged.

## Design the coverage contract

Define the question before choosing a percentage:

- Which public contracts, safety boundaries, error paths, feature combinations, targets, and generated code matter?
- Is the gate line, region, or function coverage, or merely a report for review?
- Which code is legitimately unreachable or generated, and who reviews exclusions?
- Is the baseline global, changed-lines, package-specific, or risk-specific?
- Does a threshold prevent regression relative to an accepted baseline, or merely enforce an arbitrary number?

Do not introduce a universal percentage. A high score can execute weak assertions; a lower score can cover the critical state space. Pair coverage with mutation, property, fuzz, concurrency, or integration testing only when those techniques expose a named risk.

## Reproducible run protocol

1. Reproduce the project's normal test gate first. Coverage instrumentation can change timing, linking, optimization, process environment, and available disk space.
2. Freeze the exact package/feature/target/runner population. Do not compare different populations as a trend.
3. Use the project's pinned toolchain and already installed cargo-llvm-cov. Record version and channel.
4. Start a fresh coverage session only when removal of prior coverage data is authorized. Scope cleanup to cargo-llvm-cov's owned data rather than the entire Cargo target directory.
5. Run once with reporting deferred when multiple output formats are required.
6. Produce each report from the same retained data. Store explicit output paths under an authorized artifact directory.
7. Apply project-owned thresholds to the final combined report, not to an accidental subset.
8. Preserve command, versions, population, raw-data lifecycle, summaries, paths, exit status, and excluded files.

### One local report

<!-- command-contract: tool=cargo-llvm-cov; channel=external; platform=project-host; effects=build-artifacts,process-execution,report-artifacts; evidence=cargo-llvm-cov -->
```bash
cargo llvm-cov --workspace --locked --offline --html --output-dir <authorized-report-dir>
```

Treat option spelling as version-sensitive and confirm it with installed help. Do not open a browser automatically; return the report path.

### One execution, several reports

<!-- command-contract: tool=cargo-llvm-cov; channel=external; platform=project-host; effects=build-artifacts,process-execution,report-artifacts; evidence=cargo-llvm-cov -->
```bash
cargo llvm-cov --workspace --locked --offline --no-report
cargo llvm-cov report --lcov --output-path <authorized-report-dir>/lcov.info
cargo llvm-cov report --html --output-dir <authorized-report-dir>/html
```

The point is lifecycle separation: execute the selected population once, then render formats from the same data. Recheck the resolved tool's exact support for each report command and avoid combining flags merely because each works alone.

## Threshold policy

Current cargo-llvm-cov supports project gates for documented summary dimensions such as lines, regions, and functions. Verify the resolved version before choosing one.

- Put threshold intent in project configuration or an owned task/CI script, not in an agent default.
- Explain scope and rounding. A workspace aggregate can hide an uncovered critical package.
- Review threshold changes as policy changes. Lowering a threshold to make CI green needs explicit rationale.
- Avoid thresholds for unstable metrics unless the project pins the toolchain and accepts churn.
- Report both the threshold result and meaningful uncovered contracts; a single percentage is incomplete evidence.

## Nextest integration

Read [the nextest protocol](cargo-nextest.md) before combining the tools.

1. Confirm both tools are installed and compatible with the pinned Rust toolchain.
2. Preserve the same nextest profile, filter expression, package/features/target, retries, groups, and timeout policy used by the intended gate.
3. Remember that nextest omits doctests and that process-per-test does not isolate external resources.
4. Prefer the cargo-llvm-cov integration entrypoint documented by the resolved version; then create reports from the captured data.

<!-- command-contract: tool=cargo-llvm-cov,cargo-nextest; channel=external; platform=project-host; effects=build-artifacts,process-execution,report-artifacts; evidence=cargo-llvm-cov,nextest-coverage -->
```bash
cargo llvm-cov nextest --workspace --locked --offline --no-report --profile <project-profile>
cargo llvm-cov report --lcov --output-path <authorized-report-dir>/lcov.info
```

Do not enable broad retries merely to complete a coverage run. Retried passes remain flaky evidence and must be reported.

## Nightly-only and unstable modes

Branch coverage and doctest coverage are unstable/nightly-sensitive in the current tool-owner contract. They require:

- an explicitly project-pinned nightly rather than an implicit toolchain switch;
- exact cargo-llvm-cov and LLVM-tools compatibility;
- a documented supported target;
- acceptance that report semantics and flags may change;
- a stable fallback or explicit `SKIP` when the project does not own nightly.

Do not invent a branch-threshold flag by analogy with line/function/region thresholds. Inspect installed help and upstream release notes. Doctest coverage also has a different execution model and cannot be inferred from a separate normal doctest pass.

## Formats and consumers

| Format | Primary use | Guardrail |
|---|---|---|
| Text summary | local diagnosis and CI log | not a stable parser API unless the tool documents it |
| HTML | human line-level inspection | report artifacts may embed paths/source; do not auto-open |
| LCOV | interoperable downstream ingestion | consumer interpretation and path rewriting must be tested |
| JSON | structured analysis | pin schema/tool version before parsing |
| Cobertura XML | CI/report-system integration | validate consumer schema and package/path mapping |

Generating a report does not authorize uploading it. Coverage artifacts can expose source paths, filenames, function names, repository layout, and test behavior. Apply retention and access policy before external publication.

## Exclusions

Filename regex exclusions can improve signal or silently hide risk.

- Prefer structural package/target selection where it matches the intended contract.
- Anchor and test regexes against the actual file list before applying them.
- Exclude generated or vendored code only when its owning generator/upstream is tested elsewhere.
- Do not exclude tests merely to inflate production percentages without documenting the metric definition.
- Keep exclusion rationale beside project policy and review it when paths change.

## Cleanup and artifact safety

- Never use a broad Cargo clean as a routine coverage fix; it destroys unrelated build cache and hides invalidation evidence.
- Use cargo-llvm-cov's scoped cleanup only after confirming its effects for the installed version.
- Do not assume reports live under a default `target` path. Resolve the effective target directory and use explicit report paths.
- Keep raw profiles until every required report and threshold has completed; then remove them only under project retention policy.
- A stale-looking report should first be traced to population, raw-data, output-path, and version identity—not "fixed" by deleting all build artifacts.

## Failure diagnosis

| Symptom | Inspect first | Avoid |
|---|---|---|
| Missing LLVM tools | pinned toolchain and component availability | implicit component/toolchain install |
| Report omits tests | package/features/target/runner/filter population | assuming workspace means every executable path |
| Nextest coverage differs | profile, retries, doctest gap, filter, raw-data lifecycle | comparing unlike runner populations |
| Coverage changes after refactor | LLVM/tool version, inlining/generics, region mapping | treating metric drift as behavioral regression automatically |
| Report path missing | explicit output and effective target directory | hardcoded build layout |
| CI threshold unexpectedly passes | aggregation scope, exclusions, rounding, empty population | trusting one percentage without inventory |
| Nightly mode fails | pinned nightly, target matrix, exact resolved flags | installing/switching toolchain silently |

## Evidence record

Return toolchain, cargo-llvm-cov/LLVM-tools versions, channel, target, package/features, runner/profile/filter, cleanup decision, exact commands, effects, report formats and paths, thresholds, exclusions, summary, exit status, missing populations such as doctests, and residual gaps. A coverage report is useful only when another engineer can reproduce what was actually measured.
