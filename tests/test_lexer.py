
import unittest
import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_path))

from lexer import tokenize


class TestLexer(unittest.TestCase):

    def test_identifiers_and_numbers(self):
        tokens = tokenize("x = 123;")

        self.assertEqual(tokens[0].type, "id")
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(tokens[2].type, "num")
        self.assertEqual(tokens[2].value, "123")

    def test_print_keyword(self):
        tokens = tokenize("print(10);")
        self.assertEqual(tokens[0].type, "print")

    def test_arithmetic_operators(self):
        tokens = tokenize("x = 2 + 3 - 4 * 5 / 2 % 3;")
        types = [token.type for token in tokens]

        for operator in ["+", "-", "*", "/", "%"]:
            self.assertIn(operator, types)

    def test_assignment_operator(self):
        tokens = tokenize("x = 5;")
        self.assertEqual(tokens[1].type, "=")

    def test_special_symbols(self):
        tokens = tokenize("print(x);")
        types = [token.type for token in tokens]

        self.assertIn("(", types)
        self.assertIn(")", types)
        self.assertIn(";", types)

    def test_comments(self):
        tokens = tokenize("x = 5; # comment")
        values = [token.value for token in tokens]

        self.assertNotIn("#", values)
        self.assertIn("5", values)

    def test_line_numbers(self):
        tokens = tokenize("x = 5;\nprint(x);")

        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[4].line, 2)

    def test_end_of_input(self):
        tokens = tokenize("x = 5;")
        self.assertEqual(tokens[-1].type, "$")

    def test_invalid_character(self):
        with self.assertRaisesRegex(SyntaxError, "invalid character '@'"):
            tokenize("x = 5 @ 2;")

    def test_invalid_character_on_second_line(self):
        with self.assertRaisesRegex(SyntaxError, "line 2"):
            tokenize("x = 5;\n@")

    def test_empty_input(self):
        tokens = tokenize("")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, "$")

    def test_underscore_identifier(self):
        tokens = tokenize("total_sum = 25;")

        self.assertEqual(tokens[0].type, "id")
        self.assertEqual(tokens[0].value, "total_sum")


if __name__ == "__main__":
    unittest.main()
