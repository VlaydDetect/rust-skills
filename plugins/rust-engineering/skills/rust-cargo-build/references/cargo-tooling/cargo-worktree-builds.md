# Cargo builds in Git worktrees
Default to isolated writable Cargo state for each Git worktree. A common writable target directory is not a general-purpose compiler cache and is not this product's default.

## Ownership

- `$rust-cargo-build` owns effective target/build directories, config precedence, profiles, target triples, compiler wrappers, and build commands.
- `$rust-performance` measures duplicated work, lock contention, disk use, and cache hit rate before any optimization.
- `$rust-verify` runs the selected command separately in each intended worktree and reports baseline failures by path.
- `$rust-workspace` joins only if Cargo package membership or crate boundaries change. A Git worktree alone does not change package topology.

Official [Cargo build-cache](https://doc.rust-lang.org/stable/cargo/reference/build-cache.html) and [configuration](https://doc.rust-lang.org/cargo/reference/config.html) documentation own directory semantics. [Git worktree](https://git-scm.com/docs/git-worktree.html) owns linked-checkout administration. [sccache's Rust notes](https://github.com/mozilla/sccache/blob/main/docs/Rust.md) own compiler-cache limitations.

## Mental model

Cargo distinguishes:

- **target directory**: final artifacts such as binaries, docs, packages, and timing reports;
- **build directory**: internal compiler/build-script/incremental artifacts whose layout is not a public API;
- **compiler cache**: an optional external wrapper such as an already configured sccache, with its own cacheability contract.

Both Cargo directories default to the workspace-root `target` directory. Since each linked worktree has a different workspace root, defaults are naturally isolated. That costs disk and compilation time, but it preserves source/config/build-script identity and allows builds to proceed independently.

## Required discovery

Before changing layout:

1. Enumerate actual worktrees and resolve each path, branch/detached state, workspace root, and dirty state.
2. Record pinned Cargo/rustc versions, host and target triples, effective `.cargo/config*`, task runner, profiles, features, environment, compiler wrapper, and CI overrides.
3. Use Cargo metadata in each worktree to obtain `workspace_root` and effective `target_directory`; do not infer them from folder names.
4. Determine whether the current Cargo supports a separate templated `build.build-dir` and the exact `{workspace-path-hash}` semantics.
5. Measure clean/incremental duration, wait/lock time, disk use, and sccache statistics if already configured.
6. Name the goal: independent parallelism, lower disk use, shared compiler cache, faster warm builds, preserved artifacts after removing a worktree, or CI reuse. These goals need different layouts.

<!-- command-contract: tool=git,cargo; channel=project; platform=project-host; effects=read-only-host; evidence=git-worktree,cargo-metadata,cargo-config -->
```bash
git worktree list --porcelain
cargo metadata --format-version 1 --locked --offline --no-deps
```

Run metadata from each worktree under its actual environment. An offline cache miss is a reported environment limitation, not permission to fetch.

## Safe layouts

### A. Default per-worktree state

Use when correctness, independent parallel builds, or simplicity dominates.

```text
worktree-a/target/
worktree-b/target/
worktree-c/target/
```

This is the baseline. No configuration is needed. Cleanup is local to the worktree, though deleting the worktree also deletes its default artifacts.

### B. External but isolated directories

Use when build state should survive worktree removal or workspace disks are constrained, while keeping each worktree independent.

```text
<approved-cache-root>/<worktree-identity>/
```

Derive identity from a stable, collision-resistant representation of the canonical workspace path plus relevant host/target context. Validate the resolved absolute directory remains within the approved cache root before cleanup. Do not use a branch name alone: several worktrees can be detached or reuse names over time.

Set a unique target directory per worktree through the repository's approved environment/task runner. Environment values are process effects and should be printed in the evidence record.

### C. Templated intermediate build directory

When the pinned Cargo documents `build.build-dir`, it can move intermediate artifacts while preserving per-workspace identity. The path template below is illustrative; choose an approved root and confirm resolution on the project's Cargo version.

```toml
[build]
build-dir = "{cargo-cache-home}/rust-builds/{workspace-path-hash}"
```

`{workspace-path-hash}` is derived from the manifest path, so linked worktrees remain isolated. Final artifacts still follow the effective target-directory policy. Do not commit a machine-specific absolute path; prefer an explicitly managed local config or environment when repository policy allows it.

### D. Existing sccache wrapper

Use sccache for reusable rustc outputs across workspaces only when it is already installed and configured or installation/configuration is separately authorized.

- Verify `RUSTC_WRAPPER`/`build.rustc-wrapper` precedence and exact sccache version.
- Measure requests, hits, misses, non-cacheable compilations, errors, and storage before/after.
- sccache documents that rustc incremental compilation must be disabled for cacheability. This is a project-level trade-off, not an automatic change.
- Link-producing crates, proc macros, build scripts, environment macros, generated inputs, and filesystem-reading macros have limitations. A low hit rate is a diagnosis input, not proof that sccache is broken.
- Remote cache credentials, service endpoints, network use, eviction, and trust are deployment decisions outside automatic workflow.

## Why one writable target is rejected as the default

Two divergent worktrees may differ in source, lockfile, features, cfg, rustflags, build-script inputs, generated outputs, target, profile, compiler wrapper, environment, and toolchain. Cargo fingerprints and locks coordinate Cargo's own build state, but the target directory is not documented as a content-addressed cross-workspace cache API.

A shared writable directory can therefore cause:

- global lock contention that removes the intended parallelism;
- repeated invalidation when leaf crates and build scripts differ;
- confusing artifact ownership and report paths;
- cleanup by one task affecting another;
- final binaries/reports being mistaken for a different worktree's result;
- poor reproducibility when absolute paths or environment-dependent inputs enter fingerprints;
- difficult incident diagnosis because source identity and build state no longer align visibly.

Do not dismiss a compiler error as transient cache noise. Reproduce the exact command with an isolated target/build directory. If it still fails, it is a project/toolchain issue; if it does not, preserve both layouts and investigate Cargo/tool versions, fingerprints, build scripts, and concurrent effects. Never mutate source timestamps as a cache-recovery ritual.

## Decision algorithm

1. Start from per-worktree defaults.
2. Reproduce the duplication or disk problem and collect a comparable baseline.
3. If parallelism is desired, keep writable state isolated and cap CPU/job concurrency explicitly rather than relying on target-directory locks.
4. If worktree deletion should not remove artifacts, move each worktree to a unique external directory.
5. If the pinned Cargo supports templated build directories, test an isolated path template in two divergent worktrees.
6. If cross-workspace compiler reuse is the goal, evaluate the existing sccache path and its hit/miss/non-cacheable evidence.
7. Change one variable. Run distinct modifications in two worktrees concurrently, then rerun incrementally and compare correctness, duration, lock wait, cache statistics, and disk.
8. Keep the new layout only if it improves the named metric without weakening source/artifact identity or cleanup safety.

## Validation matrix

Create two disposable linked worktrees or use existing authorized ones. Do not create/remove worktrees unless the task includes that mutation.

- Same revision and same command: establishes duplicate-work baseline.
- Divergent source in one leaf crate: proves final artifact identity.
- Divergent manifest/feature/lockfile: exercises dependency invalidation.
- Build script or generated output change: exercises intermediate ownership.
- Different target or profile: proves path separation.
- Concurrent builds: measures parallel progress versus lock wait.
- Repeat with no changes: measures warm incremental/cache behavior.
- Remove one worktree: confirms another worktree's artifacts remain valid.

<!-- command-contract: tool=cargo; channel=project; platform=project-host; effects=build-artifacts,process-execution; evidence=cargo-build-cache,cargo-config -->
```bash
cargo check --workspace --all-targets --locked --offline
```

Run the command separately with each worktree's recorded directory policy; never treat one worktree's green result as evidence for another's source.

## Cleanup

- Resolve every target/build path before deleting anything and confirm it is inside the explicitly approved cache root or named worktree.
- Do not recursively clean a shared root when the intended target is one worktree identity.
- Coordinate with active Cargo processes and retain evidence needed for an unresolved failure.
- Report what was removed, whether it was reproducible, and whether other worktrees still reference it.

## Diagnosis table

| Symptom | Inspect first | Response |
|---|---|---|
| Every worktree recompiles dependencies | toolchain/config/features/path differences and sccache stats | quantify before changing layout |
| Concurrent jobs mostly wait | Cargo locks, job count, disk/CPU pressure | preserve isolation; schedule or cap jobs explicitly |
| Unexpected old/new API diagnostic | exact source revision, metadata, rustc command, isolated reproduction | investigate; do not label it spurious |
| Disk use grows linearly | target/build paths and artifact retention | external isolated dirs or approved scoped cleanup |
| sccache misses | incremental mode, environment, proc macros, linker crates, generated inputs | classify cacheability before remote-cache proposals |
| Wrong binary/report consumed | effective target dir, target triple, profile, worktree identity | resolve artifact from the producing command, not a guessed path |

The final record includes worktree/source identity, Cargo/rustc/sccache versions, effective config, target/build directories, target/profile/features, exact commands, concurrency, timings, cache statistics, disk use, failures, cleanup, and the reason the chosen layout is safer than the baseline.
