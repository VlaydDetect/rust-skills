# Design protocol command adapters

Claude-specific slash commands are not duplicated as a second command system. Their workflows map to skill modes:

- [crate-info](./commands/crate-info.md)
- [sync-crate-skills](./commands/sync-crate-skills.md)
- [update-crate-skill](./commands/update-crate-skill.md)
- [clean-crate-skills](./commands/clean-crate-skills.md)
- [rust-features](./commands/rust-features.md)
- [docs](./commands/docs.md)
- [rust-daily](./commands/rust-daily.md)

Invoke the corresponding `rust-research` mode in Codex or Claude. Mutation and approval boundaries in the canonical research/dossier protocols remain authoritative.
