from typing import List, TypeVar, Any

from app.Expr import Binary, Unary, Literal, Grouping, Variable, Assign
from app.Lox import Lox
from app.Stmt import Stmt, Print, Expression, Var, Block
from app.Token import Token, TokenType
from app.lexems import statements

E = TypeVar('E')


class ParserError(Exception):
    ...


class Parser:

    def __init__(self, tokens: List[Token]):
        self._tokens = tokens
        self._current = 0

    def parse(self) -> List['Stmt']:
        """Parse method returns a list of statements."""
        stmts: List[Stmt] = []
        while not self.is_at_end():
            stmts.append(self.declaration())
        return stmts

    def expression(self) -> E:
        """Returns expression(Binary, Unary etc)"""
        return self.assignment()

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
        return self.primary()

    def primary(self) -> E:
        """Then complex literals Booleans and Statements."""
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

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
        """Panic unwind mechanism."""
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return
            if self.peek().token_type in statements:
                return

            self.advance()

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()

    def block(self) -> List[Stmt]:
        stmts: List[Stmt] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            stmts.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return stmts

    def print_statement(self):
        value: Any = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self):
        expr: Any = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def assignment(self) -> Any:
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            equals: Token = self.previous()
            value: Any = self.assignment()

            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParserError:
            self.synchronize()
            return None

    def var_declaration(self) -> Any:
        name: Token = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer: Any = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)
