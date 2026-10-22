# Simple Calculator Compiler

A compiler front end for a simple calculator language built as a mini project for the **Compiler Design** course (B.Tech CSE, S5).

The compiler supports **variable assignments**, **arithmetic operations**, **modulo**, and **print() statements**. It produces an **Abstract Syntax Tree (AST)** for every valid program and performs **semantic checks** through a symbol table.

---

## Team Members

| # | Name | Module |
|---|------|--------|
| 1 | Meliza Mariya Byiju | Language Specification and Grammar |
| 2 | Sandra Anna Biju | Lexical Analyzer |
| 3 | Robin B Philip | Syntax Analyzer (Parser) |
| 4 | Parvathy A Nair | AST Construction |
| 5 | Vaisakh Rajesh | Semantic Analyzer |
| 6 | Tijo Joe Joseph | Main Program and Integration |

---

## Project Structure

```
simple-calculator-compiler/
├── docs/
│   ├── grammar.txt                  # Formal CFG and LL(1) grammar (Member 1)
│   ├── language_spec.md             # Language specification and token definitions (Member 1)
│   ├── grammar_transformations.md   # Left-recursion elimination, FIRST/FOLLOW sets, LL(1) parsing table (Member 1)
│   ├── grammar_test_cases.md        # Valid and invalid grammar test cases (Member 1)
│   └── semantic_interface.md        # Semantic analyzer interface documentation (Member 5)
├── src/
│   ├── lexer.py                     # Tokenizer / Lexical Analyzer (Member 2)
│   ├── parser.py                    # Recursive-descent parser (Member 3)
│   ├── ast_nodes.py                 # AST node class definitions (Member 4)
│   ├── ast_printer.py               # Human-readable AST display (Member 4)
│   ├── semantic.py                  # Semantic analyzer and symbol table (Member 5)
│   └── gui.py                       # Tkinter GUI - full compiler interface (Member 6)
├── tests/
│   ├── test_lexer.py                # Lexer unit tests (Member 2)
│   ├── test_parser.py               # Parser unit tests (Member 3)
│   ├── test_ast.py                  # AST unit tests (Member 4)
│   └── test_semantic.py             # Semantic analyzer unit tests (Member 5)
├── .gitignore
└── README.md
```

---

## Language Specification

### Supported Statements

```text
# Variable assignment
x = 10 + 5;

# Print statement
print(x);
```

### Supported Operators

| Operator | Operation | Precedence | Associativity |
|:--------:|-----------|:----------:|:-------------:|
| `( )` | Grouping | Highest | — |
| `*` | Multiplication | 2 | Left to Right |
| `/` | Division | 2 | Left to Right |
| `%` | Modulo | 2 | Left to Right |
| `+` | Addition | 3 | Left to Right |
| `-` | Subtraction | 3 | Left to Right |

### Tokens

| Token | Pattern / Lexeme | Description |
|-------|-----------------|-------------|
| `id` | `[a-zA-Z_][a-zA-Z0-9_]*` | Variable name |
| `num` | `[0-9]+` | Integer literal |
| `print` | `print` | Keyword |
| `=` | `=` | Assignment |
| `+` `-` `*` `/` `%` | Arithmetic | Operators |
| `(` `)` | Parentheses | Grouping |
| `;` | `;` | Statement terminator |

**Ignored by the lexer:** spaces, tabs, newlines, and `#` single-line comments.

---

## Grammar (LL(1), Left-Recursion Eliminated)

```text
Program  -> StmtList $

StmtList -> Stmt StmtList | ε

Stmt     -> id = E ;
          | print ( E ) ;

E        -> T E'
E'       -> + T E'  |  - T E'  |  ε

T        -> F T'
T'       -> * F T'  |  / F T'  |  % F T'  |  ε

F        -> ( E )  |  id  |  num
```

See [`docs/grammar.txt`](docs/grammar.txt) and [`docs/grammar_transformations.md`](docs/grammar_transformations.md) for the complete derivation, FIRST/FOLLOW sets, and LL(1) parsing table.

---

## Modules

### Member 1 — Language Specification and Grammar (`docs/`)
Defines all language rules: tokens, CFG, operator precedence and associativity, ambiguity elimination, left-recursion elimination, left-factoring analysis, FIRST/FOLLOW sets, and the LL(1) parsing table. Also provides grammar test cases for valid and invalid inputs.

### Member 2 — Lexical Analyzer (`src/lexer.py`)
Reads source code character by character and produces a list of `Token` objects. Supports all arithmetic operators including `%`. Ignores whitespace and `#` comments. Reports a `SyntaxError` on invalid characters.

```python
from src.lexer import tokenize
tokens = tokenize("x = 10 + 5;")
```

### Member 3 — Syntax Analyzer / Parser (`src/parser.py`)
Recursive-descent parser implementing one function per grammar non-terminal (`parse_expression`, `parse_term`, `parse_factor`, etc.). Returns a `Program` AST node. Raises `SyntaxError` with the line number on invalid syntax.

```python
from src.parser import parse_source
tree = parse_source("x = 10 + 5; print(x);")
```

### Member 4 — AST Construction (`src/ast_nodes.py`, `src/ast_printer.py`)
Defines all AST node classes:
- `Program(statements)`
- `Assignment(target, expression)`
- `PrintStatement(expression)`
- `BinaryOp(left, operator, right)`
- `Number(value)`
- `Variable(name)`

`ast_printer.py` prints the AST in a readable tree format for debugging and presentation.

### Member 5 — Semantic Analyzer (`src/semantic.py`)
Traverses the AST and performs:
1. Use of undefined variables
2. Invalid assignment targets
3. Assignment to the reserved keyword `print`
4. Division by a known constant zero
5. Modulo by a known constant zero

Maintains a `SymbolTable` tracking all defined variables.

```python
from src.semantic import analyze
errors = analyze(tree)   # returns a list of error strings; [] means no errors
```

See [`docs/semantic_interface.md`](docs/semantic_interface.md) for the full interface.

### Member 6 — Main Program and Integration (`src/gui.py`)
Tkinter-based GUI that integrates all modules into one application. Provides:
- **Source Code Editor** — write or paste programs
- **Tokens Tab** — lexer output
- **AST Tab** — structured parse tree
- **Semantic Tab** — symbol table and semantic check results
- **Errors Tab** — all lexical, syntax, and semantic errors
- **Output Tab** — result of `print()` statements

---

## How to Run

### Requirements
- Python 3.8 or higher
- No external libraries required (standard library only)

### Run the GUI (Full Compiler)

```bash
python src/gui.py
```

### Run the Compiler from the Command Line

```python
from src.lexer import tokenize
from src.parser import parse
from src.semantic import analyze

tokens = tokenize("x = 5 + 3; print(x);")
tree = parse(tokens)
errors = analyze(tree)

if errors:
    for e in errors:
        print(e)
else:
    print("Program is valid.")
```

### Run All Tests

```bash
python -m unittest discover -s tests -v
```

**Test results:** 50 tests — all passing ✅

---

## Sample Programs

### Valid Program
```text
# Calculate area
w = 5;
h = 10;
area = w * h;
print(area);
```

### Modulo Example
```text
x = 10;
y = x % 3;
print(y);
```

### Operator Precedence (`*` before `+`)
```text
result = 2 + 3 * 4;
print(result);
```
Expected output: `14` (not 20)

### Invalid — Missing Semicolon
```text
x = 10
print(x);
```
Error: `Syntax error at line 1: expected ';', got 'print'`

### Invalid — Undefined Variable
```text
print(z);
```
Error: `Undefined variable: z`

---

## Branch Structure

| Branch | Contents | Status |
|--------|----------|--------|
| `main` | Grammar docs + Lexer | Active |
| `feature/grammar` | Member 1 docs | Merged into main |
| `feature/lexer` | `lexer.py`, `test_lexer.py` | Open PR |
| `feature/parser` | `parser.py`, `ast_nodes.py`, tests | Merged into main |
| `feature/ast_construction` | `ast_nodes.py`, `ast_printer.py`, tests | Open PR |
| `feature/semantic` | All modules + GUI + all tests | Open PR |

---

## Presentation Date

**23 October 2026**
