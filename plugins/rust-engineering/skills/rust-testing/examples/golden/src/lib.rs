//! Table and invariant tests for a small parser.

pub fn parse_pair(input: &str) -> Option<(i32, i32)> {
    let (left, right) = input.split_once(',')?;
    Some((left.trim().parse().ok()?, right.trim().parse().ok()?))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn representative_table() {
        for (input, expected) in [("1,2", Some((1, 2))), (" -3, 5 ", Some((-3, 5))), ("1", None), ("x,2", None)] {
            assert_eq!(parse_pair(input), expected, "input={input:?}");
        }
    }
    #[test]
    fn rendered_values_round_trip() {
        for left in -3..=3 { for right in -3..=3 { assert_eq!(parse_pair(&format!("{left},{right}")), Some((left, right))); } }
    }
}
