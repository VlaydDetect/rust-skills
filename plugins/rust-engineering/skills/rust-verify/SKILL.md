---
name: rust-verify
description: Select and run the smallest sufficient read-only evidence matrix for an existing Rust or Nix state. Use to test, check, validate, reproduce CI, or prove behavior with exact package, target, feature, toolchain, and environment scope. Do not edit source, accept formatter rewrites, install tools, or fix failures.
---

# Rust Verify

Validation is evidence for the changed contract, not a fixed command dump. Do not edit source.

## Select the Matrix

1. Read the task, repository instructions, dirty state, CI, task runners, toolchain, packages, targets, features, and lockfile policy.
2. State the contract being proved and select one primary and at most two supporting profiles from the [routing index](../rust-workflow/references/routing-index.md) to determine risk-specific evidence.
3. Select commands from [Quality gates](references/quality-gates.md) and explain what each command proves and does not prove.
4. Start narrow: non-mutating format check when relevant, affected package or target check, then targeted behavior tests.
5. Expand to Clippy, docs, workspace, feature combinations, platforms, Miri, benchmarks, foreign consumers, Nix builds, or packaging only when the changed surface requires them.
6. Never install tools, update dependencies, accept formatter rewrites, or use network access merely to make a check run. Report unavailable evidence as `SKIP`.
7. Record every command with scope, result, cause classification, evidence, and residual risk. Stop on a narrow change-caused failure unless broader execution is needed to classify it.

## Risk Escalation

- Public library API: rustdoc and SemVer checks when configured.
- Unsafe or FFI: Miri where applicable plus real ABI or platform integration tests.
- Dependencies or features: metadata or tree inspection and the declared feature matrix; audit or deny only when available or requested.
- Async or concurrency: cancellation, shutdown, race, timeout, and bounded-load tests.
- Performance: correctness tests plus the same benchmark and environment used for the baseline.
- Cross-platform or embedded code: supported targets and hardware or emulator evidence; do not infer success from the host build.

## Report

For every check, return a `VerificationRecord`: exact command, scope, `PASS|FAIL|SKIP`, evidence, and residual risk. Classify failures as `change`, `pre-existing`, `environmental`, or `unknown` only when evidence supports it. Never hide a failing narrow check behind a later broad pass.

Verification does not authorize source changes. If a failure requires repair, return the smallest reproduction and route it to `debugging` through `rust-workflow`. If command output requires a quality judgment rather than an execution record, route it to `rust-review`.

Read [Quality gates](references/quality-gates.md) to choose commands.
