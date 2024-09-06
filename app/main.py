import sys
from typing import TextIO
from app.TokenScanner import TokenScanner
from app.lexems import lexems


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
            scanner = TokenScanner(file)
            scanner.scan_tokens()
        else:
            print(lexems["EOF"])


if __name__ == "__main__":
    main()
