from plox.ast_printer import pretty_print
from plox.expressions import Binary, Grouping, Literal, Unary
from plox.token_type import Token, TokenType


def test_pretty_print():
    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )
    result = pretty_print(expression)
    assert result == "(- 123) * (45.67)"
