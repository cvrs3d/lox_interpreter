from typing import List, TypeVar, Optional

from app.Expr import Binary, Unary, Literal, Grouping
from app.Lox import Lox
from app.Token import Token, TokenType
from app.lexems import statements

E = TypeVar('E')


class ParserError(Exception):
    ...


class Parser:

    def __init__(self, tokens: List[Token]):
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Optional[E]:
        """Initial method returns ExpressionType"""
        try:
            return self.expression()
        except ParserError as error:
            return None

    def expression(self) -> E:
        """Returns expression(Binary, Unary etc)"""
        return self.equality()

    def equality(self) -> E:
        """First expressions in syntax tree are != and == we check for all of them and go deeper
        into descent recursion. Simply we jump to the comparison()"""
        expr: E = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: E = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def match(self, *types) -> bool:
        """Helper method. Returns True if current Token is of the expected types"""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        """Used by match() checks if not EOF and if given type equals to type of the current Token"""
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        """If not EOF we increment current(go forward on the list) returns previous Token
            Well actually returns Token that was current"""
        if not self.is_at_end():
            self._current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        """Checks for EOF"""
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        """Returns current token without advance"""
        return self._tokens[self._current]

    def previous(self) -> Token:
        """Returns previous Token"""
        return self._tokens[self._current - 1]

    def comparison(self) -> E:
        """Next step in syntax tree. Here we collect all the > < >= <= operators and jump to binaries"""
        expr: E = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL, TokenType.LESS):
            operator: Token = self.previous()
            right: E = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> E:
        """First binaries to collect are + or -"""
        expr: E = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator: Token = self.previous()
            right: E = self.factor()
            expr: E = Binary(expr, operator, right)

        return expr

    def factor(self) -> E:
        """Collects / and * binaries"""
        expr: E = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self.previous()
            right: E = self.unary()
            expr: E = Binary(expr, operator, right)

        return expr

    def unary(self) -> E:
        """Next step, unary operators. We seek for ! and -"""
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: E = self.unary()
            return Unary(operator, right)

    def primary(self) -> E:
        """Then complex literals Booleans and Statements.
            This method is likely to cause a panic when doesn't find a closing paren."""
        if self.match(TokenType.FALSE):
            return Literal("false")
        if self.match(TokenType.TRUE):
            return Literal("true")
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr: E = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def consume(self, token_type: TokenType, message: str) -> Token:
        """We consume the token which caused panic and then raise ParseException
            We try to catch it in parse() and synchronize"""
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    @staticmethod
    def error(token: Token, message: str) -> ParserError:
        """Tells our framework that we have a problem"""
        Lox.error(token, message)
        return ParserError()

    def synchronize(self) -> None:
        """Panic unwind mechanism. Yet is not in use"""
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return
            if self.peek().token_type in statements:
                return

            self.advance()
