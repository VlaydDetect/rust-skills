//! Deterministic retry and idempotency-budget models.

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Outcome {
    Applied,
    PermanentFailure,
    TransientFailure,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RetryDecision {
    Complete,
    Stop,
    Retry,
}

#[derive(Debug, Clone, Copy)]
pub struct RetryBudget {
    pub max_attempts: u32,
    pub max_elapsed_ms: u64,
}

impl RetryBudget {
    pub fn decide(self, attempt: u32, elapsed_ms: u64, outcome: Outcome) -> RetryDecision {
        match outcome {
            Outcome::Applied => RetryDecision::Complete,
            Outcome::PermanentFailure => RetryDecision::Stop,
            Outcome::TransientFailure | Outcome::Unknown
                if attempt < self.max_attempts && elapsed_ms < self.max_elapsed_ms =>
            {
                RetryDecision::Retry
            }
            Outcome::TransientFailure | Outcome::Unknown => RetryDecision::Stop,
        }
    }
}

#[derive(Debug, Default)]
pub struct IdempotencyLedger {
    results: HashMap<String, String>,
}

impl IdempotencyLedger {
    pub fn record(&mut self, key: impl Into<String>, result: impl Into<String>) -> &str {
        self.results.entry(key.into()).or_insert_with(|| result.into())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn retries_are_bounded_and_duplicate_keys_replay_the_first_result() {
        let budget = RetryBudget { max_attempts: 3, max_elapsed_ms: 500 };
        assert_eq!(budget.decide(2, 300, Outcome::Unknown), RetryDecision::Retry);
        assert_eq!(budget.decide(3, 300, Outcome::TransientFailure), RetryDecision::Stop);

        let mut ledger = IdempotencyLedger::default();
        assert_eq!(ledger.record("order-7", "accepted"), "accepted");
        assert_eq!(ledger.record("order-7", "duplicate-effect"), "accepted");
    }
}

