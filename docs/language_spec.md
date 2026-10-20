# Language Specification: Simple Calculator Language

## 1. Introduction
The **Simple Calculator Language** is a simple programming language for arithmetic calculations, variable assignments, and printing values.

Our compiler has 6 team members:
- **Member 1:** Language Specification and Grammar
- **Member 2:** Lexical Analyzer (`lexer.py`)
- **Member 3:** Recursive-Descent Parser (`parser.py`)
- **Member 4:** Abstract Syntax Tree (`ast_nodes.py`)
- **Member 5:** Semantic Analyzer (`semantic.py`)
- **Member 6:** Main Integration (`main.py`)

---

## 2. Tokens (For Member 2: Lexical Analyzer)

| Token Name | Lexeme / Example | Description |
| :--- | :--- | :--- |
| `print` | `print` | Keyword to output a value |
| `id` | `x`, `a`, `total` | Variable names: letter followed by letters/digits (`[a-zA-Z_][a-zA-Z0-9_]*`) |
| `num` | `0`, `5`, `42` | Integer numbers (`[0-9]+`) |
| `=` | `=` | Assignment operator |
| `+` | `+` | Addition |
| `-` | `-` | Subtraction |
| `*` | `*` | Multiplication |
| `/` | `/` | Division |
| `(` | `(` | Left parenthesis |
| `)` | `)` | Right parenthesis |
| `;` | `;` | Semicolon (end of statement) |
| `$` | End of input | End of file (EOF) marker |

**Things ignored by the Lexer:**
- Spaces, tabs, and newlines (`[ \t\r\n]+`)
- Comments starting with `#` up to the end of the line (e.g. `# this is a comment`)

---

## 3. Language Statements

A program contains statements. Each statement ends with a semicolon (`;`).

1. **Assignment Statement:**
   ```text
   id = E ;
   ```
   *Example:* `x = 10 + 2;`

2. **Print Statement:**
   ```text
   print ( E ) ;
   ```
   *Example:* `print(x * 5);`

---

## 4. Operator Precedence and Associativity

Expressions follow standard math rules:

| Precedence | Operators | Meaning | Associativity | Grammar Non-Terminal |
| :---: | :---: | :---: | :---: | :---: |
| 1 (Highest) | `( )` | Parentheses | None | `F` (Factor) |
| 2 | `*`, `/` | Multiplication, Division | Left to Right | `T` (Term) |
| 3 (Lowest) | `+`, `-` | Addition, Subtraction | Left to Right | `E` (Expression) |

---

## 5. Team Coordination & Interfaces

### For Member 2 (Lexer):
The lexer will return tokens in this simple format:
```python
# Each token has a type, value, and line number
class Token:
    def __init__(self, type, value, line):
        self.type = type      # 'id', 'num', 'print', '+', '-', '*', '/', '=', '(', ')', ';', '$'
        self.value = value    # e.g., 'x', 42, '+'
        self.line = line      # line number in source code
```

### For Member 3 (Parser):
The recursive-descent parser uses simple functions matching the non-terminals:
- `parse_program()`
- `parse_stmt_list()`
- `parse_stmt()`
- `parse_E()` and `parse_E_prime()`
- `parse_T()` and `parse_T_prime()`
- `parse_F()`

### For Member 4 (AST Construction):
The AST classes are simple and direct:
- `AssignNode(name, expr)`
- `PrintNode(expr)`
- `BinOpNode(left, op, right)`
- `NumNode(value)`
- `VarNode(name)`
