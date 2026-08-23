# Rust Systems Networking Field Guide

## eBPF Branch

Record program type, hook/attach point, kernel range, target architecture, verifier limits, helper availability, map ABI, event transport, privileges, load/attach/detach ownership, and userspace consumer behavior. Keep loops and memory access bounded and verifier-legible. Treat map keys and values as an explicit cross-boundary byte contract.

## DPDK Branch

Record EAL configuration, ports, queues, descriptors, mempool ownership, mbuf headroom/tailroom, offloads, RSS mapping, sockets, cores, huge pages, and shutdown order. Every RX result, clone, external buffer, enqueue, transmit completion, drop, and error path must end with exactly one valid ownership disposition.

## Lifecycle Questions

- Who owns a packet or event at this point?
- Can the next operation retain it, clone metadata, or transfer ownership?
- What returns the resource to its pool or detaches the kernel object on failure?
- Which CPU/queue may touch it, and which synchronization or affinity rule enforces that?
- What happens on a partial burst, full TX queue, consumer lag, attach failure, or shutdown?

## Verification

- Compile host and target halves separately where applicable.
- Validate struct size, alignment, endian interpretation, and generated/bindgen ABI against the target.
- Run verifier/load tests on the supported kernel; record rejection logs.
- Exercise partial-burst and cleanup paths without hardware through dependency-free models where possible.
- Benchmark only on stated NIC/CPU/NUMA/topology and traffic distributions.

## Compiling Example

The dependency-free fixture in `../examples/golden/` models bounded packet ownership through receive, process, transmit, retry, and recycle outcomes. It intentionally avoids claiming DPDK hardware execution.

