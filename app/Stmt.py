from typing import Any, List

from app.Expr import Expr
from app.Token import Token


class Stmt:
    def accept(self, visitor: 'StmtVisitor') -> Any:
        raise NotImplementedError()


class StmtVisitor:
    def visit_expression(self, stmt: 'Expression') -> Any:
        pass

    def visit_print(self, stmt: 'Print') -> Any:
        pass

    def visit_variable_stm(self, stmt: 'Var') -> Any:
        pass

    def visit_block_stmt(self, stmt: 'Block'):
        pass


class Expression(Stmt):
    def __init__(self, expression: 'Expr') -> None:
        self.expression = expression

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_expression(self)


class Print(Stmt):
    def __init__(self, expression: 'Expr') -> None:
        self.expression = expression

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_print(self)


class Var(Stmt):
    def __init__(self, name: Token, initializer: 'Expr') -> None:
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_variable_stm(self)


class Block(Stmt):
    def __init__(self, statements: List['Stmt']):
        self.statements = statements

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_block_stmt(self)
