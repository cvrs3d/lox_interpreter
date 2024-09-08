import io
import unittest
from unittest.mock import patch

from app.Expr import Binary, Literal
from app.Parser import Parser
from app.Scanner import Scanner
from app.Token import TokenType, Token


class TestScanner(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, 1)  # add assertion here

    def test_scan_for_empty_source(self):
        scanner = Scanner("")
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, TokenType.EOF)

    def test_scan_tokens_single_chars(self):
        scanner = Scanner("(){},.")
        tokens = scanner.scan_tokens()
        expected = [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN, TokenType.LEFT_BRACE, TokenType.RIGHT_BRACE,
                    TokenType.COMMA, TokenType.DOT, TokenType.EOF]
        self.assertEqual(len(tokens), len(expected))
        print(tokens)
        for token, expected_type in zip(tokens, expected):
            self.assertEqual(token.token_type, expected_type)

    def test_scan_token_numbers(self):
        scanner = Scanner("123 43.67 89.")
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].token_type, TokenType.NUMBER)
        self.assertEqual(tokens[1].token_type, TokenType.NUMBER)
        self.assertEqual(tokens[0].lexeme, "123")
        self.assertEqual(tokens[0].literal, "123.0")
        self.assertEqual(tokens[1].lexeme, "43.67")
        self.assertEqual(tokens[1].literal, '43.67')
        self.assertEqual(tokens[2].lexeme, "89")
        self.assertEqual(tokens[2].literal, '89.0')
        self.assertEqual(tokens[3].token_type, TokenType.DOT)
        self.assertEqual(tokens[-1].token_type, TokenType.EOF)

    def test_scan_strings(self):
        scanner = Scanner('"hello" "world"')
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].token_type, TokenType.STRING)
        self.assertEqual(tokens[1].token_type, TokenType.STRING)
        self.assertEqual(tokens[0].literal, "hello")
        self.assertEqual(tokens[1].literal, "world")
        self.assertEqual(tokens[0].lexeme, '"hello"')
        self.assertEqual(tokens[1].lexeme, '"world"')
        self.assertEqual(tokens[2].token_type, TokenType.EOF)

    def test_scan_tokens_identifiers(self):
        scanner = Scanner("foo bar_baz")
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 3)  # 2 identifiers + EOF
        self.assertEqual(tokens[0].token_type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].token_type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].literal, "null")
        self.assertEqual(tokens[1].literal, "null")
        self.assertEqual(tokens[0].lexeme, "foo")
        self.assertEqual(tokens[1].lexeme, "bar_baz")
        self.assertEqual(tokens[2].token_type, TokenType.EOF)

    def test_scan_tokens_comments(self):
        scanner = Scanner("// this is a comment\nfoo")
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].token_type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "foo")
        self.assertEqual(tokens[0].literal, "null")
        self.assertEqual(tokens[1].token_type, TokenType.EOF)

    @patch('sys.stderr', new_callable=io.StringIO)
    def test_scan_unexpected_chars(self, mock_stderr):
        scanner = Scanner("@")
        scanner.scan_tokens()
        output = mock_stderr.getvalue().strip()
        expected = "[line 1] Error: Unexpected character: @"
        self.assertIn(expected, output)


class TestParser(unittest.TestCase):

    def test_parse_term(self):
        tokens = [
            Token(TokenType.NUMBER, "1", 1, 1),
            Token(TokenType.PLUS, "+", "null", 1),
            Token(TokenType.NUMBER, "2", 2, 1),
            Token(TokenType.EOF, "", "null", 1)
        ]
        parser = Parser(tokens)
        expr = parser.parse()
        self.assertIsInstance(expr, Binary)
        self.assertIsInstance(expr.left, Literal)
        self.assertIsInstance(expr.right, Literal)
        self.assertEqual(expr.operator.token_type, TokenType.PLUS)

    def test_parse_boolean_true(self):
        tokens = [
            Token(TokenType.TRUE, "true", "null", 1),
            Token(TokenType.EOF," ","null", 1)
        ]
        parser = Parser(tokens)
        expr = parser.parse()
        self.assertIsInstance(expr, Literal)
        self.assertEqual(expr.value, "true")

    def test_parse_boolean_false(self):
        tokens = [
            Token(TokenType.FALSE, "false", "null", 1),
            Token(TokenType.EOF," ","null", 1)
        ]
        parser = Parser(tokens)
        expr = parser.parse()
        self.assertIsInstance(expr, Literal)
        self.assertEqual(expr.value, "false")

    def test_parse_boolean_nil(self):
        tokens = [
            Token(TokenType.NIL, "nil", "null", 1),
            Token(TokenType.EOF," ","null", 1)
        ]
        parser = Parser(tokens)
        expr = parser.parse()
        self.assertIsInstance(expr, Literal)
        self.assertEqual(expr.value, "nil")