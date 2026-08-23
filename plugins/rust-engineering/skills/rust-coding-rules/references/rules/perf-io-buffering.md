# perf-io-buffering

> Wrap `Read`/`Write` in `BufReader`/`BufWriter` for many small operations## Decision

Consider this rule only after its prerequisites are satisfied: Wrap `Read`/`Write` in `BufReader`/`BufWriter` for many small operations.

## Apply When

Apply when a controlled benchmark or profile identifies the operation and the proposed pattern preserves the correctness contract, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the change is based on source aesthetics, a synthetic non-representative workload, or an unapproved faster-but-weaker primitive. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Define metric and baseline, locate the bottleneck, test one pattern, compare repeated samples, and reject noise-level wins.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Lower runtime cost may increase code, dependency, memory, security, build-time, determinism, or maintenance cost.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `bytes`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Record exact workload, toolchain, target, features, profile, environment, before/after distributions, and functional equivalence.

## Why It Matters

Every unbuffered read or write to a file or socket is a syscall. Calling `read()` byte-by-byte or line-by-line without buffering can issue millions of syscalls per second, each with kernel-transition overhead that dwarfs the actual data transfer. `BufReader` and `BufWriter` batch those operations into large internal buffer reads and writes, cutting syscall count by orders of magnitude. This is one of the highest-impact, lowest-effort performance fixes available for IO-heavy code.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::fs::File;
use std::io::{Read, Write};

// Every read call goes to the OS — catastrophic for line-by-line processing
fn count_lines_slow(path: &str) -> std::io::Result<usize> {
    let file = File::open(path)?;
    let mut count = 0usize;
    let mut byte = [0u8; 1];
    loop {
        match file.read(&mut byte) { // one syscall per byte
            Ok(0) => break,
            Ok(_) => {
                if byte[0] == b'\n' {
                    count += 1;
                }
            }
            Err(e) => return Err(e),
        }
    }
    Ok(count)
}

// Writing many small records without buffering — each write is a syscall
fn write_records_slow(path: &str, records: &[String]) -> std::io::Result<()> {
    let mut file = File::create(path)?;
    for record in records {
        file.write_all(record.as_bytes())?; // one syscall per record
        file.write_all(b"\n")?;             // another syscall
    }
    Ok(())
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};

// BufReader batches OS reads; lines() iterates safely without extra allocation per line
fn count_lines_fast(path: &str) -> io::Result<usize> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut count = 0usize;
    for line in reader.lines() {
        line?; // propagate IO errors
        count += 1;
    }
    Ok(count)
}

// BufWriter batches writes; explicit flush() surfaces errors that drop() would swallow
fn write_records_fast(path: &str, records: &[String]) -> io::Result<()> {
    let file = File::create(path)?;
    let mut writer = BufWriter::new(file);
    for record in records {
        writer.write_all(record.as_bytes())?;
        writer.write_all(b"\n")?;
    }
    writer.flush()?; // MUST flush explicitly — drop() swallows flush errors
    Ok(())
}

// Custom buffer size when the default 8 KiB isn't optimal
fn process_large_file(path: &str) -> io::Result<()> {
    let file = File::open(path)?;
    let reader = BufReader::with_capacity(64 * 1024, file); // 64 KiB buffer
    for line in reader.lines() {
        let _line = line?;
        // process...
    }
    Ok(())
}
```

## Key Points

- `BufWriter::flush()?` must be called explicitly. When a `BufWriter` is dropped, it attempts to flush, but any resulting error is **silently discarded**. Always flush before the writer goes out of scope.
- The default buffer size for both `BufReader` and `BufWriter` is 8 KiB. For sequential reads of large files, a larger buffer (32–512 KiB) can improve throughput by reducing the number of `read` syscalls further.
- `BufReader` implements `BufRead`, which provides `lines()`, `read_line()`, and `read_until()` — use these instead of reading bytes manually.
- Network streams (`TcpStream`, etc.) benefit equally from buffering, since each `write` on an unbuffered stream may send a tiny TCP segment.
- If you wrap a type that is already internally buffered (e.g., `tokio::io::BufWriter` in async code), adding another layer is redundant.

## Related Rules
- [mem-with-capacity](mem-with-capacity.md) - pre-size buffers when the final size is known
- [perf-profile-first](perf-profile-first.md) - confirm IO is the bottleneck before tuning
