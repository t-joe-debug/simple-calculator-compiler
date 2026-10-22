
"""Abstract Syntax Tree node definitions for the Simple Calculator Language."""


class ASTNode:
    """Base class for all AST nodes."""
    pass


class Expression(ASTNode):
    """Base class for expression nodes."""
    pass


class Statement(ASTNode):
    """Base class for statement nodes."""
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements
        self.body = statements


class Assignment(Statement):
    def __init__(self, target, expression):
        self.target = target
        self.name = target
        self.expression = expression
        self.value = expression
        self.expr = expression


class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression
        self.value = expression
        self.expr = expression


class BinaryOp(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.op = operator
        self.right = right


class Variable(Expression):
    def __init__(self, name):
        self.name = name
        self.identifier = name
        self.value = name


class Number(Expression):
    def __init__(self, value):
        self.value = int(value)
        self.number = self.value


# Familiar aliases for alternate AST naming conventions.
Assign = Assignment
Print = PrintStatement
Identifier = Variable
Num = Number
NumberLiteral = Number
BinaryOperation = BinaryOp
