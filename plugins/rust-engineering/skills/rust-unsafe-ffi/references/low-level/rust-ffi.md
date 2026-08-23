# Low-level Rust Ffi protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-unsafe-ffi`.
- Supporting profiles: `$rust-unsafe`, `$rust-cargo-build`.
- Retained scope: Manual and generated bindings, sys-crate layering, safe wrappers, exported C APIs, linking, ownership transfer, and error translation.
- Baseline correction: Pointer non-null and length checks do not prove validity, alignment, initialization, lifetime, allocator pairing, or exclusivity. Verify the exact ABI and target.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- target ABI and object format.
- type layout and calling convention.
- ownership/allocator pairing.
- pointer validity and lifetimes.
- panic/unwind, callbacks and thread rules.

## Decision protocol

1. Write the foreign contract independently of Rust syntax and identify each allocation and destruction owner.
2. Represent ABI-safe values and opaque handles; validate all lengths, alignments, encodings and nullability.
3. Keep raw declarations separate from the safe wrapper and expose unsafe obligations only where callers can satisfy them.
4. Contain panics/unwind and translate errors without borrowing temporary foreign storage.
5. Verify symbols/layout with the actual target toolchain and at least one real foreign consumer.

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `bindgen Options` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `Builder configuration` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `Command-line bindgen` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `bindgen.toml (configuration file)` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `cbindgen Options` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `cbindgen.toml` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `Language options` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `cc Crate for Building C Code` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `pkg-config Integration` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `Common FFI Safety Patterns` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `Null-checked constructor` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `Lifetime-bounded reference` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `Thread-safety annotations` — inspect when relevant; source `skills/rust/rust-ffi/references/bindgen-cbindgen.md`.
- `Calling C without bindgen (manual declarations)` — inspect when relevant; source `skills/rust/rust-ffi/SKILL.md`.
- `bindgen for automatic binding generation` — inspect when relevant; source `skills/rust/rust-ffi/SKILL.md`.
- `sys crate pattern` — inspect when relevant; source `skills/rust/rust-ffi/SKILL.md`.
- `Writing safe wrappers` — inspect when relevant; source `skills/rust/rust-ffi/SKILL.md`.
- `Exporting Rust to C with cbindgen` — inspect when relevant; source `skills/rust/rust-ffi/SKILL.md`.
- `Linking libraries in build.rs` — inspect when relevant; source `skills/rust/rust-ffi/SKILL.md`.

## Failure modes and guardrails

- repr(C) does not prove semantic compatibility.
- A non-null pointer may still be invalid, unaligned, stale or aliased.
- Foreign allocators and callbacks carry independent lifecycle/thread contracts.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 24 unique source block bodies: 23 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`cargo-build-scripts`](https://doc.rust-lang.org/cargo/reference/build-scripts.html) — Build-script inputs, outputs, directives, and host/target behavior; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
