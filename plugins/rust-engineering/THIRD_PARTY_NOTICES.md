# Third-party notices

The plugin combines an original, reorganized synthesis of two comparison corpora with an adapted copy of the Leonardomso Rust rule corpus. None of the reference repositories is required at plugin runtime. Detailed craft/full-stack coverage is recorded in [`provenance/source-coverage.json`](provenance/source-coverage.json); all 265 Leonardomso source IDs, hashes, aliases, owners, and target files are recorded in [`provenance/rule-coverage.json`](provenance/rule-coverage.json).

| Source | Revision | Role | License evidence in the inspected snapshot |
|---|---|---|---|
| [gurinderu/craft](https://github.com/gurinderu/craft) | `d9caf7faf36b565a59534c581fdc27516e87600a` | Action-first workflows, findings lifecycle, reviewer discipline, read-only roles, Rust process and language profiles, architecture, and Nix | The plugin manifest declares MIT; no standalone license file was present in the local snapshot. |
| [full-stack-skills/rust-skills](https://github.com/full-stack-skills/rust-skills) | `25e44452df00055ca246ec806425d99028eaae19` | Detailed Rust language, API, Cargo, workspace, dependency, interop, documentation, observability, and example coverage | Apache License 2.0 file present. |
| [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills) | `fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9` (`1.5.1`) | 265 detailed Rust rules, decision guidance, algorithms, exceptions, and examples, adapted into a context-aware rulebook overlay | MIT License file present; copyright 2025 Leonardo Maldonado. |

The 46 in-scope craft/full-stack skills are adapted into 41 decision owners, with five overlapping subjects merged under one owner; `rust-workflow`, `rust-verify`, and `rust-coding-rules` complete the 44-skill product catalog. Fifteen vertical domain specializations are explicitly marked out of scope in the coverage file. The resulting `rust-engineering` plugin is distributed under the repository's MIT license. This notice records provenance; it does not alter upstream licenses.

## Leonardomso MIT License

MIT License

Copyright (c) 2025 Leonardo Maldonado

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
