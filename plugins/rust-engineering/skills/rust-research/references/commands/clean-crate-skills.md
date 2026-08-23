# `clean-crate-skills` adapter

Product route: explicit `rust-research crate <package-id> remove <host>` for generated wrappers.

1. Resolve the exact wrapper directory beneath the expected Codex or Claude skill root.
2. Verify it is a generated `rust-crate-<name>` wrapper for the requested package.
3. Ask before deleting the exact directory outside the project.
4. Never use a wildcard, parent-directory recursive delete, or “clean all”.

Project-local dossiers are ordinary project data and are not removed by this adapter unless the user names the exact dossier path separately.
