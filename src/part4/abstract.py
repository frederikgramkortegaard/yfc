"""
Abstract Syntax Tree (AST) node definitions.

Simple AST nodes for basic arithmetic expressions.
"""

from lexer import Token, TokenType  # TokenType will be used in examples later


class Expression:
    """Base class for all expression nodes."""
    pass


class NumberExpr(Expression):
    """Represents a numeric literal like 42 or 3.14"""
    def __init__(self, value: Token):
        self.value = value


class BinaryOp(Expression):
    """Represents a binary operation like 2 + 3"""
    def __init__(self, left: Expression, op: Token, right: Expression):
        self.left = left
        self.op = op
        self.right = right


# Example: manually building an AST for "2 + 3 * 4"
if __name__ == "__main__":
    # Manually build AST for: 2 + (3 * 4)
    ast = BinaryOp(
        left=NumberExpr(Token(TokenType.Number, "2")),
        op=Token(TokenType.Plus, "+"),
        right=BinaryOp(
            left=NumberExpr(Token(TokenType.Number, "3")),
            op=Token(TokenType.Mul, "*"),
            right=NumberExpr(Token(TokenType.Number, "4"))
        )
    )

    print("AST for: 2 + 3 * 4")
    print(f"Root operation: {ast.op.value}")
    print(f"  Left: {ast.left.value.value}")
    print(f"  Right operation: {ast.right.op.value}")
    print(f"    Left: {ast.right.left.value.value}")
    print(f"    Right: {ast.right.right.value.value}")
