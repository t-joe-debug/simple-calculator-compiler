"""
AST node definitions for the Simple Calculator Language.
"""


class ASTNode:
    pass


class Expression(ASTNode):
    pass


class Statement(ASTNode):
    pass


class Number(Expression):
    def __init__(self, value):
        self.value = value


class Variable(Expression):
    def __init__(self, name):
        self.name = name


class BinaryOp(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Assignment(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class PrintStatement(Statement):
    def __init__(self, value):
        self.value = value


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements
