from plox.token_type import KEYWORDS, Token, TokenType
from plox.error import error

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []

        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end:
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, 0))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end:
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case '"':
                self.string()
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                self.number()
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case _:
                if self.is_alpha(c):
                    self.identifier()
                    return

                error(self.line, None, f"Unexpected token {c}.")

    def add_token(self, token_type: TokenType, literal: object = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def is_alpha(self, c: str) -> bool:
        return c.isalpha() or c == "_"

    def string(self):
        while self.peek() != '"' and not self.is_at_end:
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end:
            error(self.line, None, "Unterminated string.")
            return

        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start : self.current])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.is_alpha(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    @property
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected):
        if self.is_at_end:
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end:
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
