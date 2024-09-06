import sys
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
    "EOF": "EOF  null",
}


def scan_tokens(file_contents: str) -> None:
    for token in file_contents:
        try:
            print(lexems[token])
        except KeyError:
            print(f"{token} Unexpected character!")
            break
    print(lexems["EOF"])


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Uncomment this block to pass the first stage
    if file_contents:
        scan_tokens(file_contents)
    else:
        print(lexems["EOF"])


if __name__ == "__main__":
    main()
