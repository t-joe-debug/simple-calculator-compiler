
class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        # Display a readable category without changing the token type
        categories = {
            "id": "Identifier",
            "num": "Number",
            "print": "Keyword",
            "=": "Assignment Operator",
            "+": "Operator",
            "-": "Operator",
            "*": "Operator",
            "/": "Operator",
            "(": "Special Symbol",
            ")": "Special Symbol",
            ";": "Special Symbol",
            "$": "EOF"
        }

        category = categories.get(self.type, self.type)
        return f"{self.value:<10} : {category:<20} (Line {self.line})"


def tokenize(code):
    tokens = []
    i = 0
    line = 1

    while i < len(code):
        ch = code[i]

        # Ignore spaces and tabs
        if ch in " \t\r":
            i += 1

        # Count new lines
        elif ch == "\n":
            line += 1
            i += 1

        # Ignore comments starting with #
        elif ch == "#":
            while i < len(code) and code[i] != "\n":
                i += 1

        # Identify keywords and identifiers
        elif ch.isascii() and (ch.isalpha() or ch == "_"):
            start = i

            while i < len(code) and code[i].isascii() and (
                code[i].isalnum() or code[i] == "_"
            ):
                i += 1

            word = code[start:i]

            if word == "print":
                tokens.append(Token("print", word, line))
            else:
                tokens.append(Token("id", word, line))

        # Identify integer numbers
        elif ch.isascii() and ch.isdigit():
            start = i

            while i < len(code) and code[i].isascii() and code[i].isdigit():
                i += 1

            number = code[start:i]
            tokens.append(Token("num", number, line))

        # Arithmetic operators
        elif ch in "+-*/":
            tokens.append(Token(ch, ch, line))
            i += 1

        # Assignment operator
        elif ch == "=":
            tokens.append(Token("=", ch, line))
            i += 1

        # Special symbols
        elif ch in "();":
            tokens.append(Token(ch, ch, line))
            i += 1

        # Report invalid characters
        else:
            raise SyntaxError(
                f"Lexical error: invalid character '{ch}' at line {line}"
            )

    # Add end-of-file token
    tokens.append(Token("$", "$", line))
    return tokens


if __name__ == "__main__":
    code = """
# Simple Calculator Language
x = 10 + 20;
total = x * 2;
print(total);
"""

    try:
        print("LEXICAL ANALYZER OUTPUT")
        print("-" * 65)

        tokens = tokenize(code)

        for token in tokens:
            print(token)

    except SyntaxError as error:
        print(error)
