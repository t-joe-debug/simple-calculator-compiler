import os
import sys
import unittest
from dataclasses import dataclass
from typing import Any, List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from semantic import SemanticAnalyzer, analyze as agreed_analyze


# Stand-in AST nodes (replace with Member 4's ast_nodes later)
@dataclass
class Number:
    value: float
    line: Optional[int] = None


@dataclass
class Variable:
    name: str
    line: Optional[int] = None


@dataclass
class BinaryOp:
    op: str
    left: Any
    right: Any
    line: Optional[int] = None


@dataclass
class Assign:
    name: str
    value: Any
    line: Optional[int] = None


@dataclass
class Print:
    expr: Any
    line: Optional[int] = None


@dataclass
class Program:
    statements: List[Any]


def analyze(*statements):
    return SemanticAnalyzer().analyze(Program(list(statements)))


class TestSemanticAnalyzer(unittest.TestCase):
    def test_valid_program(self):
        symbols, errors = analyze(
            Assign("x", Number(5), 1),
            Assign("y", BinaryOp("+", Variable("x", 2), Number(2), 2), 2),
            Print(Variable("y", 3), 3),
        )
        self.assertEqual(errors, [])
        self.assertTrue(symbols.is_defined("x"))
        self.assertTrue(symbols.is_defined("y"))

    def test_undefined_in_expression(self):
        _, errors = analyze(Assign("y", BinaryOp("+", Variable("x", 1), Number(1), 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("'x'", errors[0])

    def test_undefined_in_print(self):
        _, errors = analyze(Print(Variable("z", 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("'z'", errors[0])

    def test_self_reference_before_definition(self):
        symbols, errors = analyze(Assign("x", BinaryOp("+", Variable("x", 1), Number(1), 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertTrue(symbols.is_defined("x"))

    def test_reassignment_ok(self):
        _, errors = analyze(
            Assign("x", Number(1), 1),
            Assign("x", BinaryOp("*", Variable("x", 2), Number(3), 2), 2),
        )
        self.assertEqual(errors, [])

    def test_multiple_errors_collected(self):
        _, errors = analyze(Print(Variable("a", 1), 1), Print(Variable("b", 2), 2))
        self.assertEqual(len(errors), 2)

    def test_division_by_zero(self):
        _, errors = analyze(Assign("x", BinaryOp("/", Number(5), Number(0), 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("division by zero", errors[0])

    def test_line_number_in_message(self):
        _, errors = analyze(Print(Variable("q", 7), 7))
        self.assertIn("line 7", errors[0])

    def test_empty_program(self):
        symbols, errors = analyze()
        self.assertEqual(errors, [])
        self.assertEqual(symbols.names(), [])


class TestAgreedInterface(unittest.TestCase):
    def test_returns_list_of_errors(self):
        errors = agreed_analyze(Program([Print(Variable("a", 1), 1)]))
        self.assertIsInstance(errors, list)
        self.assertEqual(len(errors), 1)

    def test_valid_program_returns_empty_list(self):
        errors = agreed_analyze(Program([Assign("x", Number(1), 1), Print(Variable("x", 2), 2)]))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()