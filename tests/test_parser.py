
import unittest

from src.parser import parse, parse_source
from src.ast_nodes import Assignment, PrintStatement, BinaryOp, Variable, Number
from src.lexer import tokenize


class TestParser(unittest.TestCase):

    def test_assignment(self):
        ast = parse_source("x = 10;")

        self.assertEqual(len(ast.statements), 1)
        statement = ast.statements[0]

        self.assertIsInstance(statement, Assignment)
        self.assertEqual(statement.target, "x")
        self.assertIsInstance(statement.expression, Number)
        self.assertEqual(statement.expression.value, 10)

    def test_print_statement(self):
        ast = parse_source("print(42);")

        self.assertIsInstance(ast.statements[0], PrintStatement)
        self.assertEqual(ast.statements[0].expression.value, 42)

    def test_operator_precedence(self):
        ast = parse_source("x = 2 + 3 * 4;")
        expression = ast.statements[0].expression

        self.assertIsInstance(expression, BinaryOp)
        self.assertEqual(expression.operator, "+")
        self.assertIsInstance(expression.right, BinaryOp)
        self.assertEqual(expression.right.operator, "*")

    def test_parentheses(self):
        ast = parse_source("x = (2 + 3) * 4;")
        expression = ast.statements[0].expression

        self.assertEqual(expression.operator, "*")
        self.assertIsInstance(expression.left, BinaryOp)
        self.assertEqual(expression.left.operator, "+")

    def test_modulo(self):
        ast = parse_source("x = 10 % 3;")
        expression = ast.statements[0].expression

        self.assertIsInstance(expression, BinaryOp)
        self.assertEqual(expression.operator, "%")

    def test_multiple_statements(self):
        ast = parse_source(
            "x = 10; y = x + 2; print(y);"
        )

        self.assertEqual(len(ast.statements), 3)
        self.assertIsInstance(ast.statements[0], Assignment)
        self.assertIsInstance(ast.statements[1], Assignment)
        self.assertIsInstance(ast.statements[2], PrintStatement)

    def test_variable_expression(self):
        ast = parse_source("x = y;")

        self.assertIsInstance(
            ast.statements[0].expression, Variable
        )
        self.assertEqual(
            ast.statements[0].expression.name, "y"
        )

    def test_missing_semicolon(self):
        with self.assertRaises(SyntaxError):
            parse_source("x = 10")

    def test_missing_parenthesis(self):
        with self.assertRaises(SyntaxError):
            parse_source("print(10;")

    def test_invalid_expression(self):
        with self.assertRaises(SyntaxError):
            parse_source("x = + 2;")

    def test_unexpected_statement(self):
        with self.assertRaises(SyntaxError):
            parse_source("print 10;")

    def test_parse_token_list(self):
        ast = parse(tokenize("x = 7;"))
        self.assertEqual(len(ast.statements), 1)


if __name__ == "__main__":
    unittest.main()
