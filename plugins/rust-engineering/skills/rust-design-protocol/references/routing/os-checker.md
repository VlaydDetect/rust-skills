# Safety-tool integration

> Use only tools already present in the project or explicitly approved; these names are options, not plugin dependencies.

> Integration with code-review and security-audit tools

## Available Commands

| Use Case | Command | Tools |
|----------|---------|-------|
| Diff review | `rust-review` | Repository-native checks and selected profiles |
| Dependency security | `rust-verify` + `rust-dependencies` | `cargo audit` only when installed/approved |
| Unsafe audit | `rust-review` + `rust-unsafe` | Miri when supported by the project/toolchain |
| Concurrency audit | `rust-review` + `rust-concurrency` | Tests, Loom, or specialist tools only when already configured |
| Release evidence | `rust-verify` | CI-equivalent commands defined by the repository |

## When to Suggest OS-Checker

| User Intent | Suggest |
|-------------|---------|
| Code review request | `rust-review` |
| Security concerns | `rust-review` with the relevant security/dependency profile |
| Unsafe code review | `rust-review` with `rust-unsafe` or `rust-unsafe-ffi` |
| Deadlock/race concerns | `rust-review` with `rust-concurrency` |
| Pre-release check | `rust-verify` using the repository's release gates |

## Tool Descriptions

### clippy
Standard Rust linter for code style and common mistakes.

### cargo audit
Security vulnerability scanner for dependencies.

### geiger
Counts unsafe code usage in dependencies.

### miri
Interprets MIR to detect undefined behavior.

### rudra
Memory safety bug detector.

### lockbud
Deadlock and concurrency bug detector.

## Integration Flow

```
User: "Review my unsafe code"
     │
     ▼
Router detects: unsafe + review
     │
     ├── Load: rust-unsafe or rust-unsafe-ffi (for manual review)
     │
     └── Run only the repository-supported safety evidence through rust-verify
```
