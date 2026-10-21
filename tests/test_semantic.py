"""
test_semantic.py - tests for semantic.py (Member 5)

Run from the project root:
    python -m unittest tests/test_semantic.py -v

The classes below are stand-ins so the tests run on their own.
"""
import os
import sys
import unittest
from dataclasses import dataclass
from typing import Any, List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from semantic import SemanticAnalyzer, analyze as agreed_analyze  # noqa: E402


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
class UnaryOp:
    op: str
    operand: Any
    line: Optional[int] = None


@dataclass
class Assign:
    name: Any
    value: Any
    line: Optional[int] = None


@dataclass
class Print:
    expr: Any
    line: Optional[int] = None


@dataclass
class Program:
    statements: List[Any]


def run(*statements):
    return SemanticAnalyzer().analyze(Program(list(statements)))


class TestUndefinedVariables(unittest.TestCase):
    def test_valid_program(self):
        symbols, errors = run(
            Assign("x", Number(5), 1),
            Assign("y", BinaryOp("+", Variable("x", 2), Number(2), 2), 2),
            Print(Variable("y", 3), 3),
        )
        self.assertEqual(errors, [])
        self.assertTrue(symbols.is_defined("x"))
        self.assertTrue(symbols.is_defined("y"))

    def test_undefined_in_expression(self):
        _, errors = run(Assign("y", BinaryOp("+", Variable("x", 1), Number(1), 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("'x'", errors[0])

    def test_undefined_in_print(self):
        _, errors = run(Print(Variable("z", 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("'z'", errors[0])

    def test_self_reference_before_definition(self):
        symbols, errors = run(Assign("x", BinaryOp("+", Variable("x", 1), Number(1), 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertTrue(symbols.is_defined("x"))

    def test_reassignment_ok(self):
        _, errors = run(
            Assign("x", Number(1), 1),
            Assign("x", BinaryOp("*", Variable("x", 2), Number(3), 2), 2),
        )
        self.assertEqual(errors, [])

    def test_use_before_later_definition(self):
        _, errors = run(Print(Variable("a", 1), 1), Assign("a", Number(1), 2))
        self.assertEqual(len(errors), 1)

    def test_multiple_errors_collected(self):
        _, errors = run(Print(Variable("a", 1), 1), Print(Variable("b", 2), 2))
        self.assertEqual(len(errors), 2)

    def test_line_number_in_message(self):
        _, errors = run(Print(Variable("q", 7), 7))
        self.assertIn("line 7", errors[0])

    def test_empty_program(self):
        symbols, errors = run()
        self.assertEqual(errors, [])
        self.assertEqual(symbols.names(), [])


class TestZeroChecks(unittest.TestCase):
    def test_division_by_zero(self):
        _, errors = run(Assign("x", BinaryOp("/", Number(5), Number(0), 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("division by zero", errors[0])

    def test_modulo_by_zero(self):
        _, errors = run(Assign("x", BinaryOp("%", Number(5), Number(0), 1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("modulo by zero", errors[0])

    def test_zero_from_constant_expression(self):
        # 10 / (3 - 3)
        expr = BinaryOp("/", Number(10), BinaryOp("-", Number(3), Number(3)), 1)
        _, errors = run(Print(expr, 1))
        self.assertEqual(len(errors), 1)

    def test_division_by_variable_not_flagged(self):
        _, errors = run(
            Assign("d", Number(0), 1),
            Print(BinaryOp("/", Number(4), Variable("d", 2), 2), 2),
        )
        self.assertEqual(errors, [])

    def test_division_by_nonzero_ok(self):
        _, errors = run(Print(BinaryOp("/", Number(4), Number(2), 1), 1))
        self.assertEqual(errors, [])

    def test_unary_minus_visited(self):
        _, errors = run(Print(UnaryOp("-", Variable("u", 1), 1), 1))
        self.assertEqual(len(errors), 1)


class TestAssignmentTargets(unittest.TestCase):
    def test_reserved_word_target(self):
        _, errors = run(Assign("print", Number(1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("reserved word", errors[0])

    def test_invalid_name_target(self):
        _, errors = run(Assign("9x", Number(1), 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("invalid assignment target", errors[0])

    def test_variable_node_as_target(self):
        symbols, errors = run(Assign(Variable("t"), Number(1), 1))
        self.assertEqual(errors, [])
        self.assertTrue(symbols.is_defined("t"))


class TestWarningsAndTable(unittest.TestCase):
    def test_unused_variable_warning(self):
        analyzer = SemanticAnalyzer()
        _, errors = analyzer.analyze(Program([Assign("x", Number(1), 1)]))
        self.assertEqual(errors, [])
        self.assertEqual(len(analyzer.warnings), 1)
        self.assertIn("'x'", analyzer.warnings[0])

    def test_used_variable_no_warning(self):
        analyzer = SemanticAnalyzer()
        analyzer.analyze(Program([Assign("x", Number(1), 1), Print(Variable("x", 2), 2)]))
        self.assertEqual(analyzer.warnings, [])

    def test_symbol_table_text(self):
        symbols, _ = run(Assign("x", Number(1), 4))
        self.assertIn("x", str(symbols))
        self.assertIn("4", str(symbols))


class TestAgreedInterface(unittest.TestCase):
    def test_returns_list_of_errors(self):
        errors = agreed_analyze(Program([Print(Variable("a", 1), 1)]))
        self.assertIsInstance(errors, list)
        self.assertEqual(len(errors), 1)

    def test_valid_program_returns_empty_list(self):
        errors = agreed_analyze(Program([Assign("x", Number(1), 1), Print(Variable("x", 2), 2)]))
        self.assertEqual(errors, [])


class TestOtherNodeNames(unittest.TestCase):
    """Works even if Member 4 uses different class/field names."""

    def test_alternative_names(self):
        @dataclass
        class Num:
            value: int

        @dataclass
        class Identifier:
            name: str

        @dataclass
        class BinOp:
            operator: str
            lhs: Any
            rhs: Any

        @dataclass
        class AssignStmt:
            target: str
            expr: Any

        @dataclass
        class PrintStmt:
            expression: Any

        @dataclass
        class Block:
            body: list

        tree = Block([
            AssignStmt("a", Num(1)),
            PrintStmt(BinOp("%", Identifier("a"), Num(0))),
            PrintStmt(Identifier("missing")),
        ])
        errors = agreed_analyze(tree)
        self.assertEqual(len(errors), 2)

    def test_unknown_node_reported(self):
        class Weird:
            pass

        errors = agreed_analyze(Program([Weird()]))
        self.assertEqual(len(errors), 1)
        self.assertIn("unsupported AST node", errors[0])


if __name__ == "__main__":
    unittest.main()