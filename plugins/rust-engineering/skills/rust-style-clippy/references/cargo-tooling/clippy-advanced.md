# Advanced Clippy policy

<!-- laurigates-source-family: clippy-advanced; source=rust-plugin/skills/clippy-advanced/SKILL.md; sha256=17e0eccdc7523805aa1bc52361d9a3e4bfa9ee38804e4f58e574efe37e551ee7; revision=a1e72ed186b97555256d8c058ff291c182332df7 -->

Use this reference to design or repair a project-owned Clippy policy. Do not activate it for an ordinary Rust task merely because Clippy could run.

## Evidence and ownership

- `$rust-style-clippy` owns lint levels, workspace inheritance, `clippy.toml`, command scope, suppressions, and remediation policy.
- `$rust-stable` establishes the pinned toolchain, MSRV, lint availability, and attribute support.
- `$rust-verify` runs the exact project gate and separates new findings from baseline failures.
- `$rust-review` decides whether a proposed lint fix preserves semantics, API, allocation, error behavior, concurrency, and readability.

Check the pinned `cargo clippy --version`, current [lint catalog](https://rust-lang.github.io/rust-clippy/), [typed Clippy configuration](https://doc.rust-lang.org/clippy/lint_configuration.html), and [Cargo lint tables](https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section). Lint names, groups, defaults, config keys, suggestions, and MSRV behavior change with the Rust toolchain.

If Clippy is unavailable for the project toolchain, report `SKIP`. Do not install or update the component/toolchain automatically.

## Keep two configuration planes separate

### Cargo manifest lint levels

`[lints]` and `[workspace.lints]` select Rust and Clippy lint levels and priorities. They answer "which diagnostics are allow/warn/deny/forbid?"

```toml
[workspace.lints.rust]
unsafe_code = "warn"

[workspace.lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
missing_errors_doc = "allow"
must_use_candidate = "allow"
```

When a group and individual lints coexist, give the group a lower priority so individual decisions win regardless of table key ordering. Priorities are integers; lower values are applied first. Confirm semantics with the project's Cargo version.

Workspace members opt into inherited policy explicitly:

```toml
[lints]
workspace = true
```

A package that owns different public/API or generated-code constraints may need a deliberate local policy instead of inheritance. Cargo's inheritance rules, not file location assumptions, decide the effective table.

### `clippy.toml` typed values

`clippy.toml` configures parameters consumed by particular lints. It does not assign lint levels. Use only keys and types listed for the pinned toolchain.

```toml
cognitive-complexity-threshold = 25
too-many-arguments-threshold = 7
allowed-idents-below-min-chars = ["db", "id", "io", "x", "y"]

disallowed-methods = [
  { path = "project_api::legacy_call", reason = "Use project_api::checked_call so failures retain context" },
]
```

Thresholds need a measured project reason. A smaller number is not inherently better. Disallowed items should encode an actual boundary or migration with an available replacement; they are not a vehicle for universal ecosystem preferences.

Before adding a key:

1. Find the exact key in the pinned toolchain's configuration page.
2. Check its type, default, associated lint, accepted paths, and MSRV behavior.
3. Add the lint level separately if the associated lint is not enabled.
4. Exercise one positive and one negative fixture so a typo or renamed key cannot silently masquerade as policy.

## Group selection

- `correctness`, `suspicious`, `style`, `complexity`, and `perf` are included through the ordinary Clippy group surface; inspect the exact toolchain catalog.
- `pedantic` is opt-in and opinionated. Enable it only after reviewing the initial corpus and setting intentional individual overrides.
- `nursery` is opt-in and less stable. Adopt individual proven lints or accept pinned-toolchain churn explicitly; never make it a blanket default.
- `cargo` examines manifest concerns and can be noisy in workspaces with intentional version duplication or metadata policy. Select it for a named dependency/manifest goal.
- The restriction collection is not designed to be enabled as a whole. Select individual restriction lints that encode a real project invariant.

Do not turn these into universal bans:

- `HashMap` versus ordered maps depends on ordering, hashing, memory, API, and threat requirements.
- Standard channels versus third-party channels depends on the protocol and measured needs.
- `unwrap`/`expect` depends on whether the boundary is an invariant, test, example, initialization, or recoverable input.
- process termination can be correct at a CLI boundary and wrong inside a library.
- stdout/stderr can be the CLI protocol rather than an observability defect.

## Build the effective command

1. Read repository instructions, `rust-toolchain*`, manifests, Cargo config, `clippy.toml`, CI/task commands, and generated/vendor boundaries.
2. Determine package, targets, features, target triple, and whether tests/examples/benches are part of the gate.
3. Reproduce the narrowest failing scope before expanding to workspace/all-targets.
4. Keep Cargo arguments before `--` and lint-driver arguments after it.
5. Do not assume all features are mutually compatible. Use the repository's supported feature matrix.
6. Treat warnings-as-errors as project policy. It also converts newly introduced toolchain warnings into failures, so pinning/update cadence matters.

<!-- command-contract: tool=clippy,cargo; channel=project; platform=project-host; effects=build-artifacts; evidence=clippy-catalog,cargo-lints -->
```bash
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
```

This is only valid when the repository declares that scope and strictness. Otherwise use its exact command. Machine-readable Cargo diagnostics are a Cargo interface; parsers must preserve rendered diagnostic, code, spans, applicability, child diagnostics, and process exit status rather than matching human text.

## Remediation algorithm

For each diagnostic:

1. Capture lint ID, level source, primary span, suggestion applicability, package/target/features, toolchain, and whether it is new or baseline.
2. Classify it:
   - mechanical and semantics-preserving;
   - semantic/API/MSRV/allocation/error-order change;
   - project-policy disagreement;
   - generated/vendor/test/example scope mismatch;
   - false positive or unavoidable boundary;
   - removed/renamed/deprecated lint after toolchain change.
3. Read the lint documentation and examples for the pinned toolchain.
4. Fix the owning code once. Do not add a broad allow around a local issue.
5. Review evaluation order, borrowing/drop timing, panic/error context, public types, feature/target cfg, performance claim, and MSRV.
6. Use automatic fix mode only in an authorized implementation workflow on a reviewed scope; inspect every source edit and keep unrelated dirty changes untouched.
7. For intentional exceptions, use the narrowest supported annotation with a reason and verify that the annotation itself is accepted by the MSRV.
8. Rerun the narrow command, then the declared repository gate. Report baseline failures separately.

## Allows and expectations

Use a local exception when the code intentionally violates a lint and changing it would weaken the contract.

<!-- rust-example: fragment -->
```rust
#[expect(
    clippy::cast_possible_truncation,
    reason = "range was checked against u16::MAX immediately above"
)]
let wire_length = validated_length as u16;
```

The example is a fragment: the actual proof must be visible and `#[expect]` plus `reason` must satisfy the project's toolchain/MSRV. If unsupported, use the narrow documented mechanism the project accepts. Avoid crate-wide allows unless the entire crate is an intentionally different boundary such as generated code.

An expectation can help reveal stale suppression when the lint no longer fires. Still review toolchain upgrades: a renamed lint can change what the annotation means.

## Disallowed items

Use `disallowed-methods`, `disallowed-types`, or related supported keys only when all of these hold:

- the path is confirmed in the pinned config schema;
- the forbidden item violates a project-specific boundary;
- a viable replacement or exception path exists;
- public API/MSRV/dependency consequences are understood;
- tests cover both the rejected and accepted shapes;
- generated, test, migration, or FFI code can receive a narrow exception when justified.

Prefer a domain API path over forbidding a standard primitive globally. For example, a project may require an audited clock or filesystem wrapper at a deterministic core boundary while allowing standard I/O in adapters and binaries.

## CI and developer tooling

- CI should use the same pinned toolchain and owned lint configuration as local reproduction.
- Keep installation actions, moving action revisions, review bots, uploads, and IDE settings outside this plugin's automatic workflow.
- rust-analyzer may run Clippy for feedback, but editor settings are not proof of the CI gate and can have different features/targets.
- Pre-commit execution is a repository choice; hooks must not hide slow network/build mutations or rewrite source unexpectedly.
- Generated and vendored files should be excluded at their owning build boundary rather than silenced through unrelated production modules.

## Toolchain upgrades

1. Run the old pinned gate and save baseline diagnostics.
2. Inspect Rust/Clippy release notes, renamed/removed/new lints, and config-key changes.
3. Run the new toolchain without bulk fixing.
4. Classify new diagnostics into newly found defects, policy churn, and changed semantics.
5. Update group overrides and config keys deliberately; keep priorities explicit.
6. Review source changes separately from policy changes.
7. Record accepted lint churn and upgrade the pinned toolchain only after the supported matrix passes.

## Failure diagnosis

| Symptom | Inspect first | Avoid |
|---|---|---|
| Individual allow does not override a group | lint-table priorities and inheritance | relying on TOML key order |
| Config key is ignored/rejected | pinned Clippy key/type and file discovery | copying a large sample config |
| Member has no workspace lints | member `[lints]` inheritance | assuming workspace tables apply automatically |
| CI has many more findings | package/target/features/toolchain/flags | broad suppression before reproducing scope |
| Toolchain update breaks policy | lint rename/default/group membership/config schema | bulk auto-fix and unreviewed allows |
| Suggested fix changes behavior | applicability, evaluation/drop order, API/MSRV | treating every Clippy suggestion as mechanical |
| Disallowed item blocks valid boundary code | invariant scope and exception path | swapping in an external crate universally |

The final report records the effective toolchain, config sources, lint levels and priorities, exact command/scope, each semantic policy choice, exceptions with reasons, source/config diffs, rerun evidence, and unrelated baseline diagnostics.
