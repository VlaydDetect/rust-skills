# `update-crate-skill` adapter

Product route: `rust-research crate <package-id> sync` against an existing dossier.

- Verify the old dossier identity and current metadata before writing.
- Never delete the old dossier first; produce the replacement successfully, then report obsolete exact paths.
- Preserve user-authored notes or report a conflict instead of overwriting them silently.
- Updating a host wrapper is a separate approved `export` operation.

If only upstream `/latest/` changed but the locked package did not, refresh evidence only when explicitly requested and keep the version mismatch visible.
