# cargo-generate: reviewed scaffolding protocol
Use this reference only when a task explicitly creates or maintains a project template. The existence of `Cargo.toml` does not activate it.

## Ownership and hand-offs

- `$rust-cargo-build` owns generator invocation, effective Cargo state, output validation, and mutation accounting.
- `$rust-workspace` joins only when generated packages change an existing workspace topology.
- `$rust-research` verifies the resolved cargo-generate version and remote template revision.
- Prefer `cargo new` for a plain binary or library. Prefer a reviewed file copy for a fixed, substitution-free skeleton. Use cargo-generate when reusable placeholders, variants, path rendering, or hooks justify the extra trust boundary.

## Required evidence

Before proposing or running the tool, establish:

1. The repository instructions, pinned Rust toolchain, effective workspace root, Cargo config, VCS policy, and intended destination.
2. Whether `cargo-generate` is already installed. Record its exact `--version` and consult its matching `--help`; absence is `SKIP`, not permission to install.
3. Template origin: local path or remote URL, immutable revision when remote, license, expected output, and who controls updates.
4. The complete `cargo-generate.toml`, every included Rhai hook, nested templates, and files that contain Liquid-like braces.
5. All effects: network access, process execution, output writes, overwrite/init behavior, VCS initialization, and possible parent-workspace edits.

The product baseline is [cargo-generate's guide](https://cargo-generate.github.io/cargo-generate/) plus the [resolved `GenerateArgs` API](https://docs.rs/cargo-generate/latest/cargo_generate/struct.GenerateArgs.html). Exact arguments remain version-specific.

## Trust and effects matrix

| Source or mode | Minimum trust gate | Effects to disclose |
|---|---|---|
| Local reviewed template | Inspect config, rendered paths, hooks, and destination | output writes; optional process/VCS/workspace writes |
| Remote template | Pin and review a revision before generation | network plus all local-template effects |
| Generate into a new temporary directory | Ensure destination does not exist or is disposable | isolated output writes |
| Initialize an existing directory | Review every collision and current dirty state | in-place writes and possible overwrite |
| Hook command execution | Review the exact Rhai program and commands | arbitrary child processes and their transitive effects |
| Automatic parent-workspace addition | Inspect owning workspace manifest and membership policy | manifest mutation and metadata change |

`--silent` suppresses prompts. It does not make the operation read-only, trusted, deterministic, or safe for automation. Likewise, a local template can execute reviewed hooks and a remote template can change at an unpinned branch or tag.

## Generation algorithm

1. Decide whether a generator is needed. Record why `cargo new` or a fixed copy is insufficient.
2. Resolve the installed tool version and template revision. Never install or fetch implicitly.
3. Review template configuration before expansion:
   - `[template]` render/include/exclude behavior;
   - placeholder types, defaults, choices, validation, and secret-shaped inputs;
   - conditions that remove files or introduce nested placeholders;
   - path-name rendering and case conversion;
   - init/pre/post hooks and every use of a command-execution API;
   - literal `${{ ... }}`, `{{ ... }}`, Jinja, Handlebars, Vue, or other brace syntax that Liquid could consume.
4. Make inputs explicit. Prefer a reviewed values file for many values; never put secrets in committed template values or command history.
5. Generate into a fresh temporary directory outside the intended destination. Disable VCS initialization when the result will be integrated into an existing repository.
6. Inspect the generated tree before copying anything: unexpected files, symlinks, executable bits, generated credentials, nested VCS metadata, lockfiles, licenses, CI, and scripts.
7. Validate Cargo state from the generated directory with project-compatible locked/offline policy. If dependencies are not cached, report an environment `SKIP` rather than silently fetching.
8. Compare the generated result with the intended destination, integrate the reviewed diff, and separately review parent-workspace or lockfile changes.
9. Record the template URL/path, immutable revision, tool version, input values excluding secrets, and validation evidence so regeneration is reproducible.

## Safe command shapes

The following is a mutation example, not an automatic hook. Replace placeholders only after checking the installed tool's help.

<!-- command-contract: tool=cargo-generate; channel=external; platform=project-host; effects=source-writes,process-execution; evidence=cargo-generate-guide,cargo-generate-api -->
```bash
cargo generate --path <reviewed-local-template> --name <probe-name> --destination <fresh-temp-parent> --vcs none --silent
```

For a remote source, first obtain explicit network authorization and pin the reviewed revision rather than a moving branch. Do not combine remote retrieval, command-enabled hooks, and in-place initialization into one opaque operation.

<!-- command-contract: tool=cargo-generate; channel=external; platform=project-host; effects=network,source-writes,process-execution; evidence=cargo-generate-guide,cargo-generate-api -->
```bash
cargo generate --git <reviewed-url> --revision <immutable-revision> --name <probe-name> --destination <fresh-temp-parent> --vcs none --silent
```

Treat version-specific spelling as illustrative until `cargo generate --help` confirms it. If the resolved version lacks a required pinning or destination control, stop instead of weakening the trust gate.

## Template authoring model

### Placeholders and derived values

- Ask only for independent user choices. Derive crate-safe names, identifiers, and related values from one canonical input.
- Validate at the earliest boundary that still sees the original value; name normalization may occur before hooks.
- Keep placeholder types, defaults, choices, and regex constraints coherent. A default must itself satisfy the declared constraints.
- Treat date, username, architecture, and environment-derived values as reproducibility inputs. Allow explicit override when stable output matters.

### Rendering and file selection

- `ignore` removes a file from output; render include/exclude controls whether copied content is interpreted. Verify semantics against the installed version.
- Exclude files that contain foreign templating syntax when they need no cargo-generate substitution.
- Where both syntaxes are needed, use the template engine's documented raw/literal mechanism and test the rendered bytes.
- Rendering applies to paths as well as contents. Check collisions after case conversion and on case-insensitive filesystems.
- A magic template suffix can alter the emitted filename. Include this in parity tests for literal template files.

### Rhai hooks

Hooks are programs, not declarative substitutions.

- Review reads, writes, deletes, renames, directory traversal, environment access, date usage, and abort paths.
- Command execution is denied by default in the product protocol. Enabling it requires explicit authorization after reviewing the exact pinned hook.
- Keep hooks deterministic where possible and return actionable errors before partial output becomes indistinguishable from success.
- Test failure cleanup and partial-generation behavior; do not assume the generator rolls every mutation back.

## Template tests

Maintain a small matrix that covers each meaningful variant and the collisions most likely to corrupt output:

- defaults versus fully supplied noninteractive values;
- every conditional branch that changes file presence;
- path/name case conversion and invalid input;
- foreign brace syntax preservation;
- hook success, intentional abort, and forbidden command execution;
- fresh destination versus explicitly authorized init behavior;
- generated Cargo metadata, formatting/check gates, and expected workspace membership.

A byte-level or semantic diff against a reviewed fixture is useful for deterministic template output. Avoid snapshots that include timestamps, usernames, absolute paths, or tool-version noise unless normalized deliberately.

## Failure diagnosis

| Symptom | Check first | Do not conclude |
|---|---|---|
| Missing rendered file | condition, ignore/include/exclude, nested template | the generator randomly skipped it |
| Empty foreign expression | Liquid collision and raw/exclude policy | source framework syntax was invalid |
| Hook cannot set a value | resolved Rhai API and expected value type | arbitrary coercion is supported |
| Wrong project spelling | pre-hook name normalization | the hook saw the original spelling |
| Existing files changed | init/overwrite/destination and dirty state | noninteractive mode was read-only |
| Generated package absent from metadata | parent workspace membership/excludes and manifest validity | Cargo metadata is stale |

Stop when the template or tool version cannot be pinned, hooks cannot be reviewed, the destination cannot be isolated, or required effects exceed the user's authorization.
