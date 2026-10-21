"""
semantic.py - Semantic Analyzer (Member 5)
Checks an AST for undefined variables and division by zero,
and builds a symbol table.
"""


class SymbolTable:
    """Tracks variables defined in the program."""

    def __init__(self):
        self._symbols = {}

    def define(self, name, line=None):
        if name not in self._symbols:
            self._symbols[name] = {"line": line}

    def is_defined(self, name):
        return name in self._symbols

    def lookup(self, name):
        return self._symbols.get(name)

    def names(self):
        return list(self._symbols)

    def __str__(self):
        if not self._symbols:
            return "Symbol Table: (empty)"
        rows = ["Symbol Table:", f"  {'Name':<12}{'Defined at line'}"]
        for name, info in self._symbols.items():
            line = info["line"] if info["line"] is not None else "-"
            rows.append(f"  {name:<12}{line}")
        return "\n".join(rows)


class SemanticAnalyzer:
    """Walks the AST, fills the symbol table and collects errors."""

    def __init__(self):
        self.symbols = SymbolTable()
        self.errors = []

    def analyze(self, program):
        """Returns (symbol_table, errors)."""
        self.symbols = SymbolTable()
        self.errors = []
        self._visit(program)
        return self.symbols, self.errors

    def _error(self, message, node):
        line = getattr(node, "line", None)
        prefix = f"Semantic Error (line {line}): " if line is not None else "Semantic Error: "
        self.errors.append(prefix + message)

    def _visit(self, node):
        method = getattr(self, "_visit_" + type(node).__name__, None)
        if method is None:
            self._error(f"unknown AST node '{type(node).__name__}'", node)
            return
        method(node)

    def _visit_Program(self, node):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_Assign(self, node):
        # Check the right side FIRST so `x = x + 1` fails if x is undefined.
        self._visit(node.value)
        self.symbols.define(node.name, getattr(node, "line", None))

    def _visit_Print(self, node):
        self._visit(node.expr)

    def _visit_BinaryOp(self, node):
        self._visit(node.left)
        self._visit(node.right)
        if node.op == "/" and type(node.right).__name__ == "Number" and node.right.value == 0:
            self._error("division by zero", node)

    def _visit_Number(self, node):
        pass

    def _visit_Variable(self, node):
        if not self.symbols.is_defined(node.name):
            self._error(f"variable '{node.name}' used before assignment", node)
def analyze(ast):
    """Agreed team interface: returns a list of semantic error messages."""
    _, errors = SemanticAnalyzer().analyze(ast)
    return errors