import sys
from typing import List, Optional

from app.Errors import RuntimeException
from app.Interpreter import Interpreter
from app.Token import Token, TokenType


class Lox:
    had_error = False
    had_runtime_error = False
    interpreter = Interpreter()

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
        Lox.had_runtime_error = False
        if command == 'tokenize':
            scanner: Scanner = Scanner(source)
            tokens: List[Token] = scanner.scan_tokens()
            for token in tokens:
                print(token)
        elif command == 'parse':
            scanner: Scanner = Scanner(source)
            tokens: List[Token] = scanner.scan_tokens()
            parser: Parser = Parser(tokens)
            try:
                expr: E = parser.parse()
                print(AstPrinter().print(expr))
            except AttributeError:
                Lox.had_error = True
        elif command == 'evaluate':
            scanner: Scanner = Scanner(source)
            tokens: List[Token] = scanner.scan_tokens()
            parser: Parser = Parser(tokens)
            try:
                expr: E = parser.parse()
                Lox.interpreter.interpret(expr)
            except AttributeError:
                Lox.had_error = True
        if Lox.had_error:
            exit(65)
        if Lox.had_runtime_error:
            exit(70)

    @staticmethod
    def error(token: Token, message: str) -> None:
        if token.token_type == TokenType.EOF:
            Lox.report(token.line, message=message, where=" at end")
        else:
            Lox.report(token.line, message=message, where=" at '" + token.lexeme + "'")

    @staticmethod
    def report(line: int, message: str, char: Optional[str] = None, where: str = '') -> None:
        Lox.had_error = True
        print(f"[line {line}] Error{where}: {message}{char if char is not None else ''}", file=sys.stderr)

    @staticmethod
    def runtime_error(error: RuntimeException) -> None:
        print(f"\n{error} [line {error.token.line}]")
        Lox.had_runtime_error = True


# if __name__ == "__main__":
#     Lox.run('"hello"-"hello"', "evaluate")
