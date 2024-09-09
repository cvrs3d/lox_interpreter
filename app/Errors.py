from app.Token import Token


class RuntimeException(Exception):

    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token
        self.message = message

    def __str__(self) -> str:
        return super().__str__()



