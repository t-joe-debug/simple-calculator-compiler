import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from ast_nodes import (
    ASTNode,
    Expression,
    Statement,
    Number,
    Variable,
    BinaryOp,
    Assignment,
    PrintStatement,
    Program,
)


class TestASTConstruction(unittest.TestCase):

    def test_number_node(self):
        node = Number(42)
        self.assertEqual(node.value, 42)
        self.assertIsInstance(node, Expression)

    def test_variable_node(self):
        node = Variable("x")
        self.assertEqual(node.name, "x")
        self.assertIsInstance(node, Expression)

    def test_binary_operation_node(self):
        left = Number(2)
        right = Number(3)
        node = BinaryOp(left, "+", right)

        self.assertIs(node.left, left)
        self.assertEqual(node.operator, "+")
        self.assertIs(node.right, right)

    def test_assignment_node(self):
        value = Number(10)
        node = Assignment("x", value)

        self.assertEqual(node.name, "x")
        self.assertIs(node.value, value)
        self.assertIsInstance(node, Statement)

    def test_print_statement_node(self):
        value = Variable("x")
        node = PrintStatement(value)

        self.assertIs(node.value, value)
        self.assertIsInstance(node, Statement)

    def test_program_node(self):
        statements = [
            Assignment("x", Number(5)),
            PrintStatement(Variable("x")),
        ]
        program = Program(statements)

        self.assertEqual(program.statements, statements)
        self.assertEqual(len(program.statements), 2)


if __name__ == "__main__":
    unittest.main()
