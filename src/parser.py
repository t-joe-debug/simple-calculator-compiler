
"""Recursive-descent parser for the Simple Calculator Language."""

try:
    from .lexer import tokenize
    from .ast_nodes import (
        Program,
        Assignment,
        PrintStatement,
        BinaryOp,
        Variable,
        Number,
    )
except ImportError:
    from lexer import tokenize
    from ast_nodes import (
        Program,
        Assignment,
        PrintStatement,
        BinaryOp,
        Variable,
        Number,
    )


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.position]

    def advance(self):
        token = self.current()
        if token.type != "$":
            self.position += 1
        return token

    def expect(self, token_type):
        token = self.current()

        if token.type != token_type:
            raise SyntaxError(
                f"Syntax error at line {token.line}: "
                f"expected '{token_type}', got '{token.value}'"
            )

        return self.advance()

    def parse(self):
        statements = []

        while self.current().type != "$":
            previous_position = self.position
            statements.append(self.parse_statement())

            if self.position == previous_position:
                raise SyntaxError("Parser made no progress.")

        self.expect("$")
        return Program(statements)

    def parse_statement(self):
        token = self.current()

        if token.type == "id":
            target = self.advance().value
            self.expect("=")
            expression = self.parse_expression()
            self.expect(";")
            return Assignment(target, expression)

        if token.type == "print":
            self.advance()
            self.expect("(")
            expression = self.parse_expression()
            self.expect(")")
            self.expect(";")
            return PrintStatement(expression)

        raise SyntaxError(
            f"Syntax error at line {token.line}: "
            f"expected an assignment or print statement, "
            f"got '{token.value}'"
        )

    def parse_expression(self):
        """E -> T ((+ | -) T)*"""
        node = self.parse_term()

        while self.current().type in ("+", "-"):
            operator = self.advance().type
            right = self.parse_term()
            node = BinaryOp(node, operator, right)

        return node

    def parse_term(self):
        """T -> F ((* | / | %) F)*"""
        node = self.parse_factor()

        while self.current().type in ("*", "/", "%"):
            operator = self.advance().type
            right = self.parse_factor()
            node = BinaryOp(node, operator, right)

        return node

    def parse_factor(self):
        """F -> (E) | id | num"""
        token = self.current()

        if token.type == "(":
            self.advance()
            node = self.parse_expression()
            self.expect(")")
            return node

        if token.type == "id":
            self.advance()
            return Variable(token.value)

        if token.type == "num":
            self.advance()
            return Number(token.value)

        raise SyntaxError(
            f"Syntax error at line {token.line}: "
            f"expected a number, identifier, or '(', "
            f"got '{token.value}'"
        )


def parse(tokens):
    """Parse a token list and return the Program AST."""
    return Parser(tokens).parse()


def parse_source(source):
    """Tokenize and parse source code in one call."""
    return parse(tokenize(source))


if __name__ == "__main__":
    source = """
    x = 10 + 20;
    total = x * 2;
    print(total);
    """

    try:
        ast = parse_source(source)
        print("Parsing successful!")
        print(f"AST: {ast!r}")
        print(f"Statements parsed: {len(ast.statements)}")
    except (SyntaxError, ValueError) as error:
        print(error)
