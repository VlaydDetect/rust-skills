# Specialized Rust Coroutine Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-concurrency`.
- Supporting profiles when needed: `$rust-pin`, `$rust-stable`.
- Scope retained: Stackless and stackful models, explicit state machines, suspension, scheduling, pinning, cancellation, and resource cleanup.
- Baseline correction: Old generators/generator_trait material is not current baseline. Nightly uses coroutines/coroutine_trait; prefer stable Future, streams, iterators, or an explicit state machine unless nightly is an explicit project constraint.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Coroutines vs Threads

| Property | OS thread | Coroutine |
|-----|--------|------|
| Scheduling | Kernel | User space |
| Context-switch cost | ~1 μs | ~100 ns |
| Practical count | Thousands | Hundreds of thousands |
| Stack size | 1-8 MB | A few KB |
| Preemption | Preemptive | Cooperative |


## Native Rust Generators

> Rejected Specialized Rust Rust block `3e9c1ebe143d`: Obsolete generator feature/API example was rejected; use current nightly coroutines only when required, otherwise stable Future/stream/state-machine code.


## Stackful Coroutines<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use a stackful coroutine library
use corosensei::{Coroutine, Pin, Unpin};

fn runner<'a>(start: bool, coroutine: &'a Coroutine<'_, ()>) {
    if start {
        println!("Starting coroutine");
        coroutine.run();
    }
}

fn main() {
    let coroutine = Coroutine::new(|_| {
        println!("  In coroutine - 1");
        corosensei::yield!();
        println!("  In coroutine - 2");
        corosensei::yield!();
        println!("  In coroutine - 3");
    });

    let mut pin = Pin::new(&coroutine);
    unsafe { pin.as_mut().set_running(true) };

    println!("Main: first resume");
    unsafe { pin.resume(false) }; // false = not the first resume

    println!("Main: second resume");
    unsafe { pin.resume(false) };

    println!("Main: third resume");
    unsafe { pin.resume(false) };

    println!("Main: done");
}
```


## Stackful Coroutine Design Patterns

### 1. Coroutine State Machine<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
enum CoroutineState {
    Init,
    Processing,
    Waiting,
    Done,
}

struct StatefulCoroutine {
    state: CoroutineState,
    data: Vec<u8>,
}

impl StatefulCoroutine {
    fn new() -> Self {
        Self {
            state: CoroutineState::Init,
            data: Vec::new(),
        }
    }

    fn step(&mut self) {
        match self.state {
            CoroutineState::Init => {
                println!("Initialize");
                self.state = CoroutineState::Processing;
            }
            CoroutineState::Processing => {
                println!("Processing data");
                self.state = CoroutineState::Waiting;
            }
            CoroutineState::Waiting => {
                println!("Waiting for I/O");
                self.state = CoroutineState::Done;
            }
            CoroutineState::Done => {
                println!("Already done");
            }
        }
    }
}
```

### 2. Coroutine Pool<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::Arc;
use std::thread;
use std::sync::mpsc;

struct CoroutinePool {
    workers: Vec<thread::JoinHandle<()>>,
    sender: mpsc::Sender<Job>,
}

struct Job {
    data: Vec<u8>,
    result_tx: mpsc::Sender<Result<Vec<u8>, ()>>,
}

impl CoroutinePool {
    pub fn new(size: usize) -> Self {
        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(receiver);

        let workers = (0..size)
            .map(|_| {
                let receiver = Arc::clone(&receiver);
                thread::spawn(move || {
                    while let Ok(job) = receiver.recv() {
                        // Process the job
                        let result = process_job(&job);
                        let _ = job.result_tx.send(result);
                    }
                })
            })
            .collect();

        Self { workers, sender }
    }

    pub fn submit(&self, data: Vec<u8>) -> mpsc::Receiver<Result<Vec<u8>, ()>> {
        let (result_tx, result_rx) = mpsc::channel();
        let job = Job { data, result_tx };
        self.sender.send(job).unwrap();
        result_rx
    }
}

fn process_job(job: &Job) -> Result<Vec<u8>, ()> {
    Ok(job.data.clone())
}
```


## Stackless Coroutines<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Implement stackless coroutines with async/await
async fn async_task(id: u32) -> u32 {
    println!("Task {} started", id);

    // Simulate an I/O operation
    tokio::time::sleep(std::time::Duration::from_millis(100)).await;

    println!("Task {} resumed", id);
    id * 2
}

async fn main() {
    // Run multiple coroutines concurrently
    let results = futures::future::join_all(
        (0..10).map(|i| async_task(i))
    ).await;

    println!("Results: {:?}", results);
}
```


## Context-Switching Mechanism<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Manual context switching
use std::arch::asm;

struct Context {
    rsp: u64,
    r15: u64,
    r14: u64,
    r13: u64,
    r12: u64,
    rbp: u64,
    rbx: u64,
}

impl Context {
    unsafe fn new(stack: &mut [u8]) -> Self {
        let stack_top = stack.as_mut_ptr().add(stack.len());
        let rsp = (stack_top as *mut u64).wrapping_sub(1) as u64;

        Self {
            rsp,
            r15: 0,
            r14: 0,
            r13: 0,
            r12: 0,
            rbp: 0,
            rbx: 0,
        }
    }

    unsafe fn switch(&mut self, next: &mut Context) {
        asm!(
            "push rbx",
            "push rbp",
            "push r12",
            "push r13",
            "push r14",
            "push r15",
            "mov [rdi], rsp",     // Save the current stack pointer
            "mov rsp, [rsi]",     // Switch to the new stack
            "pop r15",
            "pop r14",
            "pop r13",
            "pop r12",
            "pop rbp",
            "pop rbx",
            in("rdi") self as *mut Context,
            in("rsi") next as *mut Context,
        );
    }
}
```


## Coroutine Scheduler<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Simple coroutine scheduler
enum Task {
    Coroutine(fn(&mut Scheduler)),
    Finished,
}

struct Scheduler {
    ready: Vec<Task>,
    current: Option<Task>,
}

impl Scheduler {
    pub fn new() -> Self {
        Self {
            ready: Vec::new(),
            current: None,
        }
    }

    pub fn spawn(&mut self, task: Task) {
        self.ready.push(task);
    }

    pub fn run(&mut self) {
        while let Some(task) = self.ready.pop() {
            self.current = Some(task);
            match std::mem::replace(&mut self.ready, vec![]) {
                Task::Coroutine(f) => f(self),
                Task::Finished => continue,
            }
        }
    }
}
```


## Common Problems

| Problem | Cause | Solution |
|-----|------|-----|
| Coroutine does not run | Missing scheduler | Implement or use a scheduler |
| Stack overflow | Recursion is too deep | Use a heap-allocated stack |
| Memory leak | Task never completes | Clean up coroutines correctly |
| Deadlock | Circular wait | Avoid circular dependencies |


## Related Skills

```
rust-coroutine
    │
    ├─► rust-async → async/await implementations
    ├─► rust-concurrency → concurrency models
    └─► rust-performance → performance optimization
```
