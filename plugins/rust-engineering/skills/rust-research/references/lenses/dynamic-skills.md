# Dynamic crate dossier protocol

> Project-local dossiers are canonical; Codex and Claude wrappers are optional explicit exports. No session hook parses manifests, fetches documentation, or writes skills.

## Modes

| Mode | Mutation | Purpose |
|---|---:|---|
| `inspect` | No | Identify exact resolved packages and existing dossier freshness |
| `sync <package>` | Yes, project-local | Create or refresh one exact package dossier |
| `export <package> <host>` | Yes, user home | Install or update one thin host wrapper |
| `remove <package> <host>` | Yes, user home | Remove one validated generated wrapper |

All mutating modes require an explicit user request. Never prompt merely because a `Cargo.toml` was opened.

## Resolve effective Cargo state

Run from the selected workspace:

```text
cargo metadata --format-version 1 --locked --offline
```

Treat Cargo package IDs as opaque. From format version 1, retain:

- workspace root and workspace members;
- package ID, name, version, source, manifest path, edition, and `rust_version`;
- dependency rename, kind, target expression, optional flag, default features, and requested features;
- resolve graph nodes and resolved features;
- target names, kinds, crate types, and required features.

Do not infer the effective graph from `[dependencies]` text. This specifically covers workspace-inherited dependencies, renamed packages, target-specific tables, patches, alternate registries, path/git sources, optional features, and multiple resolved versions.

### Failure policy

- Missing or stale lockfile: stop and report the Cargo diagnostic.
- Offline cache miss: report the package/source gap; do not silently remove `--offline`.
- Networked resolution or a command that may create/change `Cargo.lock`: obtain explicit approval first.
- Multiple package IDs for the requested name: present exact versions and sources and require a package selection.
- Invalid metadata JSON: preserve the command and stderr; do not fall back to manifest grep.

## Canonical project dossier

For the selected package ID, normalize the package name to lower-case Cargo name characters and compute the first 12 hexadecimal characters of SHA-256(package ID). Store:

```text
.rust-engineering/crate-skills/<name>/<version>/<package-id-sha12>/
├── SKILL.md
├── metadata.json
└── references/source-notes.md
```

`metadata.json` records:

```text
schema_version; package_id; package_id_sha256; name; version; source;
manifest_path; aliases; dependency_kinds; target_conditions; resolved_features;
edition; rust_version; workspace_member; cargo_version; rustc_version;
cargo_lock_sha256; manifest_sha256; metadata_sha256;
evidence[{url, retrieved_at, sha256, confidence}]
```

Use paths relative to the workspace where practical. Never store registry credentials, tokens, environment dumps, or private source content in the dossier.

## Dossier content

`SKILL.md` is explicit-only guidance for the exact package version. It must distinguish:

- API facts verified from version-specific rustdoc or the package source;
- resolved project features and target conditions from Cargo metadata;
- examples that compile under the package's edition/MSRV from illustrative fragments;
- project usage discovered locally from generic crate documentation;
- unknown or unavailable documentation.

`source-notes.md` records source URLs, retrieval dates, relevant modules and types, migration or safety notes, and unresolved gaps. Prefer docs.rs for the exact version, then the declared repository and crates.io metadata. Do not substitute `/latest/` documentation for a pinned version without marking the mismatch.

## Freshness

A dossier is stale when the exact package ID disappears or any recorded Cargo lock, selected manifest, normalized metadata, or evidence-version fingerprint changes. `inspect` may report staleness but may not rewrite the dossier. `sync` writes only the selected package dossier and reports every changed project-local path.

## Host wrapper export

Wrappers contain no duplicated crate manual. They locate the active project's exact dossier and instruct the host to read it.

- Codex: `$CODEX_HOME/skills/rust-crate-<name>/`, falling back to `~/.codex/skills/` only when `CODEX_HOME` is unset.
- Claude: `~/.claude/skills/rust-crate-<name>/`.
- Wrapper policy: `allow_implicit_invocation: false` where supported.

Before export or removal:

1. Resolve the exact absolute host target.
2. Reject a target outside the expected host skill root.
3. Reject ambiguous package IDs.
4. Ask for approval because the operation writes outside the project.
5. Never use globs or recursive deletion against a parent directory.

Do not edit `.gitignore`; report the project-local dossier so the user can choose whether to commit it.

## Result

Return the exact package ID, resolved features/targets, dossier path and freshness, evidence dates, wrapper action if any, Cargo failures, and remaining gaps.
