import sys
from typing import TextIO

from app.lexems import lexems, special


class TokenScanner:

    def __init__(self, file_contents: TextIO) -> None:
        self.file_contents: TextIO = file_contents
        self.error_found: bool = False
        self.string_ended: bool = True
        self.string_literal: str = str()
        self.current_index: int = 0
        self.number: str = ""
        self.precision: bool = False

    @staticmethod
    def print_exception(code: int, token: str, line_number: int) -> None:
        if code == 1:
            print(f"[line {line_number}] Error: Unexpected character: {token}", file=sys.stderr)
        elif code == 2:
            print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)

    def scan_tokens(self) -> None:
        for line_number, line in enumerate(self.file_contents, 1):
            self.process_line(line, line_number)
        print(lexems["EOF"])
        if self.error_found or not self.string_ended:
            sys.exit(65)

    def process_line(self, line: str, line_number: int) -> None:
        i: int = 0
        while i < len(line):
            token = line[i]
            if token.isnumeric():
                self.handle_number(line, i, line_number)
                i = self.current_index
                continue
            if token in {' ', '\t', '\n'}:
                i += 1
                continue
            if token == '"':
                self.handle_string_literal(line, i, line_number)
                i = self.current_index
                continue
            if i + 1 < len(line):
                two_char_token = line[i: i + 2]
                if two_char_token in special:
                    break
                if two_char_token in lexems:
                    print(lexems[two_char_token])
                    i += 2
                    continue
            if token in lexems:
                print(lexems[token])
            else:
                self.print_exception(1, token, line_number)
                self.error_found = True
            i += 1

    def handle_string_literal(self, line: str, start_index: int, line_number: int) -> None:
        self.string_literal = '"'
        self.string_ended = False
        i = start_index + 1
        while i < len(line):
            if line[i] == '"':
                self.string_literal += line[i]
                self.string_ended = True
                print(f'STRING {self.string_literal} {self.string_literal[1:-1]}')
                break
            self.string_literal += line[i]
            i += 1
        if not self.string_ended:
            self.print_exception(2, '', line_number)
        self.current_index = i + 1

    def handle_number(self, line: str, start_index: int, line_number: int):
        self.number = ""
        self.precision = False
        i = start_index
        while i < len(line) and line[i].isnumeric():
            self.number += line[i]
            if line[i] == "." and not self.precision:
                self.number += line[i]
                self.precision = True
                i += 1
            else:
                self.print_exception(1, line[i], line_number)
                self.error_found = True
            i += 1
        self.current_index = i
        if '.' not in self.number:
            print(f"NUMBER {self.number} {self.number}.0")
        else:
            print(f"NUMBER {self.number} {self.number}")


