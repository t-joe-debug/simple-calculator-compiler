import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from ast_nodes import *


class TestASTNodes(unittest.TestCase):

    def test_integer_literal(self):
        # Replace with the correct AST node class and constructor
        self.assertTrue(True)

    def test_binary_expression(self):
        # Replace with the correct AST node class and constructor
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
