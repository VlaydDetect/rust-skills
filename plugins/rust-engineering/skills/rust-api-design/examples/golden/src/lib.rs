//! A narrow public surface with validated construction and borrowed input.

#[derive(Debug, PartialEq, Eq)]
pub struct Label(String);

#[derive(Debug, PartialEq, Eq)]
pub enum LabelError { Empty, TooLong }

impl Label {
    pub fn new(value: impl Into<String>) -> Result<Self, LabelError> {
        let value = value.into();
        if value.is_empty() { return Err(LabelError::Empty); }
        if value.len() > 32 { return Err(LabelError::TooLong); }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str { &self.0 }
}

pub fn has_prefix(label: &Label, prefix: &str) -> bool {
    label.as_str().starts_with(prefix)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn construction_preserves_the_invariant() {
        assert_eq!(Label::new(""), Err(LabelError::Empty));
        let label = Label::new("rust").unwrap();
        assert!(has_prefix(&label, "ru"));
    }
}
