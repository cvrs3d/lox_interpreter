from typing import Dict

lexems: Dict[str, str] = {
    "(": "LEFT_PAREN ( null",
    ")": "RIGHT_PAREN ) null",
    "{": "LEFT_BRACE { null",
    "}": "RIGHT_BRACE } null",
    ",": "COMMA , null",
    ".": "DOT . null",
    "*": "STAR * null",
    ";": "SEMICOLON ; null",
    "-": "MINUS - null",
    "+": "PLUS + null",
    "=": "EQUAL = null",
    "==": "EQUAL_EQUAL == null",
    "!=": "BANG_EQUAL != null",
    ">": "GREATER_THEN > null",
    "<": "LESS_THEN < null",
    ">=": "GREATER_EQUAL >= null",
    "<=": "LESS_EQUAL <= null",
    "EOF": "EOF  null",
}
