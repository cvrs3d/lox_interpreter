from typing import List

from app.Expr import Visitor, Binary, Unary, Grouping, Literal, Variable
from app.Token import Token, TokenType


class AstPrinter(Visitor):
    def print(self, expr):
        return expr.accept(self)

    def visit_binary(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme,
                                 expr.left, expr.right)

    def visit_grouping(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        if expr.value is True:
            return "true"
        if expr.value is False:
            return "false"
        return str(expr.value)

    def visit_unary(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable(self, expr: Variable) -> str:
        return f"var {expr.name}"

    def parenthesize(self, name: str, *args) -> str:
        builder: List[str] = ["(", name]
        for expr in args:
            builder.append(" ")
            builder.append(expr.accept(self))
        builder.append(")")
        return ''.join(builder)


# if __name__ == '__main__':
#     expression = Binary(
#         Unary(Token(TokenType.MINUS, "-", "null", 1),Literal(123)),
#         Token(TokenType.STAR, "*", "null", 1),
#         Grouping(Literal(43.65))
#     )
#     unary = Unary(
#         Token(TokenType.PLUS, '+', 'null', 1),
#         Literal(99),
#     )
#     print(AstPrinter().print(expression))
#     print(AstPrinter().print(unary))
