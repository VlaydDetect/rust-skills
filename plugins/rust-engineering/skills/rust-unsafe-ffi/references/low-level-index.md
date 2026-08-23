# Low-level references for `rust-unsafe-ffi`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`abi-and-calling-conventions`](low-level/abi-and-calling-conventions.md) — primary; System V, AAPCS, RISC-V, stack frames, registers, variadics, unwind, and compiler-output verification.
- [`binary-hardening`](../../rust-cargo-build/references/low-level/binary-hardening.md) — supporting; Hardening-property inspection, compiler/linker mitigation families, control-flow integrity, platform mechanisms, and residual attack surface.
- [`binutils`](../../debugging/references/low-level/binutils.md) — supporting; Archive, strip, objcopy, address translation, demangling, strings, headers, disassembly, and cross-tool selection.
- [`dynamic-linking`](../../rust-cargo-build/references/low-level/dynamic-linking.md) — supporting; Shared-library identity, SONAME, RPATH/RUNPATH, loader search, plugins, interposition, visibility, and loader errors.
- [`elf-inspection`](../../debugging/references/low-level/elf-inspection.md) — supporting; ELF identity, sections, symbols, dynamic dependencies, disassembly, hardening properties, size, and build IDs.
- [`io-uring`](../../rust-concurrency/references/low-level/io-uring.md) — supporting; Submission/completion ownership, operation lifetimes, registered resources, multishot operations, cancellation, zero-copy, and fallback I/O.
- [`linker-scripts`](../../rust-cargo-build/references/low-level/linker-scripts.md) — supporting; Memory regions, sections, VMA/LMA, startup initialization, placement, KEEP/ALIGN/PROVIDE, symbols, and map-based verification.
- [`linkers-lto`](../../rust-cargo-build/references/low-level/linkers-lto.md) — supporting; Linker selection, argument ordering, LTO modes, dead-code elimination, visibility, map files, and link-failure diagnosis.
- [`rust-cross`](../../rust-cargo-build/references/low-level/rust-cross.md) — supporting; Host/target separation, target support tiers, linker and runner configuration, native libraries, containers, emulators, and deployment validation.
- [`rust-ffi`](low-level/rust-ffi.md) — primary; Manual and generated bindings, sys-crate layering, safe wrappers, exported C APIs, linking, ownership transfer, and error translation.
- [`sanitizers`](../../rust-unsafe/references/low-level/sanitizers.md) — supporting; ASan, TSan, MSan, hardware-assisted modes, suppression and report concepts, and native dependency instrumentation.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.
