# Specialized Rust Dpdk Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-systems-networking`.
- Supporting profiles when needed: `$rust-unsafe`, `$rust-performance`.
- Scope retained: Mempools, mbuf ownership, queues, burst processing, RSS, NUMA placement, affinity, and bounded packet-resource lifecycles.
- Baseline correction: Keep the execution and ownership model binding-neutral. Never infer a Rust binding, NIC topology, queue count, huge-page layout, or core placement without project and hardware evidence.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## DPDK vs the Kernel Network Stack

| Property | Kernel network stack | DPDK |
|-----|----------|------|
| Context switching | A switch for each packet | Poll mode with no switches |
| Memory copies | Multiple copies | Zero-copy |
| Interrupts | Frequent interrupts | Polling (poll mode driver) |
| Latency | Higher | Microsecond-scale |
| Throughput | Tens of thousands of PPS | Millions of PPS |
| CPU utilization | Lower, but with overhead | High, but efficient |


## Core Components<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Core DPDK structure
struct DpdkContext {
    memory_pool: Mempool,        // Memory pool
    ports: Vec<Port>,            // Network-interface ports
    rx_queues: Vec<RxQueue>,     // Receive queues
    tx_queues: Vec<TxQueue>,     // Transmit queues
    cpu_cores: Vec<Core>,        // CPU-core assignment
}

struct Port {
    port_id: u16,
    mac_addr: [u8; 6],
    link_speed: u32,
    max_queues: u16,
}

struct Mempool {
    name: String,
    buffer_size: usize,
    cache_size: usize,
    total_buffers: u32,
}
```


## Memory-Pool Management<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Create a DPDK memory pool
fn create_mempool() -> Result<Mempool, DpdkError> {
    let mempool = unsafe {
        rte_mempool_create(
            b"packet_pool\0".as_ptr() as *const c_char,
            NUM_BUFFERS as u32,        // Number of buffers
            BUFFER_SIZE as u16,        // Size of each buffer
            CACHE_SIZE as u32,         // CPU cache size
            0,                         // Private-data size
            Some(rte_pktmbuf_pool_init), // Initialization function
            std::ptr::null(),          // Initialization argument
            Some(rte_pktmbuf_init),    // Object-initialization function
            std::ptr::null(),          // Object argument
            rte_socket_id() as i32,    // Socket where memory resides
            0,                         // Flags
        )
    };

    if mempool.is_null() {
        Err(DpdkError::MempoolCreateFailed)
    } else {
        Ok(Mempool { inner: mempool })
    }
}

// Allocate a buffer
fn alloc_mbuf(mempool: &Mempool) -> Option<*mut rte_mbuf> {
    unsafe {
        let mbuf = rte_pktmbuf_alloc(mempool.inner);
        if mbuf.is_null() {
            None
        } else {
            Some(mbuf)
        }
    }
}
```


## Zero-Copy Receive<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Receive packets without copying
fn process_packets(
    port_id: u16,
    queue_id: u16,
    bufs: &mut [*mut rte_mbuf; MAX_BURST_SIZE],
) -> usize {
    let num_received = unsafe {
        rte_eth_rx_burst(
            port_id,
            queue_id,
            bufs.as_mut_ptr(),
            MAX_BURST_SIZE as u16,
        )
    };

    // Process the mbuf directly without copying
    for i in 0..num_received {
        let mbuf = bufs[i];

        // Access the data without copying
        let data_ptr = unsafe {
            rte_pktmbuf_mtod(mbuf, *const u8)
        };
        let data_len = unsafe {
            rte_pktmbuf_pkt_len(mbuf)
        };

        // Process the packet
        process_packet(data_ptr, data_len);

        // Return the mbuf to the memory pool
        unsafe {
            rte_pktmbuf_free(mbuf);
        }
    }

    num_received
}
```


## Batched Transmission<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Transmit packets in a batch
fn transmit_packets(
    port_id: u16,
    queue_id: u16,
    packets: &[Packet],
) -> usize {
    let mut mbufs: Vec<*mut rte_mbuf> = packets
        .iter()
        .map(|p| p.to_mbuf())
        .collect();

    let sent = unsafe {
        rte_eth_tx_burst(
            port_id,
            queue_id,
            mbufs.as_mut_ptr(),
            mbufs.len() as u16,
        )
    };

    // Free mbufs that were not sent
    for i in sent..mbufs.len() {
        unsafe {
            rte_pktmbuf_free(mbufs[i]);
        }
    }

    sent
}
```


## RSS Load Balancing<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Configure RSS (Receive Side Scaling)
fn configure_rss(port_id: u16) -> Result<(), DpdkError> {
    let mut port_info: rte_eth_dev_info = unsafe { std::mem::zeroed() };
    unsafe {
        rte_eth_dev_info_get(port_id, &mut port_info);
    }

    // Configure RSS hashing
    let mut rss_conf: rte_eth_rss_conf = unsafe { std::mem::zeroed() };
    rss_conf.rss_key_len = 40;
    rss_conf.rss_hf = RTE_ETH_RSS_TCP | RTE_ETH_RSS_UDP | RTE_ETH_RSS_IPV4;

    unsafe {
        let ret = rte_eth_dev_rss_hash_conf_update(
            port_id,
            &rss_conf,
        );
        if ret < 0 {
            return Err(DpdkError::RssConfigFailed);
        }
    }

    Ok(())
}

// Select a queue from the hash value
fn get_queue_by_hash(hash: u32, num_queues: u16) -> u16 {
    // Use simple modulo distribution
    (hash % num_queues as u32) as u16
}
```


## Multi-Queue Configuration<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Configure multiple queues
fn configure_multi_queue(port_id: u16, num_queues: u16) -> Result<(), DpdkError> {
    let mut port_conf: rte_eth_conf = unsafe { std::mem::zeroed() };
    port_conf.rxmode.split_hdr_size = 0;
    port_conf.rxmode.mq_mode = rte_eth_mq_mode::ETH_MQ_RX_RSS;
    port_conf.txmode.mq_mode = rte_eth_mq_mode::ETH_MQ_TX_NONE;

    // Configure RX queues
    let mut rx_conf: rte_eth_rxconf = unsafe { std::mem::zeroed() };
    rx_conf.rx_free_thresh = 32;
    rx_conf.rx_drop_en = 0;

    // Configure TX queues
    let mut tx_conf: rte_eth_txconf = unsafe { std::mem::zeroed() };
    tx_conf.tx_free_thresh = 32;

    // Allocate RX queues
    for queue in 0..num_queues {
        unsafe {
            let ret = rte_eth_rx_queue_setup(
                port_id,
                queue,
                1024, // Queue depth
                rte_socket_id() as u32,
                &rx_conf,
                mempool.inner,
            );
            if ret < 0 {
                return Err(DpdkError::QueueSetupFailed);
            }
        }
    }

    // Allocate TX queues
    for queue in 0..num_queues {
        unsafe {
            let ret = rte_eth_tx_queue_setup(
                port_id,
                queue,
                1024,
                rte_socket_id() as u32,
                &tx_conf,
            );
            if ret < 0 {
                return Err(DpdkError::QueueSetupFailed);
            }
        }
    }

    Ok(())
}
```


## CPU Affinity<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::os::raw::c_int;
use std::thread;

fn set_cpu_affinity(core_id: u32) -> Result<(), DpdkError> {
    let mut cpuset: cpu_set_t = unsafe { std::mem::zeroed() };

    unsafe {
        CPU_SET(core_id as usize, &mut cpuset);

        let ret = pthread_setaffinity_np(
            pthread_self(),
            std::mem::size_of::<cpu_set_t>(),
            &cpuset,
        );

        if ret != 0 {
            return Err(DpdkError::AffinitySetFailed);
        }
    }

    Ok(())
}

// Assign a dedicated core to each RX queue
fn allocate_cores_for_queues(num_queues: u16) {
    for queue in 0..num_queues {
        thread::spawn(move || {
            set_cpu_affinity(queue as u32).unwrap();
            process_queue(queue);
        });
    }
}
```


## Performance Optimization

| Optimization target | Method |
|-------|------|
| Memory alignment | Align to a 64-byte cache line |
| Lock-free queues | Use SPSC queues |
| Batching | Batch receives and transmits to reduce system calls |
| CPU affinity | Bind cores to reduce context switches |
| Hugepages | Use 2 MB or 1 GB pages to reduce TLB misses |


## Related Skills

```
rust-dpdk
    │
    ├─► rust-performance → performance optimization
    ├─► rust-embedded → no_std environments
    └─► rust-concurrency → concurrency models
```
