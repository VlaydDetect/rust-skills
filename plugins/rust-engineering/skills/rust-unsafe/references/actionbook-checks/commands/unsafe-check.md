# Unsafe check workflow adapter

Use this adapter when a prompt equivalent to `/unsafe-check [path]` asks for a
focused static review.

1. Resolve the requested file or smallest relevant module. Do not scan the
   whole repository unless the user asks for it.
2. Enumerate unsafe blocks, unsafe functions or traits, foreign declarations,
   exported symbols, raw-pointer dereferences, union field reads, manual auto
   traits, `MaybeUninit`, layout assumptions, and raw handles.
3. For each operation, establish its local contract before selecting rule IDs
   from the [internal index](../index.md) or
   [FFI index](../../../../rust-unsafe-ffi/references/actionbook-checks/index.md).
4. Trace constructors and callers with `rg`, language-server navigation, or a
   fresh Graphify graph when available. Pattern matching alone cannot prove
   pointer validity, aliasing, lifetime, or ownership.
5. Report evidence-backed findings by severity, location, violated invariant,
   canonical rule ID, and the smallest sound repair. Separate confirmed defects
   from questions and tool limitations.

Do not auto-install Miri, sanitizers, cargo-geiger, or other tools. Offer or run
them only when available, applicable, and authorized by the selected workflow.
