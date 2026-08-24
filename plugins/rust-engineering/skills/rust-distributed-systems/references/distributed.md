# Specialized Rust Distributed Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-distributed-systems`.
- Supporting profiles when needed: `$rust-architecture`, `$rust-errors`, `$rust-concurrency`.
- Scope retained: Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.
- Baseline correction: Model partial failure before selecting a protocol. Do not implement Raft, consensus, or two-phase commit from scratch for production; use mature, verified components and state their failure assumptions.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Raft Consensus Algorithm

### Core Raft Concepts

```
┌─────────────────────────────────────────────────────┐
│                   Raft cluster                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐      │
│   │ Leader  │ ◄──►│ Follower│ ◄──►│ Follower│      │
│   │  node   │     │  node   │     │  node   │      │
│   └────┬────┘     └─────────┘     └─────────┘      │
│        │                                           │
│   - Handle client requests                          │
│   - Replicate logs to followers                     │
│   - Manage heartbeats and elections                 │
└─────────────────────────────────────────────────────┘
```

### State Machine<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Raft node state
enum RaftState {
    Follower,
    Candidate,
    Leader,
}

struct RaftNode {
    state: RaftState,
    current_term: u64,
    voted_for: Option<u64>,
    log: Vec<LogEntry>,
    commit_index: usize,
    last_applied: usize,

    // Election state
    election_timeout: Duration,
    last_heartbeat: Instant,

    // Cluster configuration
    node_id: u64,
    peers: Vec<u64>,
}
```

### Log Replication<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct LogEntry {
    term: u64,
    index: usize,
    command: Vec<u8>,
}

impl RaftNode {
    // The leader replicates logs to a follower
    fn replicate_log(&mut self, peer: u64) {
        let prev_log_index = self.get_last_log_index_for(peer);
        let prev_log_term = self.get_last_log_term_for(peer);

        let entries: Vec<LogEntry> = self.log
            [(prev_log_index + 1)..]
            .to_vec();

        let rpc = AppendEntriesRequest {
            term: self.current_term,
            leader_id: self.node_id,
            prev_log_index,
            prev_log_term,
            entries,
            leader_commit: self.commit_index,
        };

        self.send_append_entries(peer, rpc);
    }
}
```

### Election Mechanism<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
impl RaftNode {
    fn start_election(&mut self) {
        self.state = RaftState::Candidate;
        self.current_term += 1;
        self.voted_for = Some(self.node_id);

        let mut votes = 1;

        // Request votes from every node
        for peer in &self.peers {
            let request = RequestVoteRequest {
                term: self.current_term,
                candidate_id: self.node_id,
                last_log_index: self.log.len(),
                last_log_term: self.get_last_log_term(),
            };

            if let Some(response) = self.send_request_vote(peer, request) {
                if response.vote_granted {
                    votes += 1;
                    if votes > self.peers.len() / 2 {
                        self.become_leader();
                        return;
                    }
                }
            }
        }

        // The election failed; return to Follower
        self.state = RaftState::Follower;
    }
}
```


## Two-Phase Commit (2PC)

### Coordinator<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct TwoPhaseCommitCoordinator {
    transaction_id: u128,
    participants: Vec<Participant>,
    state: TwoPCState,
}

enum TwoPCState {
    Init,
    WaitingPrepare,
    WaitingCommit,
    Committed,
    Aborted,
}

impl TwoPhaseCommitCoordinator {
    pub fn start_transaction(&mut self) {
        self.state = TwoPCState::WaitingPrepare;

        // Phase one: send prepare
        for participant in &self.participants {
            participant.send(PrepareMessage {
                transaction_id: self.transaction_id,
            });
        }
    }

    pub fn handle_prepare_response(&mut self, response: PrepareResponse) {
        if response.vote == Vote::Abort {
            self.abort();
        } else if self.all_prepared() {
            self.state = TwoPCState::WaitingCommit;

            // Phase two: send commit
            for participant in &self.participants {
                participant.send(CommitMessage {
                    transaction_id: self.transaction_id,
                });
            }
        }
    }
}
```

### Participant<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct Participant {
    transaction_manager: TransactionManager,
    state: ParticipantState,
}

enum ParticipantState {
    Init,
    Prepared,
    Committed,
    Aborted,
}

impl Participant {
    pub fn handle_prepare(&mut self, msg: PrepareMessage) {
        // Execute the local transaction operation
        let result = self.transaction_manager.execute();

        match result {
            Ok(_) => {
                self.state = ParticipantState::Prepared;
                self.send(PrepareResponse {
                    vote: Vote::Commit,
                    ..msg
                });
            }
            Err(_) => {
                self.send(PrepareResponse {
                    vote: Vote::Abort,
                    ..msg
                });
            }
        }
    }
}
```

### 2PC Problems and Solutions

| Problem | Cause | Solution |
|-----|------|---------|
| Blocking | Coordinator failure | Timeouts and a backup coordinator |
| Single point of failure | Coordinator dependency | Distributed coordinator (etcd/ZooKeeper) |
| Performance | Multiple network round trips | Batch commits and tuned timeouts |


## Distributed Consistency Models<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Eventual consistency
trait EventuallyConsistent {
    fn put(&self, key: &str, value: &str);
    fn get(&self, key: &str) -> Option<String>;
}

// Strong consistency (linearizability)
trait Linearizable {
    fn put(&self, key: &str, value: &str) -> Result<()>;
    fn get(&self, key: &str) -> Result<String>;
}

// Sequential consistency
trait SequentialConsistent {
    fn put(&self, key: &str, value: &str);
    fn get(&self, key: &str) -> Vec<String>; // Return historical versions
}
```


## Distributed ID Generation<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Snowflake algorithm
struct SnowflakeGenerator {
    worker_id: u64,
    datacenter_id: u64,
    sequence: u64,
    last_timestamp: u64,
}

impl SnowflakeGenerator {
    pub fn generate(&mut self) -> u64 {
        let timestamp = current_timestamp();

        if timestamp == self.last_timestamp {
            self.sequence = (self.sequence + 1) & 0xFFF; // 12 bits
            if self.sequence == 0 {
                // Wait for the next millisecond
                while current_timestamp() == timestamp {}
            }
        } else {
            self.sequence = 0;
        }

        self.last_timestamp = timestamp;

        (timestamp << 22)       // 41-bit timestamp
        | (self.datacenter_id << 17)  // 5-bit data-center ID
        | (self.worker_id << 12)      // 5-bit worker-node ID
        | self.sequence               // 12-bit sequence number
    }
}
```


## Distributed Locks<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::{Arc, atomic::{AtomicU64, Ordering}};
use std::time::Duration;

struct DistributedLock {
    key: String,
    ttl: Duration,
    owner: u64,
}

impl DistributedLock {
    // Distributed lock backed by etcd
    pub async fn try_lock(&self, owner: u64, ttl: Duration) -> Result<bool, LockError> {
        let response = etcd_client.put(
            format!("/lock/{}", self.key),
            owner.to_string(),
            Some(PutOptions::new().with_ttl(ttl))
        ).await?;

        // Acquire the lock when this is the first setter
        Ok(response.prev_key().is_none())
    }

    pub async fn unlock(&self, owner: u64) -> Result<(), LockError> {
        // Only the lock holder may release it
        let response = etcd_client.get(format!("/lock/{}", self.key)).await?;

        if response.value() == owner.to_string() {
            etcd_client.delete(format!("/lock/{}", self.key)).await?;
        }

        Ok(())
    }
}
```


## Distributed Event Sourcing<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Event-sourcing pattern
trait EventSourced {
    type Event;

    fn apply(&mut self, event: Self::Event);
    fn snapshot(&self) -> Self;
}

struct Aggregate {
    version: u64,
    events: Vec<Event>,
    state: AggregateState,
}

impl Aggregate {
    pub fn new() -> Self {
        Self {
            version: 0,
            events: Vec::new(),
            state: AggregateState::Init,
        }
    }

    pub fn apply_event(&mut self, event: Event) {
        self.state.transition(&event);
        self.events.push(event);
        self.version += 1;
    }

    pub fn snapshot(&self) -> EventSourcedSnapshot {
        EventSourcedSnapshot {
            version: self.version,
            state: self.state.clone(),
        }
    }
}
```


## Common Problems

| Problem | Cause | Solution |
|-----|------|-----|
| Split brain | Network partition | Quorums and term management |
| Livelock | Conflicting election timeouts | Randomized timeouts |
| Data inconsistency | Concurrent writes | Conflict-resolution strategy |
| Performance bottleneck | Single write point | Sharding and replication |


## Related Skills

```
rust-distributed
    │
    ├─► rust-concurrency → concurrency control
    ├─► rust-performance → performance optimization
    └─► rust-async → asynchronous communication
```
