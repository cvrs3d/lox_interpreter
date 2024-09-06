import sys
from typing import Dict, TextIO
from app.lexems import lexems
from app.exceptions import print_exception


def scan_tokens(file_contents: TextIO) -> None:
    """Scanning file contents line by line"""
    error_found = False
    for line_number, line in enumerate(file_contents, 1):
        i = 0
        while i < len(line):
            if i + 1 < len(line):
                two_char_token = line[i: i + 2]
                if two_char_token in lexems:
                    print(lexems[two_char_token])
                    i += 2
                    continue
            token = line[i]
            if token in lexems:
                print(lexems[token])
            else:
                print_exception(65, token, line_number)
    print(lexems["EOF"])
    if error_found:
        exit(65)


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
