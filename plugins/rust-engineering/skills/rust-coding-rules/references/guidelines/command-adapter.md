# `guideline` command adapter

Design protocol's `/guideline` intent maps to the existing addressable rulebook:

- exact ID or prefix → `rust-coding-rules <id|prefix>`;
- contextual style question → select the owner profile, then at most nine rules;
- Clippy lint → `rust-style-clippy`, optionally `rust-research` for current lint documentation;
- unsafe or FFI → `rust-unsafe` or `rust-unsafe-ffi` plus the relevant safety checks.

Design protocol P/G labels do not override repository policy. Use the [crosswalk](./crosswalk.md) for every source summary item and lint mapping.
