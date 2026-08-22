//! A bounded-cardinality event contract independent of one telemetry crate.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Outcome { Success, InvalidInput, Unavailable }

#[derive(Debug, PartialEq, Eq)]
pub struct OperationEvent<'a> {
    pub operation: &'static str,
    pub outcome: Outcome,
    pub request_id: &'a str,
    pub elapsed_ms: u64,
}

pub fn metric_label(outcome: Outcome) -> &'static str {
    match outcome { Outcome::Success => "success", Outcome::InvalidInput => "invalid_input", Outcome::Unavailable => "unavailable" }
}

#[cfg(test)]
mod tests {
    #[test]
    fn labels_are_closed_and_bounded() {
        assert_eq!(super::metric_label(super::Outcome::InvalidInput), "invalid_input");
    }
}
