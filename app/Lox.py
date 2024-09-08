import sys
from typing import List, Optional

from app.Token import Token, TokenType


class Lox:
    had_error = False

    @staticmethod
    def main(args: List[str]):
        if len(args) < 3:
            print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
            exit(1)
        elif len(args) == 3:
            Lox.run_file(args[2], args[1])
        # else:
        #     Lox.run_prompt()

    @staticmethod
    def run_file(path: str, command: str) -> None:
        with open(path, 'r') as file:
            source = file.read()
        Lox.run(source, command)

    # @staticmethod
    # def run_prompt() -> None:
    #     while True:
    #         try:
    #             line = input("> ")
    #             if line.strip() == "":
    #                 continue
    #             Lox.run(line)
    #         except (EOFError, KeyboardInterrupt):
    #             break

    @staticmethod
    def run(source: str, command: str) -> None:
        from app.Scanner import Scanner
        from app.Parser import Parser, E
        from app.ASTPrinter import AstPrinter  # We do not want circular import
        Lox.had_error = False
        if command == 'tokenize':
            scanner: Scanner = Scanner(source)
            tokens: List[Token] = scanner.scan_tokens()
            for token in tokens:
                print(token)
        elif command == 'parse':
            scanner: Scanner = Scanner(source)
            tokens: List[Token] = scanner.scan_tokens()
            parser: Parser = Parser(tokens)
            expr: E = parser.parse()
            print(AstPrinter().print(expr))
        if Lox.had_error:
            sys.exit(65)

    @staticmethod
    def error(token: Token, message: str) -> None:
        if token.token_type == TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, " at '" + token.lexeme + "'", message)

    @staticmethod
    def report(line: int, message: str, char: Optional[str] = None, where: str = '') -> None:
        Lox.had_error = True
        print(f"[line {line}] Error{where}: {message}{char if char is not None else ''}", file=sys.stderr)

#
# if __name__ == "__main__":
#     Lox.run("2 @+ 3@", "tokenize")
