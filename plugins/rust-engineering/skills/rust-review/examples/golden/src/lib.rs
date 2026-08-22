//! Review fixture: boundary behavior is explicit and regression-testable.

#[derive(Debug, PartialEq, Eq)]
pub enum WindowError { Reversed }

pub fn inclusive_width(start: u32, end: u32) -> Result<u32, WindowError> {
    end.checked_sub(start)
        .and_then(|width| width.checked_add(1))
        .ok_or(WindowError::Reversed)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn checks_both_boundaries() {
        assert_eq!(inclusive_width(4, 4), Ok(1));
        assert_eq!(inclusive_width(5, 4), Err(WindowError::Reversed));
        assert_eq!(inclusive_width(0, u32::MAX), Err(WindowError::Reversed));
    }
}
