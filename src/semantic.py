"""
semantic.py - Semantic Analyzer (Member 5)

Checks a parsed AST of the Simple Calculator Language for:
  1. use of undefined variables
  2. invalid assignment targets (bad names, reserved word 'print')
  3. division / modulo by a constant zero (e.g. 5 / 0, 7 % (2 - 2))
and builds a symbol table. Variables that are assigned but never used are
reported separately as warnings (they are NOT errors).

Public interface (agreed with the team):
    analyze(ast) -> list of error message strings (empty list = no errors)

Extra API:
    SemanticAnalyzer().analyze(ast) -> (symbol_table, errors)
    SemanticAnalyzer().warnings     -> list of warning strings

The analyzer is tolerant about node/field names so it works with whatever
AST classes Member 4 writes. See docs/semantic_interface.md.
"""

import re

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
RESERVED_WORDS = {"print"}
_MISSING = object()

# normalised class name -> canonical node kind
_KINDS = {
    "program": "program", "block": "program", "module": "program",
    "statementlist": "program", "stmtlist": "program",
    "assign": "assign", "assignment": "assign",
    "print": "print",
    "binary": "binary", "binop": "binary", "binaryop": "binary",
    "binaryoperation": "binary",
    "unary": "unary", "unaryop": "unary", "unaryoperation": "unary",
    "number": "number", "num": "number", "literal": "number",
    "intliteral": "number", "integer": "number", "int": "number",
    "constant": "number", "numberliteral": "number",
    "variable": "variable", "var": "variable", "identifier": "variable",
    "id": "variable", "name": "variable",
}

# canonical kind -> accepted attribute names (first match wins)
_FIELDS = {
    "statements": ("statements", "body", "stmts", "children"),
    "target": ("name", "target", "id", "var", "variable"),
    "value": ("value", "expr", "expression", "rhs", "right"),
    "print_expr": ("expr", "expression", "value", "arg", "argument"),
    "op": ("op", "operator"),
    "left": ("left", "lhs"),
    "right": ("right", "rhs"),
    "operand": ("operand", "expr", "expression", "value", "right"),
    "number": ("value", "num", "n"),
    "var_name": ("name", "id", "identifier"),
}


def _kind(node):
    """Canonical kind of an AST node, from its class name."""
    name = type(node).__name__.lower()
    for suffix in ("node", "statement", "stmt", "expression", "expr"):
        if name.endswith(suffix) and len(name) > len(suffix):
            name = name[: -len(suffix)]
            break
    return _KINDS.get(name)


def _get(node, field):
    """First existing attribute of `node` among the accepted names."""
    for attr in _FIELDS[field]:
        if hasattr(node, attr):
            return getattr(node, attr)
    return _MISSING


def _op_text(op):
    """Operator as a plain string (accepts str or token-like objects)."""
    if isinstance(op, str):
        return op
    for attr in ("value", "lexeme", "text", "symbol"):
        if isinstance(getattr(op, attr, None), str):
            return getattr(op, attr)
    return str(op)


class SymbolTable:
    """Tracks the variables defined in the program."""

    def __init__(self):
        self._symbols = {}

    def define(self, name, line=None):
        """Register a variable. Re-assignment keeps the first definition."""
        if name not in self._symbols:
            self._symbols[name] = {"line": line}

    def is_defined(self, name):
        return name in self._symbols

    def lookup(self, name):
        return self._symbols.get(name)

    def names(self):
        return list(self._symbols)

    def __len__(self):
        return len(self._symbols)

    def __str__(self):
        if not self._symbols:
            return "Symbol Table: (empty)"
        rows = ["Symbol Table:", f"  {'Name':<14}{'Defined at line'}"]
        for name, info in self._symbols.items():
            line = info["line"] if info["line"] is not None else "-"
            rows.append(f"  {name:<14}{line}")
        return "\n".join(rows)


class SemanticAnalyzer:
    """Walks the AST, fills the symbol table and collects errors/warnings."""

    def __init__(self):
        self.symbols = SymbolTable()
        self.errors = []
        self.warnings = []
        self._used = set()

    # ---- public API -------------------------------------------------
    def analyze(self, program):
        """Analyze an AST. Returns (symbol_table, errors)."""
        self.symbols = SymbolTable()
        self.errors = []
        self.warnings = []
        self._used = set()
        self._visit(program)
        for name in self.symbols.names():
            if name not in self._used:
                line = self.symbols.lookup(name)["line"]
                where = f" (line {line})" if line is not None else ""
                self.warnings.append(
                    f"Semantic Warning{where}: variable '{name}' is assigned but never used"
                )
        return self.symbols, self.errors

    # ---- helpers ----------------------------------------------------
    @staticmethod
    def _line(node):
        for attr in ("line", "lineno", "line_no"):
            if getattr(node, attr, None) is not None:
                return getattr(node, attr)
        return None

    def _error(self, message, node):
        line = self._line(node)
        where = f" (line {line})" if line is not None else ""
        self.errors.append(f"Semantic Error{where}: {message}")

    def _need(self, node, field, kind):
        value = _get(node, field)
        if value is _MISSING:
            self._error(f"malformed {kind} node (missing '{field}')", node)
        return value

    def _visit(self, node):
        kind = _kind(node)
        method = getattr(self, "_visit_" + str(kind), None)
        if method is None:
            self._error(f"unsupported AST node '{type(node).__name__}'", node)
            return
        method(node)

    def _const(self, node):
        """Value of a constant expression, or None if not constant."""
        kind = _kind(node)
        if kind == "number":
            value = _get(node, "number")
            return value if isinstance(value, (int, float)) else None
        if kind == "unary":
            operand, op = _get(node, "operand"), _get(node, "op")
            if operand is _MISSING or op is _MISSING:
                return None
            value = self._const(operand)
            if value is None:
                return None
            op = _op_text(op)
            return -value if op == "-" else value if op == "+" else None
        if kind == "binary":
            left, right, op = _get(node, "left"), _get(node, "right"), _get(node, "op")
            if _MISSING in (left, right, op):
                return None
            a, b = self._const(left), self._const(right)
            if a is None or b is None:
                return None
            op = _op_text(op)
            if op == "+":
                return a + b
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if op in ("/", "%") and b != 0:
                return a / b if op == "/" else a % b
        return None

    # ---- node visitors ----------------------------------------------
    def _visit_program(self, node):
        statements = self._need(node, "statements", "program")
        if statements is _MISSING:
            return
        for stmt in statements:
            self._visit(stmt)

    def _visit_assign(self, node):
        target = self._need(node, "target", "assignment")
        value = self._need(node, "value", "assignment")
        if value is not _MISSING:
            # Check the right side FIRST so `x = x + 1` fails if x is undefined.
            self._visit(value)
        if target is _MISSING:
            return
        if not isinstance(target, str) and _kind(target) == "variable":
            target = _get(target, "var_name")
        if not isinstance(target, str) or not _IDENT.match(target):
            self._error(f"invalid assignment target '{target}'", node)
        elif target in RESERVED_WORDS:
            self._error(f"cannot assign to reserved word '{target}'", node)
        else:
            self.symbols.define(target, self._line(node))

    def _visit_print(self, node):
        expr = self._need(node, "print_expr", "print")
        if expr is not _MISSING:
            self._visit(expr)

    def _visit_binary(self, node):
        left = self._need(node, "left", "binary operation")
        right = self._need(node, "right", "binary operation")
        op = self._need(node, "op", "binary operation")
        if left is not _MISSING:
            self._visit(left)
        if right is not _MISSING:
            self._visit(right)
        if right is not _MISSING and op is not _MISSING:
            op = _op_text(op)
            if op in ("/", "%") and self._const(right) == 0:
                what = "division" if op == "/" else "modulo"
                self._error(f"{what} by zero", node)

    def _visit_unary(self, node):
        operand = self._need(node, "operand", "unary operation")
        if operand is not _MISSING:
            self._visit(operand)

    def _visit_number(self, node):
        pass

    def _visit_variable(self, node):
        name = self._need(node, "var_name", "variable")
        if name is _MISSING:
            return
        self._used.add(name)
        if not self.symbols.is_defined(name):
            self._error(f"variable '{name}' used before assignment", node)


def analyze(ast):
    """Agreed team interface: returns a list of semantic error messages."""
    _, errors = SemanticAnalyzer().analyze(ast)
    return errors