\# Semantic Analyzer — Interface Documentation



\## 1. Purpose



The semantic analyzer checks the semantic correctness of a parsed Simple Calculator Language program. It receives an Abstract Syntax Tree (AST), traverses the tree, builds a symbol table, and reports semantic errors.



\## 2. Public Interface



```python

from semantic import analyze



errors = analyze(ast)

```



\- \*\*Input:\*\* The AST representing the parsed program.

\- \*\*Output:\*\* A list of semantic error messages.

\- An empty list (`\[]`) indicates that no semantic errors were detected.

\- The function does not execute the program.



\## 3. Semantic Checks



The analyzer checks:



1\. Use of variables before assignment.

2\. Invalid assignment targets.

3\. Assignment to the reserved keyword `print`.

4\. Division by a statically known constant zero.

5\. Modulo by a statically known constant zero.

6\. Unsupported AST node types.



Line numbers are included when available in the AST.



\## 4. Symbol Table



The symbol table records assigned variable names and their first known definition line.



Methods provided by `SymbolTable`:



\- `define(name, line=None)`

\- `is\_defined(name)`

\- `lookup(name)`

\- `names()`



Reassigning a variable does not create a duplicate symbol.



\## 5. Additional API



```python

from semantic import SemanticAnalyzer



analyzer = SemanticAnalyzer()

symbols, errors = analyzer.analyze(ast)

warnings = analyzer.warnings

```



`SemanticAnalyzer.analyze(ast)` returns a tuple containing the symbol table and error list. Unused-variable warnings are available separately through `analyzer.warnings`.



The public function `analyze(ast)` returns only the error list, as required for integration.



\## 6. AST Compatibility



The analyzer recognizes common node categories:



\- Program or statement list

\- Assignment

\- Print

\- Binary operation

\- Unary operation, if present

\- Numeric literal

\- Variable or identifier



Common expression fields include `left`, `right`, and `op` for binary operations, `value` for numeric literals, and `name` for variables.



\*\*Integration note:\*\* The actual AST classes and fields supplied by Member 4 must be checked before integration is considered complete.



\## 7. Division and Modulo by Zero



The analyzer detects constant-zero divisors, including:



```text

x = 10 / 0;

y = 7 % 0;

z = 10 / (3 - 3);

```



It does not guarantee detection of all runtime cases, such as division by a variable whose value happens to be zero.



\## 8. Testing



Run semantic tests:



```bat

python -m unittest tests/test\_semantic.py -v

```



Run the complete test suite:



```bat

python -m unittest discover -s tests -v

```



\## 9. Team Integration



\- \*\*Member 4:\*\* Confirm AST class names, fields, and source-line information.

\- \*\*Member 5:\*\* Maintain the semantic analyzer, tests, and documentation.

\- \*\*Member 6:\*\* Call `analyze(ast)` and handle the returned list of semantic errors.



Final integration requires verifying compatibility with the actual AST and passing the full test suite.

