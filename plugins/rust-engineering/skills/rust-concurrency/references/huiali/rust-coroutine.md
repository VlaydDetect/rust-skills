# Huiali Coroutine Protocol

> Product adaptation of `skills/rust-coroutine/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-concurrency`.
- Supporting profiles when needed: `$rust-pin`, `$rust-stable`.
- Scope retained: Stackless and stackful models, explicit state machines, suspension, scheduling, pinning, cancellation, and resource cleanup.
- Baseline correction: Old generators/generator_trait material is not current baseline. Nightly uses coroutines/coroutine_trait; prefer stable Future, streams, iterators, or an explicit state machine unless nightly is an explicit project constraint.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## 协程 vs 线程

| 特性 | OS 线程 | 协程 |
|-----|--------|------|
| 调度 | 内核 | 用户态 |
| 切换开销 | ~1μs | ~100ns |
| 数量限制 | 数千 | 数十万 |
| 栈大小 | 1-8MB | 几 KB |
| 抢占 | 抢占式 | 协作式 |


## Rust 原生 Generator

> Rejected Huiali Rust block `3e9c1ebe143d`: Obsolete generator feature/API example was rejected; use current nightly coroutines only when required, otherwise stable Future/stream/state-machine code.


## 栈式协程 (Stackful Coroutine)

<!-- huiali-source: skills/rust-coroutine/SKILL.md#rust-block-2; sha256=c960b47abfd04c1bbf507532160e35b88674f77a7eece6f07fafed9aa9818172 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 使用 stackful 协程库
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
    unsafe { pin.resume(false) }; // false = 不是第一次

    println!("Main: second resume");
    unsafe { pin.resume(false) };

    println!("Main: third resume");
    unsafe { pin.resume(false) };

    println!("Main: done");
}
```


## 栈式协程设计模式

### 1. 协程状态机

<!-- huiali-source: skills/rust-coroutine/SKILL.md#rust-block-3; sha256=53b72677bdb616ec75cc3a977b792c37a0eb9ae6c2670b92547c90b2d61ac4fb -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

### 2. 协程池

<!-- huiali-source: skills/rust-coroutine/SKILL.md#rust-block-4; sha256=96f43ba105aaed1df372f40cba22430803297ac02c721e69cd2798f5cbc13ae8 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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
                        // 处理 job
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


## 栈无关协程 (Stackless Coroutine)

<!-- huiali-source: skills/rust-coroutine/SKILL.md#rust-block-5; sha256=40b0d6c32eb2465723617777846f49e8acb9a924245ebbebd823e5975e80a417 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 使用 async/await 实现栈无关协程
async fn async_task(id: u32) -> u32 {
    println!("Task {} started", id);

    // 模拟 I/O 操作
    tokio::time::sleep(std::time::Duration::from_millis(100)).await;

    println!("Task {} resumed", id);
    id * 2
}

async fn main() {
    // 并发执行多个协程
    let results = futures::future::join_all(
        (0..10).map(|i| async_task(i))
    ).await;

    println!("Results: {:?}", results);
}
```


## 上下文切换机制

<!-- huiali-source: skills/rust-coroutine/SKILL.md#rust-block-6; sha256=136f51af15f02b0bc07657338f097ff8c71f9a5efc93d51bee5d0c113cd7b6bb -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 手动上下文切换
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
            "mov [rdi], rsp",     // 保存当前栈指针
            "mov rsp, [rsi]",     // 切换到新栈
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


## 协程调度器

<!-- huiali-source: skills/rust-coroutine/SKILL.md#rust-block-7; sha256=ea46bd67d04562c225bcb7dec2006b0f14139a43208f053f17862f26367aaea4 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 简单协程调度器
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


## 常见问题

| 问题 | 原因 | 解决 |
|-----|------|-----|
| 协程不执行 | 缺少调度器 | 实现或使用调度器 |
| 栈溢出 | 递归太深 | 使用堆分配栈 |
| 内存泄漏 | 任务未完成 | 正确清理协程 |
| 死锁 | 循环等待 | 避免循环依赖 |


## 与其他技能关联

```
rust-coroutine
    │
    ├─► rust-async → async/await 实现
    ├─► rust-concurrency → 并发模型
    └─► rust-performance → 性能优化
```
