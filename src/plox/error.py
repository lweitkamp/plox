from typing import Optional

from plox.token_type import Token, TokenType

error_raised = False


class ParseError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        error(token.line, token, message)


def error(line: int, token: Optional[Token] = None, message: str = ""):
    if token is None:
        report(line, "", message)
    elif token.type == TokenType.EOF:
        report(line, " at end", message)
    else:
        report(line, f" at '{token.lexeme}'", message)


def report(line: int, where: str, message: str):
    print(f"[line {line}] Error {where}: {message}")
    set_error(True)


def set_error(value: bool):
    global error_raised
    error_raised = value


def had_error() -> bool:
    global error_raised
    return error_raised
