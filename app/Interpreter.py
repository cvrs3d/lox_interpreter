import sys
from typing import Any, List

from app.Environment import Environment
from app.Errors import RuntimeException
from app.Expr import ExprVisitor, Literal, Grouping, Unary, Binary, Variable, Assign
from app.Stmt import StmtVisitor, Expression, Print, Var, Stmt
from app.Token import TokenType, Token


class Interpreter(ExprVisitor, StmtVisitor):
    environment: Environment = Environment()

    def interpret(self, statements: List[Any]) -> None:
        from app.Lox import Lox
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeException as e:
            Lox.runtime_error(e)

    def execute(self, stmt) -> None:
        stmt.accept(self)

    def visit_block_stmt(self, stmt) -> None:
        self.execute_block(stmt.statements, Environment(enclosing=self.environment))
        return None

    def visit_variable_stm(self, stmt: Var) -> Any:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def execute_block(self, stmts: List[Stmt], environ: Environment) -> None:
        previous: Environment = self.environment
        try:
            self.environment = environ
            for stm in stmts:
                self.execute(stm)
        finally:
            self.environment = previous

    @staticmethod
    def stringify(value: Any) -> str:
        print(f"From {Interpreter.stringify.__qualname__} being called with {value} of type {type(value)}",
              file=sys.stderr)
        """Java's stringify"""
        if value is None:
            return "nil"
        if value is False:
            return "false"
        if value is True:
            return "true"

        text = str(value)
        if text.endswith(".0"):
            text = text[:-2]  # Trim zeroes for decimal
            return text
        print(f"From {Interpreter.stringify.__qualname__} returning {value} of type {type(value)}", file=sys.stderr)
        return str(value)

    def visit_literal(self, expr: Literal) -> Any:
        return expr.value

    def visit_grouping(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def evaluate(self, expr) -> Any:
        return expr.accept(self)

    def visit_unary(self, expr: Unary) -> Any:
        """This method is likely to throw a runtime error if operand is not a number"""
        right: Any = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, right=right)
            return -float(right)

        return None

    def visit_variable_expr(self, expr: Variable) -> Any:
        return self.environment.get(expr.name)

    def visit_assign(self, expr: Assign) -> Any:
        value: Any = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    @staticmethod
    def is_truthy(obj: Any) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def visit_binary(self, expr: Binary) -> Any:
        """This method is likely to throw a runtime error if operand is not a number"""
        left: Any = self.evaluate(expr.left)
        right: Any = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)

        if expr.operator.token_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        if expr.operator.token_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)

        if expr.operator.token_type == TokenType.PLUS:
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            if isinstance(left, float) and isinstance(right, float):
                self.check_number_operands(expr.operator, left, right)
                return float(left) + float(right)
            else:
                raise RuntimeException(expr.operator, "Operands must be two numbers or two strings.")

        if expr.operator.token_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)

        if expr.operator.token_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)

        if expr.operator.token_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)

        if expr.operator.token_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        if expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)

        if expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        return None

    def visit_expression(self, stmt: 'Expression') -> None:
        self.evaluate(stmt.expression)
        return None

    def visit_print(self, stmt: 'Print') -> None:
        value: Any = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visit_variable_stmt(self, stmt: 'Var') -> None:
        value: Any = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    @staticmethod
    def is_equal(left: Any, right: Any) -> bool:
        if left is None and right is None:
            return True
        if left is None:
            return False

        return left == right

    @staticmethod
    def check_number_operands(operator: Token, left: Any = None, right: Any = None) -> None:
        if left is None:
            if isinstance(right, float):
                return
            else:
                raise RuntimeException(operator, f"Operand must be a number.")
        if isinstance(left, float) and isinstance(right, float):
            return
        else:
            raise RuntimeException(operator, f"Operands must be a numbers.")
