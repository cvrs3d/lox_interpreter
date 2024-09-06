import sys
from typing import TextIO, List

from app.Token import TokenType, Token
from app.lexems import lexems


class TokenScannerParsing:
    def __init__(self, file_contents: TextIO) -> None:
        self.file_contents = file_contents
        self.tokens = []
        self.error_found = False

    def scan_tokens(self):
        for line in self.file_contents:
            self.process_line(line)

        self.tokens.append(Token(lexems['EOF'][1], "EOF"))
        return self.tokens

    def process_line(self, line: str) -> None:
        for token in line.split():
            if token == "true":
                self.tokens.append(Token(lexems['true'][1], token))
            elif token == "false":
                self.tokens.append(Token(lexems['false'][1], token))
            elif token == "nil":
                self.tokens.append(Token(lexems['nil'][1], token))
            else:
                self.error_found = True
                print(f"Unexpected token: {token}", file=sys.stderr)


class Parser:
    def __init__(self, tokens):
        self.tokens: List[Token] = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def expression(self):
        return self.literal()

    def literal(self):
        if self.match(TokenType.TRUE):
            return "true"
        if self.match(TokenType.FALSE):
            return "false"
        if self.match(TokenType.NIL):
            return "nil"
        raise Exception("Expected literal")

    def match(self, token_type):
        if self.check(token_type):
            self.advance()
            return True
        return False

    def check(self, token_type):
        return self.tokens[self.current].type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1

    def is_at_end(self):
        return self.tokens[self.current].type == "EOF"
