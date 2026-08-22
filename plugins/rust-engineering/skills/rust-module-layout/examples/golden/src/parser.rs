mod lexer;

#[derive(Debug, PartialEq, Eq)]
pub enum ParseError { Empty, Invalid }

pub fn parse_number(input: &str) -> Result<i64, ParseError> {
    let token = lexer::one_token(input).ok_or(ParseError::Empty)?;
    token.parse().map_err(|_| ParseError::Invalid)
}
