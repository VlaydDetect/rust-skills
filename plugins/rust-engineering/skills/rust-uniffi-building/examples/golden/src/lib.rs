//! A language-neutral boundary model before UniFFI attributes are added.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Greeting { pub text: String }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GreetingError { EmptyName }

pub fn greet(name: String) -> Result<Greeting, GreetingError> {
    if name.trim().is_empty() { return Err(GreetingError::EmptyName); }
    Ok(Greeting { text: format!("Hello, {name}!") })
}

#[cfg(test)]
mod tests {
    #[test]
    fn boundary_uses_owned_language_neutral_values() {
        assert_eq!(super::greet("Ada".into()).unwrap().text, "Hello, Ada!");
        assert_eq!(super::greet(" ".into()), Err(super::GreetingError::EmptyName));
    }
}
