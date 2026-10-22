
"""Lexer for the Simple Calculator Language."""


class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        categories = {
            "id": "Identifier",
            "num": "Number",
            "print": "Keyword",
            "=": "Assignment Operator",
            "+": "Operator",
            "-": "Operator",
            "*": "Operator",
            "/": "Operator",
            "%": "Operator",
            "(": "Special Symbol",
            ")": "Special Symbol",
            ";": "Special Symbol",
            "$": "EOF",
        }
        category = categories.get(self.type, self.type)
        return f"{self.value:<10} : {category:<20} (Line {self.line})"


def tokenize(code):
    tokens = []
    i = 0
    line = 1

    while i < len(code):
        ch = code[i]

        if ch in " \t\r":
            i += 1

        elif ch == "\n":
            line += 1
            i += 1

        elif ch == "#":
            while i < len(code) and code[i] != "\n":
                i += 1

        elif ch.isascii() and (ch.isalpha() or ch == "_"):
            start = i

            while i < len(code) and code[i].isascii() and (
                code[i].isalnum() or code[i] == "_"
            ):
                i += 1

            word = code[start:i]
            token_type = "print" if word == "print" else "id"
            tokens.append(Token(token_type, word, line))

        elif ch.isascii() and ch.isdigit():
            start = i

            while i < len(code) and code[i].isascii() and code[i].isdigit():
                i += 1

            tokens.append(Token("num", code[start:i], line))

        elif ch in "+-*/%":
            tokens.append(Token(ch, ch, line))
            i += 1

        elif ch == "=":
            tokens.append(Token("=", ch, line))
            i += 1

        elif ch in "();":
            tokens.append(Token(ch, ch, line))
            i += 1

        else:
            raise SyntaxError(
                f"Lexical error: invalid character '{ch}' at line {line}"
            )

    tokens.append(Token("$", "$", line))
    return tokens
