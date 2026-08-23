# Clippy Lint → Rule Mapping

| Clippy Lint | Category | Fix |
|-------------|----------|-----|
| `unwrap_used` | Error | Propagate/handle recoverable errors; use `expect` only for a documented bug invariant |
| `needless_clone` | Perf | Use reference |
| `await_holding_lock` | Async | Scope guard before await |
| `linkedlist` | Perf | Evaluate access/removal topology; usually compare Vec/VecDeque |
| `wildcard_imports` | Style | Explicit imports |
| `missing_safety_doc` | Safety | Add `# Safety` doc |
| `undocumented_unsafe_blocks` | Safety | Add `// SAFETY:` |
| `transmute_ptr_to_ptr` | Safety | Use `pointer::cast()` |
| `large_stack_arrays` | Mem | Measure stack limits; consider heap/static storage when warranted |
| `too_many_arguments` | Design | Group parameters only when they form a coherent concept or stable boundary |

For unsafe-related lints, route to `rust-unsafe` or `rust-unsafe-ffi` and the relevant safety checks.
