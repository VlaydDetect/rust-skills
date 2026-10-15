# Rust Engineering

**Focused Rust guidance, from the first question to verified changes.**

[English](README.md) · [Русский](README_ru.md) · [Releases](https://github.com/VlaydDetect/rust-skills/releases) · [MIT license](plugins/rust-engineering/LICENSE)

One plugin for **Codex / ChatGPT Desktop** and **Claude Code / Desktop**. Rust Engineering helps an agent understand the repository, choose the right specialist, preserve contracts, and collect evidence for its changes.

| Skills | Coding rules | Unsafe / FFI rules | Evaluation scenarios |
| :---: | :---: | :---: | :---: |
| **57** | **265** | **47** | **369** |

[Install](#install) · [Choose a starting point](#choose-a-starting-point) · [Skill directory](#skill-directory) · [How it works](#how-it-works) · [Validation](#validation)

## Choose a starting point

Describe the outcome and constraints in ordinary language, or invoke a skill directly: `$skill-name` in Codex and `/rust-engineering:skill-name` in Claude Code.

| Your task | Start with | What happens next |
| --- | --- | --- |
| Implement a feature or fix | `rust-workflow` | Discover the project, assign decision owners, make the change, verify it. |
| Investigate an unexplained failure | `debugging` | Reproduce the failure and isolate its cause before proposing a patch. |
| Understand a new repository | `codebase-onboarding` | Map packages, entrypoints, boundaries, commands, and risks. |
| Review a change | `rust-review` | Inspect the diff and connected code; report confirmed findings. |
| Run checks on an existing state | `rust-verify` | Select sufficient evidence and separate failures from unavailable tools. |
| Improve performance | `rust-performance` | Route measurement to `rust-profiling`, changes to `rust-optimization`, and safety proofs to `rust-unsafe`. |
| Prepare a Rust development shell | `nix-dev-env` | Inspect the toolchain and native dependencies before designing the environment. |

## Install

The current stable release is **1.0.3**, pinned to Git tag `v1.0.3`. Choose either installer; both use the host's native plugin commands and have no package dependencies of their own.

**With uv**

~~~powershell
uv run --no-project https://raw.githubusercontent.com/VlaydDetect/rust-skills/v1.0.3/installers/install.py --target all
~~~

**With npx**

~~~powershell
npx --yes github:VlaydDetect/rust-skills#v1.0.3 --target all
~~~

<details>
<summary>Other package runners and installer options</summary>

~~~powershell
npm exec --yes --package=github:VlaydDetect/rust-skills#v1.0.3 -- rust-engineering-install --target all
pnpm dlx github:VlaydDetect/rust-skills#v1.0.3 --target all
~~~

- `--target codex-cli|chatgpt-desktop|claude-code|claude-desktop|all` (default: `all`).
- `--scope user|project|local` for Claude (default: `user`).
- `--dry-run` prints the plan without changing anything.
- `--yes` skips the installer's confirmation prompt.

The installers require the relevant host CLI for CLI targets. They do not install Codex, Claude, Node.js, uv, or Rust. A marketplace name pointing to another source is rejected.

</details>

<details>
<summary>Native CLI installation and updates</summary>

Codex:

~~~powershell
codex plugin marketplace add VlaydDetect/rust-skills --ref v1.0.3
codex plugin add rust-engineering@rust-skills
~~~

Claude Code:

~~~powershell
claude plugin marketplace add VlaydDetect/rust-skills@v1.0.3 --scope user
claude plugin install rust-engineering@rust-skills --scope user
~~~

To refresh the configured source, use `codex plugin marketplace upgrade rust-skills` or `claude plugin marketplace update rust-skills`. For Claude, follow with `claude plugin update rust-engineering@rust-skills --scope user`.

Refreshing preserves the configured Git ref. If you pinned an older release, select the desired release ref through the host's marketplace commands or UI first; refreshing an old tag does not select a newer release. Check the installed version with `codex plugin list --json` or `claude plugin list --json`.

</details>

**Desktop:** use the host's plugin catalog or local-session `/plugin` interface to confirm installation. Start a new task in Codex / ChatGPT Desktop; in Claude, use `/reload-plugins` or restart when needed. The installers provide Desktop instructions and never edit Desktop configuration or caches directly.

## Skill directory

Each link opens the skill's instructions. Supporting references are loaded only when the current decision needs them.

### Workflow and discovery

| Skill | Use it to |
| --- | --- |
| [rust-workflow](plugins/rust-engineering/skills/rust-workflow/SKILL.md) | Coordinate a repository change, assign decision owners, and close the evidence loop. |
| [specs](plugins/rust-engineering/skills/specs/SKILL.md) | Turn a request into observable contracts and acceptance scenarios. |
| [codebase-onboarding](plugins/rust-engineering/skills/codebase-onboarding/SKILL.md) | Map an unfamiliar repository before consequential work. |
| [rust-navigation](plugins/rust-engineering/skills/rust-navigation/SKILL.md) | Find definitions, callers, trait implementations, macros, and feature gates. |
| [rust-design-protocol](plugins/rust-engineering/skills/rust-design-protocol/SKILL.md) | Resolve consequential questions across language, design, and domain constraints. |
| [debugging](plugins/rust-engineering/skills/debugging/SKILL.md) | Reproduce and isolate compile, runtime, concurrency, and performance failures. |
| [refactoring](plugins/rust-engineering/skills/refactoring/SKILL.md) | Restructure code while preserving an explicit behavior and compatibility contract. |
| [addressing-findings](plugins/rust-engineering/skills/addressing-findings/SKILL.md) | Triage supplied findings, implement fixes, and verify each resolution. |

### Review and evidence

| Skill | Use it to |
| --- | --- |
| [rust-review](plugins/rust-engineering/skills/rust-review/SKILL.md) | Review a bounded diff and report confirmed findings with a verdict. |
| [rust-architecture-review](plugins/rust-engineering/skills/rust-architecture-review/SKILL.md) | Assess package boundaries, dependency direction, coupling, and complexity. |
| [rust-verify](plugins/rust-engineering/skills/rust-verify/SKILL.md) | Run the smallest sufficient checks and classify failures by evidence. |
| [rust-research](plugins/rust-engineering/skills/rust-research/SKILL.md) | Verify current Rust and ecosystem facts using dated primary sources. |

### Language and APIs

| Skill | Use it to |
| --- | --- |
| [rust-api-design](plugins/rust-engineering/skills/rust-api-design/SKILL.md) | Design public contracts, visibility, extensibility, and downstream ergonomics. |
| [rust-ownership](plugins/rust-engineering/skills/rust-ownership/SKILL.md) | Resolve borrowing, lifetimes, moves, RAII, and resource ownership. |
| [rust-traits](plugins/rust-engineering/skills/rust-traits/SKILL.md) | Choose generics, trait objects, bounds, associated types, and typestates. |
| [rust-errors](plugins/rust-engineering/skills/rust-errors/SKILL.md) | Define failure boundaries, recovery, context, and panic policy. |
| [rust-idioms](plugins/rust-engineering/skills/rust-idioms/SKILL.md) | Improve Rust expression and maintainability within project constraints. |
| [rust-stable](plugins/rust-engineering/skills/rust-stable/SKILL.md) | Choose editions, MSRV, stable features, and compatibility tactics. |
| [rust-stdlib](plugins/rust-engineering/skills/rust-stdlib/SKILL.md) | Select standard collections, iterators, I/O, paths, and synchronization. |
| [rust-by-example](plugins/rust-engineering/skills/rust-by-example/SKILL.md) | Explain a Rust concept with a minimal compiling example. |
| [rust-pin](plugins/rust-engineering/skills/rust-pin/SKILL.md) | Establish address stability, projection, polling, and pinned destruction contracts. |

### Cargo, structure, and quality

| Skill | Use it to |
| --- | --- |
| [rust-cargo-build](plugins/rust-engineering/skills/rust-cargo-build/SKILL.md) | Diagnose manifests, features, profiles, build scripts, and effective Cargo state. |
| [rust-workspace](plugins/rust-engineering/skills/rust-workspace/SKILL.md) | Design crate boundaries, shared metadata, resolver policy, and release groups. |
| [rust-module-layout](plugins/rust-engineering/skills/rust-module-layout/SKILL.md) | Organize modules, files, visibility, re-exports, and test placement. |
| [rust-dependencies](plugins/rust-engineering/skills/rust-dependencies/SKILL.md) | Govern adopted dependency versions, features, sources, security, and removal. |
| [rust-crate-discovery](plugins/rust-engineering/skills/rust-crate-discovery/SKILL.md) | Evaluate candidate crates against requirements before adopting them. |
| [rust-semver](plugins/rust-engineering/skills/rust-semver/SKILL.md) | Classify API, behavior, feature, and MSRV compatibility changes. |
| [rust-style-clippy](plugins/rust-engineering/skills/rust-style-clippy/SKILL.md) | Apply formatting and lint policy with justified, scoped exceptions. |
| [rust-testing](plugins/rust-engineering/skills/rust-testing/SKILL.md) | Design unit, integration, property, async, fuzz, and end-to-end tests. |
| [rust-documentation](plugins/rust-engineering/skills/rust-documentation/SKILL.md) | Maintain rustdoc, examples, doctests, READMEs, and migration guidance. |
| [rust-ecosystem](plugins/rust-engineering/skills/rust-ecosystem/SKILL.md) | Choose a project shape and toolchain conventions before crate selection. |
| [rust-coding-rules](plugins/rust-engineering/skills/rust-coding-rules/SKILL.md) | Select concrete rules from the 265-rule catalog after routing. |

### Architecture and runtime

| Skill | Use it to |
| --- | --- |
| [rust-architecture](plugins/rust-engineering/skills/rust-architecture/SKILL.md) | Define system boundaries, dependency direction, ports, adapters, and composition. |
| [rust-concurrency](plugins/rust-engineering/skills/rust-concurrency/SKILL.md) | Design tasks, threads, locks, channels, cancellation, and backpressure. |
| [rust-data](plugins/rust-engineering/skills/rust-data/SKILL.md) | Shape layouts and traversal around measured data access patterns. |
| [rust-database](plugins/rust-engineering/skills/rust-database/SKILL.md) | Handle transactions, pools, migrations, retries, backups, and integration tests. |
| [rust-distributed-systems](plugins/rust-engineering/skills/rust-distributed-systems/SKILL.md) | Reason about partial failure, idempotency, consistency, and coordination. |
| [rust-serialization](plugins/rust-engineering/skills/rust-serialization/SKILL.md) | Specify binary formats, schema evolution, canonical bytes, and decode limits. |
| [rust-platforms](plugins/rust-engineering/skills/rust-platforms/SKILL.md) | Engineer Unix and Windows runtime behavior and resource lifecycles. |
| [rust-observability](plugins/rust-engineering/skills/rust-observability/SKILL.md) | Design tracing, logs, metrics, correlation, redaction, and cardinality. |

### Performance and safety

| Skill | Use it to |
| --- | --- |
| [rust-performance](plugins/rust-engineering/skills/rust-performance/SKILL.md) | Use the compatible entrypoint to frame a performance question and route it. |
| [rust-profiling](plugins/rust-engineering/skills/rust-profiling/SKILL.md) | Design valid experiments and interpret benchmarks, profiles, counters, and traces. |
| [rust-optimization](plugins/rust-engineering/skills/rust-optimization/SKILL.md) | Choose changes from confirmed bottlenecks and verify their system effect. |
| [rust-unsafe](plugins/rust-engineering/skills/rust-unsafe/SKILL.md) | Prove unsafe preconditions and sound safe abstractions; use Miri as supporting evidence. |
| [rust-unsafe-ffi](plugins/rust-engineering/skills/rust-unsafe-ffi/SKILL.md) | Specify external ABI, ownership transfer, callbacks, unwinding, and foreign lifetimes. |

### Specialized Rust

| Skill | Use it to |
| --- | --- |
| [rust-macros](plugins/rust-engineering/skills/rust-macros/SKILL.md) | Design declarative and procedural macros with bounded expansion and useful diagnostics. |
| [rust-lombok-macros](plugins/rust-engineering/skills/rust-lombok-macros/SKILL.md) | Evaluate derives and attributes for constructors, builders, and boilerplate. |
| [rust-tauri](plugins/rust-engineering/skills/rust-tauri/SKILL.md) | Build Tauri 2 IPC, capabilities, plugin, updater, and frontend boundaries. |
| [rust-uniffi-building](plugins/rust-engineering/skills/rust-uniffi-building/SKILL.md) | Maintain UniFFI interfaces, bindings, scaffolding, and cross-language tests. |
| [rust-ml](plugins/rust-engineering/skills/rust-ml/SKILL.md) | Design model, tensor, preprocessing, device, and serving workflows. |
| [rust-gpu](plugins/rust-engineering/skills/rust-gpu/SKILL.md) | Diagnose host-device transfers, layouts, dispatch, synchronization, and bottlenecks. |
| [rust-systems-networking](plugins/rust-engineering/skills/rust-systems-networking/SKILL.md) | Engineer eBPF and DPDK buffers, queues, ownership, affinity, and NUMA placement. |

### Nix and NixOS

| Skill | Use it to |
| --- | --- |
| [nix-flakes](plugins/rust-engineering/skills/nix-flakes/SKILL.md) | Design flake inputs, locks, systems, overlays, packages, and checks. |
| [nix-dev-env](plugins/rust-engineering/skills/nix-dev-env/SKILL.md) | Create reproducible Rust development shells and editor environments. |
| [nix-packaging](plugins/rust-engineering/skills/nix-packaging/SKILL.md) | Package Rust software with fixed Cargo sources and reproducible builds. |
| [nixos](plugins/rust-engineering/skills/nixos/SKILL.md) | Configure NixOS and Home Manager modules, services, options, and secrets. |
| [nix-review](plugins/rust-engineering/skills/nix-review/SKILL.md) | Review Nix changes for purity, platform support, hashes, and security. |

## How it works

~~~text
Request → rust-workflow → project discovery → decision owners
        → relevant coding profiles and rules → implementation
        → rust-verify → rust-review when requested or proportionate to risk
~~~

The workflow selects profiles from the current change. Each decision has one owner; helpers require an observed trigger. The `ProfileStack` limits of **3 owners / 6 coding profiles / 10 helpers** force a phase split when exceeded. The rulebook adds at most **nine relevant rules per decision** after routing. The main agent writes; supporting agents are read-only.

For performance work, start with a workload and a measurable goal. Validate the experiment, identify the limiting resource, choose a change supported by data and invariants, then recheck the whole system. Criterion, VTune, WPR/WPA, perf, allocation tools, code inspection, PGO, and BOLT are selected by the question and platform. Miri checks executed paths for correctness; its timings are not native performance evidence.

SessionStart hooks inspect local project signals. They stay fast, offline, deterministic, and read-only: a non-Rust directory is silent; Rust projects receive context and an opt-in setup offer. Nix/NixOS setup is a separate offer. Tools are proposed from project evidence and installed only with authorization.

The product source is `plugins/rust-engineering/`. Skill instructions and shared scripts are host-neutral; Codex and Claude keep their own manifests and SessionStart schemas. The plugin itself needs no extra runtime dependencies or network access; individual research and measurement tasks may need external tools or online sources.

## Validation

Run from the repository root:

~~~powershell
uv run --no-project plugins/rust-engineering/scripts/validate.py --examples
node installers/install.mjs --target all --dry-run
git diff --check
~~~

The release gate checks both README catalogs and links, all 57 skills, reference layout, 265 rule IDs/aliases, 47 unsafe/FFI rules, 369 schema-9 evaluation scenarios, four read-only agent contracts, manifests, installer parity, source collisions, offline hooks, and example fixtures. It runs **25 golden example projects** and checks the classification of **1,141 rule examples**; compilable examples are tested in their declared context.

Evaluation JSON validation checks structure and routing contracts. Model behavior checks and hardware measurements are separate evidence. Run `claude plugin validate ./plugins/rust-engineering` when Claude CLI is available, and the host's own validator when exposed by the installed version.

If Miri fails before executing tests because a sandbox cannot write to the user's cache, inspect the error and retry the same focused command under the normal account through the host's authorized execution mechanism. Keep the toolchain, target, features, and offline policy fixed. Do not treat this as a failing test or automatically reinstall Miri.

## License

Distributed under the [MIT License](plugins/rust-engineering/LICENSE). Third-party license texts and attribution are recorded in [THIRD_PARTY_NOTICES.md](plugins/rust-engineering/THIRD_PARTY_NOTICES.md).

## Sources

- [gurinderu/craft](https://github.com/gurinderu/craft), revision `d9caf7faf36b565a59534c581fdc27516e87600a`.
- [full-stack-skills/rust-skills](https://github.com/full-stack-skills/rust-skills), revision `25e44452df00055ca246ec806425d99028eaae19`.
- [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills), revision `fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9`.
- [actionbook/rust-skills](https://github.com/actionbook/rust-skills), revision `fa60f7931223646fb71c4586b4a6c8545016076a`.
- [huiali/rust-skills](https://github.com/huiali/rust-skills), revision `947bf77509d9b421035037e983da6662d08cbb8e`.
- [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills), revision `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`.
- [laurigates/claude-plugins](https://github.com/laurigates/claude-plugins), revision `a1e72ed186b97555256d8c058ff291c182332df7`.

Optimization and measurement reading (reviewed 2026-10-15; authors' results were not reproduced):

- [Figma: memory optimizations in Rust](https://www.figma.com/blog/supporting-faster-file-load-times-with-memory-optimizations-in-rust/).
- [Cloudflare: trie-hard](https://blog.cloudflare.com/pingora-saving-compute-1-percent-at-a-time/).
- [Cloudflare: WAF ML pipeline](https://blog.cloudflare.com/making-waf-ai-models-go-brr/).
- [Sentry: A locking war story](https://blog.sentry.io/locking-war-story/).
- [ScyllaDB: Rust Alternator driver](https://www.scylladb.com/2026/08/27/new-rust-driver-for-scylladbs-dynamodb-api/).
- [Cloudflare: DNS cache memory](https://blog.cloudflare.com/dns-cache-memory-optimization-1111/).
- [Cloudflare: consistent hashing memory](https://blog.cloudflare.com/saving-100-tb-of-ram-with-math/).
- [ClickHouse: hash tables and zero-cost abstractions](https://clickhouse.com/blog/hash-tables-in-clickhouse-and-zero-cost-abstractions).
- [ScyllaDB: asymmetric io_uring backend](https://www.scylladb.com/2026/07/22/asymmetric-io_uring-backend-seastar/).
- [Cloudflare: WAN throughput and latency](https://blog.cloudflare.com/optimizing-tcp-for-high-throughput-and-low-latency/).
- [Abseil #75: How to microbenchmark](https://abseil.io/fast/75).
- [Abseil #53: Hardware Performance Counters](https://abseil.io/fast/53).
- [Abseil #83: Reducing memory indirections](https://abseil.io/fast/83).
- [Abseil #39: Microbenchmark limitations](https://abseil.io/fast/39).
- [Abseil #88: Measurement methodology](https://abseil.io/fast/88).

The ScyllaDB asymmetric io_uring source was available only as an indexed excerpt; unverified numerical details were excluded. Tool contracts are checked against the official documentation linked from the relevant protocols.
