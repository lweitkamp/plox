import pytest

from .scanner import Scanner
from .token_type import Token, TokenType


@pytest.mark.parametrize(
    "source, expected_tokens",
    [
        ("// this is a comment", [TokenType.EOF]),
        (
            "(( )){} // grouping stuff",
            [
                TokenType.LEFT_PAREN,
                TokenType.LEFT_PAREN,
                TokenType.RIGHT_PAREN,
                TokenType.RIGHT_PAREN,
                TokenType.LEFT_BRACE,
                TokenType.RIGHT_BRACE,
                TokenType.EOF,
            ],
        ),
        (
            "!*+-/=<> <= == // operators",
            [
                TokenType.BANG,
                TokenType.STAR,
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.SLASH,
                TokenType.EQUAL,
                TokenType.LESS,
                TokenType.GREATER,
                TokenType.LESS_EQUAL,
                TokenType.EQUAL_EQUAL,
                TokenType.EOF,
            ],
        ),
    ],
)
def test_scan_tokens(source: str, expected_tokens: list[TokenType]):
    token_types = [token.type for token in Scanner(source).scan_tokens()]
    assert token_types == expected_tokens


def test_scan_tokens_string(source: str = '"hello world"'):
    tokens = Scanner(source).scan_tokens()
    assert tokens[0] == Token(TokenType.STRING, '"hello world"', "hello world", 1)
    assert tokens[1] == Token(TokenType.EOF, "", None, 0)


def test_scan_tokens_number(source: str = "123.456"):
    tokens = Scanner(source).scan_tokens()
    assert tokens[0] == Token(TokenType.NUMBER, "123.456", 123.456, 1)
    assert tokens[1] == Token(TokenType.EOF, "", None, 0)


def test_scan_tokens_identifier(source: str = "myVar"):
    tokens = Scanner(source).scan_tokens()
    print(tokens)
    assert tokens[0] == Token(TokenType.IDENTIFIER, "myVar", None, 1)
    assert tokens[1] == Token(TokenType.EOF, "", None, 0)


def test_scan_tokens_keyword(source: str = "class"):
    tokens = Scanner(source).scan_tokens()
    assert tokens[0] == Token(TokenType.CLASS, "class", None, 1)
    assert tokens[1] == Token(TokenType.EOF, "", None, 0)
