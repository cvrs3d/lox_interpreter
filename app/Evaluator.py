import sys
from typing import Any

from app.Errors import RuntimeException
from app.Expr import ExprVisitor, Literal, Grouping, Unary, Binary
from app.Token import TokenType, Token


class Evaluator(ExprVisitor):

    def interpret(self, expression: Any) -> None:
        from app.Lox import Lox
        try:
            value: Any = self.evaluate(expression)
            print(self.stringify(value))
        except RuntimeException as e:
            Lox.runtime_error(e)

    @staticmethod
    def stringify(value: Any) -> str:
        print(f"From {Evaluator.stringify.__qualname__} being called with {value} of type {type(value)}",
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
        print(f"From {Evaluator.stringify.__qualname__} returning {value} of type {type(value)}", file=sys.stderr)
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
            print(f"from{self.visit_unary.__qualname__} entering is_truthy with {right}", file=sys.stderr)
            return not self.is_truthy(right)
        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, right=right)
            return -float(right)

        return None

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
            print(f"From {Evaluator.visit_binary.__qualname__} entering + if clause with left{left} right{right}",
                  file=sys.stderr)
            if isinstance(left, str) and isinstance(right, str):
                print(f"From {Evaluator.visit_binary.__qualname__} entered concat left is str{isinstance(left, str)}"
                      f"right is str {isinstance(right, str)}", file=sys.stderr)
                return str(left) + str(right)
            if isinstance(left, float) and isinstance(right, float):
                print(f"From {Evaluator.visit_binary.__qualname__} entered + left is str{isinstance(left, str)}"
                      f"right is str {isinstance(right, str)}", file=sys.stderr)
                self.check_number_operands(expr.operator, left, right)
                return float(left) + float(right)
            else:
                print(f"From {Evaluator.visit_binary.__qualname__} entered else left is str{isinstance(left, str)}"
                      f"right is str {isinstance(right, str)} operator = {expr.operator}", file=sys.stderr)
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
