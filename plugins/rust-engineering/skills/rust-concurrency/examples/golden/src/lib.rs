//! A bounded command channel with one state owner and an observed shutdown.

use std::sync::mpsc::{sync_channel, SyncSender};
use std::thread::{self, JoinHandle};

enum Command { Add(u64), Stop }

pub struct CounterWorker { tx: SyncSender<Command>, join: Option<JoinHandle<u64>> }

impl CounterWorker {
    pub fn start(capacity: usize) -> Self {
        let (tx, rx) = sync_channel(capacity);
        let join = thread::spawn(move || {
            let mut total = 0;
            while let Ok(command) = rx.recv() {
                match command { Command::Add(value) => total += value, Command::Stop => break }
            }
            total
        });
        Self { tx, join: Some(join) }
    }

    pub fn add(&self, value: u64) { self.tx.send(Command::Add(value)).unwrap(); }
    pub fn stop(mut self) -> u64 {
        self.tx.send(Command::Stop).unwrap();
        self.join.take().unwrap().join().unwrap()
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn owner_is_joined_on_shutdown() {
        let worker = super::CounterWorker::start(2);
        worker.add(2); worker.add(3);
        assert_eq!(worker.stop(), 5);
    }
}
