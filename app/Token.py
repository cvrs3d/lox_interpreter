class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class TokenType:
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    NIL = "NIL"
    EOF = "EOF"
    FALSE = "FALSE"
    TRUE = "TRUE"