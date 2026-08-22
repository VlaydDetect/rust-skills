# Third-party notices

The plugin is an original, reorganized synthesis informed by two local comparison corpora. Their files are not required as plugin runtime content and were not copied wholesale. Detailed source-skill and supporting-file coverage, including pinned hashes for the inspected snapshots, is recorded in [`provenance/source-coverage.json`](provenance/source-coverage.json).

| Source | Revision | Role | License evidence in the inspected snapshot |
|---|---|---|---|
| [gurinderu/craft](https://github.com/gurinderu/craft) | `d9caf7faf36b565a59534c581fdc27516e87600a` | Action-first workflows, findings lifecycle, reviewer discipline, read-only roles, Rust process and language profiles, architecture, and Nix | The plugin manifest declares MIT; no standalone license file was present in the local snapshot. |
| [full-stack-skills/rust-skills](https://github.com/full-stack-skills/rust-skills) | `25e44452df00055ca246ec806425d99028eaae19` | Detailed Rust language, API, Cargo, workspace, dependency, interop, documentation, observability, and example coverage | Apache License 2.0 file present. |

The 46 in-scope source skills are adapted into 41 decision owners, with five overlapping subjects merged under one owner; `rust-workflow` and `rust-verify` complete the 43-skill product catalog. Fifteen vertical domain specializations are explicitly marked out of scope in the coverage file. The resulting `rust-engineering` plugin is distributed under the repository's MIT license. This notice records provenance; it does not alter either upstream license.
