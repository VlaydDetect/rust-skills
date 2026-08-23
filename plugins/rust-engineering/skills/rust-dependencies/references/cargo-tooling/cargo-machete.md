# cargo-machete: unused-dependency evidence protocol

<!-- laurigates-source-family: cargo-machete; source=rust-plugin/skills/cargo-machete/SKILL.md; sha256=924a6c4372df995df89f0fc35d729a35ba4d36b7cf61e81630ef5f596ca719a1; revision=a1e72ed186b97555256d8c058ff291c182332df7 -->

Use cargo-machete as a fast heuristic that proposes dependency-removal candidates. `$rust-dependencies` owns the decision; the tool never proves that removal is safe.

## Current contract

The [tool-owner documentation](https://github.com/bnjbvr/cargo-machete) describes directory scanning as the primary interface:

- run in a directory containing one or more Cargo projects, or pass an explicit directory;
- exit `0` means no unused dependencies were reported;
- exit `1` means at least one candidate was reported and is not a processing failure;
- exit `2` means processing failed, so the dependency result is unknown;
- optional JSON output is a versioned external-tool interface and must be tested against the installed version;
- metadata-assisted analysis can be more accurate but may modify project lockfiles.

The source corpus's workspace/package/exclude and automatic-removal recipes are not current product policy. Check `cargo machete --version` and matching help before every version-sensitive invocation. If the tool is absent, return `SKIP`; do not install it.

## Ownership and routing

- `$rust-dependencies` classifies findings and owns manifest removal, false-positive policy, lockfile review, and dependency risk.
- `$rust-cargo-build` supplies effective workspace, package, feature, target, build-script, metadata, and lockfile mechanics.
- `$rust-verify` runs only the already approved scan and post-removal matrix.
- `$rust-performance` joins only when a dependency has measured build/runtime/size cost; "unused" alone is not a performance result.
- `$rust-research` is required when installed CLI behavior or an alternative analyzer is uncertain.

## Read-only scan

First identify the effective workspace root and dirty state. A normal scan reads manifests and source heuristically and should not edit the repository.

<!-- command-contract: tool=cargo-machete; channel=external; platform=project-host; effects=read-only-host; evidence=cargo-machete -->
```bash
cargo machete <reviewed-project-directory>
```

Record the tool version, directory, stdout/stderr, and numeric exit code. Treat code `1` as findings to review, not an infrastructure failure. Treat code `2` as no conclusion.

For automation that consumes JSON, pin the installed tool version and validate the actual schema against clean, findings, ignored, and processing-error samples. Do not infer an empty object from a failed process.

## Why findings are heuristic

Textual or syntax-oriented analysis can miss dependencies referenced outside ordinary Rust source paths or under configurations not visible to the scan. Investigate at least:

- renamed dependencies and the difference between manifest package name and Rust import name;
- proc-macro and derive usage where the expanded code or helper crate name differs;
- macro-only dependencies and macros re-exported through another crate;
- `build.rs`, build-dependencies, generated Rust, `include!`, code generation, and links metadata;
- target-specific tables and `cfg`-gated modules;
- optional dependencies activated through implicit or explicit features;
- examples, benches, integration tests, doctests, fuzz targets, tools, and xtask packages;
- public re-exports and types that make a dependency part of downstream API;
- runtime plugin/loading conventions, resources, schemas, or external commands not represented by an import;
- feature matrices where the dependency is absent from default features but required elsewhere.

The tool also does not establish that declared features on a used dependency are unused. Analyze feature edges through Cargo metadata and the dependency's contract rather than accepting invented feature-level output.

## False-positive metadata

Use Cargo manifest metadata only after proving why the heuristic cannot see a real use. Keep the explanation beside the dependency or in the review record.

For a package-owned exception:

```toml
[dependencies]
prost = "<project-version>"

[package.metadata.cargo-machete]
ignored = ["prost"]
```

For a workspace-owned exception:

```toml
[workspace.metadata.cargo-machete]
ignored = ["prost"]
```

Ignoring hides future transitions from used to unused. Prefer a rename mapping when the only problem is the Rust import name:

```toml
[dependencies]
rustls-webpki = "<project-version>"

[package.metadata.cargo-machete.renamed]
rustls-webpki = "webpki"
```

The equivalent workspace table is `[workspace.metadata.cargo-machete.renamed]`. A rename keeps the dependency analyzable; an ignored entry suppresses the finding. Re-run the clean and candidate fixtures when upgrading cargo-machete because metadata semantics are external-tool behavior.

Do not move a dependency between normal, build, and dev sections merely to satisfy the analyzer. Its section must match the real Cargo compilation boundary.

## Metadata-assisted mode

The installed tool may offer metadata-assisted analysis that calls Cargo metadata with broad features. Its documented side effect is important: it can change `Cargo.lock`.

Before authorizing that mode:

1. Confirm the exact installed flag and behavior from owner documentation/help.
2. Inspect dirty state and current lockfile policy.
3. Decide whether network/resolution is allowed; the tool's internal Cargo invocation may not preserve the caller's desired locked/offline contract.
4. Snapshot the existing diff and define the expected lockfile outcome.
5. Run only in an implementation workflow with explicit lockfile authorization.
6. Review the lockfile diff separately. Do not discard unrelated user changes or present a mutated lockfile as read-only evidence.

If lockfile mutation is not allowed, use the ordinary heuristic plus independent Cargo metadata and source/config inspection instead.

## Candidate decision algorithm

For each reported dependency:

1. Locate the exact declaration, owner package, section, target condition, optional status, workspace inheritance, source, version, and enabled features.
2. Confirm the reported name against `package`, local rename, generated import, and proc-macro naming.
3. Search Rust source, manifests, build scripts, generated-code inputs, examples, benches, tests, doctests, fuzz targets, tasks, documentation, and CI.
4. Inspect Cargo metadata for reverse edges, features, targets, build dependencies, and target-specific activation. Metadata describes the resolved graph; it does not prove semantic use.
5. Classify the candidate:
   - genuinely unused in every supported configuration;
   - used only under a documented configuration;
   - heuristic false positive requiring rename/ignore metadata;
   - uncertain because a generated/runtime boundary cannot be resolved;
   - declaration belongs in a different Cargo section for independent semantic reasons.
6. For genuine candidates, predict public API, build-script, native-link, feature, license, advisory, lockfile, and MSRV effects before editing.
7. Remove one coherent set manually from the owning manifest. Review the manifest and lockfile diff; do not delegate source edits to an opaque analyzer action.
8. Run the relevant target/feature/test/doc/example/bench matrix and repeat the ordinary scan.
9. Report residual configurations not exercised.

## Post-removal verification

Use repository-defined commands whenever they exist. The following is only a shape; package, target, features, and locked/offline policy must match the removed dependency's reach.

<!-- command-contract: tool=cargo; channel=project; platform=project-host; effects=build-artifacts; evidence=cargo-metadata -->
```bash
cargo metadata --format-version 1 --locked --offline
cargo check --workspace --all-targets --locked --offline
cargo test --workspace --no-run --locked --offline
```

One all-features build is not a substitute for mutually constrained feature combinations, target-specific dependencies, or no-default-features support. Add only the smallest matrix that reaches the candidate's former use sites.

## CI policy

- Pin or otherwise resolve cargo-machete under the project's tool-management policy.
- Preserve exit `1` as a findings outcome and exit `2` as an analyzer error.
- Run the ordinary no-mutation mode unless the job explicitly owns lockfile updates.
- Do not place installation, moving-branch actions, or automatic manifest edits inside this plugin's workflow.
- Review ignored and renamed metadata as code; stale ignores can hide real cleanup opportunities.
- Keep security, license, outdated-version, and duplicate-version checks separate. They answer different questions and have different false-positive models.

## Diagnosis table

| Finding or failure | Evidence to inspect | Decision |
|---|---|---|
| Renamed crate reported | manifest key, `package`, Rust import | add a reviewed rename mapping if use is real |
| Generated/proc-macro use reported | build script, generator input/output, macro expansion boundary | document and narrowly ignore only when mapping cannot express it |
| Dev dependency reported | integration tests, examples, benches, doctests, fuzz/xtask | remove only after the supported dev matrix proves absence |
| Optional dependency reported | feature edges and all supported feature combinations | retain or remove the owning feature and dependency coherently |
| Exit code `2` | stderr, path, manifest parsing, tool version | report analyzer failure; make no dependency claim |
| Lockfile changed | metadata-assisted effect and resolution diff | review as a separate authorized mutation |
| Build still passes after removal | untested target/feature/generated/public paths | do not conclude full safety from one build |

The final evidence record names every candidate, classification, proof or uncertainty, manifest/lockfile changes, exact verification matrix, and any accepted ignore/rename metadata.
