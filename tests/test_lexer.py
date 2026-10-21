
import unittest
import sys
from pathlib import Path

# Add the src folder to Python's import path
src_path = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_path))

from lexer import tokenize


class TestLexer(unittest.TestCase):

    def test_identifiers_and_numbers(self):
        tokens = tokenize("x = 123;")
        self.assertEqual(tokens[0].type, "id")
        self.assertEqual(tokens[2].type, "num")

    def test_operators(self):
        tokens = tokenize("x = 2 + 3 * 4;")
        types = [token.type for token in tokens]

        self.assertIn("+", types)
        self.assertIn("*", types)
        self.assertIn("=", types)

    def test_special_symbols(self):
        tokens = tokenize("print(x);")
        types = [token.type for token in tokens]

        self.assertIn("(", types)
        self.assertIn(")", types)
        self.assertIn(";", types)

    def test_keyword(self):
        tokens = tokenize("print(10);")
        self.assertEqual(tokens[0].type, "print")

    def test_comments(self):
        tokens = tokenize("x = 5; # this is a comment")
        values = [token.value for token in tokens]

        self.assertNotIn("#", values)
        self.assertIn("5", values)

    def test_end_of_file(self):
        tokens = tokenize("x = 5;")
        self.assertEqual(tokens[-1].type, "$")

    def test_invalid_character(self):
        with self.assertRaises(SyntaxError):
            tokenize("x = 5 @ 2;")


if __name__ == "__main__":
    unittest.main()
