from typing import List, Optional

from app.Lox import Lox
from app.Token import Token, TokenType
from app.lexems import lexems


class Scanner:
    def __init__(self, source: str) -> None:
        self._previous: int = 0
        self._source: str = source
        self._tokens: List[Token] = []
        self._current: int = 0
        self._start: int = 0
        self._line: int = 1

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self._start = self._current
            self.scan_token()

        self._tokens.append(Token(TokenType.EOF, "", "null", self._line))
        return self._tokens

    def is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def scan_token(self) -> None:
        """Scanning single token(char) in sequence by using advance() we're automatically setting _curr to next char
        index"""
        c: str = self.advance()
        if c in {' ', '\r', '\t', '\n'}:
            if c == '\n':
                self._line += 1
            return
        if c.isdigit():
            self.handle_number()
            return
        if c == '"':
            self.handle_string()
            return
        if c == '/':
            if self.match_next('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH, literal=None)
            return
        if c in lexems:
            if c in ['!', '=', '<', '>']:
                if self.match_next('='):
                    self.add_token(lexems[c + '='], literal=None)
                else:
                    self.add_token(lexems[c], literal=None)
                return
            else:
                self.add_token(lexems[c], literal=None)
        elif c.isalpha() or c == '_':
            self.handle_identifier()
            return
        else:
            Lox.report(self._line, message="Unexpected character: ", char=c, where='')

    def advance(self) -> str:
        """Returns current symbol in sequence and increments index"""
        c: str = self._source[self._current]
        self._previous = self._current
        self._current += 1
        return c

    def match_next(self, expected: str) -> bool:
        """Compares next symbol to expected if True that means we take 2 symbols so current++"""
        if self.is_at_end():
            return False
        if self._source[self._current] != expected:
            return False
        self._current += 1
        return True

    def add_token(self, token_type: TokenType, literal: Optional[object] = None) -> None:
        """Adds tokens to the list"""
        if literal is None:
            literal = "null"

        text: str = self._source[self._start:self._current]
        self._tokens.append(Token(token_type, text, literal, self._line))

    def handle_identifier(self) -> None:
        """Scans trough identifier substring then adds it to tokens"""
        while not self.is_at_end() and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()
        value: str = self._source[self._start:self._current]
        if value in lexems:
            self.add_token(lexems[value], literal=None)
        else:
            self.add_token(TokenType.IDENTIFIER, literal=None)

    def handle_string(self):
        """Similar to handle_identifier() but it seeks for closing quote if there is none raises an error"""
        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == '\n':
                self._line += 1
            self.advance()
        if self.is_at_end():
            Lox.report(self._line, message="Unterminated string.")
            return
        self.advance()  # Closing "
        value = self._source[self._start + 1:self._current - 1]  # Trim the ""
        self.add_token(TokenType.STRING, literal=value)

    def handle_number(self):
        """Scans through every digit if encounter 1st dot and digit after continue while digits appear"""
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, float(self._source[self._start: self._current]))

    def peek(self) -> str:
        """Returns current without moving forward"""
        if self.is_at_end():
            return '\0'
        return self._source[self._current]

    def peek_next(self) -> str:
        """Returns next after current without advance()"""
        if self._current + 1 >= len(self._source):
            return '\0'
        return self._source[self._current + 1]
