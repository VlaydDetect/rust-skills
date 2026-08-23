# Huiali Actor Protocol

> Product adaptation of `skills/rust-actor/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-concurrency`.
- Supporting profiles when needed: `$rust-architecture`, `$rust-errors`.
- Scope retained: Actor ownership, bounded mailboxes, request-response, supervision, restart policy, lifecycle, and backpressure.
- Baseline correction: The actor model is conditional, and Actix is not a default. Select actors only when isolated mutable state and message-driven failure boundaries fit the problem.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Solution Patterns

### Pattern 1: Basic Actor Implementation

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-1; sha256=2d12279aa7a384647bd1d9977c7486eb64feb0e228a930e4e5a53023d378c64f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::sync::mpsc::{channel, Sender, Receiver};
use std::collections::HashMap;

// Actor trait
trait Actor: Send + 'static {
    type Message: Send + 'static;
    type Error: std::error::Error;

    fn receive(&mut self, ctx: &mut Context<Self>, msg: Self::Message);
}

// Actor context
struct Context<A: Actor> {
    mailbox: Receiver<A::Message>,
    sender: Sender<A::Message>,
    state: ActorState,
    supervisor: Option<SupervisorAddr>,
}

#[derive(Debug, Clone)]
enum ActorState {
    Starting,
    Running,
    Restarting,
    Stopping,
    Stopped,
}

// Address handle for sending messages
#[derive(Clone)]
struct Addr<A: Actor> {
    sender: Sender<A::Message>,
}

impl<A: Actor> Addr<A> {
    pub async fn send(&self, msg: A::Message) -> Result<(), SendError> {
        self.sender.send(msg).await
            .map_err(|_| SendError::Disconnected)
    }
}

// Example actor
struct CounterActor {
    count: usize,
}

#[derive(Debug)]
enum CounterMessage {
    Increment,
    Decrement,
    GetCount(Sender<usize>),
}

impl Actor for CounterActor {
    type Message = CounterMessage;
    type Error = std::io::Error;

    fn receive(&mut self, ctx: &mut Context<Self>, msg: Self::Message) {
        match msg {
            CounterMessage::Increment => {
                self.count += 1;
            }
            CounterMessage::Decrement => {
                self.count = self.count.saturating_sub(1);
            }
            CounterMessage::GetCount(reply) => {
                let _ = reply.try_send(self.count);
            }
        }
    }
}
```

### Pattern 2: Request-Response Pattern

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-2; sha256=4fc8ef46c2ae8644f26a4667e24d3a418644d14f325c96d06a9b9e288a75a2e8 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::sync::oneshot;
use std::time::Duration;

// Request wrapper with response channel
struct Request<M, R> {
    payload: M,
    response: oneshot::Sender<R>,
}

// Synchronous request with timeout
async fn request<A: Actor, R>(
    actor: &Addr<A>,
    msg: A::Message,
    timeout: Duration,
) -> Result<R, RequestError> {
    let (tx, rx) = oneshot::channel();

    let request = Request {
        payload: msg,
        response: tx,
    };

    actor.send(request).await
        .map_err(|_| RequestError::SendFailed)?;

    tokio::time::timeout(timeout, rx).await
        .map_err(|_| RequestError::Timeout)?
        .map_err(|_| RequestError::Canceled)
}

// Usage example
async fn example_request_response() {
    let (tx, rx) = oneshot::channel();

    let addr = counter_actor.start();
    addr.send(CounterMessage::GetCount(tx)).await.unwrap();

    let count = rx.await.unwrap();
    println!("Count: {}", count);
}
```

### Pattern 3: Supervision Tree

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-3; sha256=0dc00c42244842d92ab885f50259edbf6373282d844e9efc431934a8617f5424 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::collections::HashMap;

#[derive(Debug, Clone)]
enum SupervisionStrategy {
    OneForOne,    // Only restart failed child
    AllForOne,    // Restart all children if one fails
    RestForOne,   // Restart failed child and all after it
}

struct Supervisor {
    children: HashMap<ChildId, Child>,
    strategy: SupervisionStrategy,
    max_restarts: u32,
    window: Duration,
}

struct Child {
    id: ChildId,
    addr: Box<dyn std::any::Any + Send>,
    restart_count: u32,
    last_restart: Option<Instant>,
    spec: ChildSpec,
}

struct ChildSpec {
    factory: Box<dyn Fn() -> Box<dyn std::any::Any + Send>>,
    restart_strategy: RestartStrategy,
}

#[derive(Debug, Clone)]
enum RestartStrategy {
    Permanent,   // Always restart
    Temporary,   // Never restart
    Transient,   // Restart only on abnormal exit
}

impl Supervisor {
    fn new(strategy: SupervisionStrategy, max_restarts: u32, window: Duration) -> Self {
        Self {
            children: HashMap::new(),
            strategy,
            max_restarts,
            window,
        }
    }

    async fn handle_child_error(&mut self, child_id: ChildId, error: &dyn std::error::Error) {
        log::warn!("Child {} failed: {}", child_id, error);

        match self.strategy {
            SupervisionStrategy::OneForOne => {
                self.restart_child(child_id).await;
            }
            SupervisionStrategy::AllForOne => {
                for id in self.children.keys().cloned().collect::<Vec<_>>() {
                    self.stop_child(id).await;
                }
                for id in self.children.keys().cloned().collect::<Vec<_>>() {
                    self.restart_child(id).await;
                }
            }
            SupervisionStrategy::RestForOne => {
                let ids: Vec<_> = self.children.keys()
                    .filter(|&&id| id >= child_id)
                    .cloned()
                    .collect();

                for id in ids {
                    self.stop_child(id).await;
                    self.restart_child(id).await;
                }
            }
        }
    }

    async fn restart_child(&mut self, child_id: ChildId) -> bool {
        if let Some(child) = self.children.get_mut(&child_id) {
            child.restart_count += 1;

            // Check restart rate limit
            if self.should_give_up(child) {
                log::error!("Child {} exceeded max restarts, giving up", child_id);
                self.stop_child(child_id).await;
                return false;
            }

            child.last_restart = Some(Instant::now());
            log::info!("Restarting child {}", child_id);

            // Factory creates new instance
            let new_instance = (child.spec.factory)();
            child.addr = new_instance;

            true
        } else {
            false
        }
    }

    fn should_give_up(&self, child: &Child) -> bool {
        if child.restart_count > self.max_restarts {
            if let Some(last_restart) = child.last_restart {
                if last_restart.elapsed() < self.window {
                    return true;
                }
            }
        }
        false
    }

    async fn stop_child(&mut self, child_id: ChildId) {
        if let Some(child) = self.children.remove(&child_id) {
            log::info!("Stopping child {}", child_id);
            // Send stop signal
        }
    }
}
```

### Pattern 4: Deadlock Prevention with Bounded Mailboxes

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-4; sha256=00d4cf78ffb89b7a0154b6f478a3b94365c4ac8ee2ab3e7cc6497fc433732abc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::sync::mpsc;

struct BoundedMailbox<A: Actor> {
    receiver: mpsc::Receiver<A::Message>,
    sender: mpsc::Sender<A::Message>,
    capacity: usize,
}

impl<A: Actor> BoundedMailbox<A> {
    fn new(capacity: usize) -> Self {
        let (sender, receiver) = mpsc::channel(capacity);
        Self {
            receiver,
            sender,
            capacity,
        }
    }

    fn capacity(&self) -> usize {
        self.capacity
    }

    async fn send_with_backpressure(&self, msg: A::Message) -> Result<(), SendError> {
        // Will wait if mailbox is full (backpressure)
        self.sender.send(msg).await
            .map_err(|_| SendError::Disconnected)
    }

    fn try_send(&self, msg: A::Message) -> Result<(), TrySendError<A::Message>> {
        // Returns immediately if mailbox is full
        self.sender.try_send(msg)
            .map_err(|e| match e {
                mpsc::error::TrySendError::Full(msg) => TrySendError::Full(msg),
                mpsc::error::TrySendError::Closed(msg) => TrySendError::Disconnected(msg),
            })
    }
}

// Usage
async fn example_bounded_mailbox() {
    let mailbox: BoundedMailbox<CounterActor> = BoundedMailbox::new(100);

    // This will block if mailbox is full
    mailbox.send_with_backpressure(CounterMessage::Increment).await.unwrap();

    // This returns error immediately if full
    match mailbox.try_send(CounterMessage::Increment) {
        Ok(_) => println!("Sent"),
        Err(TrySendError::Full(_)) => println!("Mailbox full"),
        Err(TrySendError::Disconnected(_)) => println!("Actor stopped"),
    }
}
```

### Pattern 5: Actor Lifecycle Management

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-5; sha256=8853a5586389b95bf709e98e0b768116cd68f06d28ee0a1a26ef8e931f7e90d7 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
trait LifecycleHandler: Actor {
    fn pre_start(&mut self, ctx: &mut Context<Self>) {
        // Initialize resources
        log::info!("Actor starting");
    }

    fn post_start(&mut self, ctx: &mut Context<Self>) {
        // Start timers, establish connections
        log::info!("Actor started");
    }

    fn pre_restart(&mut self, ctx: &mut Context<Self>, error: &dyn std::error::Error) {
        // Clean up resources before restart
        log::warn!("Actor restarting due to: {}", error);
    }

    fn post_restart(&mut self, ctx: &mut Context<Self>) {
        // Reinitialize after restart
        log::info!("Actor restarted");
    }

    fn post_stop(&mut self) {
        // Save state, close connections
        log::info!("Actor stopped");
    }
}

// Example with lifecycle hooks
struct DatabaseActor {
    connection: Option<DatabaseConnection>,
}

impl LifecycleHandler for DatabaseActor {
    fn pre_start(&mut self, ctx: &mut Context<Self>) {
        // Establish database connection
        self.connection = Some(DatabaseConnection::new());
    }

    fn pre_restart(&mut self, ctx: &mut Context<Self>, error: &dyn std::error::Error) {
        // Close existing connection
        if let Some(conn) = self.connection.take() {
            conn.close();
        }
    }

    fn post_stop(&mut self) {
        // Ensure connection is closed
        if let Some(conn) = self.connection.take() {
            conn.close();
        }
    }
}
```


## Actor vs Thread Model

| Feature | Thread Model | Actor Model |
|---------|-------------|-------------|
| State sharing | Shared memory + locks | Isolated, message passing |
| Deadlock risk | High (lock ordering) | Low (message queues) |
| Scalability | Limited by thread count | Millions of actors possible |
| Fault handling | Manual | Supervision trees |
| Debugging | Hard (race conditions) | Easier (message sequence) |
| Memory | Shared | Isolated per actor |


## Workflow

### Step 1: Design Actor Hierarchy

```
Design questions:
  → What state needs isolation? Each isolated state = 1 actor
  → What operations need sequential processing? Group in same actor
  → What can fail independently? Separate actors with supervision
  → What needs to scale? Use actor pool pattern
```

### Step 2: Choose Messaging Pattern

```
Message patterns:
  → Fire-and-forget: Async send, no response
  → Request-response: Oneshot channel for reply
  → Streaming: Channel for multiple responses
  → Broadcast: Multiple recipients
```

### Step 3: Set Up Supervision

```
Supervision strategy:
  → OneForOne: Independent actors (default choice)
  → AllForOne: Tightly coupled actors needing consistent state
  → RestForOne: Sequential dependencies

Restart policy:
  → Permanent: Critical actors (always restart)
  → Temporary: One-time tasks (never restart)
  → Transient: Restart on errors only
```


## Review Checklist

When implementing actor systems:

- [ ] Each actor has clear single responsibility
- [ ] Mailboxes have bounded capacity (prevent memory leaks)
- [ ] Message types are Send + 'static
- [ ] No shared mutable state between actors
- [ ] Supervision strategy appropriate for error handling
- [ ] Actor lifecycle properly managed (cleanup in post_stop)
- [ ] No circular message dependencies (deadlock risk)
- [ ] Timeouts on request-response patterns
- [ ] Monitoring tracks mailbox size and message latency
- [ ] Backpressure handled when mailbox is full


## Verification Commands

```bash
# Run tests with actor system
cargo test --test actor_tests

# Check for deadlocks with timeout
cargo test --test deadlock_tests -- --test-threads=1 --nocapture

# Profile actor message throughput
cargo bench --bench actor_bench

# Check memory usage under load
cargo run --release --bin load_test

# Monitor actor lifecycle events
RUST_LOG=debug cargo run
```


## Common Pitfalls

### 1. Circular Message Dependencies (Deadlock)

**Symptom**: Actors waiting for each other's responses

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-6; sha256=fb8fc8069837de472bf9a2fe4d3496c2071148885a2bc1b5af5567681c1b0575 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: Actor A waits for Actor B, Actor B waits for Actor A
async fn actor_a_handler(&mut self, msg: Message) {
    let response = self.actor_b.request(msg).await;  // Blocks
    // Actor A is blocked, can't process Actor B's request
}

async fn actor_b_handler(&mut self, msg: Message) {
    let response = self.actor_a.request(msg).await;  // Blocks
    // Deadlock!
}

// ✅ Good: Use timeouts and avoid circular dependencies
async fn actor_a_handler(&mut self, msg: Message) {
    match tokio::time::timeout(
        Duration::from_secs(5),
        self.actor_b.request(msg)
    ).await {
        Ok(response) => { /* handle response */ }
        Err(_) => { /* timeout, handle error */ }
    }
}

// Better: redesign to avoid circular dependency
```

### 2. Unbounded Mailbox Growth

**Symptom**: Memory grows unbounded, OOM crashes

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-7; sha256=b35390866420eb9facc17b812eb81c6a88b4dec2198f4d364f5fee92341c4966 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: unbounded channel
let (tx, rx) = mpsc::unbounded_channel();

// Slow consumer can't keep up, mailbox grows forever

// ✅ Good: bounded channel with backpressure
let (tx, rx) = mpsc::channel(100);  // Max 100 messages

// Sender will wait when mailbox is full (backpressure)
tx.send(msg).await?;
```

### 3. Blocking Operations in Actor

**Symptom**: Actor becomes unresponsive, messages pile up

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-8; sha256=f77428b539fc73d93ae70c1d7a62f8424b5a8e271c09be674523702ebea91415 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: blocking I/O in actor
impl Actor for MyActor {
    fn receive(&mut self, ctx: &mut Context<Self>, msg: Self::Message) {
        // Blocks entire actor!
        let data = std::fs::read("file.txt").unwrap();
        // Other messages can't be processed
    }
}

// ✅ Good: use async I/O or spawn blocking task
impl Actor for MyActor {
    fn receive(&mut self, ctx: &mut Context<Self>, msg: Self::Message) {
        let addr = ctx.address();
        tokio::spawn(async move {
            // Runs in separate task
            let data = tokio::fs::read("file.txt").await.unwrap();
            addr.send(ProcessData(data)).await;
        });
        // Actor continues processing messages
    }
}
```


## Actix Framework Example

<!-- huiali-source: skills/rust-actor/SKILL.md#rust-block-9; sha256=b45a03f40799a851e7c40b9d1befed04deecf00e1e78be23718d2f0ab929c38e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use actix::{Actor, Handler, Message, Context};

struct MyActor {
    counter: usize,
}

impl Actor for MyActor {
    type Context = Context<Self>;

    fn started(&mut self, _ctx: &mut Self::Context) {
        println!("Actor started");
    }

    fn stopped(&mut self, _ctx: &mut Self::Context) {
        println!("Actor stopped");
    }
}

#[derive(Message)]
#[rtype(result = "usize")]
struct Increment;

impl Handler<Increment> for MyActor {
    type Result = usize;

    fn handle(&mut self, _msg: Increment, _ctx: &mut Self::Context) -> Self::Result {
        self.counter += 1;
        self.counter
    }
}

// Usage
#[actix_rt::main]
async fn main() {
    let actor = MyActor { counter: 0 }.start();
    let result = actor.send(Increment).await.unwrap();
    println!("Counter: {}", result);
}
```


## Related Skills

- **rust-concurrency** - Concurrency primitives and patterns
- **rust-async** - Async message handling
- **rust-error** - Error propagation in actor systems
- **rust-channel** - Channel-based communication
- **rust-performance** - Actor system optimization

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_EN.md` example 1

<!-- huiali-source: skills/rust-actor/SKILL_EN.md#rust-block-1; sha256=c904862d99dd5beab2674b344f79d9160d56c16379ff4a68ce0df37caa4677c3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
trait Actor: Send + 'static {
    type Message: Send + 'static;
    type Error: std::error::Error + Send + Sync + 'static;

    fn receive(&mut self, ctx: &mut Context<Self::Message>, msg: Self::Message);
}

struct Context<M> {
    // mailbox/runtime-specific fields
    _marker: std::marker::PhantomData<M>,
}

enum ActorState {
    Starting,
    Running,
    Restarting,
    Stopping,
    Stopped,
}
```

### `SKILL_EN.md` example 2

<!-- huiali-source: skills/rust-actor/SKILL_EN.md#rust-block-2; sha256=4f40d474a136d31742d26e82fa4252bf7e4f0e925ce1679eab685f62f9cca910 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// fire-and-forget
fn send_async<A: Actor>(addr: &Addr<A>, msg: A::Message) {
    let _ = addr.try_send(msg);
}

// request-response with timeout
async fn request_with_timeout<A, R>(
    addr: &Addr<A>,
    msg: A::Message,
    timeout: std::time::Duration,
) -> Result<R, RequestError>
where
    A: Actor,
    A: Handler<A::Message, Result = R>,
{
    tokio::time::timeout(timeout, addr.send(msg))
        .await
        .map_err(|_| RequestError::Timeout)?
        .map_err(|_| RequestError::MailboxClosed)
}
```

### `SKILL_EN.md` example 3

<!-- huiali-source: skills/rust-actor/SKILL_EN.md#rust-block-3; sha256=988535d6db98814588ecf95c83c2e2a5640f21be1aa52d104ae2b394b5ec76ab -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
enum SendError {
    Timeout,
    MailboxFull,
    MailboxClosed,
}
```

### `SKILL_EN.md` example 4

<!-- huiali-source: skills/rust-actor/SKILL_EN.md#rust-block-4; sha256=e63e1a7ceb0652c4e2df7c879b5b910c8b89208a64bb233a055aaad2149b55e4 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
enum SupervisionStrategy {
    OneForOne,
    AllForOne,
    RestForOne,
}
```

### `SKILL_EN.md` example 5

<!-- huiali-source: skills/rust-actor/SKILL_EN.md#rust-block-5; sha256=97cfef9c8c0fda96ea6035581642a971f84825ba38089d7e7bf142aef67abf6b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct UserActor {
    id: u64,
    online: bool,
    followers: std::collections::HashSet<u64>,
}

impl UserActor {
    fn snapshot(&self) -> UserSnapshot {
        UserSnapshot {
            id: self.id,
            online: self.online,
            followers_count: self.followers.len(),
        }
    }
}
```

### `SKILL_EN.md` example 6

<!-- huiali-source: skills/rust-actor/SKILL_EN.md#rust-block-6; sha256=5a31e8f1a8e5680a9821a1ea84782c9eb89e319a3fbfb2e9a34b82e6b75271b8 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use actix::{Actor, Context, Handler, Message};

struct CounterActor {
    counter: usize,
}

impl Actor for CounterActor {
    type Context = Context<Self>;
}

#[derive(Message)]
#[rtype(result = "usize")]
struct Increment;

impl Handler<Increment> for CounterActor {
    type Result = usize;

    fn handle(&mut self, _msg: Increment, _ctx: &mut Self::Context) -> Self::Result {
        self.counter += 1;
        self.counter
    }
}
```

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-actor/SKILL_ZH.md#rust-block-1; sha256=1f8a24c994477756a1b4f24460c69509319e299103e0b290e48309dbfef09541 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Actor 基础 trait
trait Actor: Send + 'static {
    type Message: Send + 'static;
    type Error: std::error::Error;

    fn receive(&mut self, ctx: &mut Context<Self::Message>, msg: Self::Message);
}

// Actor 上下文
struct Context<A: Actor> {
    mailbox: Receiver<A::Message>,
    sender: Sender<A::Message>,
    state: ActorState,
    supervisor: Option<SupervisorAddr>,
}

enum ActorState {
    Starting,
    Running,
    Restarting,
    Stopping,
    Stopped,
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-actor/SKILL_ZH.md#rust-block-2; sha256=3675e69867c8f8a9b9fa50a581a52b2ae12542f956206fc36da1e7fdacb64be5 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 同步消息
fn sync_request<A: Actor, R>(
    actor: &Addr<A>,
    msg: A::Message,
    timeout: Duration,
) -> Result<R, A::Error> {
    let (tx, rx) = channel();
    let request = Request {
        payload: msg,
        response: tx,
    };

    actor.send(request)?;

    rx.recv_timeout(timeout)?
}

// 异步消息
fn async_send<A: Actor>(actor: &Addr<A>, msg: A::Message) {
    actor.send(msg);
}

// 消息信封
enum Envelope<A: Actor> {
    Async(A::Message),
    Request {
        payload: A::Message,
        response: Sender<Result<A::Response, A::Error>>,
    },
    Signal(ActorSignal),
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-actor/SKILL_ZH.md#rust-block-3; sha256=4a5f78366090dff30cc65f27adf55e0d1e64c84f2423663373ecd1b23c4cfd6d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 1. 避免循环等待：使用唯一消息顺序
enum GlobalMessage {
    // 按固定顺序排列
    UserMsg(UserMessage),
    SystemMsg(SystemMessage),
    InternalMsg(InternalMessage),
}

// 2. 超时机制
fn send_with_timeout<A: Actor, M: Send + 'static>(
    addr: &Addr<A>,
    msg: M,
    timeout: Duration,
) -> Result<(), SendError<M>> {
    let (tx, rx) = channel();

    addr.send(AsyncWrapper { msg, reply_to: tx });

    rx.recv_timeout(timeout)
        .map(|_| ())
        .map_err(|_| SendError::Timeout)
}

// 3. 限制邮箱大小（背压）
struct BoundedMailbox<A: Actor> {
    receiver: Receiver<A::Message>,
    sender: Sender<A::Message>,
    capacity: usize,
}

impl<A: Actor> Mailbox for BoundedMailbox<A> {
    fn capacity(&self) -> usize {
        self.capacity
    }
}
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-actor/SKILL_ZH.md#rust-block-4; sha256=f469f7f6372ff5f7f496aab2ad7952320f5434793e920f2e1a0a9baa6388b902 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Supervision 策略
enum SupervisionStrategy {
    OneForOne,    // 只重启出错的子 actor
    AllForOne,    // 一个出错，全部重启
    RestForOne,   // 出错的和之后的重启
}

struct Supervisor {
    children: HashMap<ChildId, Child>,
    strategy: SupervisionStrategy,
    max_restarts: u32,
    window: Duration,
}

impl Supervisor {
    fn handle_child_error(&mut self, child_id: ChildId, error: &dyn std::error::Error) {
        let child = self.children.get_mut(&child_id).unwrap();
        child.restart_count += 1;

        if self.should_restart(child_id) {
            self.restart_child(child_id);
        } else {
            self.stop_child(child_id);
        }
    }

    fn should_restart(&self, child_id: ChildId) -> bool {
        let child = &self.children[&child_id];
        child.restart_count <= self.max_restarts
    }
}
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-actor/SKILL_ZH.md#rust-block-5; sha256=a3ba40b1bd235f04c1242e9597bdece03562fab0b56b0949a5fe5a5af16d0e01 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Actor 内部状态
struct UserActor {
    id: UserId,
    session: Option<Session>,
    message_history: Vec<Message>,
    followers: HashSet<UserId>,
}

impl Actor for UserActor {
    type Message = UserMessage;

    fn receive(&mut self, ctx: &mut Context<Self::Message>, msg: Self::Message) {
        match msg {
            UserMessage::Login(session) => {
                self.session = Some(session);
            }
            UserMessage::Post(content) => {
                if let Some(session) = &self.session {
                    self.message_history.push(Message {
                        content,
                        timestamp: Utc::now(),
                        user: session.user_id,
                    });
                }
            }
            UserMessage::Follow(target_id) => {
                self.followers.insert(target_id);
            }
        }
    }
}

// 状态快照
impl UserActor {
    fn snapshot(&self) -> UserSnapshot {
        UserSnapshot {
            id: self.id,
            message_count: self.message_history.len(),
            followers_count: self.followers.len(),
            is_online: self.session.is_some(),
        }
    }
}
```

### `SKILL_ZH.md` example 6

<!-- huiali-source: skills/rust-actor/SKILL_ZH.md#rust-block-6; sha256=6874a3f98f35690cd8d77d4b004346ff0c42de4ce4dea9e41f200b8ac4d8f584 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 生命周期事件
enum LifecycleEvent {
    PreStart,
    PostStart,
    PreRestart,
    PostRestart,
    PostStop,
}

trait LifecycleHandler: Actor {
    fn pre_start(&mut self, ctx: &mut Context<Self::Message>) {
        // 初始化资源
    }

    fn post_start(&mut self, ctx: &mut Context<Self::Message>) {
        // 启动定时器、连接等
    }

    fn pre_restart(&mut self, ctx: &mut Context<Self::Message>, error: &dyn std::error::Error) {
        // 清理资源
    }

    fn post_stop(&mut self) {
        // 保存状态、关闭连接
    }
}
```

### `SKILL_ZH.md` example 7

<!-- huiali-source: skills/rust-actor/SKILL_ZH.md#rust-block-7; sha256=3a1782c4adbdf5997d06747d1890417f4c6fd0dffc8cb964306d09686b47ef04 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Actix Web Actor
use actix::{Actor, Handler, Message, Context};

struct MyActor {
    counter: usize,
}

impl Actor for MyActor {
    type Context = Context<Self>;

    fn started(&mut self, _ctx: &mut Self::Context) {
        println!("Actor started");
    }
}

#[derive(Message)]
#[rtype(result = "usize")]
struct Increment;

impl Handler<Increment> for MyActor {
    type Result = usize;

    fn handle(&mut self, msg: Increment, _ctx: &mut Self::Context) -> Self::Result {
        self.counter += 1;
        self.counter
    }
}

// 使用
let actor = MyActor { counter: 0 }.start();
let result = actor.send(Increment).await?;
```
