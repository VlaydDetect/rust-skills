# Actionbook coding-guideline crosswalk

This ledger prevents Actionbook summary statements from becoming a second competing rulebook. `canonical` points to an existing addressable rule; `profile-owned` keeps a contextual decision with its owner; `rejected-universal` preserves the source recommendation while rejecting it as a default.

## Core summary

| Source guidance | Disposition | Product owner or canonical rule |
|---|---|---|
| No `get_` prefix | canonical | `name-no-get-prefix` |
| `iter` / `iter_mut` / `into_iter` | canonical | `name-iter-convention` |
| `as_`, `to_`, `into_` conversions | canonical | `name-as-free`, `name-to-expensive`, `name-into-ownership` |
| Prefix every static with `G_` | rejected-universal | Rust/project naming; `const-vs-static` decides semantics |
| Newtypes for domain semantics | conditional | `api-newtype-safety` |
| Slice-pattern matching | profile-owned | `rust-idioms`; use when it clarifies the actual shape invariant |
| Preallocate collections | conditional | `mem-with-capacity`; only with a useful size estimate |
| Arrays instead of every fixed `Vec` | conditional | `coll-seq-choice`; consider stack size and API needs |
| Bytes instead of chars for ASCII | conditional | `rust-stdlib`; ASCII/byte semantics must be proven |
| `Cow<str>` for possible modification | conditional | `own-cow-conditional` |
| Always prefer `format!` to `+` | rejected-universal | `mem-write-over-format`, `mem-avoid-format`; readability and allocation decide |
| String `contains` warning | profile-owned | `rust-performance`; measure the actual repeated-search workload |
| Propagate with `?` | conditional | `err-question-mark` |
| Always prefer `expect` to `unwrap` | rejected-universal | `err-expect-bugs-only`, `err-no-unwrap-prod` |
| Assertions at every function entry | rejected-universal | `rust-errors` / `rust-api-design`; trust and failure contract decide |
| Descriptive lifetime names | conditional | `name-lifetime-short`; use descriptive names only for nontrivial relationships |
| Always use `try_borrow` | rejected-universal | `own-refcell-interior`; runtime borrow failure policy decides |
| Shadow values during transformation | profile-owned | `rust-idioms`; preserve clarity and diagnostics |
| Document lock ordering | profile-owned | `rust-concurrency`; required when multiple locks can overlap |
| Atomics for primitive values | rejected-universal | `conc-atomic-ordering`; protocol, not primitive type, decides |
| Choose memory ordering carefully | canonical | `conc-atomic-ordering` |
| CPU-bound work must be synchronous | corrected | Keep it off async executor threads; threads/pools/runtime blocking facilities depend on topology |
| Do not hold guards across await | canonical | `async-no-lock-await` |
| Prefer functions/generics to macros | canonical | `macro-prefer-functions` |
| Macro inputs should resemble Rust | profile-owned | `rust-macros`; syntax and diagnostics must fit the DSL |
| `lazy_static!` to `OnceLock` | conditional | `const-vs-static`; initialization/lifecycle and MSRV decide |
| `once_cell::Lazy` to `LazyLock` | conditional | `rust-stable` / `rust-stdlib`; require MSRV ≥ 1.80 and matching API needs |
| std mpsc to crossbeam | rejected-universal | `rust-concurrency`; topology, backpressure, runtime, and dependency policy decide |
| std Mutex to parking_lot | rejected-universal | `rust-concurrency`; poisoning, fairness, runtime, MSRV, size, and dependency policy decide |
| failure/error-chain to thiserror/anyhow | conditional | `rust-errors`; public error contract and dependency policy decide |
| `try!` to `?` | canonical | `err-question-mark`, subject to edition/MSRV and control-flow semantics |

## Clippy mapping

| Source lint mapping | Disposition | Product mapping |
|---|---|---|
| `unwrap_used` → expect | corrected | `err-no-unwrap-prod` plus `err-expect-bugs-only` |
| `needless_clone` → borrow | conditional | `own-borrow-over-clone`; duplication semantics and borrow shape decide |
| `await_holding_lock` | canonical | `async-no-lock-await` |
| `linkedlist` → Vec/VecDeque | conditional | `coll-seq-choice`; access/removal topology decides |
| `wildcard_imports` | profile-owned | `rust-style-clippy`; public preludes/tests/generated code may differ |
| `missing_safety_doc` | canonical | `doc-safety-section`, `lint-unsafe-doc` |
| `undocumented_unsafe_blocks` | canonical | `unsafe-safety-comment` |
| `transmute_ptr_to_ptr` | conditional | `rust-unsafe`; prefer pointer casts when semantics match |
| `large_stack_arrays` → Vec/Box | conditional | `mem-box-large-variant` and measured stack constraints |
| `too_many_arguments` → parameter struct | conditional | `rust-api-design`; group only a coherent concept or stable boundary |

## Selection

For a task, route to the owner first and load no more than eight canonical rules. Source rows marked `profile-owned`, `corrected`, or `rejected-universal` do not create new rule IDs.
