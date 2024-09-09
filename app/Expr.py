from __future__ import annotations

from typing import Any

from app.Token import Token


class Expr:
    def accept(self, visitor: Visitor) -> Any:
        raise NotImplementedError()


class Visitor:
    def visit_binary(self, expr: Binary) -> Any:
        raise NotImplementedError()

    def visit_grouping(self, expr: Grouping) -> Any:
        raise NotImplementedError()

    def visit_literal(self, expr: Literal) -> Any:
        raise NotImplementedError()

    def visit_unary(self, expr: Unary) -> Any:
        raise NotImplementedError()

    def visit_variable(self, expr: Variable) -> Any:
        raise NotImplementedError()


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_binary(self)

    def __repr__(self) -> str:
        return f" From {self.__class__}Left Operand: {self.left} Operator: {self.operator} Right Operand: {self.right}"


class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_grouping(self)


class Literal(Expr):
    def __init__(self, value: Any) -> None:
        self.value = value

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_literal(self)

    def __repr__(self):
        return f" VALUE: {self.value}"


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_unary(self)


class Variable(Expr):
    def __init__(self, name: str) -> None:
        self.name = name

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_variable(self)
