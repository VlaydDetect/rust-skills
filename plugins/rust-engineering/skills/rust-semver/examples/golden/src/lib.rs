//! A stable facade keeps the public path independent of implementation layout.

mod implementation {
    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub struct Token(pub(crate) u32);
    impl Token { pub(crate) fn value(self) -> u32 { self.0 } }
}

pub use implementation::Token;

impl Token {
    pub fn new(value: u32) -> Self { Self(value) }
    pub fn get(self) -> u32 { self.value() }
}

#[cfg(test)]
mod tests {
    #[test]
    fn public_path_and_behavior_are_explicit() {
        let token = super::Token::new(7);
        assert_eq!(token.get(), 7);
    }
}
