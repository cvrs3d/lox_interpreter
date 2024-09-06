class UnknownSymbolError(Exception):
    def __init__(self, line, char) -> None:
        self.line = line
        self.char = char
        super().__init__(f"[{line}] Error: Unexpected character: {char}")

