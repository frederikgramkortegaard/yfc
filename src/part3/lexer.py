"""
Simple lexer for basic arithmetic expressions.
This is the version from Part 3 of the tutorial.

Supports: numbers, +, -, *, /, (, )
"""

from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    Number = auto()
    Plus = auto()
    Minus = auto()
    Mul = auto()
    Div = auto()
    LParen = auto()
    RParen = auto()
    Eof = auto()


@dataclass
class Token:
    _type: TokenType
    value: str


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.cursor = 0

    @property
    def current(self) -> str:
        """Return the current character or EOF"""
        if self.cursor < len(self.source):
            return self.source[self.cursor]
        return "\0"

    def increment(self):
        """Move to the next character."""
        self.cursor += 1

    def push_token(self, token_type: TokenType, value: str):
        """Add a token to our list."""
        self.tokens.append(Token(token_type, value))

    def lex(self) -> list[Token]:
        while self.current != '\0':
            # Skip whitespace
            if self.current.isspace():
                self.increment()
                continue

            # Recognize numbers
            if self.current.isdigit():
                start = self.cursor
                while self.current.isdigit():
                    self.increment()

                self.push_token(TokenType.Number, self.source[start:self.cursor])
                continue

            # Recognize operators and parentheses
            single_char_tokens = {
                '(': TokenType.LParen,
                ')': TokenType.RParen,
                '+': TokenType.Plus,
                '-': TokenType.Minus,
                '*': TokenType.Mul,
                '/': TokenType.Div,
            }

            if token_type := single_char_tokens.get(self.current):
                self.push_token(token_type, self.current)
                self.increment()
                continue

            raise Exception(f"Unexpected character: '{self.current}'")

        # Add EOF token
        self.tokens.append(Token(TokenType.Eof, ""))
        return self.tokens


if __name__ == "__main__":
    # Test the lexer
    source = "(2 + 3) * 4"
    lexer = Lexer(source)
    tokens = lexer.lex()

    print(f"Tokenizing: {source}\n")
    for token in tokens:
        print(token)
