
"""Abstract Syntax Tree node definitions."""


class Program:
    def __init__(self, statements):
        self.statements = statements
        self.body = statements


class Assignment:
    def __init__(self, target, expression):
        self.target = target
        self.name = target
        self.expression = expression
        self.value = expression
        self.expr = expression


class PrintStatement:
    def __init__(self, expression):
        self.expression = expression
        self.value = expression
        self.expr = expression


class BinaryOp:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.op = operator
        self.right = right


class Variable:
    def __init__(self, name):
        self.name = name
        self.identifier = name
        self.value = name


class Number:
    def __init__(self, value):
        self.value = int(value)
        self.number = self.value


# Familiar aliases for code that uses alternate AST naming conventions.
Assign = Assignment
Print = PrintStatement
Identifier = Variable
Num = Number
NumberLiteral = Number
BinaryOperation = BinaryOp
