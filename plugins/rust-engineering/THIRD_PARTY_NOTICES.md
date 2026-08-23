# Third-party notices

The plugin combines an original, reorganized synthesis of craft/full-stack material with adapted Leonardomso, Actionbook, Huiali, and reviewed low-level corpora. None of the reference repositories is required at plugin runtime. Exact source decisions are recorded in the provenance ledgers.

| Source | Revision | Role | License evidence in the inspected snapshot |
|---|---|---|---|
| [gurinderu/craft](https://github.com/gurinderu/craft) | `d9caf7faf36b565a59534c581fdc27516e87600a` | Action-first workflows, findings lifecycle, reviewer discipline, read-only roles, Rust process and language profiles, architecture, and Nix | The plugin manifest declares MIT; no standalone license file was present in the local snapshot. |
| [full-stack-skills/rust-skills](https://github.com/full-stack-skills/rust-skills) | `25e44452df00055ca246ec806425d99028eaae19` | Detailed Rust language, API, Cargo, workspace, dependency, interop, documentation, observability, and example coverage | Apache License 2.0 file present. |
| [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills) | `fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9` (`1.5.1`) | 265 detailed Rust rules, decision guidance, algorithms, exceptions, and examples, adapted into a context-aware rulebook overlay | MIT License file present; copyright 2025 Leonardo Maldonado. |
| [actionbook/rust-skills](https://github.com/actionbook/rust-skills) | `fa60f7931223646fb71c4586b4a6c8545016076a` | Cognitive protocol, mental models, navigation/research workflows, domain constraint maps, and unsafe/FFI review rules | Repository metadata declares MIT; the inspected snapshot has no standalone license file. |
| [huiali/rust-skills](https://github.com/huiali/rust-skills) | `947bf77509d9b421035037e983da6662d08cbb8e` | Pin, GPU, eBPF/DPDK, distributed systems, actor/async/resource/macro/learning protocols, domain constraints, and classified examples | MIT License file present; copyright 2026 李偏偏. |
| [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills) | `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608` | Reviewed debugging, profiling, Cargo/build-time, cross-target, sanitizer/Miri, async-internal, security, binary, and hardware protocols | MIT License file present; copyright 2026 chessMan. |

The 46 in-scope craft/full-stack skills are adapted into 41 decision owners, with five overlapping subjects merged under one owner; `rust-workflow`, `rust-verify`, `rust-coding-rules`, `rust-design-protocol`, and `rust-research` formed the 46-skill v0.4 catalog. Huiali v0.5 adds four distinct owners and merges the other source families into progressive references, producing 50 skills without source-profile duplication. Low-level v0.6 reviews 52 source families into those existing owners and adds no skill, hook, agent, MCP server, or runtime dependency. The resulting plugin is distributed under the repository's MIT license. This notice records provenance; it does not alter upstream licenses.

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

## Huiali MIT License

MIT License

Copyright (c) 2026 李偏偏 <huiali@hotmail.com>

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

## low-level-dev-skills MIT License

MIT License

Copyright (c) 2026 chessMan

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
