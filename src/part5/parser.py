"""
Parser for basic arithmetic expressions.

Uses recursive descent with precedence climbing for binary operators.
This is a simplified version that just handles numbers, operators, and parentheses.
"""

from lexer import Token, TokenType
from abstract import Expression, NumberExpr, BinaryOp


# Operator precedence - higher number = higher precedence
PRECEDENCE_MAP = {
    TokenType.Plus: 20,
    TokenType.Minus: 20,
    TokenType.Mul: 40,
    TokenType.Div: 40,
}


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.cursor = 0

    @property
    def current(self) -> Token:
        """Get the current token."""
        if 0 <= self.cursor < len(self.tokens):
            return self.tokens[self.cursor]
        # Return EOF token if we're at the end
        return self.tokens[-1]

    def consume(self) -> Token:
        """Consume and return the current token."""
        if 0 <= self.cursor < len(self.tokens):
            token = self.tokens[self.cursor]
        else:
            token = self.tokens[-1]
        self.cursor += 1
        return token

    def parse_expression(self) -> Expression:
        """Parse an expression (entry point)."""
        left = self.parse_primary()

        while PRECEDENCE_MAP.get(self.current._type):
            op = self.consume()
            left = self.parse_binary_op(left, op)

        return left

    def parse_binary_op(self, left: Expression, op: Token) -> Expression:
        """Parse a binary operation using precedence climbing."""
        # Get the precedence of the current operator
        current_precedence = PRECEDENCE_MAP.get(op._type, 0)

        # Parse the right-hand side
        right = self.parse_primary()

        # Look ahead to see if there's another operator with higher precedence
        while PRECEDENCE_MAP.get(self.current._type, 0) > current_precedence:
            next_op = self.consume()
            right = self.parse_binary_op(right, next_op)

        # Build the binary operation node
        return BinaryOp(left, op, right)

    def parse_primary(self) -> Expression:
        """Parse a primary expression (number or parenthesized expression)."""
        match self.current._type:
            # Grammar: '(' expression ')'
            case TokenType.LParen:
                self.consume()
                expr = self.parse_expression()
                if self.current._type != TokenType.RParen:
                    raise ParserError(f"Expected RParen after parsing parenthesized expression, but got {self.current._type}")
                self.consume()
                return expr

            # Grammar: NUMBER
            case TokenType.Number:
                token = self.consume()
                return NumberExpr(token)

            case _:
                raise ParserError(f"Unexpected token: {self.current._type}")


# Example usage - test operator precedence
if __name__ == "__main__":
    from lexer import Lexer

    # Test operator precedence: 2 + 3 * 4
    source = "2 + 3 * 4"
    lexer = Lexer(source)
    tokens = lexer.lex()
    parser = Parser(tokens)
    ast = parser.parse_expression()

    print(f"Expression: {source}")
    print(f"Root: {ast.op.value}")
    print(f"  Left: {ast.left.value.value}")
    print(f"  Right: BinaryOp {ast.right.op.value}")
    print(f"    Left: {ast.right.left.value.value}")
    print(f"    Right: {ast.right.right.value.value}")
