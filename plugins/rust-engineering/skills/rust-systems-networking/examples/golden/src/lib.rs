//! A bounded packet token whose pool capacity is restored on every exit path.

use std::cell::Cell;

#[derive(Debug)]
pub struct PacketPool {
    capacity: usize,
    available: Cell<usize>,
}

impl PacketPool {
    pub fn new(capacity: usize) -> Self {
        Self { capacity, available: Cell::new(capacity) }
    }

    pub fn receive(&self, bytes: usize) -> Option<Packet<'_>> {
        let available = self.available.get();
        if available == 0 {
            return None;
        }
        self.available.set(available - 1);
        Some(Packet { pool: self, bytes, processed: false })
    }

    pub fn available(&self) -> usize {
        self.available.get()
    }
}

#[derive(Debug)]
pub struct Packet<'a> {
    pool: &'a PacketPool,
    bytes: usize,
    processed: bool,
}

impl Packet<'_> {
    pub fn process(&mut self) {
        self.processed = true;
    }

    pub fn transmit(self, queue_capacity: usize) -> Result<usize, Self> {
        if self.processed && queue_capacity > 0 {
            Ok(self.bytes)
        } else {
            Err(self)
        }
    }
}

impl Drop for Packet<'_> {
    fn drop(&mut self) {
        let next = self.pool.available.get() + 1;
        debug_assert!(next <= self.pool.capacity);
        self.pool.available.set(next);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn success_and_backpressure_both_recycle_the_packet() {
        let pool = PacketPool::new(1);
        let mut packet = pool.receive(128).unwrap();
        assert_eq!(pool.available(), 0);
        packet.process();
        let packet = packet.transmit(0).unwrap_err();
        assert_eq!(packet.transmit(1).unwrap(), 128);
        assert_eq!(pool.available(), 1);
    }
}
