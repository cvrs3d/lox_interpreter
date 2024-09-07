from typing import Dict, Set, Tuple
from app.Token import TokenType

lexems: Dict[str, TokenType] = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "*": TokenType.STAR,
    ";": TokenType.SEMICOLON,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    "=": TokenType.EQUAL,
    "==": TokenType.EQUAL_EQUAL,
    "!=": TokenType.BANG_EQUAL,
    ">": TokenType.GREATER,
    "<": TokenType.LESS,
    ">=": TokenType.GREATER_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    "!": TokenType.BANG,
    "/": TokenType.SLASH,
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
    "EOF": TokenType.EOF,
}

statements: Set[TokenType] = {
    TokenType.PRINT, TokenType.IF, TokenType.CLASS, TokenType.FUN, TokenType.FOR, TokenType.VAR, TokenType.WHILE,
    TokenType.RETURN
}


special: Set[str] = {"//", }
