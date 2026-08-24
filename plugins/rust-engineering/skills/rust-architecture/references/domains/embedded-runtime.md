# Specialized Rust Embedded Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-architecture`.
- Supporting profiles when needed: `$rust-unsafe`, `$rust-concurrency`.
- Scope retained: no_std constraints, HAL ownership, interrupts, bounded memory, timing, peripherals, power, and deterministic cleanup.
- Baseline correction: Target MCU, HAL, allocator, interrupt model, and timing budget are required evidence. Do not infer heapless data structures, executors, or hardware topology.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## no_std Fundamentals<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#![no_std]
// std, alloc, and test are unavailable

use core::panic::PanicMessage;

// A panic handler is required
#[panic_handler]
fn panic(info: &PanicMessage) -> ! {
    loop {}
}

// Optional: define a global allocator
#[global_allocator]
static ALLOC: some_allocator::Allocator = some_allocator::Allocator;
```

### Available Modules

| Module | Purpose |
|-----|------|
| `core` | Basic language features |
| `alloc` | Heap allocation; requires an allocator |
| `compiler_builtins` | Compiler built-in functions |


## embedded-hal<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use embedded_hal as hal;
use hal::digital::v2::OutputPin;

// Abstract hardware access
fn blink_led<L: OutputPin>(mut led: L) -> ! {
    loop {
        led.set_high().unwrap();
        delay_ms(1000);
        led.set_low().unwrap();
        delay_ms(1000);
    }
}
```

### Common Traits

| Trait | Operation |
|-------|------|
| `OutputPin` | Set the output high or low |
| `InputPin` | Read a pin |
| `SpiBus` | SPI communication |
| `I2c` | I2C communication |
| `Serial` | Serial communication |


## Interrupt Handling<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#![no_std]
#![feature(abi_vectorcall)]

use cortex_m::interrupt::{free, Mutex};
use cortex_m::peripheral::NVIC;

// Shared state
static MY_DEVICE: Mutex<Cell<Option<MyDevice>>> = Mutex::new(None);

#[interrupt]
fn TIM2() {
    free(|cs| {
        let device = MY_DEVICE.borrow(cs).take();
        if let Some(dev) = device {
            // Handle the interrupt
            dev.handle();
            MY_DEVICE.borrow(cs).set(Some(dev));
        }
    });
}

// Enable the interrupt
fn enable_interrupt(nvic: &mut NVIC, irq: interrupt::TIM2) {
    nvic.enable(irq);
}
```


## Memory Management

### Stack Size

```toml
[profile.dev]
panic = "abort"  # Reduce binary size

[profile.release]
lto = true
opt-level = "z"  # Minimize size
```

### Avoid Dynamic Allocation<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use a stack array instead of Vec
let buffer: [u8; 256] = [0; 256];

// Or use a fixed-size ring buffer
struct RingBuffer {
    data: [u8; 256],
    write_idx: usize,
    read_idx: usize,
}
```


## Peripheral-Access Pattern<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Register mapping
const GPIOA_BASE: *const u32 = 0x4002_0000 as *const u32;
const GPIOA_ODR: *const u32 = (GPIOA_BASE + 0x14) as *const u32;

// Safe abstraction
mod gpioa {
    use super::*;

    pub fn set_high() {
        unsafe {
            GPIOA_ODR.write_volatile(1 << 5);
        }
    }
}
```


## Common Problems

| Problem | Cause | Solution |
|-----|------|-----|
| Infinite panic loop | No panic handler | Implement #[panic_handler] |
| Stack overflow | Nested interrupts or large local variables | Increase the stack or reduce local variables |
| Memory corruption | Raw-pointer operations | Use a safe abstraction |
| Program does not run | Linker-script problem | Check the startup code |
| Peripheral does not respond | Clock is not enabled | Configure RCC first |


## Resource-Constrained Techniques

| Technique | Effect |
|-----|------|
| `opt-level = "z"` | Minimize size |
| `lto = true` | Link-time optimization |
| `panic = "abort"` | Remove unwinding |
| `codegen-units = 1` | Better optimization |
| Avoid alloc | Use the stack or static arrays |


## Project-Configuration Example

```toml
[package]
name = "my-firmware"
version = "0.1.0"
edition = "2024"

[dependencies]
cortex-m = "0.7"
cortex-m-rt = "0.7"
embedded-hal = "1.0"
nb = "1.0"

[profile.dev]
panic = "abort"

[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
```


## WebAssembly Multithreading

### SharedArrayBuffer<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Configure Cross-Origin-Opener-Policy on the server
// before the browser can use SharedArrayBuffer

// wasm-bindgen configuration
[dependencies]
wasm-bindgen = { version = "0.2", features = ["enable-threads"] }

// Use atomic memory ordering
use std::sync::atomic::{AtomicUsize, Ordering};

static COUNTER: AtomicUsize = AtomicUsize::new(0);

#[wasm_bindgen]
pub fn increment_counter() -> usize {
    COUNTER.fetch_add(1, Ordering::SeqCst)
}

#[wasm_bindgen]
pub fn get_counter() -> usize {
    COUNTER.load(Ordering::SeqCst)
}
```

### Atomics and Memory Ordering<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::atomic::{AtomicI32, Ordering};

// Performance and visibility tradeoffs among memory orderings
#[wasm_bindgen]
pub fn atomic_demo() {
    let atom = AtomicI32::new(0);

    // Strongest guarantees and slowest
    atom.store(1, Ordering::SeqCst);

    // Release semantics (producer)
    atom.store(2, Ordering::Release);

    // Acquire semantics (consumer)
    let val = atom.load(Ordering::Acquire);

    // Relaxed semantics are fastest, but operations may be reordered
    atom.store(3, Ordering::Relaxed);
    let val = atom.load(Ordering::Relaxed);
}
```

### Thread-Local Storage (TLS)<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// WASM thread-local storage
use std::cell::RefCell;

thread_local! {
    static THREAD_ID: RefCell<u32> = RefCell::new(0);
}

#[wasm_bindgen]
pub fn set_thread_id(id: u32) {
    THREAD_ID.with(|tid| {
        *tid.borrow_mut() = id;
    });
}

#[wasm_bindgen]
pub fn get_thread_id() -> u32 {
    THREAD_ID.with(|tid| *tid.borrow())
}
```


## RISC-V Embedded Development

### Basic Setup<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Cargo.toml
[package]
name = "riscv-firmware"
version = "0.1.0"
edition = "2024"

[dependencies]
riscv = "0.10"
embedded-hal = "1.0"

[profile.release]
opt-level = "z"
lto = true
```

### Interrupts and Exceptions<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// RISC-V interrupt handling
#![no_std]

use riscv::register::{
    mie::MIE,
    mstatus::MSTATUS,
    mip::MIP,
};

/// Enable machine interrupts
pub fn enable_interrupt() {
    // Enable external, timer, and software interrupts
    unsafe {
        MIE::set_mext();
        MIE::set_mtimer();
        MIE::set_msip();

        // Enable interrupts globally
        MSTATUS::set_mie();
    }
}

/// Disable all interrupts
pub fn disable_interrupt() {
    unsafe {
        MSTATUS::clear_mie();
    }
}
```

### Memory Barriers<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// RISC-V memory barriers
use riscv::asm;

/// Data-memory barrier: ensure all memory accesses complete
fn data_memory_barrier() {
    unsafe {
        asm!("fence iorw, iorw");
    }
}

/// Instruction barrier: ensure instruction-stream updates are visible
fn instruction_barrier() {
    unsafe {
        asm!("fence i, i");
    }
}
```

### Atomic Operations<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use the riscv::atomic module
use riscv::asm::atomic;

fn atomic_add(dst: &mut usize, val: usize) {
    unsafe {
        // Use the amoadd.w instruction
        atomic::amoadd(dst as *mut usize, val);
    }
}

fn compare_and_swap(ptr: &mut usize, old: usize, new: usize) -> bool {
    unsafe {
        // Use the amoswap.w instruction
        let current = atomic::amoswap(ptr as *mut usize, new);
        current == old
    }
}
```

### Multicore Synchronization<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// RISC-V inter-processor interrupt (IPI)
const M_SOFT_INT: *mut u32 = 0x3FF0_FFF0 as *mut u32;

fn send_soft_interrupt(core_id: u32) {
    unsafe {
        // Set the software-interrupt bit
        M_SOFT_INT.write_volatile(1 << core_id);
    }
}

fn clear_soft_interrupt(core_id: u32) {
    unsafe {
        M_SOFT_INT.write_volatile(0);
    }
}
```

### RISC-V Privilege Levels<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Check the RISC-V privilege level
use riscv::register::{mstatus, misa};

fn check_privilege_level() -> u8 {
    // Read the current privilege level
    // 0 = User, 1 = Supervisor, 2 = Hypervisor, 3 = Machine
    (mstatus::read().bits() >> 11) & 0b11
}

fn is_machine_mode() -> bool {
    check_privilege_level() == 3
}

/// Get the available ISA extensions
fn get_isa_extensions() -> String {
    let misa = misa::read();
    format!("{:?}", misa)
}
```


## RISC-V Performance Optimization

| Optimization target | Method |
|-------|------|
| Memory access | Use unaligned-access instructions when supported |
| Atomic operations | Use A-extension instructions |
| Multiplication and division | Use M-extension instructions |
| Vector operations | Use the V extension (RV64V) |
| Compressed instructions | Use the C extension to reduce code size |
