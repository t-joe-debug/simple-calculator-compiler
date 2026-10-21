
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
            "+": "Arithmetic Operator",
            "-": "Arithmetic Operator",
            "*": "Arithmetic Operator",
            "/": "Arithmetic Operator",
            "%": "Arithmetic Operator",
            "(": "Special Symbol",
            ")": "Special Symbol",
            ";": "Special Symbol",
            "$": "End of Input"
        }
        category = categories.get(self.type, self.type)
        return f"{self.value:<10} : {category:<20} (Line {self.line})"


def tokenize(text):
    tokens = []
    i = 0
    line = 1

    while i < len(text):
        ch = text[i]

        if ch in " \t\r":
            i += 1

        elif ch == "\n":
            line += 1
            i += 1

        elif ch == "#":
            while i < len(text) and text[i] != "\n":
                i += 1

        elif ch.isascii() and (ch.isalpha() or ch == "_"):
            start = i

            while i < len(text) and text[i].isascii() and (
                text[i].isalnum() or text[i] == "_"
            ):
                i += 1

            word = text[start:i]

            if word == "print":
                tokens.append(Token("print", word, line))
            else:
                tokens.append(Token("id", word, line))

        elif ch.isascii() and ch.isdigit():
            start = i

            while i < len(text) and text[i].isascii() and text[i].isdigit():
                i += 1

            number = text[start:i]
            tokens.append(Token("num", number, line))

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


if __name__ == "__main__":
    code = """
# Simple Calculator Language
x = 10 + 20;
total = x * 2;
remainder = total % 3;
print(remainder);
"""

    try:
        print("LEXICAL ANALYZER OUTPUT")
        print("-" * 65)

        tokens = tokenize(code)

        for token in tokens:
            print(token)

    except SyntaxError as error:
        print(error)
