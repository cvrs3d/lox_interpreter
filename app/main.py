import sys
from typing import Dict, TextIO

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
    "EOF": "EOF  null",
}


def scan_tokens(file_contents: TextIO) -> None:
    error_found = False
    for line_number, line in enumerate(file_contents, 1):
        for token in line:
            if token in lexems:
                print(lexems[token])
            else:
                print(f"[line {line_number}] Error: Unexpected character: {token}")
                error_found = True
    print(lexems["EOF"])
    if error_found:
        sys.exit(65)


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


    with open(filename, 'r') as file:
        if file:
            scan_tokens(file)
        else:
            print(lexems["EOF"])


if __name__ == "__main__":
    main()
