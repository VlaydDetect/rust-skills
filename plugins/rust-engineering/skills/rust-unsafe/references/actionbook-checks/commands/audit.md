# Optional unsafe and dependency audit adapter

This is an explicitly selected, potentially expensive workflow. Start with
tools already present in the repository or toolchain:

| Concern | First check | Optional escalation |
|---|---|---|
| Compiler and lint contracts | repository build, tests, Clippy | target-specific sanitizers |
| Undefined behavior | focused tests and manual proof | Miri on a supported nightly path |
| Dependency advisories | existing lockfile and project policy | `cargo audit` if installed and current data are available |
| Unsafe footprint | `rg` plus ownership review | geiger-style inventory if already installed |
| Concurrency | model and focused stress tests | specialized tools only with an explained signal model |

Do not install tools, fetch advisory databases, mutate lockfiles, or enable
nightly automatically. An unavailable checker is a coverage limitation, not a
finding. Never infer severity from an unsafe-block count alone.

For each command that runs, record the exact command, toolchain, target,
features, exit status, and whether a failure is local to the reviewed change.

