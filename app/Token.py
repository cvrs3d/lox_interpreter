class TokenType:
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    STAR = "STAR"
    SEMICOLON = "SEMICOLON"
    MINUS = "MINUS"
    PLUS = "PLUS"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG_EQUAL = "BANG_EQUAL"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    BANG = "BANG"
    SLASH = "SLASH"
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FOR = "FOR"
    FUN = "FUN"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"
    EOF = "EOF"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = str(literal)
        self.line = line

    def __str__(self) -> str:
        return f'{self.token_type} {self.lexeme} {self.literal}'

    def __repr__(self) -> str:
        return f'{self.token_type} {self.lexeme} {self.literal}'
