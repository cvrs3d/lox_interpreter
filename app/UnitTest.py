import io
import unittest
from unittest.mock import patch

from app.Expr import Binary, Literal, Unary
from app.Interpreter import Interpreter
from app.Lox import Lox
from app.Parser import Parser
from app.Scanner import Scanner
from app.Token import TokenType, Token


class TestInterpreter(unittest.TestCase):

    def setUp(self) -> None:
        self.interpreter = Interpreter()

    def evaluate_expression(self, expr):
        return self.interpreter.evaluate(expr)

    def test_literal(self):
        expr = Literal(42)
        result = self.evaluate_expression(expr)
        print(result)
        self.assertEqual(result, 42)

    def test_unary_negation(self):
        expr = Unary(Token(TokenType.MINUS, "-", None, 1), Literal(3.5))
        result = self.evaluate_expression(expr)
        self.assertEqual(result, -3.5)

    def test_unary_not(self):
        expr = Unary(Token(TokenType.BANG, "!", None, 1), Literal(True))
        result = self.interpreter.stringify(self.evaluate_expression(expr))
        self.assertEqual(result, "false")

    def test_binary_addition(self):
        expr = Binary(Literal(3.0), Token(TokenType.PLUS, "+", None, 1), Literal(4.5))
        result = self.evaluate_expression(expr)
        self.assertEqual(result, 7.5)

    def test_binary_subtraction(self):
        expr = Binary(Literal(10.0), Token(TokenType.MINUS, "-", None, 1), Literal(4.5))
        result = self.evaluate_expression(expr)
        self.assertEqual(result, 5.5)

    def test_binary_multiplication(self):
        expr = Binary(Literal(2.0), Token(TokenType.STAR, "*", None, 1), Literal(3.0))
        result = self.evaluate_expression(expr)
        self.assertEqual(result, 6.0)

    def test_binary_division(self):
        expr = Binary(Literal(10.0), Token(TokenType.SLASH, "/", None, 1), Literal(2.0))
        result = self.evaluate_expression(expr)
        self.assertEqual(result, 5.0)

    def test_string_concatenation(self):
        expr = Binary(Literal("Hello, "), Token(TokenType.PLUS, "+", None, 1), Literal("World!"))
        result = self.evaluate_expression(expr)
        self.assertEqual(result, "Hello, World!")


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
        self.assertEqual(tokens[0].literal, 123.0)
        self.assertEqual(tokens[1].lexeme, "43.67")
        self.assertEqual(tokens[1].literal, 43.67)
        self.assertEqual(tokens[2].lexeme, "89")
        self.assertEqual(tokens[2].literal, 89.0)
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

    def test_custom_1(self):
        scanner = Scanner("({(<=*=)})//Comment")
        tokens = scanner.scan_tokens()
        for t in tokens:
            print(t)
        self.assertEqual(10, len(tokens))

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
            Token(TokenType.EOF, " ", "null", 1)
        ]
        parser = Parser(tokens)
        expr = parser.parse()
        self.assertIsInstance(expr, Literal)
        self.assertEqual(expr.value, "true")

    def test_parse_boolean_false(self):
        tokens = [
            Token(TokenType.FALSE, "false", "null", 1),
            Token(TokenType.EOF, " ", "null", 1)
        ]
        parser = Parser(tokens)
        expr = parser.parse()
        self.assertIsInstance(expr, Literal)
        self.assertEqual(expr.value, "false")

    def test_parse_boolean_nil(self):
        tokens = [
            Token(TokenType.NIL, "nil", "null", 1),
            Token(TokenType.EOF, " ", "null", 1)
        ]
        parser = Parser(tokens)
        expr = parser.parse()
        self.assertIsInstance(expr, Literal)
        self.assertEqual(expr.value, "nil")


class TestSystemExit(unittest.TestCase):

    @patch('sys.exit')
    def test_exit_code_65_on_error(self, mock_exit):
        Lox.had_error = True

        with self.assertRaises(SystemExit) as cm:
            Lox.run("(73 +)", "parse")

        self.assertEqual(cm.exception.code, 65)

    @patch('sys.exit')
    def test_exit_code_65_when_attribute_error(self, mock_exit):
        with patch.object(Parser, 'parse', side_effect=AttributeError):
            with self.assertRaises(SystemExit) as cm:
                Lox.run("source_code_here", "parse")

            self.assertEqual(cm.exception.code, 65)


if __name__ == "__main__":
    unittest.main()
