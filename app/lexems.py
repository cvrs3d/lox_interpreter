from typing import Dict, Set, Tuple
from app.Token import TokenType

lexems: Dict[str, Tuple[str, TokenType]] = {
    "(": ("LEFT_PAREN ( null", TokenType.LEFT_PAREN),
    ")": ("RIGHT_PAREN ) null", TokenType.RIGHT_PAREN),
    "{": ("LEFT_BRACE { null", TokenType.LEFT_BRACE),
    "}": ("RIGHT_BRACE } null", TokenType.RIGHT_BRACE),
    ",": ("COMMA , null", TokenType.COMMA),
    ".": ("DOT . null", TokenType.DOT),
    "*": ("STAR * null", TokenType.STAR),
    ";": ("SEMICOLON ; null", TokenType.SEMICOLON),
    "-": ("MINUS - null", TokenType.MINUS),
    "+": ("PLUS + null", TokenType.PLUS),
    "=": ("EQUAL = null", TokenType.EQUAL),
    "==": ("EQUAL_EQUAL == null", TokenType.EQUAL_EQUAL),
    "!=": ("BANG_EQUAL != null", TokenType.BANG_EQUAL),
    ">": ("GREATER > null", TokenType.GREATER),
    "<": ("LESS < null", TokenType.LESS),
    ">=": ("GREATER_EQUAL >= null", TokenType.GREATER_EQUAL),
    "<=": ("LESS_EQUAL <= null", TokenType.LESS_EQUAL),
    "!": ("BANG ! null", TokenType.BANG),
    "/": ("SLASH / null", TokenType.SLASH),
    "and": ("AND and null", TokenType.AND),
    "class": ("CLASS class null", TokenType.CLASS),
    "else": ("ELSE else null", TokenType.ELSE),
    "false": ("FALSE false null", TokenType.FALSE),
    "for": ("FOR for null", TokenType.FOR),
    "fun": ("FUN fun null", TokenType.FUN),
    "if": ("IF if null", TokenType.IF),
    "nil": ("NIL nil null", TokenType.NIL),
    "or": ("OR or null", TokenType.OR),
    "print": ("PRINT print null", TokenType.PRINT),
    "return": ("RETURN return null", TokenType.RETURN),
    "super": ("SUPER super null", TokenType.SUPER),
    "this": ("THIS this null", TokenType.THIS),
    "true": ("TRUE true null", TokenType.TRUE),
    "var": ("VAR var null", TokenType.VAR),
    "while": ("WHILE while null", TokenType.WHILE),
    "EOF": ("EOF  null", TokenType.EOF),
}


special: Set[str] = {"//", }
