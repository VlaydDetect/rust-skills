mod parser;
pub use parser::{ParseError, parse_number};

#[cfg(test)]
mod tests { #[test] fn facade_is_stable() { assert_eq!(super::parse_number(" 42 "), Ok(42)); } }
