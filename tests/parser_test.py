from plox.expressions import Binary, Grouping, Literal, Unary
from plox.parser import Parser
from plox.token_type import Token, TokenType


def make_token(type, lexeme, literal=None):
    # simple factory: (type, lexeme, literal, line)
    return Token(type, lexeme, literal, 1)


def parse(tokens):
    return Parser(tokens).parse()


def test_parse_number_literal():
    tokens = [make_token(TokenType.NUMBER, "123", 123)]
    node = parse(tokens)
    assert isinstance(node, Literal)
    assert node.value == 123


def test_parse_string_literal():
    tokens = [make_token(TokenType.STRING, '"hi"', "hi")]
    node = parse(tokens)
    assert isinstance(node, Literal)
    assert node.value == "hi"


def test_parse_unary_minus():
    tokens = [
        make_token(TokenType.MINUS, "-", None),
        make_token(TokenType.NUMBER, "5", 5),
    ]
    node = parse(tokens)
    assert isinstance(node, Unary)
    assert node.operator.type == TokenType.MINUS
    assert isinstance(node.right, Literal)
    assert node.right.value == 5


def test_parse_simple_binary():
    tokens = [
        make_token(TokenType.NUMBER, "1", 1),
        make_token(TokenType.PLUS, "+", None),
        make_token(TokenType.NUMBER, "2", 2),
    ]
    node = parse(tokens)
    assert isinstance(node, Binary)
    assert isinstance(node.left, Literal) and node.left.value == 1
    assert node.operator.type == TokenType.PLUS
    assert isinstance(node.right, Literal) and node.right.value == 2


def test_parse_binary_precedence():
    # 1 + 2 * 3 -> 1 + (2 * 3)
    tokens = [
        make_token(TokenType.NUMBER, "1", 1),
        make_token(TokenType.PLUS, "+", None),
        make_token(TokenType.NUMBER, "2", 2),
        make_token(TokenType.STAR, "*", None),
        make_token(TokenType.NUMBER, "3", 3),
    ]
    expr = parse(tokens)
    # top-level should be PLUS
    assert isinstance(expr, Binary)
    assert expr.operator.type == TokenType.PLUS
    # right side is a nested STAR binary
    right = expr.right
    assert isinstance(right, Binary)
    assert right.operator.type == TokenType.STAR
    assert right.left.value == 2
    assert right.right.value == 3


def test_parse_grouping_and_binary():
    # (1 + 2) * 3
    tokens = [
        make_token(TokenType.LEFT_PAREN, "(", None),
        make_token(TokenType.NUMBER, "1", 1),
        make_token(TokenType.PLUS, "+", None),
        make_token(TokenType.NUMBER, "2", 2),
        make_token(TokenType.RIGHT_PAREN, ")", None),
        make_token(TokenType.STAR, "*", None),
        make_token(TokenType.NUMBER, "3", 3),
    ]
    expr = parse(tokens)
    # top-level *
    assert isinstance(expr, Binary)
    assert expr.operator.type == TokenType.STAR
    # left should be a grouping of (1+2)
    grouping = expr.left
    assert isinstance(grouping, Grouping)
    inner = grouping.expression
    assert isinstance(inner, Binary)
    assert inner.operator.type == TokenType.PLUS
    assert inner.left.value == 1
    assert inner.right.value == 2
    # right operand 3
    assert expr.right.value == 3


def test_parse_comma_simple():
    tokens = [
        make_token(TokenType.NUMBER, "1", 1),
        make_token(TokenType.COMMA, ",", None),
        make_token(TokenType.NUMBER, "2", 2),
    ]
    expr = parse(tokens)
    assert isinstance(expr, Binary)
    assert expr.operator.type == TokenType.COMMA
    assert expr.left.value == 1
    assert expr.right.value == 2


def test_parse_comma_associative():
    tokens = [
        make_token(TokenType.NUMBER, "1", 1),
        make_token(TokenType.COMMA, ",", None),
        make_token(TokenType.NUMBER, "2", 2),
        make_token(TokenType.COMMA, ",", None),
        make_token(TokenType.NUMBER, "3", 3),
    ]
    expr = parse(tokens)
    # (1 , 2) , 3
    assert isinstance(expr, Binary)
    assert expr.operator.type == TokenType.COMMA
    left = expr.left
    assert isinstance(left, Binary)
    assert left.operator.type == TokenType.COMMA
    assert left.left.value == 1
    assert left.right.value == 2
    assert expr.right.value == 3
