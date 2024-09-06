import sys


def print_exception(code: int, token: str, line_number: int) -> None:
    if code == 65:
        print(f"[line {line_number}] Error: Unexpected character: {token}", file=sys.stderr)

